# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404

from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django_723e.models.currency.models import Currency
from django_723e.models.currency.serializers import CurrencySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view

class api_currencies(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer