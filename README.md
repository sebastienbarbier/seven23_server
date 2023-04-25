# Seven23 server

[![Build action badge](https://github.com/sebastienbarbier/seven23_server/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/sebastienbarbier/seven23_server/actions/) [![Documentation Status](https://readthedocs.org/projects/seven23-server/badge/?version=latest)](https://seven23-server.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/sebastienbarbier/seven23_server/blob/main/LICENSE)


Fully manual budget app to track your expenses. Completely opensource, with privacy by design.

- [Seven23 official website](https://seven23.io/)
- [Online documentation](https://seven23-server.readthedocs.io/en/latest/)
- API specifications [swagger](https://api.seven23.io/swagger/) and [redoc](https://api.seven23.io/redoc/)
- [Issue tracker](https://github.com/sebastienbarbier/seven23_server/issues)
- [Code repository](https://github.com/sebastienbarbier/seven23_server)

Seven23 server instance is powered by [django](https://www.djangoproject.com/) and [django-rest-framework](https://www.django-rest-framework.org/) to manage and expose a restful API.
**It does not include a user interface**, which is managed as a totally independant project like [seven23_webapp](https://github.com/sebastienbarbier/seven23_webapp).

## Commands

```shell
make serve
make build
make test
make docs
make clean
make docker-build
make docker-run
make docker-shell
make docker-stop
```