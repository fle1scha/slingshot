from flask import Flask, request, render_template
from twilio.rest import Client
import config

app = Flask(__name__)

# Registration configuration
WELCOME_MESSAGE = 'Woza! Welcome to slingshot. You\'ll hear from us soon.'
# Twilio client
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def index():
    success_message = None
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']

        try:
            # Send the SMS
            message = client.messages.create(
                body=WELCOME_MESSAGE,
                from_=config.TWILIO_PHONE_NUMBER,
                to=input_phone_number
            )

            print(message.sid)
            success_message = 'You\'ll hear from us soon'
        except:
            success_message = 'error, sorry'

    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run()