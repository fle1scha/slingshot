import threading
import time
from time import sleep
import pymysql
from dbutils.pooled_db import PooledDB
from config import Config

# Create a pooled database connection
pool = PooledDB(
    creator=pymysql,
    maxconnections=5,  # Adjust based on expected traffic
    mincached=2,
    blocking=True,
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.DB_NAME,
    charset=Config.MYSQL_CHARSET,
    autocommit=True
)

def get_db_connection():
    """Retrieve a connection from the pool."""
    return pool.connection()

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

CREATE_TABLE_SEGMENTS_SQL = f"""
CREATE TABLE IF NOT EXISTS `{Config.DB_NAME}`.`segments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL,
    `user_id` VARCHAR(100) NOT NULL,
    `segment_id` VARCHAR(100) NOT NULL,
    `time_taken` INT NOT NULL,
    `date_of_effort` TIMESTAMP NOT NULL,
    `date_added` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""

def run_sql_command(sql_command, logger, max_retries=3, retry_delay=5):
    """Execute an SQL command with retry logic and connection pooling."""
    retries = 0
    while retries < max_retries:
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SET wait_timeout = 172800")
                    cursor.execute("SET interactive_timeout = 172800")
                    cursor.execute(sql_command)
            return None
        except pymysql.err.OperationalError as e:
            if e.args[0] == 2006:  # MySQL server has gone away
                logger.error(f"MySQL server has gone away. Retrying {retries + 1}/{max_retries}.")
                retries += 1
                sleep(retry_delay)
            else:
                logger.error(f"Error executing SQL command: {e}")
                return str(e)
        except pymysql.MySQLError as e:
            logger.error(f"Error executing SQL command: {e}")
            return str(e)
    return "Max retries reached. Unable to execute SQL command."

def check_db_connection():
    """Check if the database connection is alive."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        return True
    except pymysql.MySQLError:
        return False

def keep_db_alive():
    """Run a background thread that pings the database every 5 minutes to keep the connection alive."""
    while True:
        if not check_db_connection():
            print("Reconnecting to the database...")
        time.sleep(300)  # Run every 5 minutes

# Start the database heartbeat thread
threading.Thread(target=keep_db_alive, daemon=True).start()

def setup_database(logger, max_retries=3, retry_delay=5):
    """Setup the database, users, and tables with retry logic."""
    retries = 0
    while retries < max_retries:
        try:
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

            table_error = run_sql_command(CREATE_TABLE_SEGMENTS_SQL, logger)
            if table_error:
                logger.error(table_error)
                return

            logger.info("Table 'segments' created or already exists in the database.")
            return
        except pymysql.err.OperationalError as e:
            if e.args[0] == 2006:  # MySQL server has gone away
                logger.error(f"MySQL server has gone away. Retrying the database setup (attempt {retries + 1}/{max_retries}).")
                retries += 1
                sleep(retry_delay)
            else:
                logger.error(f"Error setting up the database: {e}")
                return
        except pymysql.MySQLError as e:
            logger.error(f"Error setting up the database: {e}")
            return