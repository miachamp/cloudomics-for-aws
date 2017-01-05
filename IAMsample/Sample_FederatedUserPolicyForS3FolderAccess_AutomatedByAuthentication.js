
//Includes explicit deny on every other folder in bucket and allows access to a single folder
//Note :  each new user needs to be added to Group 'Client' for access to list buckets 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowRootLevelListingOfCompanyBucket",
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::omicslander"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "cloud143927bdc7/*"
                    ]
                }
            }
        },
        {
            "Sid": "AllowUserToReadWriteObjectData",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::omicslander/cloud143927bdc7/*"
            ]
        },
        {
            "Sid": "ExplicitDenyToOtherFolders",
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Deny",
            "Resource": [
                "arn:aws:s3:::*"
            ],
            "Condition": {
                "StringNotLike": {
                    "s3:prefix": [
                        "*cloud143927bdc7*"
                    ]
                },
                "Null": {
                    "s3:prefix": false
                }
            }
        }
    ]
}