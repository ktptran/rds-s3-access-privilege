# RDS endpoints

Provide the IAM users who have RDS privileges associated with them.


## Setup

Install ipython:

```
pip install ipython
```

## Deploy

In this directory, run the command:

```bash
./src/run.sh
```

## Output

iam.json

```json
{
  "Date": string,
  "Policies": [
    {
      "arn": string,
      "versionId": string,
      "Allow": [
        {
          "Action": list,
          "Resource": list
        }
      ],
      "Deny": [
        {
          "Action": list,
          "Resource": list
        }
      ],
      "Users": list,
      "Groups": [
        {
          "name": string,
          "members": list
        }
      ]
    },
    ...
  ]
}
```

Schema:
- Date: date of running the script.
- Policies: all of the policies that have RDS privileges.
  - arn: amazon resource name of the policy
  - versionId: version Id of the policy
  - Allow: explicit allow statements for the policy
    - Action: RDS actions associated with the statement
    - Resource: All resources pertaining to the statement
  - Deny: Explicit deny statements for the policy
    - Action: RDS actions associated with the statement
    - Resource: All resources pertaining to the statement
  - User: all users associated with the policy
  - Groups: All groups associated with the policy
    - name: Group name
    - members: members username

user_actions.json

```json
{
  "Date": string,
  "UserActions": [
    {
      "User": string,
      "Actions": [
        {
            "PrivilegeGuide": "Policy"|"Group",
            "PrivilegeName": string,
            "Allow": [
              {
                "Action": list,
                "Resource": list,
              },
              ...
            ],
            "Deny": [
              {
                "Action": list,
                "Resource": list,
              },
              ...
            ],
        },
        ...        
      ]
    }
  ]
}
```
Schema:
- Date: date of running the script.
- UserActions: all users associated with RDS privileges
  - User: username of IAM user
  - Actions: all RDS actions associated with the user
    - PrivilegeGuide: privilege assigning the policy
    - PrivilegeName: name of the privilege
    - Allow: all allow statements within the policy
      - Action: RDS actions associated with the statement
      - Resource: All resources pertaining to the statement
    - Deny: all deny statements within the policy
      - Action: RDS actions associated with the statement
      - Resource: All resources pertaining to the statement
