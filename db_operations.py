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

import pymysql


def connect_to_database(config):
    """
    Establishes a connection to the database.

    :param config: A dictionary containing database configuration parameters.
    :return: A database connection object.
    """
    try:
        connection = pymysql.connect(host=config['host'],
                                     user=config['user'],
                                     password=config['password'],
                                     database=config['db_name'])
        print("Database connection established.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise


def generate_backup_sql(connection):
    """
    Generates SQL for backing up all views in the database.

    :param connection: The database connection object.
    :return: A string containing the SQL commands for the backup.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW FULL TABLES WHERE TABLE_TYPE LIKE 'VIEW';")
        views = [table[0] for table in cursor.fetchall()]

        backup_sql = ""
        for view in views:
            cursor.execute(f"DESCRIBE `{view}`;")
            columns_desc = cursor.fetchall()

            create_table_sql = f"CREATE TABLE IF NOT EXISTS `{view}` (\n"
            for col in columns_desc:
                create_table_sql += f"    `{col[0]}` {col[1]}"
                if col[2] == "NO":
                    create_table_sql += " NOT NULL"
                if col[4]:
                    default_val = col[4]
                    if not (default_val.startswith("'") and default_val.endswith("'")) and not default_val.replace(".",
                                                                                                                   "",
                                                                                                                   1).isdigit():
                        default_val = f"'{default_val}'"
                    create_table_sql += f" DEFAULT {default_val}"
                create_table_sql += ",\n"
            create_table_sql = create_table_sql.rstrip(",\n") + "\n);\n\n"
            backup_sql += create_table_sql

            cursor.execute(f"SELECT * FROM `{view}`;")
            rows = cursor.fetchall()
            if rows:
                columns = [f"`{desc[0]}`" for desc in cursor.description]
                for row in rows:
                    values = []
                    for item in row:
                        if item is None:
                            values.append("NULL")
                        else:
                            values.append(f"'{connection.escape_string(str(item))}'")
                    backup_sql += f"INSERT INTO `{view}` ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
        return backup_sql
    except Exception as e:
        print(f"Error generating backup SQL: {e}")
        raise
    finally:
        cursor.close()


def close_connection(connection):
    """
    Closes the database connection.

    :param connection: The database connection object.
    """
    try:
        connection.close()
        print("Database connection closed.")
    except Exception as e:
        print(f"Error closing the database connection: {e}")
