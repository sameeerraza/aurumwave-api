@echo off
echo Django server script started

:: Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Ensure the requirements are installed
echo Installing requirements
pip install -r requirements.txt

:: Run migrations
echo Running Django migrations
python manage.py migrate

:: Run the Django server
echo Running Django server
python manage.py runserver

echo Django server has been shut down
pause
