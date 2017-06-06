#! /bin/bash
#
# Happiness Meter Master Deployment Script 1.0.0
# Chris Moran, June 2017
#

# Create and store the Lambda code
zip ${PKG_NAME} ${SRC_NAME}

# Create the configuration bucket
aws cloudformation deploy --template-file happymeter-config-bucket.yaml --stack-name Happyness-Config --parameter-overrides BucketName=${CONF_BUCKET} Region=${REGION} --region ${REGION} --profile ${PROFILE}

# Upload our Lambda source package
aws s3 mv ${PKG_NAME} s3://${CONF_BUCKET}/${PKG_NAME} --profile ${PROFILE}

# Create the IAM Roles
aws cloudformation deploy --template-file happymeter-roles.yaml --stack-name Happyness-Roles --capabilities CAPABILITY_NAMED_IAM --region ${REGION} --profile ${PROFILE} --output text
IAM_ARN=$(aws cloudformation describe-stacks --stack-name Happyness-Roles --profile $PROFILE --region $REGION --output text --query 'Stacks[0].Outputs[*].OutputValue')

# Create the Lambda function
aws cloudformation deploy --template-file happymeter-lambda.yaml --stack-name Happyness-Lambda --parameter-overrides ConfigBucket=${CONF_BUCKET} ConfigPkg=${PKG_NAME} Region=${REGION} RoleArn=${IAM_ARN} --region ${REGION} --profile ${PROFILE}
LAMBDA_ARN=$(aws cloudformation describe-stacks --stack-name Happyness-Lambda --profile $PROFILE --region $REGION --output text --query 'Stacks[0].Outputs[0].OutputValue')

# Create the data bucket for the cams
aws cloudformation deploy --template-file happymeter-s3.yaml --stack-name Happyness-Storage --parameter-overrides BucketName=${DATA_BUCKET} Region=${REGION} LambdaArn=${LAMBDA_ARN} --region ${REGION} --profile ${PROFILE}
