import os

FRESH_DESK_API_KEY = os.environ.get("FRESH_DESK_API_KEY")
FRESH_DESK_DOMAIN = os.environ.get("FRESH_DESK_DOMAIN")
TICKET_PER_MINUTE = 50
TICKET_UPDATE_LIMIT = 50
# DELTA_UPDATE_TIME = 2
SUPPORT_AGENT_ID = int(os.environ.get("SUPPORT_AGENT_ID"))
