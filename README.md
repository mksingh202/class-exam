# Project Setup

## Clone the repository
```bash
git clone https://github.com/mksingh202/class-exam.git
```

##Go to your project directory and use following for installation
### Python2
```bash
pip install -r requirements.txt
```

### Python3
```bash
pip3 install -r requirements.txt
```

## DB Setting [exam/settings.py]:
Create database on your local and setup database credentials.
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<db_name>',
        'USER': '<user_name>',
        'PASSWORD': '<password>',
        'HOST': '<host>', # For local 127.0.0.1
        'PORT': '<port>', # Default 3306
    },
}
``` 

## Set constant for minimum marks to pass [exam/settings.py]
```bash
MIN_TO_PASS = 30
```

## Set default authentication through API [exam/settings.py]
```bash
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

## Migration
### Create database with name class_exam, if want to change then change in exam/settings as well.
#### Go to project directory where you have manage.py and run the following command.
```bash
python3 manage.py migrate
```

## Create Super User
```bash
python3 manage.py createsuperuser
```

## Run Server
```bash
python3 manage.py runserver
```

## Admin Login
```bash
http://127.0.0.1:8000/admin/
```
Create new user that we can say as Teacher.


# APIs
## /api/login [POST]
```bash
Param:
{
    "username": "teacher1",
    "password": "teacher1@123"
}
```

## /api/questions [POST]
### Add questions with difficulties
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Param:
{
    "detail": "Question1",
    "difficulties": "1"
}

Response:
{
    "detail": "Question1",
    "difficulties": 1
}
```

## /api/questions [GET]
### Get all questions with possible options
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Response:
[
    {
        "detail": "Question1",
        "difficulties": 1,
        "options": [
            {
                "detail": "Option1",
                "question": 1,
                "correct": true
            },
            {
                "detail": "Option2",
                "question": 1,
                "correct": true
            },
            {
                "detail": "Option3",
                "question": 1,
                "correct": false
            },
            {
                "detail": "Option4",
                "question": 1,
                "correct": false
            }
        ]
    },
    {
        "detail": "Question2",
        "difficulties": 1,
        "options": [
            {
                "detail": "Option1",
                "question": 2,
                "correct": false
            },
            {
                "detail": "Option2",
                "question": 2,
                "correct": false
            },
            {
                "detail": "Option3",
                "question": 2,
                "correct": true
            },
            {
                "detail": "Option4",
                "question": 2,
                "correct": false
            }
        ]
    }
]
```

## /api/questions/<id> [GET]
### Get specific question and its options
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Response:
{
    "detail": "Question2",
    "difficulties": 1,
    "options": [
        {
            "detail": "Option1",
            "question": 2,
            "correct": false
        },
        {
            "detail": "Option2",
            "question": 2,
            "correct": false
        },
        {
            "detail": "Option3",
            "question": 2,
            "correct": true
        },
        {
            "detail": "Option4",
            "question": 2,
            "correct": false
        }
    ]
}
```

## /api/options/<question_id> [POST]
### Add options for questions with correct flag
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Param:
{
    "detail": "Option1",
    "correct": True
}

Response:
{
    "detail": "Option1",
    "correct": true
}
```

## /api/options/<question_id> [GET]
### Get all options for this questions with correct flag
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Response:
[
    {
        "detail": "Option1",
        "question": 1,
        "correct": true
    },
    {
        "detail": "Option2",
        "question": 1,
        "correct": true
    },
    {
        "detail": "Option3",
        "question": 1,
        "correct": false
    },
    {
        "detail": "Option4",
        "question": 1,
        "correct": false
    }
]
```
## Create group from admin section
```
Group Name  - Student
```

## /api/register [POST]
### Student registration
```bash

Param:
{
    "first_name": "Maneesh",
    "last_name": "Singh",
    "username": "maneesh",
    "email": "maneesh@wsp.com",
    "password": "maneesh@123"
}

Response:
{
    "id": 4,
    "first_name": "Maneesh",
    "last_name": "Singh",
    "username": "maneesh.singh",
    "email": "maneesh@wsp.com",
    "password": "pbkdf2_sha256$150000$UjStrBNYQZgc$IJkdgPmkIVZx6T/9P45bVgVES6WYPgyn44Wu1y2omMY="
}
```

## /api/answers [POST]
### Add answer for passed question, user will be taken through auth
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Param:
{
    "question": "1",
    "options": "1,2"
}

Response:
{
    "question": 1,
    "options": "1,2"
}
```

## /api/results/<pupil_id> [GET]
### Fetch result by pupils
```bash
header:
Authorization: Token 659298fffd868107320ce69d5273fd923794bdfb

Response:
{
    "answers": [
        {
            "question": {
                "id": 1,
                "detail": "Question1",
                "difficulties": 1
            },
            "options": "1,2"
        },
        {
            "question": {
                "id": 2,
                "detail": "Question2",
                "difficulties": 1
            },
            "options": "3"
        }
    ],
    "percent": "50.0%",
    "result": "Pass"
}
```