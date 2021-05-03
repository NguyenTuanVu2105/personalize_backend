import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if os.environ.get('SENTRY_DSN') is not None:
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )
