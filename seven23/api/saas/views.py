"""
    Views for api/va/transactions
"""
import stripe
import json
import os
import markdown2
from django.utils import timezone
from datetime import datetime
import urllib.parse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from django.contrib.auth.models import User

from django.db import models
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from seven23 import settings
from seven23.models.terms.models import TermsAndConditions
from seven23.models.saas.models import Price, StripeSubscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
def StripeGenerateSession(request):

    if hasattr(request.user, 'stripe') and request.user.profile.valid_until > timezone.now():

        if not request.GET.get("return_url"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        session = stripe.billing_portal.Session.create(
            customer=request.user.profile.stripe_customer_id,
            return_url=request.GET.get("return_url"),
        )

        j = json.dumps({
            'session_id': session
        }, separators=(',', ':'))
        return HttpResponse(j, content_type='application/json')

    else:
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
            stripe_customer_id = request.user.profile.stripe_customer_id

        trial_end_date = None

        if request.user.profile.valid_until > timezone.now():
            trial_end_date = request.user.profile.valid_until
            # Make sure trial_end_date is at least two days in the future
            # (Stripe requirement)
            if trial_end_date < timezone.now() + timezone.timedelta(days=2, hours=1):
                trial_end_date = timezone.now() + timezone.timedelta(days=2, hours=1)

        session = stripe.checkout.Session.create(
          customer=stripe_customer_id,
          customer_email=request.user.email if not stripe_customer_id else None,
          payment_method_types=['card'],
          client_reference_id=request.user.pk,
          subscription_data= {
            'trial_end': trial_end_date,
          },
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
    try:
        event = stripe.Event.construct_from(
          json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'customer.subscription.created' or event.type == 'customer.subscription.updated':

        subscription = event.data.object

        stripeCustomer, created = StripeSubscription.objects.get_or_create(
            subscription_id=subscription.id
        )

        if subscription.trial_end:
            stripeCustomer.trial_end = timezone.make_aware(datetime.utcfromtimestamp(subscription.trial_end), timezone=timezone.utc)
        else:
            stripeCustomer.trial_end = None

        if subscription.current_period_end:
            stripeCustomer.current_period_end = timezone.make_aware(datetime.utcfromtimestamp(subscription.current_period_end), timezone=timezone.utc)
        else:
            stripeCustomer.current_period_end = None

        if subscription.cancel_at:
            stripeCustomer.cancel_at = timezone.make_aware(datetime.utcfromtimestamp(subscription.cancel_at), timezone=timezone.utc)
        else:
            stripeCustomer.cancel_at = None

        stripeCustomer.status = subscription.status
        stripeCustomer.price = get_object_or_404(Price, stripe_price_id=subscription.plan.id)
        stripeCustomer.is_active = True
        stripeCustomer.save()

        return Response(status=status.HTTP_200_OK)
    elif event.type == 'customer.subscription.deleted':
        subscription = event.data.object
        try:
            StripeSubscription.objects.filter(subscription_id=subscription.id).delete()
        except:
            pass
        return Response(status=status.HTTP_200_OK)
    elif event.type == 'checkout.session.completed':
        # We create a StripeCustomer object to store user's data from Stripe
        checkout = event.data.object
        user = get_object_or_404(User, pk=checkout.client_reference_id)

        # checkout.client_reference_id is 1, 2, 4 ... user.pk
        # checkout.subscription is sub_1OHNiZILP1DzcVdZmb3bqdLr
        # checkout.customer is cus_P5Yqm6ZYR1CHFc

        subscription, created = StripeSubscription.objects.get_or_create(
            subscription_id=checkout.subscription,
        )
        subscription.user = user
        subscription.save()

        user.profile.stripe_customer_id = checkout.customer
        user.profile.save()

        return Response(status=status.HTTP_200_OK)
    else:
        print(event)
        # Unexpected event type
        return HttpResponse(status=200)
    return Response(status=status.HTTP_200_OK)