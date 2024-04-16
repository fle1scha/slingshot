from app import app 
from config import Config

application = app # required for Elastic Beanstalk

if __name__ == '__main__':
    Config.validate()
    if Config.ENVIRONMENT == 'development':
        application.run(debug=True)
    else:
        application.run(debug=False)