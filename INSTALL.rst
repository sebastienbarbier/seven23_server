============
INSTALLATION
============

You've got two projects.

 - One is the service API that will store the data;
 - One is the Web application to manage and look at your data.

Deploying the service
=====================

Requirements
------------

The service API is built on top of Django and Django REST Framework.

You will need a PostgreSQL server for the database layer.

#. Create a virtualenv using Python 2.7::

    virtualenv --python /usr/bin/python2.7 venv

#. Upgrade pip::

   ./venv/bin/pip install -U pip

#. Install requirements::

   ./venv/bin/pip install -r 723e_server/requirement.txt

#. Copy the settings.py.example and configure your application::

    cp 723e_server/settings.py.example 723e_server/settings.py

#. `Generate a new SECRET_KEY <http://www.miniwebtool.com/django-secret-key-generator/>`_
#. Set ``DEBUG=False`` if production
#. Run Django Auth migration: ``python manage.py migrate auth``
#. Run Django 723e migration: ``python manage.py migrate`
#. Then run the server: ``python manage.py runserver``


Running the client
==================

In order to run the client, you just need to install the dependencies::

    npm install
    bower install

Then build the CSS files::

    grunt less

Then serve the cient::

    grunt server
