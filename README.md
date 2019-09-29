# PySide2 OBD Dashboard
This is a car dashboard with plots instead of dials, built for Python3 on a RaspberryPi with PySide2, to demonstrate the use of PySide2 for displaying realtime data from OBD readers.
You can run the script just with
chmod +x dashboard.py
./dashboard.py
it is designed to work both on laptops and RaspberryPis. It should work fine on every device, if you are using a OBD-USB adapter. If you are using a OBD-Bluetooth adapter it might not work sometimes: some cheap adapters are known to drop the connection.

# Requirements
This program uses to Python-OBD library (https://github.com/brendan-w/python-OBD), with some minor changes to make it work with cheap bluetooth adapters.
To make the bluetooth stack work on a Debian system you ca run the ./deps.sh script.

# Autologin
If you want to run this application at boot, you can use the autologin script:
chmod +x autologin.sh
./autologin.sh
Then just reboot the system and wait for the interface to load. If you are using a Raspbian Buster image, without PySide2 libraries, you'll first need to follow instructions on the page https://www.codice-sorgente.it/raspbian-buster-pyside2-lxqt/#English, to install Qt5 and PySide2.

# Test
Not every car supports all the data in OBD protocol. But you can check every OBD code running
./test.py
If you read "None" for a code, it means your car does not support it.
