import pymysql
from config import Config

# SQL Statements
CREATE_DATABASE_SQL = f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME};"
CREATE_USER_SQL = f"""
CREATE USER IF NOT EXISTS '{Config.DB_USER}'@'{Config.MYSQL_HOST}' IDENTIFIED BY '{Config.DB_PASSWORD}';
"""
GRANT_PRIVILEGES_SQL = f"""
GRANT SELECT, UPDATE, INSERT ON `{Config.DB_NAME}`.* TO `{Config.DB_USER}`@`{Config.MYSQL_HOST}`;
"""
CREATE_TABLE_USERS_SQL = f"""
CREATE TABLE IF NOT EXISTS `{Config.DB_NAME}`.`users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100),
    `phone_number` VARCHAR(15) NOT NULL UNIQUE,
    `date_added` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def run_sql_command(sql_command, logger):
    try:
        with pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            charset=Config.MYSQL_CHARSET,
            autocommit=True
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
    except pymysql.MySQLError as e:
        logger.error(f"Error executing SQL command: {e}")
        return str(e)
    return None

def setup_database(logger):
    # Create the database
    database_error = run_sql_command(CREATE_DATABASE_SQL, logger)
    if database_error:
        logger.error(database_error)
        return

    logger.info(f"Database '{Config.DB_NAME}' created or already exists.")

    # Create the user and grant privileges
    user_error = run_sql_command(CREATE_USER_SQL, logger)
    if user_error:
        logger.error(user_error)
        return

    privileges_error = run_sql_command(GRANT_PRIVILEGES_SQL, logger)
    if privileges_error:
        logger.error(privileges_error)
        return

    logger.info(f"User '{Config.DB_USER}' created or already exists, and privileges granted.")

    # Create the table(s)
    table_error = run_sql_command(CREATE_TABLE_USERS_SQL, logger)
    if table_error:
        logger.error(table_error)
        return

    logger.info("Table 'users' created or already exists in the database.")