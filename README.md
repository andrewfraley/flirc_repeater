# Flirc Repeater

## Summary
This is a small program designed to use a [FLIRC device](https://flirc.tv/more/flirc-usb) to watch for specific IR codes, then transmit different IR codes in response.

## Use Case
An example use case is LG's Magic Remote, which doesn't have a learning function, but does have support for controlling the volume on external devices it supports.  If your amplifier isn't supported, you can use this with a flirc device to detect the volume up IR commands from the LG remote, and then send the proper IR command to your amplifier.  In the case of an LG remote, and most others as well, you can program the remote to control an arbitrary brand's devices (I successfully used Phillips).  Then setup the FLIRC to learn these button presses and send keyboard key codes.  This program will then watch the FLIRC for the key codes, and send your different IR codes in response.

## Setup
This should work with any Linux machine, but these instructions are specifically for the Raspberry Pi Zero W running Raspberry Pi OS Lite 32-bit

### Raspberry Pi Specific
- Install Raspberry PI OS Lite 32-bit on your sd card
- create the file "ssh" on the root of the sd card
- create the file "wpa_supplicant.conf" on the root of the sd card, fill with the following and edit in your SSID and password

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="WIFI_SSID"
scan_ssid=1
psk="WIFI_PASSWORD"
key_mgmt=WPA-PSK
}
```

### Setup FLIRC
- If using a Raspberry Pi, go ahead and boot it up and wait a few minutes
    - ssh into it with pi@raspberrypi or pi@raspberrypi.local, pw is raspberrypi
- Run (should work on any debian based distro): ```curl apt.flirc.tv/install.sh | sudo bash```
    - Select Yes when asked to install flirc utilities

### Setup Python
- Install Python Pip: ```sudo apt install python3-pip```
- Install evdev: ```sudo pip3 install evdev```

### Get the script
- Run: ```wget https://raw.githubusercontent.com/andrewfraley/flirc_repeater/main/flirc_repeater.py```

### Test the script
- Run: ```python3 flirc_repeater.py```
- Press your remote buttons and watch the output
- You should see your key codes being recognized, and the IR codes being sent.
- The FLIRC receiver is very sensitive, however, the range of the IR transmitter is limited.  It needs to be within 4-5 feet and have clear line of sight.

### Setup the service
