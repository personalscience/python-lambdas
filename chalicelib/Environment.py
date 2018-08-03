import os


# Environment definitions.
DEVELOPMENT = 'development'
PRODUCTION = 'production'

def get_environment():
    return os.environ.get('ENV') or DEVELOPMENT
