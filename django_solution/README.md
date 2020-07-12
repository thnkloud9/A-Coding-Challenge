# Ableton Developer Challenge

This solution uses Django 3 and Django Axes libraries, and satisfies the following requirements:

- A new user can register with their email address and password of choice.
- New user accounts must be activated with a unique token before initial login is allowed.
- Users enter their email address and password to log in. 
- The account will be locked automatically for 60 minutes after 3 login attempts with an incorrect password.

## Requirements

- Python 3.6+

## Installation

**It is recommended to install dependencies into a python3 virtual envronment.**  Once you have created and activated a python3 venv you can run the following command to install dependencies:
```
pip install -r requirements.txt
```

## Setup

### Sync the default database schema
```
python manage.py migrate
```

### Create initial admin user (optional)
```
python manage.py createsuperuser 
```

### Run dev tests
```
python manage.py test 
```

### Start the dev server
```
python manage.py runserver
```
