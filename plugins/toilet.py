# coding: utf-8
import smbus
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

LIGHT_THRESHOLD = 100

def get_lux():
    """
    接続したBH1750より照度を取得する
    :return:
    """
    bus = smbus.SMBus(1)
    address = 0x23
    lux = bus.read_i2c_block_data(address, 0x10)
    return (lux[0] * 256 + lux[1]) / 1.2


@respond_to('といれ')
def check_toilet(message):
    lux = get_lux()
    message.reply('明るさ{}'.format(lux))
    if lux > LIGHT_THRESHOLD:
        message.reply('たぶん、中に誰もいなくないですよ')
    else:
        message.reply('たぶん、中に誰もいませんよ')


@default_reply
def default_func(message):
    message.reply('といれ って話しかけてね')
