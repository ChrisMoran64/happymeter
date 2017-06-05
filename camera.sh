#!/bin/bash
#
# Raspberry Pi script to capture a webcam image
#

DATE=$(date +"%Y%m%d-%H%M%S")

fswebcam --fps 15 -S 8 -r 1024x768 --no-banner ./$DATE.jpg
python uploadimage.py $DATE.jpg happymeter-us camera01

