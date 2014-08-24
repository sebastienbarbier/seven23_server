# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404

from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django_723e.models.transactions.models import Category
from django_723e.models.transactions.serializers import CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class api_categories(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
