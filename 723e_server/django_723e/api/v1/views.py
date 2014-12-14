
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum
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

        list = DebitsCredits.objects.filter(date__year=year).extra(select={'month': "EXTRACT(month from date)"}).values('month').annotate(count=Count('amount'), sum=Sum('reference_amount'))
        months = {}
        for i in list:
            months[i['month']] = {}
            months[i['month']]['count'] = i['count']
            months[i['month']]['sum'] = i['sum']
            list2 = DebitsCredits.objects.filter(date__year=year, date__month=i['month'], amount__lt=0).extra(select={'month': "EXTRACT(month from date)"}).values('category').annotate(count=Count('amount'), sum=Sum('reference_amount'))

            if len(list2) > 0:
                months[i['month']]['sum_debits'] = list2[0]['sum']
            else:
                months[i['month']]['sum_debits'] = 0

            months[i['month']]['sum_credits'] = months[i['month']]['sum'] - months[i['month']]['sum_debits']

        return Response({"year": year, "months": months})

