class AuthenticationType:
    HEADER = 'header'
    H_MAC = 'h_mac'
    IP = 'ip'


class VerboseAuthenticationType:
    HEADER = 'header'
    H_MAC = 'h_mac'
    IP = 'ip'


AUTHENTICATION_TYPES = [
    (AuthenticationType.HEADER, VerboseAuthenticationType.HEADER),
    (AuthenticationType.H_MAC, VerboseAuthenticationType.H_MAC),
    (AuthenticationType.IP, VerboseAuthenticationType.IP)
]
