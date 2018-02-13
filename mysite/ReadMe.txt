(Note: It's a backend server which provides REST APIs to a front-end client which is developed in react-redux.
Front-end project is in the same repo with the branch hassankhan-react-socialNetwork)

Steps to set up this project:

1: Clone the repo and switch to branch hassankhan-django-REST.

2: Set up virtual environment on your local machine by giving command:
command: virtualenv <any name>

3: Activate virtual environment by giving command:
command: source <name you entered earlier>/bin/activate

4: Now install requirements file by giving command:
command: pip install -r requirements.txt

5: Run the migrations by giving command:
command: python manage.py migrate (Note: Your database should exist by the name mentioned in settings.py)

6: Start the server by giving command:
command: python manage.py runserver



