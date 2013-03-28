response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Home'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Experiments'),False,None,
    [ 
      [T('My Experiments')    ,URL('default','experiment_unit_manage')==URL(),URL('default','my_experiments')],
      [T('Public Experiments'),URL('default','experiment_unit_manage')==URL(),URL('default','public_experiments')]
    ]),
(T('Project'),False,None,
    [
      [T('Projects')          ,URL('permissions','project_manage')==URL(),URL('permissions','project_manage')],
      [T('Subprojects')          ,URL('permissions','subproject_manage')==URL(),URL('permissions','subproject_manage')],
    ]),
(T('Organism'),URL('default','organism_manage')==URL(),URL('default','organism_manage'),[]),
(T('File'),False,None,
   [
     ['My files'     , True , URL('default','my_file_manage')],
     ['Public Files' , True , URL('default','public_file_manage')]
   ]),
#(T('Sample'),URL('default','sample_manage')==URL(),URL('default','sample_manage'),[]),
#(T('Agent'),URL('default','agent_manage')==URL(),URL('default','agent_manage'),[]),
(T('Key Generation'),URL('keygen','keygen_spreadsheet')==URL(),URL('keygen','keygen_spreadsheet'),[]),
]

from applications.Bionimbus.modules.permissions import is_user_admin

if is_user_admin( db , auth ):
  response.menu.append( ( 'Admin' , True , None , [ 
   (T('Project Users'),URL('permissions','user_project_manage')==URL(),URL('permissions','user_project_manage'),[]) ,
   (T('Barcodes'),URL('default','barcode_manage')==URL(),URL('default','barcode_manage'),[]) ,
   (T('Facilities'),URL('default','facility_manage')==URL(),URL('default','facility_manage'),[]) ,
   (T('Mailing Lists'),URL('default','mailing_list_manage')==URL(),URL('default','mailing_list_manage'),[]),
   (T('Stages'),URL('default','stage_manage')==URL(),URL('default','stage_manage'),[])
 ] ) )
