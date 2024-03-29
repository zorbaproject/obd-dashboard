#!/bin/bash
#This script makes an application run automatically on boot as user "pi"
#Created by Luca Tringali - www.codice-sorgente.it
#Thanks to Dalen, this code is partially based on his answer: https://stackoverflow.com/questions/44186905/how-to-replace-the-desktop-interface-with-a-python-application

username="pi"
cat <<EOF > /etc/systemd/system/tty1.service
[Service]
Type=simple
ExecStart=/sbin/getty -a pi 38400 tty1
StandardInput=tty
StandardOutput=tty
TTYPath=/dev/tty1
TTYReset=yes
Restart=always
[Install]
WantedBy=multi-user.target
EOF

systemctl enable tty1.service
systemctl start tty1.service

cat <<EOF > /home/$username/.xinitrc
#! /bin/bash
cat
EOF
chown $username:$username /home/$username/.xinitrc

cat <<EOF > /home/$username/.bashrc
if [ \$(tty | sed s:^/dev/::) == "tty1" ]; then
export DISPLAY=:0
/home/$username/appstart &
startx
fi
EOF
chown $username:$username /home/$username/.bashrc

cat <<EOF > /home/$username/appstart
#! /bin/bash

# Wait a second for X server to start:
sleep 1
# use this if Xorg starts on tty7
# sudo chvt 7
/usr/bin/python3 /home/$username/OBD-monitor/dashboard.py
EOF
chmod +x /home/$username/appstart
chmod +x /home/$username/OBD-monitor/dashboard.py
chown $username:$username /home/$username/appstart

#Disable old autologins, give user access to tty
sudo systemctl disable sddm.service
sudo systemctl disable getty.target
sudo systemctl disable getty@tty1.service
sudo usermod -a -G tty $username
sudo usermod -a -G video $username

echo "Don't forget to turn off Splash Screen under Boot section"
read
sudo raspi-config
