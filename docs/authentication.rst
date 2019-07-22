Authentication
==============

API use Django’s Token-based authentication through the `django-rest-auth <https://github.com/Tivix/django-rest-auth>`_ library which also provide a set of endpoints to handle User Registration and Authentication tasks.

Retrieve token
--------------

`/api/v1/rest-auth/login/ (POST)`

.. code:: json

    { "username": "USERNAME", "password": "USER_PASSWORD" }

Response code 200 with body:

.. code:: json

    { "key": "d5ab4a34418b7053c86f1865003070671a7d158f" }



Fetch API being authenticated
-----------------------------

Stateless API require to provide the user token on each request. Token mush be sended threw the header using the ``Authorization`` value and ``Token YOUR_TOKEN`` key.

.. code:: shell

    curl -X GET "https://seven23.io/api/init" -H  "accept: application/json" -H  "Authorization: Token d5ab4a34418b7053c86f1865003070671a7d158f"

.. note::
    By design, a token does not expire and remains active until being manually deleted.


Revoke token
------------

Send an authenticated request to `/v1/users/token (DELETE)` will revoke used token.

.. code:: shell

    curl -X DELETE "https://seven23.io/api/v1/users/token" -H  "accept: application/json" -H  "Authorization: Token d5ab4a34418b7053c86f1865003070671a7d158f"
