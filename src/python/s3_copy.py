import boto3
import ast
import urllib
import os


class S3Copy:

    def lambda_handler(self, event, context):

        # Creating s3 session
        s3 = self.get_s3_client()

        sns_message = ast.literal_eval(event['Records'][0]['Sns']['Message'])

        # target_bucket declaration
        target_bucket = os.environ['dbHost']

        source_bucket = str(sns_message['Records'][0]['s3']['bucket']['name'])

        key = str(urllib.unquote_plus(sns_message['Records'][0]['s3']['object']['key']).decode('utf8'))

        copy_source = {'Bucket': source_bucket, 'Key': key}

        print "Copying %s from bucket %s to bucket %s ..." % (key, source_bucket, target_bucket)

        try:
            s3.copy_object(Bucket=target_bucket, Key=key, CopySource=copy_source)

        except:
            raise Exception("There is some error in copying s3 objects")

    @staticmethod
    def get_s3_client(self):

        should_assume_cross_account = os.environ['should_assume_cross_account']

        sts_client = boto3.client('sts')

        assumed_role_object = sts_client.assume_role(
            role_arn=os.environ['role_arn'],
            role_session_name="AssumeRoleSession")

        credentials = assumed_role_object['Credentials']

        s3fon = boto3.session

        s3_session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        return s3_session.client()
