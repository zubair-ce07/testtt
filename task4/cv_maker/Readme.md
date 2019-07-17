Python is required to run django projects. After installing python django can be installed by
"pip install django"
It is prefered to be installed in a virtual environment.
Once it is installed a project can be setup by
"django-admin startproject project_name"
The server can be run by
"python manage.py runserver"
in the project directory.
New app can be made by 
"django-admin startapp app_name"
and add the name of the app to INSTALLED-APPS in setting.py
To run python shell run
"python manage.py shell"

The routes are defined in the url.py file and the actions that are taken on those routes are defined in views.py file of the app.
The database structure is defined in models of the app.
For multiple apps the same settings and url file is used whereas the views and models are defined for specific apps.