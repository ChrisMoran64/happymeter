#!/bin/bash
#
# Setup development environment
#
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y build-essential cmake git pkg-config
sudo apt-get install -y libjpeg-dev libtiff-dev libjasper-dev libpng-dev
sudo apt-get install -y libgtk2.0-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python-pip
sudo apt-get install -y python2.7-dev
