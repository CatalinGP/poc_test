#!/bin/bash

# Navigate to the project directory
cd /home/RandstadDevUser

# Pull the latest changes from GitHub
git pull origin main

# Activate the virtual environment
# source env/bin/activate

# Install the new dependencies
# pip install -r requirements.txt

# Restart the Flask application
touch /var/www/randstaddevuser_pythonanywhere_com_wsgi.py

