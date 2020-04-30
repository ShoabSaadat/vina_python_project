#!/usr/bin/env bash
sudo apt update
sudo apt upgrade
sudo apt install unzip -y
sudo apt install autodock-vina -y
sudo apt install openbabel -y
sudo apt install pymol -y
sudo apt install python #Installing python 2 for mgltools. Assuming python3 and pip3 already installed
sudo apt install python-pip

#Seting up MGL Tools installation
sudo sh mgltools.sh

sudo apt update
sudo apt upgrade
