import stripe

from HUB import settings

stripe.api_key = settings.STRIPE_SK_KEY
