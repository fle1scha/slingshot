# Slingshot

## Setup Instructions

1. **Create a virtual environment** in the project directory:

    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

3. **Install the required Python modules** with `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Twilio** by creating an account, obtaining your Account SID and Auth Token, and purchasing a phone number for SMS messaging.

5. **Set up environment variables** with your Twilio credentials:

    ```bash
    export TWILIO_ACCOUNT_SID='Your_Twilio_Account_SID'
    export TWILIO_AUTH_TOKEN='Your_Twilio_Auth_Token'
    export TWILIO_PHONE_NUMBER='Your_Twilio_Phone_Number'
    ```

    For permanent configuration, you may create a `.env` file or a `config.py`.

6. **Start the Flask application**:

    ```bash
    python app.py
    ```

    The application will be accessible at `http://localhost:5000`.

## Usage

Navigate to the root URL to access the user registration form. Once submitted, the app will attempt to send an SMS to the provided phone number.

## Deployment

Deploy the application on a web hosting service like PythonAnywhere, ensuring all environment variables are set in the production environment.

## License

This project is licensed under the MIT License.