Deployment
==========

One-command deployment
----------------------

Seven23 implement a one-command deployment configuration to allow dynamic scaling on cloud platforms.

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

    ALLOW_ACCOUNT_CREATION  = false
    AWS_ACCESS_KEY_ID       = YOUR_AWS_ACCESS_KEY_ID
    AWS_S3_CUSTOM_DOMAIN    = YOUR_AWS_S3_CUSTOM_DOMAIN
    AWS_SECRET_ACCESS_KEY   = YOUR_AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = YOUR_AWS_STORAGE_BUCKET_NAME
    CONTACT_EMAIL           = admin@seven23.io
    DATABASE_URL            = postgresql://username:password@url:port/db
    SECRET_KEY              = YOUR_SECRET_KEY
    DEBUG                   = false

As Saas
-------

To deploy as a Saas service, you will need a few extra configuration values:

.. code:: shell

    SAAS              = true
    STRIPE_PUBLIC_KEY = YOUR_STRIPE_PUBLIC_KEY
    STRIPE_SECRET_KEY = YOUR_STRIPE_SECRET_KEY
