Models and api
==============

By default, your server instance deploy locally a swagger and redoc instance accessible threw the ``/swagger/`` and ``/redoc/`` urls. Those are code generated, and provide tools to describe and test available ressources.


You can also access the public instance on the seven23.io server:

- `Official swagger instance <https://seven23.io/swagger/>`_
- `Official redoc instance <https://seven23.io/redoc/>`_

Maintenance
-----------

API might be on **maintenance mode**, and then only available for superusers. All urls starting with `/api` will return `HTTP_503_Service_Unavailable` error handling.

**Maintenance mode** is define in `settings.py` and defined as ``os.environ.get('MAINTENANCE') == 'True'``