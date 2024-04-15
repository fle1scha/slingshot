from twilio.base.exceptions import TwilioRestException
import config

class Broadcaster:
 
    def __init__(self, users_repo, twilio_client, logger):
        """
        Initializes the Broadcaster class with the Twilio client and a logger.

        Args:
            users_repo (users.Users)
            twilio_client (twilio.rest.Client): The Twilio client instance.
            logger (logging.Logger): The logger instance.
        """
        self.repository = users_repo
        self.client = twilio_client
        self.logger = logger

    #  Retrieves a set of unique phone numbers from the Twilio message history.
    def get_unique_phone_numbers_twilio(self):
        messages = self.client.messages.list(limit=1000)
        phone_numbers = set()

        for message in messages:
            phone_numbers.add(message.to)

        return phone_numbers

    #  Retrieves a set of unique phone numbers from the database.
    def get_unique_phone_numbers(self):
        
        
        messages = self.client.messages.list(limit=1000)
        phone_numbers = set()

        for message in messages:
            phone_numbers.add(message.to)

        return phone_numbers
    
    # Sends a message to the number and creates a db entry
    def send_message(self, name, phone_number, message_body):
        try:
            if config.ENVIRONMENT != 'DEV':
                message = self.client.messages.create(
                    body=message_body,
                    from_=config.TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                
                self.logger.info(f"Message send initiated to {phone_number}. sid: {message.sid}")
            
            # Add the user to the database
            result, error = self.repository.insert_new_user(name, phone_number)
            if error:
                self.logger.error(f"Failed to add user {name} with phone number {phone_number} to the database. Error: {error}")
                return False, 'Error adding user to the database. Please try again later.'
            
            return True, ''
        
        except TwilioRestException as e:
            self.logger.error(f"Message send failed to {phone_number}. Error: {str(e)}")
            return False, 'Error sending message. Please try again later.'
        