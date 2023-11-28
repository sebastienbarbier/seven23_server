"""
    Views for api/va/transactions
"""
import stripe
import json
import os
import markdown2
import urllib.parse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

from django.db import models
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from seven23 import settings
from seven23.models.terms.models import TermsAndConditions
from seven23.models.saas.models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
def StripeGenerateSession(request):

    price = None

    if request.GET.get("price_id") and request.GET.get("success_url") and request.GET.get("cancel_url"):
        price = Price.objects.get(pk=request.GET.get("price_id"))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if not price.stripe_price_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    stripe_customer_id = None

    if hasattr(request.user, 'stripe'):
        # if user model has stripe foreign object
        stripe_customer_id = request.user.stripe.stripe_customer_id

    session = stripe.checkout.Session.create(
      customer=stripe_customer_id,
      customer_email=request.user.email if not stripe_customer_id else None,
      payment_method_types=['card'],
      line_items=[{
        'price': price.stripe_price_id,
        'quantity': 1,
      }],
      mode='subscription',
      # success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
      # cancel_url='https://example.com/cancel',
      success_url=urllib.parse.urljoin(request.GET.get("success_url"), 'success'),
      cancel_url=request.GET.get("cancel_url"),
    )

    j = json.dumps({
        'session_id': session
    }, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')

@csrf_exempt
@api_view(['POST'])
def StripeWebhook(request):
    payload = request.body
    print(payload)
    try:
        event = stripe.Event.construct_from(
          json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    # Handle the event
    if event.type == 'checkout.session.completed':
        checkout = event.data.object # contains a stripe.PaymentIntent


        # charge = Charge.objects.get(reference_id=checkout.id)
        # if charge:
        #     charge.status = 'SUCCESS'
        #     charge.save()

        #     charge.user.profile.stripe_customer_id = checkout.customer
        #     charge.user.profile.save()
        #     return Response(status=status.HTTP_200_OK)
        # else:
        #     return HttpResponse(status=400)
        print(checkout)
        print('checkout was completed!')
        return Response(status=status.HTTP_200_OK)
    else:
        # Unexpected event type
        return HttpResponse(status=400)
    return Response(status=status.HTTP_200_OK)