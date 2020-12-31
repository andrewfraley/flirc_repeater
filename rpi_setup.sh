#!/bin/bash

# 2020 Andy Fraley
# https://github.com/andrewfraley/flirc_repeater

# This script will setup flirc_repeater on a Rasperry Pi with a fresh install of Raspberry PI OS Lite 32-bit
# It may work for vanilla Linux systems as well as long as they are apt/debian based, but it's expecting a user account called "pi"

set -e

# Install dependencies
echo "Install dependencies"
apt install -y git expect python3-evdev python3-ruamel.yaml
pip3 install evdev


# Install FLIRC
echo "Installing FLIRC"
rm -f /tmp/flirc_install.sh
wget apt.flirc.tv/install.sh -O /tmp/flirc_install.sh
chmod 754 /tmp/flirc_install.sh

expect <<END
    spawn /tmp/flirc_install.sh
    expect "y/n"
    send "y\r"
    expect eof
END

# Get our source
if [ -d "/opt/flirc_repeater" ]
then
    echo 'Directory already exists, attempting a git pull instead of a clone'
    cd /opt/flirc_repeater
    git pull
else
    git clone https://github.com/andrewfraley/flirc_repeater.git /opt/flirc_repeater
fi

chown -R pi:pi /opt/flirc_repeater

# Setup the service
cp /opt/flirc_repeater/flirc_repeater.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable flirc_repeater

# Start the service
systemctl start flirc_repeater
echo ""
echo "Install finsihed!"
echo 'flirc_repeater service started.'
echo 'To tail the logs, do: journalctl -u flirc_repeater -f'
echo 'To restart the service do: systemctl restart flirc_service'
echo 'Note the service will automatically restart if the FLIRC is not connected, until it is connected'
