.. installation:

Installation
============

.. code:: shell

    git clone git@github.com:sebastienbarbier/seven23_server.git

Virtual env (optional)
----------------------

.. code:: shell

    virtualenv -p python3 apps
    source apps/bin/activate

Dependencies
--------------------------

.. code:: shell

    pip install -r requirements.txt


.. note::
    Dependencies related to documentation has been separated to a different file and need to run
    ``pip install -r requirements-dev.txt``

Migration
---------

Configure in settings.py access to your database, then run:


.. code:: shell

    python manage.py migrate
    python manage.py loaddata seven23/models/currency/fixtures/initial_data.json


Run server
----------

.. code:: shell

    python manage.py runserver 0.0.0.0:8000 # or just make

.. note::
    Because local instance do not support https, you cannot access the API using a https application.