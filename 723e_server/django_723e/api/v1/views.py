
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

        list_months = DebitsCredits.objects.filter(date__year=year, reference_amount__isnull=False).extra(select={'month': "EXTRACT(month from date)"}).values('month').annotate(count=Count('reference_amount'), sum=Sum('reference_amount'))

        months = {}
        for i in list_months:
            month_number = int(i['month'])
            months[month_number] = {}
            months[month_number]['count'] = i['count']
            months[month_number]['sum'] = i['sum']
            list2 = DebitsCredits.objects.filter(date__year=year, date__month=month_number, amount__lt=0, reference_amount__isnull=False).extra(select={'month': "EXTRACT(month from date)"}).values('month').annotate(count=Count('reference_amount'), sum=Sum('reference_amount'))

            if len(list2) > 0:
                months[month_number]['sum_debits'] = list2[0]['sum']
            else:
                months[month_number]['sum_debits'] = 0

            months[month_number]['sum_credits'] = months[month_number]['sum'] - months[month_number]['sum_debits']

        print(months)
        return Response({"year": year, "months": months})

