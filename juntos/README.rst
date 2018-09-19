Balloting application (Juntos) Developing & Testing
----------------------------------------------------------

Major Requirements:
 - Python3.5
 - Django2.1.1

First, create a virtual environment and install requirements (Make sure you've installed python3.5):

.. code-block:: bash

    virtualenv -p python3.5 ~/.virtualenvs/juntos
    source ~/.virtualenvs/juntos/bin/activate
    cd juntos
    pip install -r requirements.txt

Setup Postgres (Make sure you've installed postgres and it is working on your machine/server):

.. code-block:: bash

    psql
    CREATE USER <user-name> with PASSWORD '<password>';
    ALTER USER <user-name> with SUPERUSER;

Now put the user-name and pasword to `settings.py` file in `DATABASES` configurations.

Run migrations and collect static assets:

.. code-block:: bash

    python manage.py migrate
    python manage.py collectstatic


Make sure you install and run `Redis` as it is used in the project with `Celery` and start celery worker for info/logs:

.. code-block:: bash

    sudo apt-get install redis-server
    redis-server
    celery -A juntos worker -l info
    celery -A juntos beat -l info


Create a superuser to access Django Administration Console (i.e. /admin):

.. code-block:: bash

    python manage.py create_admin # This will also print superuser credentials.


Create sample Ballots in site through fixtures.

.. code-block:: bash

    python manage.py loaddata fixtures/ballot_samply.json


Finally, run development server as follow:

.. code-block:: bash

    python manage.py runserver 0.0.0.0:8000

To run tests

.. code-block:: bash

    python manage.py test user

Now, you will be able to visit Juntos @ http://localhost:8000 and Django Admin @ http://localhost:8000/admin/


To clean environment following commands can be used:

.. code-block:: bash

    deactivate
    rm -rf ~/.virtualenvs/bmi_app
    find . -name "*.pyc" -exec rm -f {} ;
