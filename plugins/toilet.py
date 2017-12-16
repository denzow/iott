# coding: utf-8
import smbus
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ



def get_lux():
    bus = smbus.SMBus(1)
    addr = 0x23
    lux = bus.read_i2c_block_data(addr,0x10)
    return (lux[0]*256+lux[1])/1.2


@respond_to('といれ')
def check_toilet(message):
    message.reply('明るさ{}'.format(get_lux()))
    if get_lux() > 100:
        message.reply('たぶん、中に誰もいなくないですよ')
    else:
        message.reply('たぶん、中に誰もいませんよ')

@default_reply
def mention_func(message):
    message.reply('といれ って話しかけてね') # メンション
