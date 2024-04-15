# run.py
from app import app
from config import Config

if __name__ == '__main__':
    Config.validate()
    if Config.ENVIRONMENT == 'development':
        app.run(debug=True)
        print()
    else:
        app.run(debug=False)