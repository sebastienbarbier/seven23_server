"""Test settings. Prefer running with Django's parallel runner::

    uv run python manage.py test seven23 --settings seven23.settings_tests --parallel auto
"""

from seven23.settings import *
import seven23.settings as _app_settings

# Force registration routes on for the test suite (urls.py reads seven23.settings).
_app_settings.ALLOW_ACCOUNT_CREATION = True
ALLOW_ACCOUNT_CREATION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
