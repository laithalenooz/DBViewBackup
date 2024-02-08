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

import json


def load_config(config_file_path):
    with open(config_file_path, 'r') as file:
        config = json.load(file)
    return config['database'], config['aws']
