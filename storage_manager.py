"""
Database Backup Script
----------------------
This script backs up database views to a local file or AWS S3.

Author: Laith Al Enooz
Date: 2024-02-08
Version: Script version (1.0)
License: MIT License

Requirements:
- Python 3.x
- pymysql
- boto3

Usage:
- Configure database and AWS credentials in the script or through a configuration file.
- Run the script using Python 3.x.
"""

import boto3
from datetime import datetime


def save_backup(backup_sql, storage_choice, aws_config, db_name):
    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{db_name}_{time}_backup.sql"
    with open(filename, "w") as file:
        file.write(backup_sql)

    if storage_choice == "s3":
        s3 = boto3.client("s3", aws_access_key_id=aws_config['access_key'],
                          aws_secret_access_key=aws_config['secret_key'])
        with open(filename, "rb") as file:
            s3.upload_fileobj(file, aws_config['bucket_name'], filename)
        return f"S3://{aws_config['bucket_name']}/{filename}"
    else:
        return filename
