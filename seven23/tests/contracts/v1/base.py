"""Shared fixtures for API contract tests."""

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.schemas import CONTRACT_API_VERSION
from seven23.tests.contracts.shapes import assert_json_shape
from seven23.models.accounts.models import Account
from seven23.models.categories.models import Category
from seven23.models.currency.models import Currency
from seven23.models.transactions.models import Change, DebitsCredits
from seven23 import settings


class ApiContractTestCase(TransactionTestCase):
    """Authenticated client plus a full sample dataset for resource contracts."""

    def setUp(self):
        self.client = APIClient()
        self.password = 'contract-pass-123'
        self.user = User.objects.create_user(
            username='contract_user',
            email='contract@seven23.test',
            password=self.password,
        )
        self.other = User.objects.create_user(
            username='contract_other',
            email='other@seven23.test',
            password=self.password,
        )
        self.usd = Currency.objects.create(
            name='US Dollars',
            sign='USD',
            code='USD',
        )
        self.eur = Currency.objects.create(
            name='Euro',
            sign='€',
            code='EUR',
        )
        self.account = Account.objects.create(
            owner=self.user,
            name='Contract Account',
            currency=self.usd,
        )
        self.other_account = Account.objects.create(
            owner=self.other,
            name='Other Account',
            currency=self.eur,
        )
        self.category = Category.objects.create(
            account=self.account,
            blob='{"name":"Food"}',
        )
        self.debit = DebitsCredits.objects.create(
            account=self.account,
            blob='{"amount":-12}',
            category=self.category,
        )
        self.debit_no_category = DebitsCredits.objects.create(
            account=self.account,
            blob='{"amount":-5}',
        )
        self.change = Change.objects.create(
            account=self.account,
            blob='{"from":"USD","to":"EUR"}',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def assertShape(self, data, schema, path='$'):
        assert_json_shape(data, schema, path=path)

    def assertJsonResponse(self, response, schema, expected_status=status.HTTP_200_OK):
        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f'Unexpected status {response.status_code}: {getattr(response, "content", b"")[:500]!r}',
        )
        data = response.json()
        self.assertShape(data, schema)
        return data

    def assertApiVersionContract(self, init_payload):
        self.assertEqual(
            init_payload['api_version'],
            CONTRACT_API_VERSION,
            msg=(
                'api_version drifted from contract schemas. '
                'If the JSON shape changed intentionally, bump API_VERSION '
                'and update seven23.tests.contracts.v1.schemas.'
            ),
        )
        self.assertEqual(
            init_payload['api_version'],
            settings.API_VERSION,
        )
