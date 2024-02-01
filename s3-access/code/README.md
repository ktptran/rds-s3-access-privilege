# S3 Access Privileges
This project Retrieves and outputs access to AWS S3 buckets through
IAM privileges and S3 bucket policies. This project is in association with NVISNx.

## Deployment
In the directory with the `README.md`, run the following commands:

```bash
./scripts/script.sh
```

## Data Output

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
- Policies: all of the policies that have S3 privileges.
  - arn: amazon resource name of the policy
  - versionId: version Id of the policy
  - Allow: explicit allow statements for the policy
    - Action: S3 actions associated with the statement
    - Resource: All resources pertaining to the statement
  - Deny: Explicit deny statements for the policy
    - Action: S3 actions associated with the statement
    - Resource: All resrouces pertaining to the statement
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
- UserActions: all users associated with s3 privileges
  - User: username of IAM user
  - Actions: all S3 actions associated with the user
    - PrivilegeGuide: privilege assigning the policy
    - PrivilegeName: name of the privilege
    - Allow: all allow statements within the policy
      - Action: S3 actions associated with the statement
      - Resource: All resources pertaining to the statement
    - Deny: all deny statements within the policy
      - Action: S3 actions associated with the statement
      - Resource: All resources pertaining to the statement


s3.json

```json
{
  "Date": string,
  "Buckets": [
    {
      "name": string,
      "AccessConfigurations": {
        "BlockPublicAcls": true|false,
        "IgnorePublicAcls": true|false,
        "BlockPublicPolicy": true|false,
        "RestrictPublicBuckets": true|false
      }
    },
    ...
  ]
}
```

Schema:
- Date: date of running the script
- Buckets: All S3 buckets in the environment
  - name: name of the bucket
  - AccessConfigurations: The PublicAccessBlock configuration currently in effect for this Amazon S3 bucket.
    - BlockPublicAcls: Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket. Setting this element to TRUE causes the following behavior:
      * PUT Bucket acl and PUT Object acl calls fail if the specified ACL is public.
      * PUT Object calls fail if the request includes a public ACL.
      * PUT Bucket calls fail if the request includes a public ACL.
    - IgnorePublicAcls: Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket. Setting this element to TRUE causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket.
    - BlockPublicPolicy: Specifies whether Amazon S3 should block public bucket policies for this bucket. Setting this element to TRUE causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.
    - RestrictPublicBuckets: Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to TRUE restricts access to this bucket to only AWS services and authorized users within this account if the bucket has a public policy.
