Balloting application (Juntos) Developing & Testing
----------------------------------------------------------

Major Requirements:
 - Python3.7
 - Django2.1.1

First, create a virtual environment and install requirements:

.. code-block:: bash

    virtualenv ~/.virtualenvs/juntos
    source ~/.virtualenvs/juntos/bin/activate
    cd juntos
    pip install -r requirements.txt

Run migrations and collect static assets:

.. code-block:: bash

    python manage.py migrate
    python manage.py collectstatic


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
