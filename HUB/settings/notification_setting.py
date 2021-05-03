# Email
import os

EMAIL_USE_TLS = True if os.environ.get("EMAIL_USE_TLS") == "TRUE" else False
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")

EMAIL_ADMIN = os.environ.get("EMAIL_ADMIN")

CLEAR_MAIL_HISTORY_DAYS = 90
