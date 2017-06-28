#!/bin/bash
#
# General script to capture a webcam image
#

CAMERAID="camera00"
PICBUCKET="happymeter-us"
DATE=$(date +"%Y%m%d-%H%M%S")

fswebcam --fps 15 -S 8 -r 1024x768 --no-banner ./$DATE.jpg
python uploadimage.py $DATE.jpg $PICBUCKET $CAMERAID

