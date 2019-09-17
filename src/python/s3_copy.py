import ast
import urllib
import os
import logging
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Creating s3 session
    s3 = boto3.client('s3')

    print event

    if 'Records' in event:
        if 'Sns' in event['Records'][0]:
            if 'Message' in event['Records'][0]['Sns']:
                sns_message = ast.literal_eval(event['Records'][0]['Sns']['Message'])

                print sns_message

                # target_bucket declaration
                target_bucket = os.environ['target_bucket']

                source_bucket = str(sns_message['Records'][0]['s3']['bucket']['name'])

                key = str(urllib.unquote_plus(sns_message['Records'][0]['s3']['object']['key']).decode('utf8'))

                print "Copying %s from bucket %s to bucket %s ..." % (key, source_bucket, target_bucket)

                # Set up logging
                logging.basicConfig(level=logging.DEBUG,
                                    format='%(levelname)s: %(asctime)s: %(message)s')

                # Copy the object
                success = copy_object(source_bucket, key, target_bucket)
                if success:
                    print "Successfully Copied {0}/{1} to {2}/{1}".format(source_bucket, key, target_bucket)
                    logging.info("Successfully Copied {0}/{1} to {2}/{1}".format(source_bucket, key, target_bucket))
                else:
                    print "Unsuccessful copy {0}/{1} to {2}/{1}".format(source_bucket, key, target_bucket)
                    logging.info("Unsuccessful copy {0}/{1} to {2}/{1}".format(source_bucket, key, target_bucket))


def copy_object(src_bucket_name, src_object_name,
                destination_bucket_name, destination_object_name=None):
    # Construct source bucket/object parameter
    copy_source = {'Bucket': src_bucket_name, 'Key': src_object_name}
    if destination_object_name is None:
        destination_object_name = src_object_name

    # Copy the object
    s3 = boto3.client('s3')
    try:
        s3.copy_object(ACL='bucket-owner-full-control', CopySource=copy_source, Bucket=destination_bucket_name,
                       Key=destination_object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
