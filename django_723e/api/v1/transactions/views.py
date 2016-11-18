# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404

from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import permission_classes

from django_723e.models.categories.models import Category
from django_723e.models.transactions.models import DebitsCredits, Change
from django_723e.models.categories.serializers import CategorySerializer
from django_723e.models.transactions.serializers import DebitsCreditsSerializer, ChangeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

@permission_classes((IsAuthenticated,))
class api_categories(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()

    def destroy(self, request, pk=None):
        category = self.get_object()
        category.delete()
        serializer = self.get_serializer(category, many=False)
        return Response(serializer.data, status=200)

@permission_classes((IsAuthenticated,))
class api_debitscredits(viewsets.ModelViewSet):
    queryset = DebitsCredits.objects.all()
    serializer_class = DebitsCreditsSerializer

    def get_queryset(self):
        return DebitsCredits.objects.filter(account__exact=self.request.user.accounts.all()[0])

    # Get list with filter year and month
    def list(self, request):
        account = self.request.user.accounts.all()[0]
        if request.GET.get('month') and request.GET.get('year'):
            queryset = DebitsCredits.objects.filter(account__exact=account, date__year=request.GET.get('year'), date__month=request.GET.get('month'))
        else:
            queryset = DebitsCredits.objects.filter(account__exact=account)
        serializer = DebitsCreditsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

@permission_classes((IsAuthenticated,))
class api_change(viewsets.ModelViewSet):
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer

    def get_queryset(self):
        return Change.objects.filter(account__exact=self.request.user.accounts.all()[0])


