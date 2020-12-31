"""
    Flirc remote repeater
    This allows you to use the flirc to send an IR command when it receives another

    This listens for the flirc to receive an IR signal and send its keypress
    We detect the keypress and then send our IR siginal
"""
# pylint: disable=line-too-long
import os
import sys
import subprocess
import logging
from subprocess import Popen
from select import select
from evdev import InputDevice
from ruamel.yaml import YAML


def main():
    """
        We're going to spawn a "flirc_util shell" process and send it commands when we see the flirc responding to IR.
        We'll watch the Flirc's USB input device for keypresses, and if we see one that matches our KEY_CODES dict,
        we'll send the corresponding IR command with the "flirc_util shell" process.
    """

    config = get_config()
    init_logger(debug=config['debug'])

    # We'll use this to listen to the FLIRC USB input device for key codes
    input_device = get_input_device(config)

    # Spawn the FLIRC shell process
    flirc_util_process = start_flirc_util(config)
    logging.debug('filrc_util shell process opened')

    key_codes = config['key_codes']
    logging.debug('key_codes: %s', key_codes)

    while True:
        # How to read the input from a console connected USB keyboard (the flirc in our case) https://superuser.com/a/562519/659822
        r, w, x = select([input_device], [], [])  # pylint: disable=unused-variable, invalid-name
        for event in input_device.read():
            if event.type == 1 and event.value == 1:
                key_code = event.code
                logging.info('Key code %s', key_code)

                # Do we know about this key? If so, send it.
                if key_code in key_codes:
                    logging.info('Key code %s recognized, sending IR command', key_code)
                    ir_code = key_codes[key_code]['ir_code']
                    repeat = key_codes[key_code]['repeat']
                    send_command(flirc_util_process, config=config, ir_code=ir_code, repeat=repeat)


def send_command(flirc_util_process, config, ir_code, repeat):
    """ Send the IR command
        flirc_util_process is a subprocess we already opened by running "flirc_util shell".
        We leave that open so we don't have to spawn a new process for every key press, which
        seems to be noticeably faster on something slow like a Raspberry Pi Zero W
    """
    interkey_delay = config['interkey_delay']
    flirc_cmd = "sendir --ik=%s --repeat=%s --pattern=%s\n" % (interkey_delay, repeat, ir_code)

    logging.debug('flirc_command: %s', flirc_cmd)
    flirc_util_process.stdin.write(str.encode(flirc_cmd))
    flirc_util_process.stdin.flush()


def start_flirc_util(config):
    """ Start the "flirc_util shell" process """
    path = config['flirc_util_path']
    flirc_util_process = Popen([path, 'shell'], stdin=subprocess.PIPE)
    return flirc_util_process


def get_input_device(config):
    """ Create the InputDevice instance and handle errors """

    dev_path = config['flirc_device_path']
    logging.debug('get_input_device() dev_path: %s', dev_path)
    try:
        input_device = InputDevice(dev_path)
        return input_device
    except FileNotFoundError as exception:
        logging.error('Error opening device path %s', dev_path)
        logging.error('Error was: %s', exception)
        logging.error('FLIRC is likely not attached or the device path (FLIRC_DEV_PATH) is wrong')
        sys.exit(1)


def get_config():
    """ Get the config dict from config.yaml """

    # If we're running this as a service or from a different directory, we need to get the config file from
    # the same dir where the script resides
    config_path = os.path.dirname(os.path.realpath(__file__)) + '/config.yaml'

    yaml = YAML(typ='safe', pure=True)
    with open(config_path) as fileh:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config = yaml.load(fileh)

    config['debug'] = str(config['debug']).lower() == 'true'
    return config


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
