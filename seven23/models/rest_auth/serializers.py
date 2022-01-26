import datetime
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from allauth.account.models import EmailAddress

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

# Get the UserModel
UserModel = get_user_model()

from seven23.models.currency.models import Currency
from seven23.models.currency.serializers import CurrencySerializer
from seven23.models.saas.serializers import ChargeSerializer
from seven23.models.profile.serializers import DatetimeSerializer, ProfileSerializer

from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(WritableNestedModelSerializer):
    """
    User model w/o password
    """
    favoritesCurrencies = serializers.PrimaryKeyRelatedField(many=True, queryset=Currency.objects.all())
    verified = serializers.SerializerMethodField()
    valid_until = serializers.SerializerMethodField()
    charges = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'first_name', 'email', 'verified', 'favoritesCurrencies', 'profile', 'valid_until', 'charges')
        read_only_fields = ('email', 'charges')

    def get_verified(self, obj):
        try:
            return EmailAddress.objects.get(user=obj).verified
        except:
            return False

    def get_valid_until(self, obj):
        return DatetimeSerializer(obj.profile).data['valid_until']

    def get_charges(self, obj):
        return [ChargeSerializer(charge).data for charge in obj.charges.all()]


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()
    origin = serializers.CharField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')

        user = UserModel.objects.get(email=self.initial_data['email'])
        self.initial_data['username'] = user.username
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'extra_email_context': self.initial_data
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)