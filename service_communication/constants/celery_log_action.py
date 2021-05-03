class CeleryLogAction:
    SEND_EMAIL = '1'


class VerboseCeleryLogAction:
    SEND_EMAIL = 'send_email'


CeleryLogActionChoices = [
    (CeleryLogAction.SEND_EMAIL, VerboseCeleryLogAction.SEND_EMAIL),
]
