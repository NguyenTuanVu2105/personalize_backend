import os

BASE_DIR = os.path.abspath(__file__).rsplit('/', 3)[0]
SERVER_URL = os.environ.get("SERVER_URL")
OBJECT_ID_PREFIX = os.environ.get("OBJECT_ID_PREFIX")
IDEMPOTENCY_KEY_PREFIX = os.environ.get("IDEMPOTENCY_KEY_PREFIX")
