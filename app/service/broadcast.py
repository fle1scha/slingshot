from twilio.base.exceptions import TwilioRestException
import config

class Broadcaster:
 
    def __init__(self, twilio_client, logger):
        """
        Initializes the Broadcaster class with the Twilio client and a logger.

        Args:
            twilio_client (twilio.rest.Client): The Twilio client instance.
            logger (logging.Logger): The logger instance.
        """
        self.client = twilio_client
        self.logger = logger

    #  Retrieves a set of unique phone numbers from the Twilio message history.
    def get_unique_phone_numbers(self):
        messages = self.client.messages.list(limit=1000)
        phone_numbers = set()

        for message in messages:
            phone_numbers.add(message.to)

        return phone_numbers

    #  Send an SMS to the specified phone number.
    def send_message(self, phone_number, message_body):
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=config.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            self.logger.info(f"message send initiated to {phone_number}. sid: {message.sid}")
            return True, ''
        except TwilioRestException as e:
            self.logger.error(f"message send failed to {phone_number}. error: {str(e)}")
            return False, 'error, sorry. try again later.'
        