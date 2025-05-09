import socket
import os

GOOGLE_API_KEY = 'AIzaSyADFBuqHulTabrfvv80c9pts3GvTtGZ44M'
# Get the hostname of the local machine
hostname = socket.gethostname()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
from core.local_settings import *  # Import local settings for development

# Check if the hostname indicates an EC2 instance
if 'ec2' in hostname:
    # Apply settings for production
    # SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://ummapp.net', 'https://www.ummapp.net']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'platform',
            'USER': 'DBprojectUser',
            'PASSWORD': 'password',
            'HOST':'umm-database.chmu088ua4n2.us-east-1.rds.amazonaws.com',
            'PORT':'3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'platform',
            'USER': 'DBprojectUser',
            'PASSWORD': 'password',
            'HOST':'localhost',
            'PORT':'',
        }
    }
    