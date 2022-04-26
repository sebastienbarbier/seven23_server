# Please note

This project is **alpha** quality. We don't yet guarantee stability, data integrity or a clean upgrade path. Only use this project if you are interested in experimenting with it.

# Seven23 server

[![Documentation Status](https://readthedocs.org/projects/seven23-server/badge/?version=latest)](https://seven23-server.readthedocs.io/en/latest/?badge=latest)

[![Documentation Status](https://travis-ci.org/sebastienbarbier/seven23_server.svg?branch=main)](https://travis-ci.org/sebastienbarbier/seven23_server)

Fully manual budget app to track your expenses. Completely opensource, with privacy by design.

- [Seven23 official website](https://seven23.io/)
- [Online documentation](https://seven23-server.readthedocs.io/en/latest/)
- API specifications [swagger](https://seven23.io/swagger/) and [redoc](https://seven23.io/redoc/)
- [Issue tracker](https://github.com/sebastienbarbier/seven23_server/issues)
- [Code repository](https://github.com/sebastienbarbier/seven23_server)

Seven23 server instance is powered by [django](https://www.djangoproject.com/) and [django-rest-framework](https://www.django-rest-framework.org/) to manage and expose a restful API.
**It does not include a user interface**, which is managed as a totally independant project like [seven23_webapp](https://github.com/sebastienbarbier/seven23_webapp).