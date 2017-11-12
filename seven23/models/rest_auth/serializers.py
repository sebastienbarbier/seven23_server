from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

# Get the UserModel
UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email')
        read_only_fields = ('email',)

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

        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'extra_email_context': self.initial_data
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)
