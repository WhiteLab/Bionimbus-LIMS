response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Home'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Experiments'),URL('default','experiment_unit_manage')==URL(),URL('default','experiment_unit_manage'),[]),
(T('Project'),URL('permissions','project_manage')==URL(),URL('permissions','project_manage'),[]),
(T('Organism'),URL('default','organism_manage')==URL(),URL('default','organism_manage'),[]),
(T('File'),URL('default','file_manage')==URL(),URL('default','file_manage'),[]),
(T('Sample'),URL('default','sample_manage')==URL(),URL('default','sample_manage'),[]),
(T('Agent'),URL('default','agent_manage')==URL(),URL('default','agent_manage'),[]),
(T('Key Generation'),URL('keygen','keygen_spreadsheet')==URL(),URL('keygen','keygen_spreadsheet'),[]),
]

from applications.BNAdmin.modules.permissions import is_user_admin

if is_user_admin( db , auth ):
  response.menu.append( (T('Project Users'),URL('permissions','user_project_manage')==URL(),URL('permissions','user_project_manage'),[]) )

if is_user_admin( db , auth ):
  response.menu.append( (T('Barcodes'),URL('default','barcode_manage')==URL(),URL('default','barcode_manage'),[]) )

