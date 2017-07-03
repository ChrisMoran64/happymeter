# Take the image from the command line and upload to S3
# When this is done, a lambda function will launch an
# analysis run against the image.

import sys
import os
import boto3
import cv2

# Pretty simple means of getting command args.
# would be better to use --key value
# but for now, it's OK
#
if len(sys.argv) == 4:
	filename=sys.argv[1]
	bucket=sys.argv[2]
	camdir=sys.argv[3]
	print 'File name: ', filename
	print 'Bucket:    ', bucket
	print 'Cam Dir:   ', camdir

# Set up face recognition
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)
	image = cv2.imread(filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Look for one or more faces in the image	
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
	)
	if len(faces) > 0:

#Send the file to our bucket for processing
#	
		print 'Opening image'
		upload_name = camdir + '/' + filename
		data = open(filename, 'rb')
		s3 = boto3.resource('s3')
		print 'Establishing connection'
		s3.Bucket(bucket).put_object(Key=upload_name, Body=data)
		print 'done'
		data.close()
		os.unlink(filename)
	
else:
	print 'Usage: ', sys.argv[0], ' file_name bucket cam_id'
		

