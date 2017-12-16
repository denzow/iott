#!/usr/bin/env python3
# coding: utf-8
import os
import time
import datetime
import smbus
import requests
import threading
from slackbot.bot import Bot


API_TOKEN = os.environ.get('SLACK_TOKEN')
API_URL = 'https://slack.com/api/users.setPresence?token={token}&presence={status}'
ON = 'auto'
OFF = 'away'


def get_lux():
    bus = smbus.SMBus(1)
    addr = 0x23
    lux = bus.read_i2c_block_data(addr, 0x10)
    return (lux[0]*256+lux[1])/1.2

def set_status(is_on):
    if is_on:
        res = requests.get(API_URL.format(token=API_TOKEN, status=ON))
        print(res.content)
    else:
        res = requests.get(API_URL.format(token=API_TOKEN, status=OFF))
        print(res.content)

def check_lux():
    """
    Threadで定期的に明るさをチェックしてしきい値を下回ったらステータスをOFFにする
    """
    # 使用開始時刻
    using_start_time = None
    is_using = False
    # 初期化
    set_status(is_using)
    while True:
        lux = get_lux()
        print(datetime.datetime.now(), lux)
        # ステータスが変化したら通知する
        # 未使用 で明るくなった -> 利用開始
        if lux > 100 and not is_using:
            is_using = True
            using_start_time = datetime.datetime.now()
            print('ON')
            set_status(is_using)
        # 使用中から暗くなった -> 利用終了
        elif lux <= 100 and is_using:
            is_using = False
            using_start_time = None
            print('OFF')
            set_status(is_using)
        
        time.sleep(3)
        

def main():

    th_me = threading.Thread(target=check_lux, name="th_check_lux")
    th_me.start()
    bot = Bot()
    bot.run()
    th_me.join()

if __name__ == "__main__":
    print('start slackbot')
    main()
