#!/usr/bin/python
# -*- coding: utf-8 -*-


"""RDS DNS endpoint & associate DB instance name.

Provides information about the DNS endpoint and associate DB instance name.
"""

import json
import datetime
import boto3


def main():
    """Extrapolate and exports RDS DNS endpoint information."""
    session = boto3.Session(profile_name='work')
    rds = session.client('rds')
    response = rds_pull_endpoint(rds)
    export_data(response)


def rds_pull_endpoint(rds: boto3) -> dict:
    """
    Extrapolate information from all RDS instances in given session.

    Parameters
    ----------
    rds: boto3
        The session for accessing aws rds data

    Returns
    -------
    response: dictionary
        An export of all the exported rds information
    """
    response = {
        "Date": "%s" % datetime.datetime.now(),
        "Endpoint": []
    }
    for inst in rds.describe_db_instances()['DBInstances']:
        data = {}
        fields = [
            'Endpoint',
            'PubliclyAccessible',
            'DBInstanceClass',
            'DBInstanceIdentifier',
            'Engine',
            'DBInstanceArn'
        ]
        for field in fields:
            data[field] = inst[field]
        response['Endpoint'].append(data)
    return response


def export_data(response: dict):
    """
    Export response data to json file.

    Parameters
    ----------
    response: dictionary
        Information about RDS.
    """
    with open('output/rds_endpoint.json', 'w') as outfile:
        json.dump(response, outfile)


if __name__ == "__main__":
    main()
