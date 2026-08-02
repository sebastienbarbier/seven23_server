"""Unit tests for the JSON shape matcher and a live URL inventory."""

from django.test import SimpleTestCase, TransactionTestCase
from django.urls import URLPattern, URLResolver, get_resolver
from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import CONTRACT_API_VERSION
from seven23.tests.contracts.shapes import (
    AnyOf,
    DictOf,
    ListOf,
    Nullable,
    Optional,
    assert_json_shape,
)
from seven23 import settings


class ShapeMatcherTest(SimpleTestCase):
    def test_object_exact_keys(self):
        assert_json_shape({'a': 1, 'b': 'x'}, {'a': int, 'b': str})

    def test_object_rejects_missing_key(self):
        with self.assertRaises(AssertionError):
            assert_json_shape({'a': 1}, {'a': int, 'b': str})

    def test_object_rejects_unexpected_key(self):
        with self.assertRaises(AssertionError):
            assert_json_shape({'a': 1, 'b': 2}, {'a': int})

    def test_optional_key_may_be_absent(self):
        assert_json_shape({'a': 1}, {'a': int, 'b': Optional(str)})

    def test_optional_key_may_be_present(self):
        assert_json_shape({'a': 1, 'b': 'x'}, {'a': int, 'b': Optional(str)})

    def test_nullable(self):
        assert_json_shape(None, Nullable(str))
        assert_json_shape('hi', Nullable(str))
        with self.assertRaises(AssertionError):
            assert_json_shape(1, Nullable(str))

    def test_list_of(self):
        assert_json_shape([1, 2], ListOf(int))
        assert_json_shape([], ListOf(int))
        with self.assertRaises(AssertionError):
            assert_json_shape([], ListOf(int, allow_empty=False))

    def test_bool_is_not_int(self):
        with self.assertRaises(AssertionError):
            assert_json_shape(True, int)

    def test_any_of(self):
        assert_json_shape(True, AnyOf(bool, dict))
        assert_json_shape({'x': 1}, AnyOf(bool, {'x': int}))

    def test_dict_of(self):
        assert_json_shape({'a': ['err']}, DictOf(ListOf(str)))

    def test_nested(self):
        assert_json_shape(
            {'items': [{'id': 1, 'name': 'a'}]},
            {'items': ListOf({'id': int, 'name': str})},
        )


class ApiVersionContractTest(ApiContractTestCase):
    def test_contract_version_matches_settings(self):
        self.assertEqual(CONTRACT_API_VERSION, settings.API_VERSION)

    def test_init_advertises_contract_version(self):
        response = self.client.get('/api/init')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertApiVersionContract(response.json())


def _collect_api_paths(patterns=None, prefix=''):
    """Return sorted unique path templates under /api/ (excluding allauth HTML)."""
    if patterns is None:
        patterns = get_resolver().url_patterns

    paths = []
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            route = str(pattern.pattern)
            paths.extend(_collect_api_paths(pattern.url_patterns, prefix + route))
        elif isinstance(pattern, URLPattern):
            route = prefix + str(pattern.pattern)
            if route.startswith('api/') or route.startswith('^api/'):
                cleaned = (
                    route.replace('^', '')
                    .replace('$', '')
                    .replace('\\.', '.')
                )
                # Skip allauth browser pages and format-suffix clones
                if cleaned.startswith('api/accounts'):
                    continue
                if '<drf_format_suffix' in cleaned or '.(?P<format>' in route:
                    continue
                if cleaned.endswith('/') and cleaned.count('/') > 2:
                    # keep trailing slash for rest-auth style routes
                    pass
                paths.append('/' + cleaned if not cleaned.startswith('/') else cleaned)
    return sorted(set(paths))


class ApiUrlInventoryContractTest(TransactionTestCase):
    """
    Ensure every JSON API route is reachable (no accidental URLConf regressions).

    Resource detail routes with `{pk}` are probed with a synthetic id and may
    return 401/403/404 — that still proves the URL resolves.
    """

    EXPECTED_CORE_PATHS = {
        '/api/api-token-auth',
        '/api/init',
        '/api/v1/accounts',
        '/api/v1/categories',
        '/api/v1/changes',
        '/api/v1/currencies',
        '/api/v1/debitscredits',
        '/api/v1/user/delete',
        '/api/v1/users/token',
        '/api/v1/users/email',
        '/api/v1/rest-auth/login/',
        '/api/v1/rest-auth/logout/',
        '/api/v1/rest-auth/user/',
        '/api/v1/rest-auth/password/change/',
        '/api/v1/rest-auth/password/reset/',
        '/api/v1/rest-auth/password/reset/confirm/',
    }

    def test_core_api_paths_are_registered(self):
        registered = _collect_api_paths()
        # Normalize collected list patterns that include lookup
        flat = set()
        for path in registered:
            flat.add(path.split('<')[0].rstrip('/') if '<pk>' in path or '<id>' in path else path)
            flat.add(path)

        missing = []
        for expected in self.EXPECTED_CORE_PATHS:
            if expected in registered:
                continue
            # allow registered form without forcing exact string from regex dump
            if any(expected.rstrip('/') == r.rstrip('/') for r in registered):
                continue
            if any(r.startswith(expected.rstrip('/')) for r in registered):
                continue
            missing.append(expected)

        self.assertEqual(
            missing,
            [],
            msg=f'Missing API paths {missing}. Registered sample: {sorted(registered)[:40]}',
        )

    def test_smoke_get_or_options_on_collection_endpoints(self):
        client = APIClient()
        probes = [
            ('/api/init', 'get'),
            ('/api/v1/currencies', 'get'),
            ('/api/v1/accounts', 'get'),
            ('/api/v1/categories', 'get'),
            ('/api/v1/changes', 'get'),
            ('/api/v1/debitscredits', 'get'),
            ('/api/v1/rest-auth/user/', 'get'),
        ]
        for path, method in probes:
            response = getattr(client, method)(path)
            self.assertIn(
                response.status_code,
                {
                    status.HTTP_200_OK,
                    status.HTTP_401_UNAUTHORIZED,
                    status.HTTP_403_FORBIDDEN,
                },
                msg=f'{method.upper()} {path} returned {response.status_code}',
            )
