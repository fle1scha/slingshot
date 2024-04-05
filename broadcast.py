from twilio.base.exceptions import TwilioRestException
import config

class Broadcaster:
    def __init__(self, twilio_client, logger):
        self.client = twilio_client
        self.logger = logger

    def get_unique_phone_numbers(self):
        messages = self.client.messages.list(limit=1000)
        phone_numbers = set()

        for message in messages:
            phone_numbers.add(message.to)

        return phone_numbers

    def send_message(self, phone_number, message_body):
        """
        Send an SMS to the specified phone number.
        Args:
            phone_number (str): The phone number to send the message to.
            message_body (str): The body text of the SMS message.
        Returns:
            bool, str: Indicates success status and an error message if applicable.
        """
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