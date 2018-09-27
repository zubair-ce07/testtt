Balloting application (Juntos) Developing & Testing
====================================================

Major Requirements:
 - Python3.5
 - Django2.1.1

API docs can be found at: docs_
--------------------------------

.. _docs:  <https://web.postman.co/collections/4713976-d83e0e60-5b09-4858-b0be-0d27dc5ed1e4?workspace=6178d999-89c4-4bb9-9513-6f3329943877>;


First, create a virtual environment and install requirements (Make sure you've installed python3.5):

.. code-block:: bash

    virtualenv -p python3.5 ~/.virtualenvs/juntos_rest
    source ~/.virtualenvs/juntos_rest/bin/activate
    cd juntos_rest
    pip install -r requirements.txt

Setup Postgres (Make sure you've installed postgres and it is working on your machine/server):

.. code-block:: bash

    psql
    CREATE USER <user-name> with PASSWORD '<password>';
    ALTER USER <user-name> with SUPERUSER;
    CREATE DATABASE juntos_rest;

Now put the user-name and pasword to `settings.py` file in `DATABASES` configurations.

Run migrations and collect static assets:

.. code-block:: bash

    python manage.py migrate
    python manage.py collectstatic


Make sure you install and run `Redis` as it is used in the project with `Celery` and start celery worker for info/logs:

.. code-block:: bash

    sudo apt-get install redis-server
    redis-server
    celery -A juntos_rest worker -l info
    celery -A juntos_rest beat -l info


Create a superuser to access Django Administration Console (i.e. /admin):

.. code-block:: bash

    python manage.py create_admin # This will also print superuser credentials.


Create sample Ballots in site through fixtures.

.. code-block:: bash

    python manage.py loaddata fixtures/ballot_samply.json

To run celery task for making ballots inactive through management command

.. code-block:: bash

    python manage.py update_ballots_status


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
    rm -rf ~/.virtualenvs/juntos_rest
    find . -name "*.pyc" -exec rm -f {} ;
