#!/usr/bin/python
# -*- coding: utf-8 -*-


"""Downloading RDS Logs.

Downloads the log files from the RDS instances.
"""

import json
import datetime
import boto3
import os


def main():
    """Downloads logs from the RDS environment."""
    session = boto3.Session(profile_name='work')
    rds = session.client('rds')
    response = rds_pull_logs(rds)


def rds_pull_logs(rds):
    """
    Extracts information from all RDS instances with logs.

    Parameters
    ----------
    rds: boto3
        The session for accessing aws rds data

    Returns
    -------
    response: dictionary
        An export of all the exported rds information
    """
    os.chdir(os.getcwd() + "/output")
    for inst in rds.describe_db_instances()['DBInstances']:
        identifier = inst['DBInstanceIdentifier']
        log_info = rds.describe_db_log_files(
            DBInstanceIdentifier=identifier
        )
        if os.path.exists(os.getcwd() + "/" + identifier):
            os.chdir(os.getcwd() + "/" + identifier)
        else:
            os.mkdir(identifier)
            os.chdir(os.getcwd() + "/" + identifier)
        for log in log_info['DescribeDBLogFiles']:
            rds.download_db_log_file_portion(
                DBInstanceIdentifier=identifier,
                LogFileName=log['LogFileName']
            )
        os.chdir(os.path.dirname(os.getcwd()))


if __name__ == "__main__":
    main()
