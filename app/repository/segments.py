import pymysql
from config import Config

class Segments:
    def __init__(self, logger):
        """
        Initializes the Segments repository with a logger.
        
        Args:
            logger (logging.Logger): The logger instance.
        """
        self.logger = logger
        self.db_connection = self.create_db_connection()

    def create_db_connection(self):
        """
        Creates a connection to the existing database.
        """
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            db=Config.DB_NAME,
            charset=Config.MYSQL_CHARSET,
            autocommit=True
        )
    
    def execute_sql_command(self, command, values=None):
        """
        Executes an SQL command that does not expect a result set.
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

    def insert_segment_time(self, athlete_id, segment_name, time_taken):
        """Insert segment time data into the database, along with date_added."""
        INSERT_TIME_SQL = """
        INSERT INTO segment_times (participant_id, segment_name, time_taken, date_added)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP);  -- Use CURRENT_TIMESTAMP to automatically set the date_added
        """
        
        try:
            self.execute_sql_command(INSERT_TIME_SQL, (athlete_id, segment_name, time_taken))
            return True, None  # Success, no error
        except pymysql.MySQLError as e:
            self.logger.error(f"Failed to insert segment time for athlete {athlete_id}: {e}")
            return False, 'unknown_error'

    def check_user_exists(self, username):
        """Check if a user exists in the database based on their username."""
        SELECT_USER_SQL = "SELECT * FROM participants WHERE name = %s;"
        try:
            result = self.run_select_query(SELECT_USER_SQL, (username,))
            return len(result) > 0  # Return True if user exists
        except pymysql.MySQLError as e:
            self.logger.error(f"Error checking if user exists: {e}")
            return False

    def get_all_segments(self):
        """Retrieve all segment times from the database."""
        SELECT_SEGMENTS_SQL = "SELECT * FROM segment_times ORDER BY segment_name;"
        try:
            return self.run_select_query(SELECT_SEGMENTS_SQL)
        except pymysql.MySQLError as e:
            self.logger.error(f"Error with get_all_segments: {e}")
            return None  # Failure

    def get_segment_times_by_participant(self, participant_id):
        """Retrieve segment times for a specific participant."""
        SELECT_SEGMENT_TIMES_SQL = "SELECT segment_name, time_taken, date_added FROM segment_times WHERE participant_id = %s ORDER BY date_added DESC;"
        try:
            return self.run_select_query(SELECT_SEGMENT_TIMES_SQL, (participant_id,))
        except pymysql.MySQLError as e:
            self.logger.error(f"Error fetching segment times for participant {participant_id}: {e}")
            return None  # Failure
            
    def get_all_participants(self):
        """Retrieve all participants from the database."""
        SELECT_PARTICIPANTS_SQL = "SELECT * FROM participants ORDER BY date_added DESC;"
        try:
            return self.run_select_query(SELECT_PARTICIPANTS_SQL)
        except pymysql.MySQLError as e:
            self.logger.error(f"Error with get_all_participants: {e}")
            return None  # Failure