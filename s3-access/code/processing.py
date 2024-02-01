# !/usr/bin/python
# -*- coding: utf-8 -*-
"""S3 Access: Sorting privileges.

Sorts through IAM privileges in the AWS environment to depict:
1. What resource is giving privileges to users.
2. What users possess an action.
3. What actions a user possesses on S3.
"""

import datetime
import json
import boto3


def action_to_users(s3_access):
    """
    Sort through policies to associate S3 IAM actions with list of users.

    Parameters
    ----------
    s3_access: dictionary
        Data containing policy information including actions, users,
        and groups.

    Returns
    -------
    s3_action_access: dictionary
        Data containing s3 type of access associated with a list of users.
    """
    s3_action_access = {
        'Date': "%s" % datetime.datetime.now(),
        's3Actions': []
    }
    all_actions = []
    for policy in s3_access['Policies']:
        users = []
        if 'Users' in policy:
            users.extend(policy['Users'])
        if 'Groups' in policy:
            for group in policy['Groups']:
                users.extend(group['members'])

        # Finding all actions
        resources = policy['Resource']
        for action in policy['Actions']:
            input_data = {
                "Action": action,
                "Resource": resources,
                "Users": list(dict.fromkeys(users))
            }
            if action in all_actions:
                action_index = all_actions.index(action)
                action_loc = s3_action_access['s3Actions'][action_index]
                current_users = action_loc['Users']
                if 'Users' in input_data:
                    current_users.extend(input_data["Users"])
                    current_users = list(dict.fromkeys(current_users))
                action_loc['Users'] = current_users
            else:
                s3_action_access['s3Actions'].append(input_data)
                all_actions.append(action)
    return s3_action_access


def users_assignment(policy_data):
    """
    List what privilege guide is assigning privileges to users.

    Parameters
    ----------
    policy_data: dictionary
        Data containing policy information including actions, users,
        and groups.

    Returns
    -------
    user_to_policy_access: dictionary
        Contains what privilege guide is assigning privileges
        to which users and to what resources.
    """
    iam = boto3.client('iam')
    user_to_policy_access = {
        "Date": "%s" % datetime.datetime.now(),
        "PolicyPrivilege": []
    }
    for curr_policy in policy_data['Policies']:
        if 'Users' in curr_policy:
            arn = curr_policy['arn']
            name = iam.get_policy(PolicyArn=arn)['Policy']['PolicyName']
            user_to_policy_access['PolicyPrivilege'].append({
                "PrivilegeGuide": "Policy",
                "PrivilegeName": name,
                "Resource": curr_policy['Resource'],
                "Actions": curr_policy['Actions'],
                "Users": curr_policy['Users']
            })
        if 'Groups' in curr_policy:
            curr_grp = curr_policy['Groups']
            for j in range(len(curr_grp)):
                user_to_policy_access['PolicyPrivilege'].append({
                    "PrivilegeGuide": "Group",
                    "PrivilegeName": curr_grp[j]['name'],
                    "Resource": curr_policy['Resource'],
                    "Actions": curr_policy['Actions'],
                    "Users": curr_grp[j]['members']
                })
    return user_to_policy_access


def user_actions(policy_data):
    """
    List what actions every user can do in S3.

    Parameters
    ----------
    s3_access: dictionary
        Data containing policy information including actions, users,
        and groups.

    Returns
    -------
    user_actions: dictionary
        Contains what actions every user can do in S3.
    """
    user_actions = {
        "Date": "%s" % datetime.datetime.now(),
        "UserActions": []
    }
    iam = boto3.client('iam')
    users_inputted = []
    for curr_policy in policy_data['Policies']:
        payload = {}
        if 'Allow' in curr_policy:
            payload['Allow'] = curr_policy['Allow']
        if 'Deny' in curr_policy:
            payload['Deny'] = curr_policy['Deny']
        if 'Users' in curr_policy:
            arn = curr_policy['arn']
            payload["PrivilegeGuide"] = "Policy"
            payload["PrivilegeName"] = iam.get_policy(PolicyArn=arn)['Policy']['PolicyName']
            for user in curr_policy['Users']:
                if user not in users_inputted:
                    users_inputted.append(user)
                    user_actions['UserActions'].append({
                        "User": user,
                        "Actions": [payload]
                    })
                else:
                    user_index = users_inputted.index(user)
                    user_actions['UserActions'][user_index]['Actions'].append(payload)
        if 'Groups' in curr_policy:
            payload['PrivilegeGuide'] = "Group"
            for group in curr_policy['Groups']:
                payload['PrivilegeName'] = group['name']
                for member in group['members']:
                    if member not in users_inputted:
                        users_inputted.append(member)
                        user_actions['UserActions'].append({
                            "User": member,
                            "Actions": [payload]
                        })
                    else:
                        user_index = users_inputted.index(member)
                        user_actions['UserActions'][user_index]['Actions'].append(payload)
    return user_actions


if __name__ == '__main__':
    f = open('Data/iam.json')
    policy_data = json.load(f)
    f.close()
    # action_user_data = action_to_users(policy_data)
    # with open('Data/action_to_users.json', 'w') as outfile:
    #     json.dump(action_user_data, outfile)
    # policy_to_user = users_assignment(policy_data)
    # with open('Data/policy_assignment.json', 'w') as outfile:
    #     json.dump(policy_to_user, outfile)
    user_actions = user_actions(policy_data)
    with open('Data/user_actions.json', 'w') as outfile:
        json.dump(user_actions, outfile)
