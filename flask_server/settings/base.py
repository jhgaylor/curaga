import os
SITE_ROOT = os.path.dirname(os.path.realpath('__file__'))

# configuration
DATABASE = os.path.join(SITE_ROOT, 'curaga.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'