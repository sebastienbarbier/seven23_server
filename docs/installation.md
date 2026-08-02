# Installation

This section describes how to install and run locally on your machine a developer instance of seven23_server.

This is not needed if you intend to use the application only. For such case, consult the instruction available wihtin the [deployment](docker_deployment) section.

## Source code

The code repository is hosted as public [github instance](https://github.com/sebastienbarbier/seven23_server), and can be pulled using the following command:

```shell
git clone git@github.com:sebastienbarbier/seven23_server.git
cd seven23_server
```

## Install uv

This project is managed with [uv](https://docs.astral.sh/uv/). Requires **Python 3.12**.

Install uv if needed:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods (Homebrew, pipx, etc.).

## Dependencies

Create the virtual environment and install locked dependencies (uv will fetch Python 3.12 if needed):

```shell
uv sync
```

This reads `pyproject.toml` and `uv.lock`, creates `.venv`, and installs the exact pinned versions.

To run any project command without activating the environment manually:

```shell
uv run python manage.py <command>
```

Or activate the environment:

```shell
source .venv/bin/activate
```

## Initialise your database

```shell
uv run python manage.py migrate
uv run python manage.py loaddata seven23/models/currency/fixtures/initial_data.json
```

:::{note}
Default settings run a local sqlite database. You can change the database settings in `seven23/settings.py`.
:::

## Create super user

Django provide a command to create a super user. This user will have access to the admin interface.

```shell
uv run python manage.py createsuperuser
```

## Runserver

Run the server in development mode. This will also run hot reload of the code.

```shell
uv run python manage.py runserver 0.0.0.0:8000
```

You should be able to access the homepage at [http://localhost:8000](http://localhost:8000).
