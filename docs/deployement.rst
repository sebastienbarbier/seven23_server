.. _deployement:

Deployement
###########

Main concept about 723e is that you need to self-host your own instance.
On this purpose, installation process has been design to be really fast and easy,
providing multiple solution to satisfy everyone.

Cloud hosting
=============

By far the easiest way, a one click installation on a specific cloud infrastructure.

.. image:: https://www.herokucdn.com/deploy/button.svg
   :target: https://heroku.com/deploy?template=https://github.com/sebastienbarbier/723e_server
   :alt: Deploy on Heroku

You can then access your application with the dedicated URL (should be https). Then go on 723e.com, scroll down and change server link to your new instance.

Dedicated Server
================

This process is quite similar to the :ref:`development installation process <installation>` and follow `generic Django deployement process <https://docs.djangoproject.com/en/1.10/howto/deployment/>`_.

Saas
====

Last solution is to go against the idea of self-hosting, and find a provider hosting an instance for your.

.. warning::
	This solution will host other users, and data privacy will no longer be guaranteed.


So far there is no official known platform, even if an instance is currently running on 723e.com.
This features might officially come if requested and when the project reach maturity.
