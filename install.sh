#! /bin/bash
nmap &> /dev/null
if [ $? != 255 ]; then
	echo "Installing NMAP, requires sudo"
	sudo apt-get install nmap &> /dev/null
else
	echo "NMAP already installed."
fi
mkdir logs &> /dev/null
if [ $? != 0 ]; then
	echo "logs/ was already present!"
else
	echo "Created logs folder."
fi
