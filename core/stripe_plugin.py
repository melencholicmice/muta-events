import stripe
from muta_event.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


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