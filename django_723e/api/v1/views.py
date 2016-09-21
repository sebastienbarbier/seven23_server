
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum
from django_723e.models.transactions.models import DebitsCredits, Change
import datetime

@api_view(['GET'])
def resume_year(request):
    """
    Give a resume of a specific year.
    """

    if request.method == 'GET':

        account = request.user.accounts.all()[0]
        year = request.GET.get('year')

        if year == None:
            year = datetime.datetime.today.year()

        list_months = DebitsCredits.objects.filter(account__exact=account, date__year=year, foreign_amount__isnull=False).extra(select={'month': "EXTRACT(month from date)"}).values('month').annotate(count=Count('foreign_amount'), sum=Sum('foreign_amount'))

        months = {}
        for i in list_months:
            month_number = int(i['month'])
            months[month_number] = {}
            months[month_number]['count'] = i['count']
            months[month_number]['sum'] = i['sum']
            list2 = DebitsCredits.objects.filter(account__exact=account, date__year=year, date__month=month_number, local_amount__lt=0, foreign_amount__isnull=False).extra(select={'month': "EXTRACT(month from date)"}).values('month').annotate(count=Count('foreign_amount'), sum=Sum('foreign_amount'))

            if len(list2) > 0:
                months[month_number]['sum_debits'] = list2[0]['sum']
            else:
                months[month_number]['sum_debits'] = 0

            months[month_number]['sum_credits'] = months[month_number]['sum'] - months[month_number]['sum_debits']

        stats = {}
        stats['changes'] = Change.objects.filter(account__exact=account, date__year=year).values('new_currency').annotate(count=Count('new_amount'), new=Sum('new_amount'), old=Sum('local_amount'))
        #define rate for each currency
        for c in stats['changes']:
            c['rate'] = c['new'] / c['old']
            c['average'] = c['old'] / c['count']

        categories = {}
        categories['list'] = DebitsCredits.objects.filter(account__exact=account, date__year=year, local_amount__lt=0, foreign_amount__isnull=False, category__isnull=False).values('category').annotate(count=Count('foreign_amount'), sum=Sum('foreign_amount')).order_by('sum')


        return Response({"year": year, "months": months, "stats": stats, "categories": categories})

