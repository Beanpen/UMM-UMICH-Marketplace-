import socket

# Get the hostname of the local machine
hostname = socket.gethostname()

# Check if the hostname indicates an EC2 instance
if 'ec2' in hostname:
    from core.local_settings import *  # Import local settings for development

    # Apply settings for production
    # SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://ummapp.net', 'https://www.ummapp.net']