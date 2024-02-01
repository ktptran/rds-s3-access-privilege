# RDS Access

## Objectives and Key Results (OKRs)

1. Provide the DNS endpoint instead & associate DB instance name / type of DB found (completed)
2. How to get user list and permission for RDS

## Background

RDS permissions can be divided into two different categories:

* IAM privileges - provision new RDS instances & monitor them through the CLI/console
* Security group, NACLs, and VPC configurations - connect to the RDS instance to use the information & data within

IAM privileges are similar to what we did through S3 whereas security groups, NACLs, and VPC configurations are all about IP addresses and ports.

Provide fields available for user access / permissions

IAM Privileges: Username, action, resource, policy, etc. (similar to S3)
Per [RDS instance](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances):
[Security Groups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_security_groups): Name, Status, IP ranges authorized or revoked
[Subnets](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_subnet_groups): Identifier, Availability Zone, Status
[NACLs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_acls) (attached to subnets): Cidr blocks, Egress, IcmpTypeCode, Ipv6 Cidr Blocks


How to get user (activity) logs for RDS

User activity [logs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/logging-using-cloudtrail.html) for RDS can only be found through CloudTrail logs. 
RDS only provides metrics to see how the database is [functioning](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MonitoringOverview.html) (reference extra information below).


## Out of Scope

Provide fields available for user activity and associated with commands: This would be out of scope because we are querying [CloudTrail logs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/logging-using-cloudtrail.html) and not doing it directly through the boto3 API.

Extra Information:

* [Enhanced Monitoring](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html) provides metrics in real time for the operating systems.
* [Performance insights](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html) provide more information on visualizing the db load, filter & load by waits (minimal info through boto3 API).
* [DB Log Files](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.html) provide information such as error logs, slow query logs, and audit logs. (Boto3 [log files](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_log_files) & [downloading](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.download_db_log_file_portion))
