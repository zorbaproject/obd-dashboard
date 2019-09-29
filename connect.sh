#!/bin/bash
#sudo adduser pi dialout
sudo rfcomm release 0
sudo rfkill unblock bluetooth
sudo hciconfig hci0 up
mymac=$(hcitool scan | grep "OBDII" | cut -f2)
#mymac="AA:BB:CC:11:22:33"
sudo rfcomm bind 0 $mymac
