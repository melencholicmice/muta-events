import stripe
import json
from muta_event.settings import (
    STRIPE_SECRET_KEY,
    STRIPE_ENDPOINT_SECRET
) 
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
stripe.api_key = STRIPE_SECRET_KEY
from user.models import User , UserPayment
from user.models import SubscriptionEnum
from event.models import Event 
from event.tasks import generate_pdf_and_send_mail

def  create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[],
            mode='payment',
            success_url=request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return checkout_session
    except Exception as e:
        return str(e)
    
@csrf_exempt  
def stripe_webhook_handler(request):
    if request.method != 'POST':
        return HttpResponse(status=400)
    print(request)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    try:
        user  = None
        if event.type == 'charge.succeeded':
            data = event.data.object
            if data['amount'] == 1000:
                try:
                    user = User.objects.get(email=data['billing_details']['email'])
                except Exception as e:
                    print(e)
                    return HttpResponse(status=400)
                print(user)
                if not user:
                    return HttpResponse(status=400)
                if user.subscription == SubscriptionEnum.PREMIUM.internal:
                    return HttpResponse(status=400)
                event = None

                try:
                    event  = Event.objects.create(
                        name = f"event bought by {user.email}",
                        is_bought = True,
                        description = "event bought by user",
                        location = "Enter location",
                        organizer = user
                    )
                    event.save()
                    event.description = f"event bought by user, you can edit it at /edit-bought-event/{event.event_id}" ,
                    event.save()

                except Exception as e:
                    print(e)
                    return HttpResponse(status=400)
                try:
                    user_payment = UserPayment.objects.create(
                        user = user,
                        payment_boolean = True,
                        payment_amount = data['amount'],
                        stripe_checkout_session_id = data['id'],
                    )
                    user_payment.save()
                    # send email to user 
                    generate_pdf_and_send_mail.delay(
                        user_email=str(user.email),
                        payment_id=str(user_payment.payment_id),
                        user_first_name=str(user_payment.user.first_name),
                        user_last_name=str(user_payment.user.last_name),
                        payment_amount=float(user_payment.payment_amount),
                        payment_boolean=bool(user_payment.payment_boolean),
                        stripe_checkout_session_id=str(user_payment.stripe_checkout_session_id),
                        created_at=str(user_payment.created_at),
                    )
                except Exception as e:
                    print(e)
                    return HttpResponse(status=400)

                return HttpResponse(status=200)
            elif data['amount'] == 500000:
                print('buy subscription called')
                email = data.billing_details.email
                try:
                    user = User.objects.get(email=data['billing_details']['email'])
                except Exception as e:
                    print(e)
                    return HttpResponse(status=400)

                if not user:
                    return HttpResponse(status=400)
                if user.subscription == SubscriptionEnum.PREMIUM.internal:
                    return HttpResponse(status=400)
                user.subscription = SubscriptionEnum.PREMIUM.internal
                user.save()

                try:
                    user_payment = UserPayment.objects.create(
                        user = user,
                        payment_boolean = True,
                        payment_amount = data['amount'],
                        stripe_checkout_session_id = data['id'],
                    )
                    user_payment.save()
                    generate_pdf_and_send_mail.delay(
                        user_email=str(user.email),
                        payment_id=str(user_payment.payment_id),
                        user_first_name=str(user_payment.user.first_name),
                        user_last_name=str(user_payment.user.last_name),
                        payment_amount=float(user_payment.payment_amount),
                        payment_boolean=bool(user_payment.payment_boolean),
                        stripe_checkout_session_id=str(user_payment.stripe_checkout_session_id),
                        created_at=str(user_payment.created_at),
                    )
                except Exception as e:
                    print(e)
                    return HttpResponse(status=400)
                

                return HttpResponse(status=200)
        return HttpResponse(status=200)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
