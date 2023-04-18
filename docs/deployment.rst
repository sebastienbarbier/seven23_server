Deployment
==========

One-command deployment
----------------------

Seven23 implements a one-command deployment configuration to allow dynamic scaling on cloud platforms.

.. code:: shell

    make build

This is actually a script running four commands:

.. code:: shell

    python manage.py test --settings seven23.settings_tests
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py loaddata seven23/models/currency/fixtures/initial_data.json

Configuration
-------------

Deployed instance will access environment variables to configure itself. Should be done before any deployment.

.. code:: shell

    DATABASE_URL            = postgresql://username:password@url:port/db
    SECRET_KEY              = YOUR_SECRET_KEY
    ALLOW_ACCOUNT_CREATION  = false
    AWS_ACCESS_KEY_ID       = YOUR_AWS_ACCESS_KEY_ID
    AWS_S3_CUSTOM_DOMAIN    = YOUR_AWS_S3_CUSTOM_DOMAIN
    AWS_SECRET_ACCESS_KEY   = YOUR_AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = YOUR_AWS_STORAGE_BUCKET_NAME
    CONTACT_EMAIL           = admin@seven23.io
    EMAIL_HOST              = YOUR_EMAIL_HOST
    EMAIL_HOST_USER         = YOUR_EMAIL_USER
    EMAIL_HOST_PASSWORD     = YOUR_EMAIL_PASSWORD
    MAIL_USE_TLS            = false
    EMAIL_PORT              = 25
    DEBUG                   = false


.. _docker_deployment:

Using Docker and docker-compose
-------------------------------

Seven23 provides a Dockerfile for building a container image.

Build the docker container from source:

.. code:: shell

    docker build -t seven23_server . # or 'make docker-build'

Run the standalone application container:

.. code:: shell

    docker run -p 8000:8000 -ti seven23_server


In addition a docker-compose setup is available which uses the following components:

:app: Main container: bundled seven23 django application using Gunicorn as application server
:postgres: PostgreSQL database server
:nginx: NGINX reverse web proxy in front of Gunicorn and for serving static assets directly to the user.

Run complete application stack using docker-compose:

.. code:: shell

    docker-compose up # or 'make docker-run'

.. note::
    A Docker Volume is used for sharing static assets from the application with the NGINX container.

As SaaS
-------

To deploy as a SaaS service, you will need a few extra configuration values:

.. code:: shell

    SAAS              = true
    STRIPE_PUBLIC_KEY = YOUR_STRIPE_PUBLIC_KEY
    STRIPE_SECRET_KEY = YOUR_STRIPE_SECRET_KEY