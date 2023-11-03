
class Config(object):
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'pzoologique@gmail.com'
    MAIL_PASSWORD = 'parc1234'

    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

    MAIL_DEFAULT_SENDER = ('Flask Mailer', 'pzoologique@gmail.com')
    MAIL_MAX_EMAILS = 20
    
