"""
    Views for api/va/transactions
"""
import stripe
import json
import os
import markdown2
from django.http import HttpResponse

from rest_framework import status

from django.db import models
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from seven23 import settings
from seven23.models.terms.models import TermsAndConditions
from seven23.models.saas.models import Charge, Product, Coupon
from seven23.models.saas.serializers import ChargeSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
def ApiCoupon(request, product_id, coupon_code):
    res = {}

    product = Product.objects.get(pk=product_id)
    coupon = Coupon.objects.get(code=coupon_code)

    if not product or not coupon or not coupon.is_active:
        return Response(status=status.HTTP_404_NOT_FOUND)

    res['coupon_id'] = coupon.id
    res['percent_off'] = coupon.percent_off
    res['price'] = product.price - (product.price * coupon.percent_off / 100)

    j = json.dumps(res, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')

@api_view(['POST'])
def ApiCharge(request):

    """
        Return status on client initialisation
    """
    result = {}
    coupon = None
    product = None
    charge = None

    if request.data.get("coupon_code"):
        coupon = Coupon.objects.get(code=request.data['coupon_code'])

    if request.data.get("product_id"):
        product = Product.objects.get(pk=request.data['product_id'])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    price = product.apply_coupon(request.data.get('coupon_code')) * 100
    try:
        if price > 0:
            # Use Stripe's library to make requests...
            result = stripe.Charge.create(
              amount=int(price),
              currency="eur",
              source=request.data['token'],
              description=request.data.get("description")
            )

            charge = Charge.objects.create(
                user=request.user,
                product=product,
                coupon=coupon,
                paiment_method='STRIPE',
                reference_id=result['id'],
                status='SUCCESS'
            )

        else:
            charge = Charge.objects.create(
                user=request.user,
                product=product,
                coupon=coupon,
                paiment_method='COUPON',
                status='SUCCESS'
            )

        j = json.dumps(ChargeSerializer(charge).data, separators=(',', ':'))
        return HttpResponse(j, content_type='application/json')

    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err  = body.get('error', {})

        # print("Status is: %s" % e.http_status)
        # print("Type is: %s" % err.get('type'))
        # print("Code is: %s" % err.get('code'))
        # # param is '' in this case
        # print("Param is: %s" % err.get('param'))
        # print("Message is: %s" % err.get('message'))
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        body = e.json_body
        err  = body.get('error', {})
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        body = e.json_body
        err  = body.get('error', {})
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        body = e.json_body
        err  = body.get('error', {})
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        body = e.json_body
        err  = body.get('error', {})
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        body = e.json_body
        err  = body.get('error', {})
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        body = e.json_body
        err  = body.get('error', {})
        pass

    try:
        charge.delete()
    except Exception as e:
        pass

    charge = Charge.objects.create(
        user=request.user,
        product=product,
        coupon=coupon,
        paiment_method='STRIPE',
        reference_id=result.get("id"),
        status='FAILED',
        comment=err.get('message')
    )

    j = json.dumps(ChargeSerializer(charge).data, separators=(',', ':'))
    return Response(j, status=status.HTTP_402_PAYMENT_REQUIRED)