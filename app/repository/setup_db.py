import pymysql
import config
import logging

# SQL Statements
CREATE_DATABASE_SQL = f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME};"
CREATE_USER_SQL = f"""
CREATE USER IF NOT EXISTS '{config.DB_USER}'@'{config.MYSQL_HOST}' IDENTIFIED BY '{config.DB_PASSWORD}';
"""
GRANT_PRIVILEGES_SQL = f"""
GRANT SELECT, UPDATE, INSERT ON `{config.DB_NAME}`.* TO `{config.DB_USER}`@`{config.MYSQL_HOST}`;
"""
CREATE_TABLE_USERS_SQL = f"""
CREATE TABLE IF NOT EXISTS `{config.DB_NAME}`.`users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100),
    `phone_number` VARCHAR(15) NOT NULL UNIQUE,
    `date_added` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute a SQL command and handle any MySQL errors.
def run_sql_command(sql):
    connection = pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        charset=config.MYSQL_CHARSET
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        return None  # Return None if the operation is successful
    except pymysql.MySQLError as e:
        error_message = f"Error with run_sql_command: {e}"
        return error_message

# Set up the database, create the user, grant privileges, and create the users table.
def setup_database(logger):
    # Create the database
    database_error = run_sql_command(CREATE_DATABASE_SQL)
    if database_error:
        logger.error(database_error)
        return

    logger.info(f"Database '{config.DB_NAME}' created or already exists.")

    # Create the user and grant privileges
    user_error = run_sql_command(CREATE_USER_SQL)
    if user_error:
        logger.error(user_error)
        return

    privileges_error = run_sql_command(GRANT_PRIVILEGES_SQL)
    if privileges_error:
        logger.error(privileges_error)
        return

    logger.info(f"User '{config.DB_USER}' created or already exists, and privileges granted.")

    # Create the table(s)
    table_error = run_sql_command(CREATE_TABLE_USERS_SQL)
    if table_error:
        logger.error(table_error)
        return

    logger.info("Table 'users' created or already exists in the database.")

if __name__ == '__main__':
    setup_database()