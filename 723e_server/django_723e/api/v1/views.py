
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django_723e.models.transactions.models import DebitsCredits
import datetime

@api_view(['GET'])
def resume_year(request):
    """
    Give a resume of a specific year.
    """

    if request.method == 'GET':

        year = request.GET.get('year')

        if year == None:
            year = datetime.datetime.today.year()

        list = DebitsCredits.objects.filter(date__year=year).extra(select={'month': "EXTRACT(month from date)"}).values('month').annotate(Count('amount'))

        months = {}
        for i in list:
            months[i['month']] = i['amount__count']

        return Response({"year": year, "months": months})

