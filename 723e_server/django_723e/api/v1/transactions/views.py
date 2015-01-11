# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404

from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django_723e.models.transactions.models import Category, DebitsCredits, Cheque, Change, Tranfert
from django_723e.models.transactions.serializers import CategorySerializer, DebitsCreditsSerializer, ChequeSerializer, ChangeSerializer, TranfertSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class api_categories(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class api_debitscredits(viewsets.ModelViewSet):
    queryset = DebitsCredits.objects.all()
    serializer_class = DebitsCreditsSerializer

    # Get list with filter year and month
    def list(self, request):
        if request.GET.get('month') and request.GET.get('year'):
            queryset = DebitsCredits.objects.filter(date__year=request.GET.get('year'), date__month=request.GET.get('month'))
        else:
            queryset = DebitsCredits.objects.all()
        serializer = DebitsCreditsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class api_cheque(viewsets.ModelViewSet):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer

class api_change(viewsets.ModelViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer

class api_transfert(viewsets.ModelViewSet):
    queryset = Tranfert.objects.all()
    serializer_class = TranfertSerializer
