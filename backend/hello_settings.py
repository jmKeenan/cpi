"""
This file looks for an env.json file in the root of backend
which determines many configuration properties for the app,
such as which database to connect to, and supplying secrets.

Ansible ensures that prod and staging having a different env.json file to allow them to work differently.

If you would like to locally simulate the environment of staging or prod,
you can set the environmental variable HELLO_FORCE_USE_ENVIRON
This will cause hello_settings.py to look in a different location for env.json (see FORCE_ENVIRON below)

Constants from this file can be freely imported from anywhere in the backend.
This file should import from no other files in the project.
"""
import os, json
import hello_config as hello_config


# project path
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_PATH = os.path.join(PROJECT_PATH, 'backend')
print 'PROJECT_PATH: {}'.format(PROJECT_PATH)
print 'BACKEND_PATH: {}'.format(BACKEND_PATH)


# configure path to env.json (default is env.json but can use FORCE_ENVIRON to override this)
FORCE_ENVIRON = os.environ.get('HELLO_FORCE_USE_ENVIRON')
if FORCE_ENVIRON == 'PROD':
    ENV_PATH = os.path.join(BACKEND_PATH, 'devops/secret_files/prod_env.json')
elif FORCE_ENVIRON == 'STAGING':
    ENV_PATH = os.path.join(BACKEND_PATH, 'devops/secret_files/staging_env.json')
elif FORCE_ENVIRON == 'TEST':
    ENV_PATH = os.path.join(BACKEND_PATH, 'devops/secret_files/test_env.json')
else:
    ENV_PATH = os.path.join(BACKEND_PATH, 'env.json')
print 'ENV_PATH: {}'.format(ENV_PATH)

# load env.json into ENV_DICT
ENV_DICT = json.loads(open(ENV_PATH, "r").read())


# configure database url dynamically
def get_db_url(db_dict=None):
    if not db_dict:
        db_dict = ENV_DICT['DB_CONNECTION']
    db_string = '{sql}://{username}:{password}@{host}:{port}/{dbname}'.format(
        sql=db_dict['sql'],
        username=db_dict['user'],
        password=db_dict['password'],
        port=db_dict['port'],
        host=db_dict['host'],
        dbname=db_dict['database']
    )
    return db_string

# constants
PASSWORD_RESET_LINK_EXPIRATION_DAYS = 2
AUTH_TOKEN_EXPIRATION_WEEKS = 4
FLASK_ADMIN_URL = '/admin'

# paths
FLASK_DIR = os.path.join(BACKEND_PATH, 'hello_webapp')
TEMPLATE_DIR = os.path.join(BACKEND_PATH, 'templates')
STATIC_DIR = os.path.join(FLASK_DIR, 'static')


# secrets not in env.json
SECRETS_PATH = os.path.join(BACKEND_PATH, 'devops/secret_files')
GOOGLE_SECRETS_PATH = os.path.join(SECRETS_PATH, 'google/client_secret.json')
GOOGLE_STORAGE_LOCATION = os.path.join(SECRETS_PATH, 'google/gmail.storage')


# for debugging sql
if ENV_DICT.get('DEBUG_SQL'):
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# configs
ENV_DICT['ALERT_EMAILS'] = hello_config.ALERT_EMAILS
