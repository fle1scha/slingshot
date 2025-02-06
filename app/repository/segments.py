from datetime import datetime
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

    def check_segment_exists(self, user_id, segment_id, date_of_effort):
        """Check if a specific segment effort exists for the user."""
        SELECT_SEGMENT_SQL = "SELECT * FROM segments WHERE user_id = %s AND segment_id = %s AND date_of_effort = %s;"
        try:
            result = self.run_select_query(SELECT_SEGMENT_SQL, (user_id, segment_id, date_of_effort))
            return len(result) > 0  # Return True if segment effort exists
        except pymysql.MySQLError as e:
            self.logger.error(f"Error checking if segment exists for user {user_id}: {e}")
            return False

    def insert_segment_time(self, username, user_id, segment_id, time_taken, date_of_effort):
        """Insert segment time data into the segments table."""
        
        # Convert date_of_effort to a suitable format
        if date_of_effort.endswith('Z'):
            date_of_effort = date_of_effort[:-1]  # Remove the 'Z'
        
        # Assuming the date_of_effort is in ISO 8601 format, convert it nicely
        try:
            # Parse the date and reformat it if necessary
            formatted_date_of_effort = datetime.fromisoformat(date_of_effort).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            self.logger.error(f"Date format error for date_of_effort: {date_of_effort}, error: {e}")
            return False, 'invalid_date_format'  # Handle date format issue early

        # First check if the segment time already exists for the user
        if self.check_segment_exists(user_id, segment_id, date_of_effort):
            self.logger.error(f"Segment effort for user {username} and segment {segment_id} on date {date_of_effort} already exists.")
            return False, 'segment_exists'  # Segment time already exists

        INSERT_TIME_SQL = """
        INSERT INTO segments (username, user_id, segment_id, time_taken, date_of_effort)
        VALUES (%s, %s, %s, %s, %s);
        """

        try:
            self.execute_sql_command(INSERT_TIME_SQL, (username, user_id, segment_id, time_taken, formatted_date_of_effort))
            return True, None  # Success, no error
        except pymysql.MySQLError as e:
            self.logger.error(f"Failed to insert segment time for user {username}: {e}")
            return False, 'unknown_error'

    def get_all_segment_times(self):
        """Retrieve all segment times from the segments table."""
        SELECT_SEGMENTS_SQL = "SELECT * FROM segments ORDER BY date_of_effort;"
        try:
            return self.run_select_query(SELECT_SEGMENTS_SQL)
        except pymysql.MySQLError as e:
            self.logger.error(f"Error retrieving all segment times: {e}")
            return None  # Failure

    def get_segment_times_by_id(self, user_id):
        """Retrieve segment times for a specific user based on user_id."""
        SELECT_SEGMENT_TIMES_SQL = "SELECT segment_id, time_taken, date_of_effort FROM segments WHERE user_id = %s ORDER BY date_of_effort DESC;"
        try:
            return self.run_select_query(SELECT_SEGMENT_TIMES_SQL, (user_id,))
        except pymysql.MySQLError as e:
            self.logger.error(f"Error fetching segment times for user {user_id}: {e}")
            return None  # Failure

    def get_all_times_by_segment_id(self, segment_id, filter_date=None):
        """Retrieve all segment times for a given segment_id with optional date filtering."""
        
        # Base SQL query to fetch segment times
        SELECT_SEGMENT_TIMES_SQL = """
        SELECT username, user_id, segment_id, time_taken, date_of_effort 
        FROM segments 
        WHERE segment_id = %s
        """
        
        # Include date filtering if a filter_date is provided
        if filter_date:
            SELECT_SEGMENT_TIMES_SQL += " AND DATE(date_of_effort) = %s"  # Using DATE to extract the date part
        
        SELECT_SEGMENT_TIMES_SQL += " ORDER BY time_taken DESC;"

        try:
            # Create parameters for the query
            params = (segment_id,)
            if filter_date:
                params += (filter_date,)  # Add filter_date to the query parameters
                
            # Execute the query and retrieve results
            raw_results = self.run_select_query(SELECT_SEGMENT_TIMES_SQL, params)
            
            # Format results into a list of dictionaries for easier access
            formatted_results = [
                {
                    'username': row[0],
                    'user_id': row[1],
                    'segment_id': row[2],
                    'time_taken': row[3],
                    'date_of_effort': row[4]
                }
                for row in raw_results
            ]
            
            print("formatted results")
            print(formatted_results)
            return formatted_results
        except pymysql.MySQLError as e:
            self.logger.error(f"Error fetching segment times for segment {segment_id}: {e}")
            return None  # Failure