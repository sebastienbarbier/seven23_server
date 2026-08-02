from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import int_to_base36

from rest_framework import serializers
from allauth.account.models import EmailAddress
from allauth.account.forms import default_token_generator

from drf_writable_nested import WritableNestedModelSerializer

from seven23.models.currency.models import Currency
from seven23.models.profile.serializers import DatetimeSerializer, ProfileSerializer

# Get the UserModel
UserModel = get_user_model()


class UserSerializer(WritableNestedModelSerializer):
    """
    User model w/o password
    """
    favoritesCurrencies = serializers.PrimaryKeyRelatedField(many=True, queryset=Currency.objects.all())
    verified = serializers.SerializerMethodField()
    valid_until = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'first_name', 'email', 'verified', 'favoritesCurrencies', 'profile', 'valid_until')
        read_only_fields = ['email']

    def get_verified(self, obj):
        try:
            return EmailAddress.objects.get(user=obj).verified
        except:
            return False

    def get_valid_until(self, obj):
        return DatetimeSerializer(obj.profile).data['valid_until']


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
        self.initial_data['uidb36'] = int_to_base36(user.pk)

        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'extra_email_context': self.initial_data,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)
