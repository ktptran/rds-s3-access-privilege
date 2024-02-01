# RDS endpoints

Provide the DNS endpoint instead & associate DB instance name / type of DB found (completed)


## Setup

Install ipython:

```
pip install ipython
```

## Deploy

In this directory, run the command:

```bash
ipython src/rds.py
```

## Output

`rds_endpoint.json` contains all of the following information for every RDS instance in us-west-2:
{
  'Date': string
  'Endpoint': [
    {
      'Endpoint': {
        'Address': 'string',
        'Port': 123,
        'HostedZoneId': 'string'
      },
      'DBInstanceArn': 'string',
      'DBInstanceClass': 'string',
      'DBInstanceIdentifier': 'string'
      'Engine': 'string'
      'PubliclyAccessible': True|False,
    },
    ...  
  ]
}

- 'Endpoint': Specifies the connection endpoint
  - 'Address': Specifies the DNS address of the DB instance.
  - 'Port': Specifies the port that the database engine is listening on.
  - HostedZoneId': Specifies the ID that Amazon Route 53 assigns when you create a hosted zone.
- 'DBInstanceArn': The Amazon Resource Name (ARN) for the DB instance.
- 'DBInstanceClass': The DB instance class for a DB instance.
- 'DBInstanceIdentifier': This identifier is the unique key that identifies a DB instance.
- 'Engine': Provides the name of the database engine to be used for this DB instance.
- 'PubliclyAccessible': Specifies the accessibility options for the DB instance.
  - When the DB instance is publicly accessible, its DNS endpoint resolves to the private IP address from within the DB instance's VPC, and to the public IP address from outside of the DB instance's VPC. Access to the DB instance is ultimately controlled by the security group it uses, and that public access is not permitted if the security group assigned to the DB instance doesn't permit it.
  - When the DB instance isn't publicly accessible, it is an internal DB instance with a DNS name that resolves to a private IP address.

For more information reference [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances) documentation.
