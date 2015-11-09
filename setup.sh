#!/bin/bash
set -x

#Update the Raspbian repos
sudo apt-get update

#Update the system
sudo apt-get upgrade

#Install tightvnc packages
sudo apt-get -y install tightvncserver

#Copy startup script and enable vncserver
sudo cp ./vncserver /etc/init.d/vncserver
sudo chmod 755 /etc/init.d/vncserver
sudo update-rc.d vncserver defaults

#Extract vnc passwd and xstartup files into the pi user's home directory
tar zxC /home/pi -f vnc_files.tar.gz 

#Copy startup script and enable printing of hostname and ip to Grove Pi LCD connected to I2C port
cp ./grove-get-ip.py ~pi/
sudo cp ./print_ip /etc/init.d/print_ip
sudo chmod 755 /etc/init.d/print_ip
sudo update-rc.d print_ip defaults

#Clone required projects from github to ~pi
cd ~pi
/usr/bin/git clone https://github.com/IoTDevLabs/iot-educ.git
cd ~pi/iot-educ/rpi
./install-python-packages.sh
python read-cpu-temp.py
sleep 5

cd ~pi
/usr/bin/git clone https://github.com/DexterInd/GrovePi
cd GrovePi/Script
sudo chmod +x install.sh
sudo ./install.sh

cd ~pi/GrovePi/Software/Python
sudo python setup.py install
