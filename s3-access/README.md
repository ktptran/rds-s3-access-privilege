# S3 Access Privileges
Overview:

## Objectives and Key Results (OKRs)

1. Retrieving and outputing IAM privilege access and S3 bucket policies of AWS S3 buckets


## Process

### IAM

To list out who has what access, we proceeded in the following manner ([/code/iam.py/](https://github.com/ktptran/NVISNx-s3-recent-access/blob/master/code/iam.py)):
1. What policies were in use within the AWS environment.
2. Collect policy information such as the name, versionId, and actions.
3. Parse through the policy to see what actions were permitted and pertained to S3 actions.
4. Collect which users and groups are associated with the policy
5. Retrieve users within the groups associated with the policy.

The output is stored in [/code/Data/iam.txt](https://github.com/ktptran/NVISNx-s3-recent-access/blob/master/code/Data/iam.txt)

Out of Scope: Roles are not included due to customer request.

### S3

To list out the access for S3 buckets, we proceeded in the following manner ([/code/s3.py](https://github.com/ktptran/NVISNx-s3-recent-access/blob/master/code/s3.py)):
1. Find all the buckets in the AWS environment.
2. Retrieved the bucket access block.

The output is stored in [/code/Data/s3.txt](https://github.com/ktptran/NVISNx-s3-recent-access/blob/master/code/Data/s3.txt)

Out of Scope:
1. Find bucket policy.
2. Parse through object/bucket ACL.


### Data Processing

After finding all of this information, we finally parse through the IAM information to list ([/code/processing.py](https://github.com/ktptran/NVISNx-s3-recent-access/blob/master/code/processing.py)):
1. What resource is giving privileges to users.
2. What users possess an action.
3. What actions a user possesses on S3.

The output is stored in [/code/Data/access_level.txt](https://github.com/ktptran/NVISNx-s3-recent-access/blob/master/code/Data/access_level.txt)