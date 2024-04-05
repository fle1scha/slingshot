# app.py
from twilio.rest import Client

from flask import Flask, request, jsonify, render_template
from broadcast import Broadcaster
import logging
import config

# Initialize Flask app
app = Flask(__name__)
app.static_folder = 'static'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
 
# Initialize Broadcaster class with Twilio client and logging
broadcaster = Broadcaster(client, logger)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        
        # The welcome message you'd like the user to receive
        welcome_message = 'welcome! slingshot is a community adventure project. you\'ll hear from us soon.'
        
        # Use broadcaster to send the message
        success, error_message = broadcaster.send_message(input_phone_number, welcome_message)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True, 'error_message': error_message}), 400
        
    # Render the page template on a GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for local development