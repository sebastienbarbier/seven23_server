# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers

from django_723e.models.transactions.models import Transaction
from djangular.views.crud import NgCRUDView
from django.contrib.auth.decorators import login_required


# Create your views here.
class api_transactions(NgCRUDView):
    model = Transaction


    def ng_query(self, request, *args, **kwargs):
        """
        Used when angular's query() method is called
        Build an array of all objects, return json response
        """
        if not request.user.is_authenticated():
            return Response({})
            
        return self.build_json_response(self.get_queryset())

    def get_queryset(self):
        return self.model.objects.filter(account__in=self.request.user.accounts.all())

 
    def delete(self, request, *args, **kwargs):
        return Response({})
