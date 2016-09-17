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

	pip install -r requirement.txt
	pip install -r requirement-dev.txt	# manage documentation and testing

Configure
---------

You need to define your own settings.py file

.. code-block:: bash

	cp django_723e/settings.py.example django_723e/settings.py

Edit your new settings file to satisfy your configuration (normally you only need to adapt ``DATABASES_URL`` variable to access your database).

Then create a default database structure with a admin user account

.. code-block:: bash

	python managed migrate

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

