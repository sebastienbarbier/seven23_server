.. _installation:

Installation
############

This section refere to a local installation for testing or developement purpose.
If you are looking for a production installation, please consult our :ref:`deployement section <deployement>` .

Download server and depandencies
--------------------------------

Download source code from our main repository on github, using git.

.. code-block:: bash

	git clone https://github.com/sebastienbarbier/723e_server

Create a virtualenv to isolate your workspace, then start it

.. code-block:: bash

	virtualenv apps
	source apps/bin/activate

Install dependancies using pip

.. code-block:: bash

	pip install -r requirements.txt
	pip install -r requirements-dev.txt	# manage documentation and testing

Configure
---------

You need to define your own settings.py file. Go on django_723e/settings.py and edit configuration to match your specification (normally you only need to adapt ``DATABASES_URL`` variable to access your database, and change ``SECRET_KEY``).

You can always consult ``django_723e/settings.py.example`` as a reminder of what default config file looks like.

Then create a default database structure with a admin user account

.. code-block:: bash

	python manage.py migrate

Run server
----------

You can now start your local server and access using your browser.

.. code-block:: bash

	python manage.py runserver

Administration should be avalaible at ``http://localhost:8000/admin/``

Documentation
-------------

To run and install documentation, run the following command from your root folder :

.. code-block:: bash

	sphinx-autobuild docs/ docs/_build/html

This should start a server instance which will automatically refresh on change.

