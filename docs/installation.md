(installation)=

# Installation

This section describes how to install and run locally on your machine a developer instance of seven23_server.

This is not needed if you intend to use the application only. For such case, consult the instruction available wihtin the [deployment](docker_deployment) section.

## Source code

The code repository is hosted as public [github instance](https://github.com/sebastienbarbier/seven23_server), and can be pulled using the following command:

```shell
git clone git@github.com:sebastienbarbier/seven23_server.git
```

## Virtual environment

Create a virtual environment and activate it:

```shell
python3 -m venv apps
source apps/bin/activate
```

## Dependencies

Install dependencies:

```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Initialise your database

```shell
python manage.py migrate
python manage.py loaddata seven23/models/currency/fixtures/initial_data.json
```

:::{note}
Default settings run a local sqlite database. You can change the database settings in `seven23/settings.py`.
:::

## Create super user

Django provide a command to create a super user. This user will have access to the admin interface.

```shell
python manage.py createsuperuser
```

## Runserver

Run the server in development mode. This will also run hot reload of the code.

```shell
python manage.py runserver 0.0.0.0:8000
```

You should be able to access the homepage at [http://localhost:8000](http://localhost:8000).