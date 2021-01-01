# FLIRC Repeater

## Summary
This is a small program designed to use a [FLIRC device](https://flirc.tv/more/flirc-usb) to watch for specific IR codes, then transmit different IR codes in response.

## Use Case
An example use case is LG's Magic Remote, which doesn't have a learning function, but does have support for controlling the volume on external devices it supports.  If your amplifier isn't supported, you can use this with a FLIRC device to detect the volume up IR commands from the LG remote, and then send the proper IR command to your amplifier.  In the case of an LG remote, and most others as well, you can program the remote to control an arbitrary brand's devices (I successfully used Phillips).  Then setup the FLIRC to learn these button presses and send keyboard key codes.  This program will then watch the FLIRC for the key codes, and send your different IR codes in response.

## Setup
This should work with any Linux machine, but these instructions are specifically for the Raspberry Pi Zero W running Raspberry Pi OS Lite 32-bit.  These instructions also assume you're just going to use SSH to log into the Pi, you don't need to connect it to a monitor.

### Prepare the Raspberry Pi
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

### Boot the Pi and run the setup script
- Boot the pi and wait a few minutes
- ssh into it with pi@raspberrypi or pi@raspberrypi.local
    - pw is raspberrypi
- Run: ```curl https://raw.githubusercontent.com/andrewfraley/flirc_repeater/main/rpi_setup.sh | sudo bash```

### Program the FLIRC for your main remote (the remote that will initiate the IR signals)
- For each button you want to manage, run the following command and follow the on-screen instructions (replace the letters with unique keyboard keys as needed).
- Note the a, b, c.  These are key presses, so we're telling the FLIRC when it sees your remote button press, send the keyboard code for the letter a.  We'll later tell our program to watch for the FLIRC sending the letter a, and then respond with our replacement IR code.
- ```flirc_util record a```
- ```flirc_util record b```
- ```flirc_util record c```
- If you need to start over, run: ```flirc_util format```

### Get the key code for each button press
- You need to get the linux key code for each key press you've defined
- You can look up the codes from [here](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h)
- Alternatively, you can tail the flirc_repeater logs.  Each button press should generate a line that says which key code was seen.
    - ```journalctl -u flirc_repeater -f```


### Get the IR codes you want to send (in response to incoming IR codes)
- Run: ```flirc_util device_log --ir -p```
- You may see some initial output, ignore this and press enter a few times to get a whitespace buffer
- The FLIRC is now in IR debug mode and will output any ir codes it sees
- Point your remote at the FLIRC and press the button you want to capture
- You will see several lines of output, you want the long line with comma separated values that looks something like the following
    - ```0,2419,557,1176,587,1168,579,605,552,579,579,1176,579,605,552,579,579,579,578,579,579,579,578,579,579,1176,582,1173,579,605,552,601```
- You'll need this line for config.yaml in the next step

### Edit config.yaml to use your remote codes
- Edit the /opt/flirc_repeater/config.yaml file
    - Add your key codes to the key_codes map
    - You need to specifify the key code, which is what the FLIRC sends as a keyboard press, followed by the ir_code you want to respond with.
    - Note if you've never worked with yaml files, heed the indentation, it matters.
    - The codes 30 and 48 in the example are for the letters a and b, replace with the codes for your keys
    - Some devices may need ```repeat: 3```, but other devices may see this as three button presses.  Adjust accordingly.

### Restart the flirc_repeater service to use your new config
- Run: ```systemctl restart flirc_repeater```

## Troubleshooting

### Viewing logs
- Run: ```journalctl -u flirc_repeater -fa```
