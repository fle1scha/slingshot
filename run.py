# run.py
from app import app, config

if __name__ == '__main__':
    app.run(debug=config.DEBUG)