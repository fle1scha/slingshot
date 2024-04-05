# slingshot

slingshot is an implementation of a simple web app to register users by taking their phone number and sending a message via SMS using Twilio's messaging service.

## Features

- Web form for users to register their phone numbers.
- Integration with Twilio's API to send out SMS messages.
- Logging to record successful and failed message delivery attempts.

### To Be Added
- Database connection for storing and looking up numbers. 
- Functionality for broadcast. 

## Requirements
See `requirements.txt`.


## Setup Instructions

Before running the application, follow these steps to set up the required environment:

1. Install necessary libraries:

    ```
    pip install requirements.txt
    ```

2. Set up Twilio:
   
   - Create a Twilio account if you haven't done so already.
   - Obtain your Account SID and Auth Token from Twilio dashboard.
   - Purchase a Twilio phone number capable of sending SMS messages.

3. Create a `config.py` file in your project directory with the following content:

    ```python
    TWILIO_ACCOUNT_SID = 'Your_Twilio_Account_SID'
    TWILIO_AUTH_TOKEN = 'Your_Twilio_Auth_Token'
    TWILIO_PHONE_NUMBER = 'Your_Twilio_Phone_Number'
    ```

    Replace the placeholder values with your actual Twilio credentials and phone number.

4. Run the Flask application:

    ```
    python app.py
    ```

    By default, the app will run on `http://localhost:5000` unless configured otherwise.

5. Access the application via the browser and test the registration feature.

## Usage

Upon accessing the root URL, users will be presented with a form to enter their phone number. Once the form is submitted, the backend will attempt to send a welcome SMS to the number provided.

## Deployment

This application is ready to be deployed on PythonAnywhere or other hosting services that support Flask apps. Ensure that you configure your environment variables accordingly for production use.

## Logging

The application makes use of Python's `logging` module to log message send events. Logs are outputted to the console with timestamps, log levels, and messages.

## License

This application is open-source software licensed under the MIT license.