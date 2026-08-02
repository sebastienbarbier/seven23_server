"""
Frozen JSON shapes for API v1 (``settings.API_VERSION == [1, 1, 0]``).

When these shapes must change incompatibly:
  1. Bump ``API_VERSION`` in ``seven23/settings.py``
  2. Add ``seven23/tests/contracts/v2/`` (keep v1 until clients migrate)
  3. Point new clients at the new ``api_version``
"""

from seven23.tests.contracts.shapes import AnyOf, DictOf, ListOf, Nullable, Optional

# Keep in sync with seven23.settings.API_VERSION
CONTRACT_API_VERSION = [1, 1, 0]

ISO_DATE = str  # YYYY-MM-DD
ISO_DATETIME = str  # YYYY-MM-DDTHH:MM:SS[.ffffff]Z


INIT_ANONYMOUS_V1 = {
    'version': ListOf(int, allow_empty=False),
    'api_version': ListOf(int, allow_empty=False),
    'saas': bool,
    'allow_account_creation': bool,
    'contact': Nullable(str),
    'subscription': AnyOf(bool, dict),
    'terms_and_conditions_date': Nullable(ISO_DATE),
    'terms_and_conditions': Nullable(str),
    # Present only when saas=True
    'stripe_product': Optional(Nullable(str)),
    'stripe_prices': Optional(list),
    'trial_period': Optional(int),
    'stripe_key': Optional(Nullable(str)),
    'subscription_price': Optional(dict),
}


PROFILE_V1 = {
    'avatar': str,
    'auto_sync': bool,
    'key_verified': bool,
    'social_networks': str,
}


USER_V1 = {
    'pk': int,
    'username': str,
    'first_name': str,
    'email': str,
    'verified': bool,
    'favoritesCurrencies': ListOf(int),
    'profile': PROFILE_V1,
    'valid_until': ISO_DATETIME,
}


TOKEN_KEY_V1 = {
    'key': str,
}


AUTH_TOKEN_V1 = {
    'token': str,
}


ACCOUNT_V1 = {
    'id': int,
    'name': str,
    'create': ISO_DATE,
    'currency': int,
    'currencies': ListOf(int),
    'archived': bool,
    'public': bool,
    'preferences': str,
}


BLOB_RESOURCE_V1 = {
    'id': int,
    'account': int,
    'blob': str,
    'active': bool,
    'last_edited': ISO_DATETIME,
    'deleted': bool,
}


# DebitsCredits serializer drops null keys (category may be omitted).
DEBITSCREDITS_V1 = {
    'id': int,
    'account': int,
    'blob': str,
    'active': bool,
    'last_edited': ISO_DATETIME,
    'deleted': bool,
    'category': Optional(int),
}


CURRENCY_V1 = {
    'id': int,
    'name': str,
    'code': Nullable(str),
    'sign': str,
    'space': bool,
    'after_amount': bool,
}


# Typical DRF validation / auth error payloads
DRF_DETAIL_V1 = {
    'detail': str,
}

DRF_VALIDATION_V1 = DictOf(AnyOf(ListOf(str), str, DictOf(AnyOf(ListOf(str), str))))

PASSWORD_CHANGE_V1 = DictOf(AnyOf(ListOf(str), str))  # often empty {} on success

LOGOUT_V1 = {
    'detail': str,
}
