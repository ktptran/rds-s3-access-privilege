# !/usr/bin/python
# -*- coding: utf-8 -*-
"""RDS IAM Access Sorting.

Sorts through IAM privileges in the AWS environment to depict what users have
associated actions for RDS.
"""

import datetime
import json
import boto3


def user_actions(policy_data):
    """
    List what actions every user can do in RDS.

    Parameters
    ----------
    policy_data: dictionary
        Data containing policy information including actions, users,
        and groups.

    Returns
    -------
    user_actions: dictionary
        Contains what actions every user can do in RDS.
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
    f = open('output/iam.json')
    policy_data = json.load(f)
    f.close()
    user_actions = user_actions(policy_data)
    with open('output/user_actions.json', 'w') as outfile:
        json.dump(user_actions, outfile)
