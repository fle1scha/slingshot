# run.py
from app import app, config
from app.repository.setup_db import setup_database

if __name__ == '__main__':
    app.run(debug=config.DEBUG)