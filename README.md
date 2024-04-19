## slingshot

### To-Do: Tickets 

- ~**[SLNG-1]** Move from pythonanywhere.com to AWS hosting.~

- ~**[SLNG-2]** Continue repository implementation for `INSERT` new number and `SELECT` for number lookup.~

- ~**[SLNG-3]** Add logic to `broadcast.py` so that a user cannot enter the same number twice.~

- **[SLNG-4]** Add logic to `broadcast.py` to get all numbers to prepare for broadcast. 

- **[SLNG-5]** Add logic to `broadcast.py` using Twilio APIs or `for` loop on `send_message` to create a broadcast function.

- ~**[SLNG-6]** Find a better way to set env vars for `local` and `prod` deployments. How does this work with AWS?~

- **[SLING-7]** Update DNS so that `slingshot.wtf` forwards to `https://slingshot.wtf`. 

- ~**[SLING-8]** Add new DWSS logo and background image~


### Setup
To set up the project, follow these steps:

1. Create a virtual environment:

```zsh
python3 -m venv venv
```

2. Activate the virtual environment:

On macOS and Linux:
```zsh
source venv/bin/activate
```

On Windows:
```zsh
venv\Scripts\activate
```

3. Install the required Python modules:

```zsh
pip3 install -r requirements.txt
```

4. Twilio 

Sign up for a Twilio account and obtain your Account SID, auth token, and a Twilio phone number.

5. Set up environment variables

Configure the following environment variables with your Twilio and MySQL credentials. At the moment, these are stored in `.env` and loaded into `config.py`. 

```python
# Twilio configuration
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER
```

On AWS, Elastic Beanstalk will also set the following environment variables, so they should be configured for local work too.
```python
RDS_HOSTNAME
RDS_PORT
RDS_USERNAME
RDS_PASSWORD
RDS_DB_NAME
```


### Usage
Run the script below to set up the database and start the server.  The web app will be accessible at http://localhost:5000.

```zsh
python3 app.py
```

To hit the mysql server locally, use the following command. You will be prompted to enter the password for the user for root.

```zsh
mysql -h localhost -u root -p
```

## Preparing for deployment
```zsh
zip -r `date +%d%m%y`-slingshot.zip . -x "*.git*" -x "__pycache__/*" -x "*.env" -x "*.vscode*" -x "venv/*"
```

### License
This project is licensed under the MIT License.