## slingshot

### To-Do: Tickets 

- **[SLNG-1]** Move from pythonanywhere.com to AWS hosting. 

- **[SLNG-2]** Continue repository implementation for `INSERT` new number and `SELECT` for number lookup. 

- **[SLNG-3]** Add logic to `broadcast.py` so that a user cannot enter the same number twice. 

- **[SLNG-4]** Add logic to `broadcast.py` to get all numbers to prepare for broadcast. 

- **[SLNG-5]** Add logic to `broadcast.py` using Twilio APIs or `for` loop on `send_message` to create a broadcast function.

- **[SLNG-6]** Find a better way to set env vars for `local` and `prod` deployments. How does this work with AWS? 

- **[SLING-7]** Update DNS so that `slingshot.wtf` forwards to `https://slingshot.wtf`. 


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

Configure the following environment variables with your Twilio and MySQL credentials. At the moment, these are stored in `config.py`.

```python
# Twilio configuration
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER

# MySQL configuration
MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_CHARSET

# Database and database user configuration
DB_NAME
DB_USER
DB_PASSWORD
```


### Usage
Run the script below to set up the database and start the server.  The web app will be accessible at http://localhost:5000.


```zsh
python3 run.py
```

### Contributing
Contributions to the project are welcome. 

### License
This project is licensed under the MIT License.