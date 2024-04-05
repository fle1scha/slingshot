import pymysql
import config

# SQL Statements
CREATE_DATABASE_SQL = f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME};"
CREATE_USER_SQL = f"""
CREATE USER IF NOT EXISTS '{config.DB_USER}'@'localhost' IDENTIFIED BY '{config.DB_PASSWORD}';
"""
GRANT_PRIVILEGES_SQL = f"""
GRANT ALL PRIVILEGES ON {config.DB_NAME}.* TO '{config.DB_USER}'@'localhost';
"""
CREATE_TABLE_USERS_SQL = f"""
CREATE TABLE IF NOT EXISTS {config.DB_NAME}.users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

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
    except pymysql.MySQLError as e:
        print(f"Error {e.args[0]}, {e.args[1]}")
    finally:
        connection.close()

def setup_database():
    # Create the database
    run_sql_command(CREATE_DATABASE_SQL)
    print(f"Database '{config.DB_NAME}' created or already exists.")

    # Create the user and grant privileges
    run_sql_command(CREATE_USER_SQL)
    run_sql_command(GRANT_PRIVILEGES_SQL)
    print(f"User '{config.DB_USER}' created or already exists, and privileges granted.")

    # Create the table(s)
    run_sql_command(CREATE_TABLE_USERS_SQL)
    print("Table 'users' created or already exists in the database.")

if __name__ == '__main__':
    setup_database()