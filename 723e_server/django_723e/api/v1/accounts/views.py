# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django_723e.models.accounts.models import Account, InvitationRequest
from django_723e.models.accounts.serializers import AccountSerializer, UserSerializer, InvitationRequestSerializer
from django_723e.models.currency.models import Currency

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class api_accounts(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class api_users(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class api_invitationrequest(viewsets.ModelViewSet):
    queryset = InvitationRequest.objects.all()
    serializer_class = InvitationRequestSerializer
	

@api_view(['POST'])
def subscription(request):
    """
    Give a resume of a specific year.
    """

    if request.method == 'POST':
        args = request.data

        try:
            user = User.objects.get(username=args.get('username'))
            return Response({'field': 'username', 'errorMsg': 'This user already exist'}, status=400)
        except User.DoesNotExist:
            # Create User
            user = User.objects.create_user(args.get('username'), args.get('email'), args.get('password'))
            user.save()
            # Create Account
            currency = Currency.objects.get(id=args.get('currency'))
            account = Account.objects.create(user=user, name=args.get('name'), currency=currency)

            token = Token.objects.get_or_create(user=user)
            # Log user with Token
            return Response({'code': 200, 'token': token[0].key}, status=200)