from flask import Flask
import logging
from twilio.rest import Client

from app.repository.users import Users
from app.service.broadcaster import Broadcaster
import config
from app.repository.setup_db import setup_database

# Set up logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)
app.static_folder = 'static'

# Setup the database
setup_database(logger)

# Initialize Users repository
users_repository = Users(logger)

# Initialise Twilio client
twilioClient = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
logger.info("Twilio client set up successfully.")

# Initialize Broadcaster class with Twilio client and logging
broadcaster = Broadcaster(users_repository, twilioClient, logger)
logger.info("Broadcaster service set up successfully.")

from . import views