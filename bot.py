#!/usr/bin/env python3
# coding: utf-8
import time
import datetime
import threading

import requests
from slackbot.bot import Bot
from slackbot.settings import API_TOKEN

from plugins.toilet import get_lux, LIGHT_THRESHOLD

API_URL = 'https://slack.com/api/users.setPresence?token={token}&presence={status}'


def set_away():
    """
    Botのステータスを離席にする
    :return:
    """
    res = requests.get(API_URL.format(token=API_TOKEN, status='away'))
    time.sleep(1)
    res = requests.get(API_URL.format(token=API_TOKEN, status='away'))
    time.sleep(1)
    res = requests.get(API_URL.format(token=API_TOKEN, status='away'))
    print(res.content)


def set_active():
    """
    Botのステータスを在籍にする
    :return:
    """
    res = requests.get(API_URL.format(token=API_TOKEN, status='auto'))
    time.sleep(1)
    res = requests.get(API_URL.format(token=API_TOKEN, status='auto'))
    time.sleep(1)
    res = requests.get(API_URL.format(token=API_TOKEN, status='auto'))
    print(res.content)


def check_lux():
    """
    Threadで定期的に明るさをチェックしてしきい値を下回ったらステータスをOFFにする
    """

    is_using = False
    # 初期化
    set_away()
    while True:
        lux = get_lux()
        print(datetime.datetime.now(), lux)
        # ステータスが変化したら通知する
        # 未使用 で明るくなった -> 利用開始
        if lux > LIGHT_THRESHOLD and not is_using:
            is_using = True
            print('ON')
            set_active()

        # 使用中から暗くなった -> 利用終了
        elif lux <= LIGHT_THRESHOLD and is_using:
            is_using = False
            print('OFF')
            set_away()

        time.sleep(3)
        

def main():
    bot = Bot()
    th_me = threading.Thread(target=check_lux, name="th_check_lux")
    th_me.setDaemon(True)
    th_me.start()
    try:
        bot.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print('start slackbot')
    main()
