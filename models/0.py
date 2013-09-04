from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.cghub = True
settings.title = 'Bionimbus WEB'
if settings.cghub == True:
  settings.title = 'CGHUB genomic data'

settings.subtitle = '' # developed by LAC'
settings.author = 'David Hanley'
settings.author_email = 'dhanley@uchicago.edu'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'postgres://dstn:cisdstn@localhost:5432/bionimbus'
settings.security_key = 'c4b1c26b-f84e-4f77-a851-66054094a416'
settings.email_server = 'localhost'
settings.email_sender = 'support@bionimbus.org'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
