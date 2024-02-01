# RDS Logs

Within RDS, we want to obtain the following information per RDS instance:
* The queries ran
* User who entered query
* Query time
* DB Instance
* Table referenced

## Setup
To setup the RDS logs you'll need access to the databases and parameter groups within RDS.
_MySQL_
1. Create a parameter group for your instances
2. Set the logging parameters for MySQL
* General_log = 1 (default value is 0 or no logging)
* Slow_query_log = 1 (default value is 0 or no logging)
* Long_query_time = 2 (to log queries that run longer than two seconds)
* log_output = FILE (to write both the general and slow query logs to the file system & allow viewing the logs from the RDS console)
3. Save changes
4. Update the instances with the parameter group

These directions are outlined in the following [link](https://aws.amazon.com/premiumsupport/knowledge-center/rds-mysql-logs/)

## Retrieve Logs
To retrieve the logs from the parameter group run the following command in this directory:

```bash
ipython src/logs.py
```

## Output
Running the code will download the log files into the output directory. Within this folder, each RDS instance will have a folder of its log files with the RDSInstanceIdentifier as its name.

The log output itself is
