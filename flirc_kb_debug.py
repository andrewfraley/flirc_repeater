# https://superuser.com/a/562519/659822
# https://github.com/andrewfraley/flirc_scripts/blob/main/topping.py
import string

from evdev import InputDevice
from select import select

keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
dev = InputDevice('/dev/input/by-id/usb-flirc.tv_flirc-if01-event-kbd')

while True:
    r, w, x = select([dev], [], [])
    for event in dev.read():
        if event.type == 1 and event.value == 1:
            print(event.code)
