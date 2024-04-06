# app/__init__.py
from flask import Flask
import logging
from twilio.rest import Client

from app.repository.setup_db import setup_database
from .service.broadcast import Broadcaster
import config

# Set up logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)
app.static_folder = 'static'

## Setup the database
setup_database(logger)

# Initialise Twilio client
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
logger.info("Twilio client set up successfully.")

# Initialize Broadcaster class with Twilio client and logging
broadcaster = Broadcaster(client, logger)
logger.info("Broadcaster service set up successfully.")


