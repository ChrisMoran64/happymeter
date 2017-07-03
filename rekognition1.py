from __future__ import print_function

from decimal import Decimal
import json
import urllib
import boto3
import uuid

print('Loading function')

rekognition = boto3.client('rekognition')


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_faces(bucket, key):
    response = rekognition.detect_faces(Attributes=["ALL"],Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response
    
def save_reaction(key, emotion, confidence):
    db = boto3.resource('dynamodb').Table('Sentiments')
    data =[ {'Emotion': str(emotion), 'Confidence': Decimal(str(confidence)) } ]
#    db.put_item(Item={ 'EntryId': str(uuid.uuid4()), 'ImageId': key, 'Data': data })
    db.put_item(Item={ 'EntryId': '1', 'ImageId': key, 'Data': data })


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response


def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Attributes=["ALL"], Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        print('Bucket', bucket, ' Key', key)
        # Calls rekognition DetectFaces API to detect faces in S3 object.
        response = detect_faces(bucket, key)

        # Print response to console and commit to database.
        for em in response["FaceDetails"]:
            for res in em["Emotions"]:
                print("Emotion: ", res["Type"], "Confidence: ", res["Confidence"])
                save_reaction(key, res["Type"], res["Confidence"])


        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
