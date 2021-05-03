import hashlib
import hmac


def authenticate_request(message, signature, secret, algorithm='sha256'):
    secret = str.encode(secret) if type(secret) == str else secret
    message = str.encode(message) if type(message) == str else message
    digest_mod = getattr(hashlib, algorithm)
    encrypted = hmac.new(secret, msg=message, digestmod=digest_mod).hexdigest()
    return encrypted == signature
