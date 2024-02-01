#!/usr/bin/python
# -*- coding: utf-8 -*-

"""S3 Access through IAM.

Checks through the attached IAM policies in the AWS environment to see what
policies are given to users and groups.
"""

import datetime
import json
import boto3


def get_iam_actions(iam, input_data, all_buckets):
    """
    Retrieve the policy statement actions and adds them to the input data.

    Parameters
    ----------
    iam: boto3
        The session for accessing aws data
    input_data: dictionary
        Object used to store input data information

    Returns
    -------
    input_data: dictionary
        An edited version of the input data with the information found
    """
    policy_version = iam.get_policy_version(
        PolicyArn=input_data["arn"],
        VersionId=input_data["versionId"]
    )
    try:
        for statement in policy_version['PolicyVersion']['Document']['Statement']:
            action_list = []

            # Retrieves all actions that are pertaining to S3
            action = statement['Action']
            if isinstance(action, list):
                for spec_action in action:
                    if spec_action.startswith('s3:'):
                        action_list.append(spec_action)
            else:
                if action.startswith('s3:') or action == '*':
                    action_list.append(action)

            # We found some permissions that explicitly allow or deny
            if action_list:
                payload = {"Action": action_list}

                # Retrieving resource
                if statement["Resource"] == '*':
                    payload['Resource'] = all_buckets
                else:
                    payload['Resource'] = statement["Resource"]

                # If the allow or deny is in the input_data
                if statement['Effect'] not in input_data:
                    input_data[statement['Effect']] = [payload]
                else:
                    input_data[statement['Effect']].append(payload)

    except KeyError as e:
        print('Failed to parse: ' + input_data["arn"])
    return input_data


def get_iam_user_groups(iam, input_data):
    """
    Retrieve what groups, group members, and users are assigned to a policy.

    Parameters
    ----------
    iam: boto3
        The session for accessing aws data
    input_data: dictionary
        Object used to store input data information

    Returns
    -------
    input_data: dictionary
        An edited version of the input data with a list of users and
        group information attached to the policy.
    """
    arn = input_data["arn"]
    users = []
    for user in iam.list_entities_for_policy(PolicyArn=arn)['PolicyUsers']:
        users.append(user['UserName'])
    if users:
        input_data['Users'] = users
    groups = iam.list_entities_for_policy(PolicyArn=arn)['PolicyGroups']
    if groups:
        input_data['Groups'] = get_group_and_users(iam, groups)
    return input_data


def get_group_and_users(iam, groups):
    """
    Retrieve the group name and users apart of the group.

    Parameters
    ----------
    iam: boto3
        The session for accessing AWS data
    groups: dictionary
        Object with the list of groups for the given policy.

    Returns
    -------
    groups_data: dictionary
        A list of group information including the users apart
        of it and the group name
    """
    groups_data = []
    for grp in groups:
        group = {}
        group["name"] = grp['GroupName']
        curr_grp = iam.get_group(GroupName=group["name"])['Users']
        grp_members = []
        for user in curr_grp:
            grp_members.append(user['UserName'])
        group["members"] = grp_members
        groups_data.append(group)
    return groups_data


def retrieve_data():
    """
    AWS IAM S3 Access.

    Check through the attached IAM policies in the given AWS
    environment to see what S3 policies are given to the users
    and groups.

    Returns
    -------
    iam_s3_access: dictionary
        All attached policies within a user's AWS environment
        that gives access to S3.
    """
    s3 = boto3.client('s3')
    all_buckets = []
    for bucket in s3.list_buckets()['Buckets']:
        all_buckets.append(bucket['Name'])
    iam = boto3.client('iam')
    iam_s3_access = {
        'Date': "%s" % datetime.datetime.now(),
        'Policies': []
    }
    used_policies = iam.list_policies(Scope='All',
                                      OnlyAttached=True)['Policies']
    for curr_policy in used_policies:
        input_data = {}
        input_data["arn"] = curr_policy['Arn']
        input_data["versionId"] = curr_policy['DefaultVersionId']
        try:
            input_data = get_iam_actions(iam, input_data, all_buckets)
            input_data = get_iam_user_groups(iam, input_data)
            # Only keep the ones associated with the user
            if ('Users' in input_data or 'Groups' in input_data) and \
                ('Allow' in input_data or 'Deny' in input_data):
                iam_s3_access['Policies'].append(input_data)
        except ValueError as err:
            print(f"Error occurred: {err}")
    return iam_s3_access


if __name__ == '__main__':
    policy_data = retrieve_data()
    with open("Data/iam.json", "w") as outfile:
        json.dump(policy_data, outfile)
