#!/bin/bash

# Activate the virtual environment
source virtual_slingshot/bin/activate

# Run the database setup script
python setup_db.py

# Start the Flask application
export FLASK_APP=app.py   # Make sure FLASK_ENV is set to 'development' if in development mode
flask run