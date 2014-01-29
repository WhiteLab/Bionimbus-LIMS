# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

settings.migrate = True

mpath = request.env.path_info.split('/')
path = mpath[ 1 ] 

#f = open( "applications/%s/config.dat" % path , "r" )
#for line in f.readlines():
#  line = line.strip()
#  (k,v) = [ t.strip() for t in line.split( '=' ) ]
#  settings[ k ] = v 

import ConfigParser
parser = ConfigParser.SafeConfigParser()
parser.read( "applications/%s/config.dat" % path )
for name,value in parser.items( 'main' ):
  settings[ name ] = value 


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    if settings[ 'sqlite' ] == 'True':
      db = DAL('sqlite://storage.db')
    else:
      db = DAL( settings[ 'postgres' ] )
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables

########################################
db.define_table('auth_user',
    Field('nicename' , type='string',
          label=T('Name')),
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('filesystem_password', type='password',
          readable=False,
          label=T('File system Password')),
    Field('is_admin',type='boolean',writable=False),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    format='%(first_name)s %(last_name)s ( %(email)s )',
    migrate=settings.migrate)

db.auth_user.f_name = Field.Virtual(
    'f_name',
    lambda row: '%s %s ( %s )' % ( row[ db.auth_user.first_name ] , row[ db.auth_user.last_name ] , row[ db.auth_user.email ] ) ) 


scheme = True
try:
  scheme = settings[ 'scheme' ]
except:
  pass

if settings[ 'login_with_openid' ] == 'True':
  from gluon.contrib.login_methods.rpx_account import RPXAccount
  auth.settings.actions_disabled=['register','change_password',
  'request_reset_password']
  u = URL( '/user/login' , scheme = scheme , host = True )
  auth.settings.login_form = RPXAccount(request,
    api_key = settings[ 'api_key' ] ,
    domain = settings[ 'domain' ] ,
    url = u , embed = True )

db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
auth.define_tables(migrate = settings.migrate)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################


#mail.settings.server = settings.email_server
#mail.settings.sender = settings.email_sender
#mail.settings.login = settings.email_login
