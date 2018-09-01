# My-Pi-Wars-Entry
This is my pi wars entry for 2018, under the name of Sargent Smash.

The script is written in python3, and it needs cwiid to be installed and serial.

The motor controller is from the CamJam EduKit #3, but the code can easily be adapted for a different motor controller.

Feel free to use this code in your own projects, and good luck!

Please contact me if there's any issues with my code.

p.s if the wiimote disconnects after 1/2 a minute, it means that the raspberry pi's not getting enough power!

Cwiid installation instructions:

install dependences:

    sudo apt-get install autotools-dev
    sudo apt-get install bison
    sudo apt-get install flex
    sudo apt-get libcwiid-dev
    sudo apt-get install bluetooth
    sudo apt-get install bluez-utils

download cwiid:

    sudo git clone https://github.com/azzra/python3-wiimote.git
    cd python3-wiimote
setup cwiid:

    sudo aclocal
    sudo autoconf
    sudo ./configure
    sudo make install

Serial installation instructions:

    sudo apt-get install python3-serial
