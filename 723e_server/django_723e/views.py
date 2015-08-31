# -*- coding: utf-8 -*-

import json

from django import template
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

def homepage(request):
    try:
        template.loader.get_template('index.html')
        return render(request, 'index.html')
    except template.TemplateDoesNotExist:
        return HttpResponse(status=404)

