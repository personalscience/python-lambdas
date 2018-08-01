import os


# Environment definitions.
DEVELOPMENT = 'development'
PRODUCTION = 'production'

def get_environment():
    return os.environ.get('ENV') or DEVELOPMENT

def get_db_host():
    env = get_environment()

    if env == PRODUCTION:
        return 'app-shard-00-00-odwna.mongodb.net:27017,app-shard-00-01-odwna.mongodb.net:27017,' \
                + 'app-shard-00-02-odwna.mongodb.net:27017'
    elif env == DEVELOPMENT:
        return 'localhost'

def get_mongo_username():
    return os.environ['MONGODB_USER']

def get_mongo_password():
    return os.environ['MONGODB_PASSWORD']

def get_cors_origin():
    env = get_environment()

    if env == PRODUCTION:
        # TODO: Make me `app.personalscience`.
        return 'https://rebuild.personalscience.com'
    elif env == DEVELOPMENT:
        return 'http://localhost:3000'
