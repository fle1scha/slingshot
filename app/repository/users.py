import pymysql
import config

class Users:
    def __init__(self, logger):
        """
        Initializes the Users repository with a logger.
        Args:
            logger (logging.Logger): The logger instance.
        """
        self.logger = logger
        self.db_connection = self.create_db_connection()

    def create_db_connection(self):
        """
        Creates a connection to the existing database with tables already set up.
        """
        return pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            db=config.DB_NAME,
            charset=config.MYSQL_CHARSET,
            autocommit=True
        )

    def setup_database(self):
        """
        Set up the database, create the user, grant privileges, and create the users table.
        """
        # Execute SQL commands to set up the database and tables
        self.execute_sql_command(self.CREATE_TABLE_USERS_SQL)

    def execute_sql_command(self, command, values=None):
        """
        Executes an SQL command that does not expect a result set
        """
        try:
            with self.db_connection.cursor() as cursor:
                if values:
                    cursor.execute(command, values)
                else:
                    cursor.execute(command)
                self.db_connection.commit()
        except pymysql.MySQLError as e:
            self.logger.error(f"Error with SQL command: {e}")
            raise

    def run_select_query(self, query, values=None):
        """
        Executes a SELECT SQL query and returns the fetched results.
        """
        try:
            with self.db_connection.cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            self.logger.error(f"Error with SELECT query: {e}")
            raise

    # Methods for inserting and retrieving users
    def insert_new_user(self, name, phone_number):
        INSERT_USER_SQL = f"""
        INSERT INTO users (name, phone_number)
        VALUES (%s, %s);
        """
        try:
            self.execute_sql_command(INSERT_USER_SQL, (name, phone_number))
            return True, None  # Success, no error
        except pymysql.err.IntegrityError:
            self.logger.info(f"Failed to add user {name} with phone number {phone_number} to the database. Error: Duplicate phone number")
            return False, 'already_registered'
        except pymysql.MySQLError as e:
            self.logger.error(f"Failed to add user {name} with phone number {phone_number} to the database. Error: {e}")
            return False, 'unknown_error'

    def get_all_users(self):
        SELECT_USER_SQL = "SELECT * FROM users ORDER BY date_added DESC;"
        try:
            return self.run_select_query(SELECT_USER_SQL)
        except pymysql.MySQLError as e:
            self.logger.error(f"Error with get_all_users: {e}")
            return None  # Failure

    # Class-level SQL statements
    CREATE_TABLE_USERS_SQL = f"""
    CREATE TABLE IF NOT EXISTS `{config.DB_NAME}`.`users` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(100),
        `phone_number` VARCHAR(15) NOT NULL UNIQUE,
        `date_added` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """