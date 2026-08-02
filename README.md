# Seven23 server

[![Build action badge](https://github.com/sebastienbarbier/seven23_server/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/sebastienbarbier/seven23_server/actions/) [![Documentation Status](https://readthedocs.org/projects/seven23-server/badge/?version=latest)](https://seven23-server.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/sebastienbarbier/seven23_server/blob/main/LICENSE)

Fully manual budget app to track your expenses. Completely opensource, with privacy by design.

- [Seven23 official website](https://seven23.io/)
- [Online documentation](https://seven23-server.readthedocs.io/en/latest/)
- API specifications [swagger](https://api.seven23.io/swagger/) and [redoc](https://api.seven23.io/redoc/)
- [Issue tracker](https://github.com/sebastienbarbier/seven23_server/issues)
- [Code repository](https://github.com/sebastienbarbier/seven23_server)
- [Docker images](https://hub.docker.com/r/sebastienbarbier/seven23)

Seven23 server instance is powered by [django](https://www.djangoproject.com/) and [django-rest-framework](https://www.django-rest-framework.org/) to manage and expose a restful API.
**It does not include a user interface**, which is managed as a totally independant project like [seven23_webapp](https://github.com/sebastienbarbier/seven23_webapp).

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and **Python 3.12**.

Install uv if needed:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods (Homebrew, pipx, etc.).

```shell
uv sync
uv run python manage.py migrate
uv run python manage.py loaddata seven23/models/currency/fixtures/initial_data.json
uv run python manage.py runserver 0.0.0.0:8000
```

See the [installation docs](https://seven23-server.readthedocs.io/en/latest/installation.html) for details.

## Commands

```shell
uv sync
uv run python manage.py runserver 0.0.0.0:8000
uv run python manage.py test --settings seven23.settings_tests
uv run sphinx-autobuild docs/ docs/_build/html
docker build --pull -t seven23 .
docker run -p 8000:8000 --name seven23 -ti seven23
```
