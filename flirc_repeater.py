"""
    Flirc remote repeater
    This allows you to use the flirc to send an IR command when it receives another

    This listens for the flirc to receive an IR signal and send its keypress
    We detect the keypress and then send our IR siginal
"""
import sys
import subprocess
import logging
from subprocess import Popen
from select import select
from evdev import InputDevice

# The key code is what the flirc sends as the USB key press
# If we see one of these codes, send the ir command for it
KEY_CODES = {
    # Keycode for PageUp - IR code is Vol Up for Topping
    '104': '0,8980,4429,580,532,557,528,557,532,553,1628,576,527,558,527,558,505,580,1646,531,1672,554,1645,558,1642,558,505,580,1619,584,1619,579,1646,557,527,558,527,558,1645,558,1615,584,531,553,532,553,531,558,1620,579,532,557,1641,558,532,553,532,532,1645,580,1619,585,1619,584,501,584,1641,584',

    # Keycode for PageDown - IR code is vol down for Topping
    '109': '0,9032,4376,633,448,640,449,636,448,636,1566,636,448,615,470,640,448,636,1561,641,1562,640,1562,640,1574,628,444,640,1561,641,1561,637,1562,641,488,597,448,641,1562,637,1562,641,448,637,1562,641,444,640,449,636,448,641,1563,640,444,641,444,641,1562,640,444,641,1562,641,1558,640,1563,641',
}

DEBUG = False
FLIRC_IK = '23000'  # interkey delay
FLIRC_REPEAT = 3   # How many times to repeat the IR signal
FLIRC_DEV_PATH = '/dev/input/by-id/usb-flirc.tv_flirc-if01-event-kbd'
FLIRC_UTIL_PATH = r'flirc_util'
# FLIRC_UTIL_PATH = r'C:\Program Files (x86)\Flirc\flirc_util.exe'  # In case you need to debug on Windows


FLIRC_CMD = '%s sendir --ik=%s --repeat=%s --pattern=' % (FLIRC_UTIL_PATH, FLIRC_IK, FLIRC_REPEAT)


def main():
    """ MAIN """
    init_logger(debug=DEBUG)
    input_device = InputDevice(FLIRC_DEV_PATH)
    flirc_util_process = Popen([FLIRC_UTIL_PATH, 'shell'], stdin=subprocess.PIPE)
    logging.info('made it')
    while True:
        # Wait for something to happen
        r, w, x = select([input_device], [], [])
        for event in input_device.read():
            if event.type == 1 and event.value == 1:
                key_code = str(event.code)
                logging.info('Key code %s', key_code)

                # Do we know about this key? If so send it
                if key_code in KEY_CODES:
                    logging.info('Key code %s recognized, sending IR command', key_code)
                    send_command(flirc_util_process, KEY_CODES[key_code])


def send_command(flirc_util_process, ir_cmd):
    """ Send the IR command """
    flirc_cmd = "sendir --ik=%s --repeat=%s --pattern=%s\n" % (FLIRC_IK, FLIRC_REPEAT, ir_cmd)
    logging.debug('flirc_command: %s', flirc_cmd)
    flirc_util_process.stdin.write(str.encode(flirc_cmd))
    flirc_util_process.stdin.flush()


def init_logger(debug=False):
    """ Start the python logger """
    log_format = '%(asctime)s %(levelname)-8s %(message)s'

    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level, format=log_format)


if __name__ == "__main__":
    main()
