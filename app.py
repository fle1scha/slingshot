from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import config
import logging

app = Flask(__name__)
app.static_folder = 'static'

# Registration configuration
WELCOME_MESSAGE = 'welcome! slingshot is a community adventure project. you\'ll hear from us soon.'

# Twilio client
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']

        try:
            # Lookup if the client has already registered.
            
            
            # Send the SMS
            message = client.messages.create(
                body=WELCOME_MESSAGE,
                from_=config.TWILIO_PHONE_NUMBER,
                to=input_phone_number
            )
            
            # Log successful message initiation
            logging.info(f"message send initiated to {input_phone_number}. sid: {message.sid}")
            return jsonify({'success': True})
        except TwilioRestException as e:
            
            # Log error with initiation
            logging.error(f"message send failed to {input_phone_number}. Error: {str(e)}")
            return jsonify({'error': True, 'error_message': 'error, sorry. try again later.'}), 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run()