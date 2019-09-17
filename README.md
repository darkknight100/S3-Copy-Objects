# S3-Copy-Objects
The Lambda function to copy S3 objects for cross AWS Accounts

*Steps for copying:*

1. Deploy the lambda in the source AWS account.
2. Create an SNS event on the s3 bucket whose objects you want to copy.
3. Add the IAM role of the lambda to the Bucket Policy of the Destination bucket with the write permission.


