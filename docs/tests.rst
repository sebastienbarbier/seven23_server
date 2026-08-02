Tests
=====

Tests can be run using the command:

.. code:: shell

    uv run python manage.py test seven23 --settings seven23.settings_tests --parallel auto

``--parallel auto`` runs tests across available CPU cores (Django creates one SQLite
database per worker). Omit it to run sequentially when debugging a single failure.

Those are performed on each deployments to minimize service unavailability and human errors.