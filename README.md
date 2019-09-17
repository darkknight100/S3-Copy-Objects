# S3-Copy-Objects
The Lambda function to copy incremental S3 objects for cross AWS Accounts

*Steps for copying:*

* Deploy the lambda in the source AWS account.
* The IAM role of the lambda should have Read access to the source s3 bucket.
```buildoutcfg
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::sourcebucket",
                "arn:aws:s3:::sourcebucket/*"
            ]
        }
```
* Create an SNS event on the s3 bucket whose objects you want to copy.
* Add the IAM role of the lambda to the Bucket Policy of the Destination bucket with the write permission.
```buildoutcfg
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::destinationbucket",
                "arn:aws:s3:::destinationbucket/*"
            ]
        }
```




