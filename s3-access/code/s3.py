#!/usr/bin/python
# -*- coding: utf-8 -*-

"""S3 Access: S3 access through S3.

Checks through the access configurations in the bucket settings.
"""

import datetime
import json
import boto3


def bucket_access_configurations(client, bucket_public):
    """
    Retrieve the bucket access configurations and adds them to the input data.

    Parameters
    ----------
    client: boto3
        The s3 session for accessing AWS s3 data
    bucket_public: dictionary
        Storage object for S3 bucket data

    Returns
    -------
    bucket_public
        Storage object with bucket name, access configurations, and publicity
    """
    list_buckets = client.list_buckets()['Buckets']
    for bucket in list_buckets:
        bucket_data = {}
        name = bucket['Name']
        bucket_data['name'] = name
        try:
            access_config = client.get_public_access_block(Bucket=name)\
                ['PublicAccessBlockConfiguration']
        except:
            access_config = "Error could not find"
        bucket_data['AccessConfigurations'] = access_config
        bucket_public['Buckets'].append(bucket_data)
    return bucket_public


def main():
    """S3 Access: S3 access through S3.

    List out an object to store the s3 bucket name, access configurations,
    and publicity.
    """
    client = boto3.client('s3')
    input_bucket = {
        'Date': "%s" % datetime.datetime.now(),
        'Buckets': []
    }
    bucket_public = bucket_access_configurations(client, input_bucket)
    return bucket_public


if __name__ == '__main__':
    result = main()
    with open('Data/s3.json', 'w') as outfile:
        json.dump(result, outfile)
