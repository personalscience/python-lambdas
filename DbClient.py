from pymongo import MongoClient

from Environment import (
        DEVELOPMENT,
        PRODUCTION,
        get_environment,
        get_db_host,
        get_mongo_username,
        get_mongo_password
        )


env = get_environment()

if env == DEVELOPMENT:
    client = MongoClient(
            host=get_db_host()
            )
elif env == PRODUCTION:
    client = MongoClient(
            host=get_db_host(),
            ssl=True,
            replicaSet='app-shard-0',
            authSource='admin',
            username=get_mongo_username(),
            password=get_mongo_password()
            )
