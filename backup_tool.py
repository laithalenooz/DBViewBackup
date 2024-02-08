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

import argparse
from config_loader import load_config
from db_operations import connect_to_database, generate_backup_sql, close_connection
from storage_manager import save_backup


def main():
    parser = argparse.ArgumentParser(description="Database Backup Tool")
    parser.add_argument("--config-file", help="Path to the configuration file", required=True)
    parser.add_argument("--storage-choice", help="Storage choice: local or S3", required=True)
    args = parser.parse_args()

    # Load configurations
    db_config, aws_config = load_config(args.config_file)

    # Establish database connection
    connection = connect_to_database(db_config)

    # Backup process
    backup_sql = generate_backup_sql(connection)
    filename = save_backup(backup_sql, args.storage_choice, aws_config, db_config['db_name'])

    # Cleanup
    close_connection(connection)
    print(f"Backup completed. File: {filename}")


if __name__ == "__main__":
    main()
