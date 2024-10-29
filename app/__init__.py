from flask import Flask
import logging
from twilio.rest import Client

from app.repository.segments import Segments
from app.repository.users import Users
from app.service.broadcaster import Broadcaster
from app.repository.setup_db import setup_database
from app.service.segments import SegmentService
from config import Config

# Set up logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)
app.static_folder = 'static'

# Setup the database
setup_database(logger)

users_repository = Users(logger)
logger.info("Users repository set up successfully.")
segments_repository = Segments(logger)
logger.info("Segments repository set up successfully.")

twilioClient = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
logger.info("Twilio client set up successfully.")

broadcaster = Broadcaster(users_repository, twilioClient, logger)
logger.info("Broadcaster service set up successfully.")

segments = SegmentService(segments_repository) 
logger.info("Segments service set up successfully.")



from . import views