# Take the image from the command line and upload to S3
# When this is done, a lambda function will launch an
# analysis run against the image.

import sys
import os
import boto3

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

#Send the file to our bucket for processing
#	
	try:
		print 'Opening image'
		upload_name = camdir + '/' + filename
		data = open(filename, 'rb')
		s3 = boto3.resource('s3')
		print 'Establishing connection'
		s3.Bucket(bucket).put_object(Key=filename, Body=data)
		print 'done'
	except:
		print 'Something went wrong.'
	
else:
	print 'Usage: ', sys.argv[0], ' file_name bucket cam_id'
		

