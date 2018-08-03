import os
from pymongo import MongoClient

from chalicelib import Environment


env = Environment.get_environment()

if env == Environment.DEVELOPMENT:
    client = MongoClient()
elif env == Environment.PRODUCTION:
    username = os.environ['MONGODB_USER']
    password = os.environ['MONGODB_PASSWORD']

    hostname = "mongodb+srv://" + username + ":" + password + "@app-odwna.mongodb.net/app?retryWrites=true"
    print('hostname', hostname)

    client = MongoClient(hostname)
