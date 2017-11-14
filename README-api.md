
EDUCARE
=======

The purpose of this project is to provide an API for the application EDUCARE. This project uses django REST framework to develop an API.

# Getting Started
1. Clone this project on your local machine.
2. Open the terminal and activate your virtual environment
3. Install the libraries mentioned in requirements.txt
4. Navigate to the project folder using the terminal
5. Run: *python manage.py runserver*

## Register a Student
Open any web browser and go to *http://127.0.0.1:8000/educare/register/student/*

- 'Email' and 'Username' are unique fields 
- 'Subjects' is a multiple choice field

## Register a Tutor
Go to *http://127.0.0.1:8000/educare/register/tutor/*

- 'Email' and 'Username' are unique fields 
- 'Subjects' is a multiple choice field
- Enter the phone number in this format **+41524204242**

## Login
Go to *http://127.0.0.1:8000/educare/login/*

All other views require token authentication so you can install *curl* and then get response through it 

## Getting Token
After registering a user and installing curl, use the command *curl -X POST -d "username=<username>&password=<password>" http://localhost:8000/educare/auth/token*
This will return you a token. Copy and save it.

## View User's Profile
To view any users profile

Use the command *curl -H "Authorization: Token <your_token>" http://localhost:8000/educare/viewprofile/<username>*

## View Student List
Only a Tutor can view this list

Use the command *curl -H "Authorization: Token <your_token>" http://localhost:8000/educare/studentlist/*

## View Tutor List
Only a Student can view this list
Use the command *curl -H "Authorization: Token <your_token>" http://localhost:8000/educare/tutorlist/*

## Edit Profile
Only the owner of the object can edit their profile

Use the command *curl -H "Authorization: Token <your_token>" http://localhost:8000/educare/editprofile/<username>*

## Reset Password
Only the owner of the object can change their password

Use the command *curl -H "Authorization: Token <your_token>" http://localhost:8000/educare/resetpassword/<username>*
