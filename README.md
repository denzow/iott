Internet Of The Toilet
==============================

toilet monitoring via raspberry pi.

setup
------------

#### clone repository

```
$ git clone https://github.com/denzow/iott.git
```

#### set environment

```bash
$ export SLACK_TOKEN=your_token 
```

#### edit wcpacho.sh

`wcpaccho.sh` edit and set path to bot.py

```diff
- python3 /path/to/bot.py
+ python3 /home/pi/apps/toi/bot.py
```

#### register service

`toiletmonitor.service.sample` rename to `toiletmonitor.service` and edit.

```diff
[Service]
- ExecStart = /path/to/wcpaccho.sh
+ ExecStart = /home/pi/apps/toi/wcpaccho.sh
```

copy to `/etc/systemd/system/`

```bash
$ sudo cp toiletmonitor.service /etc/systemd/system/
```

