class InstallAppResponseCode:
    INVALID_TOKEN = '1'
    ERROR_INSTALL = '2'
    SUCCESS = '3'
    SUCCESS_NEW_ACCOUNT = '4'
    STORE_EXISTED = '5'
    STORE_EMAIL_EXISTED = '6'
    ALL_STORE_INACTIVE = '7'

class InstallAppResponseMessage:
    INVALID_TOKEN = 'Invalid shop access token'
    ERROR_INSTALL = 'Error when installing app'
    SUCCESS = 'App has been installed successfully'
    SUCCESS_NEW_ACCOUNT = 'App has been installed successfully with new PrintHolo account'
    STORE_EXISTED = 'Store is existed on PrintHolo'
    STORE_EMAIL_EXISTED = 'Store owner email is existed on PrintHolo'
    ALL_STORE_INACTIVE = 'All store with this url is inactive'
