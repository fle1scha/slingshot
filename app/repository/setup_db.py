import pymysql
import config

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

def run_sql_command(sql_command, logger):
    try:
        with pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            charset=config.MYSQL_CHARSET,
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

    logger.info(f"Database '{config.DB_NAME}' created or already exists.")

    # Create the user and grant privileges
    user_error = run_sql_command(CREATE_USER_SQL, logger)
    if user_error:
        logger.error(user_error)
        return

    privileges_error = run_sql_command(GRANT_PRIVILEGES_SQL, logger)
    if privileges_error:
        logger.error(privileges_error)
        return

    logger.info(f"User '{config.DB_USER}' created or already exists, and privileges granted.")

    # Create the table(s)
    table_error = run_sql_command(CREATE_TABLE_USERS_SQL, logger)
    if table_error:
        logger.error(table_error)
        return

    logger.info("Table 'users' created or already exists in the database.")