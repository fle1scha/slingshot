import re
from twilio.base.exceptions import TwilioRestException
from config import Config

class BroadcasterService:
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

    # Retrieves a set of unique phone numbers from the Twilio message history.
    def get_unique_phone_numbers_twilio(self):
        messages = self.client.messages.list(limit=1000)
        phone_numbers = set()

        for message in messages:
            phone_numbers.add(message.to)

        return phone_numbers

    # Retrieves a set of unique phone numbers from the database.
    def get_unique_phone_numbers(self):
        messages = self.client.messages.list(limit=1000)
        phone_numbers = set()

        for message in messages:
            phone_numbers.add(message.to)

        return phone_numbers

    # Common method to send a message
    def _send_message_internal(self, phone_number, message_body):
        try:
            # In local, don't hit Twilio messages.create API
            if Config.ENVIRONMENT != 'development':
                try:
                    message = self.client.messages.create(
                        body=message_body,
                        from_=Config.TWILIO_PHONE_NUMBER,
                        to=phone_number
                    )
                    self.logger.info(f"Twilio message sent to {phone_number}. Message SID: {message.sid}")
                    return True, ""
                except TwilioRestException as e:
                    error_message = str(e)
                    self.logger.error(f"Message send failed to {phone_number}. Error: {error_message}")
                    return False, 'error. please try again later.'
            else:
                self.logger.info(f"Skipping Twilio API call in {Config.ENVIRONMENT} environment")
                return True, ""
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while sending message to {phone_number}. Error: {str(e)}")
            return False, 'error. please try again later.'


    def send_welcome_message(self, input_name, input_phone_number, welcome_message):
        return self.send_message(input_name, input_phone_number, welcome_message)


    def send_message(self, name, phone_number, message_body, register_user=True):
        try:
            if not is_valid_us_phone_number(phone_number):
                self.logger.warning(f"Invalid phone number format: {phone_number}")
                return False, 'invalid phone number format.'

            if not name or not is_safe_input(name) or len(name) > 100:
                self.logger.warning(f"Invalid or unsafe name: {name}")
                return False, 'invalid name.'

            if register_user:
                success, error_message = self.repository.insert_new_user(name.strip(), phone_number.strip())
                if not success:
                    if error_message == 'already_registered':
                        self.logger.info(f"{phone_number} under name {name} already in database. Error: {error_message}")
                        return False, 'already with us.'
                    else:
                        self.logger.error(f"Failed to add {name} with phone number {phone_number} to the database. Error: {error_message}")
                        return False, 'error. Please try again later.'

            return self._send_message_internal(phone_number.strip(), message_body.strip())

        except Exception as e:
            self.logger.error(f"Unexpected error occurred while sending message to {name} with number {phone_number}. Error: {str(e)}")
            return False, 'error. please try again later.'
        
def is_valid_us_phone_number(phone_number):
        pattern = re.compile(r'^(?:\+1\s?)?(?:\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}$')
        return pattern.match(phone_number) is not None

def is_safe_input(text):
        return not re.search(r'[<>{};$]', text)