#!/bin/bash

echo "Django server script started"

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment"
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Ensure the requirements are installed
echo "Installing requirements"
pip install -r requirements.txt

# Run the Django server
echo "Running Django server"
python3 manage.py runserver

echo "Django server has been shut down"
