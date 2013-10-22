response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

main = (T('Libraries/Files'),False,None,
    [
      [T('My Libraries')    ,False,None,
        [
          [T('All')    ,URL('default','experiment_unit_manage')==URL(),URL('default','my_experiments')],
          [T('ChIP-seq')    ,URL('default','experiment_unit_manage')==URL(),URL('default','my_ChipSeq')],
          [T('Exomes')    ,URL('default','experiment_unit_manage')==URL(),URL('default','my_Exomes')],
          [T('DNA seq')    ,URL('default','experiment_unit_manage')==URL(),URL('default','my_DNAseq')],
          [T('RNA seq'),URL('default','experiment_unit_manage')==URL(),URL('default','my_RNAseq')]
        ]
      ],
      [T('Public Libraries'),URL('default','experiment_unit_manage')==URL(),URL('default','public_experiments')],
      [T('Selected Files'),    URL('default','selected_files')==URL(),URL('default','selected_files')]
    ])

if settings.cghub == True:
  main = (T('Cancer Genomics'),URL('default','my_CGhub')==URL(),URL('default','my_CGhub'),[])

response.menu = [
(T('Home'),URL('default','index')==URL(),URL('default','index'),[]),
    main,
(T('Project'),False,None,
    [
      [T('My Projects')          ,URL('permissions','project_manage')==URL(),URL('permissions','project_manage')],
      [T('Public Projects')      ,URL('permissions','project_manage')==URL(),URL('permissions','public_project_manage')],
      [T('Subprojects')          ,URL('permissions','subproject_manage')==URL(),URL('permissions','subproject_manage')],
    ]),
(T('Organism'),URL('default','organism_manage')==URL(),URL('default','organism_manage'),[]),
#(T('File'),False,None,
#   [
#     ['My files'     , True , URL('default','my_file_manage')],
#     ['Public Files' , True , URL('default','public_file_manage')]
#   ]),
#(T('Sample'),URL('default','sample_manage')==URL(),URL('default','sample_manage'),[]),
#(T('Agent'),URL('default','agent_manage')==URL(),URL('default','agent_manage'),[]),
(T('Key Generation'),URL('keygen','keygen_spreadsheet')==URL(),URL('keygen','keygen_spreadsheet'),[]),
]

u = A('User Documentation',_href='/Bionimbus/static/bd/Bionimbusdocumentation.html',_target='docs')
u2 = A('Quick start',_href='https://docs.google.com/document/d/1RPb8UEQsDgsZmuDCW_rTEMHtAgGCDnNYTm7BaRsmgAo/view?usp=sharing',_target='docs')

response.menu.append( ( 'Docs' , True , None , [
  (T('Documentation'),False,u,[]),
  (T('Quick Start'),False,u2,[])
] ) )


from permissions import is_user_admin

if is_user_admin( db , auth ):
  response.menu.append( ( 'Admin' , True , None , [ 
   (T('Sample Tracking'),URL('default','sample_tracking')==URL(),URL('default','sample_tracking'),[]) ,
   (T('Project Users'),URL('permissions','user_project_manage')==URL(),URL('permissions','user_project_manage'),[]) ,
   (T('Barcodes'),URL('default','barcode_manage')==URL(),URL('default','barcode_manage'),[]) ,
   (T('Facilities'),URL('default','facility_manage')==URL(),URL('default','facility_manage'),[]) ,
   (T('Mailing Lists'),URL('default','mailing_list_manage')==URL(),URL('default','mailing_list_manage'),[]),
   (T('Stages'),URL('default','stage_manage')==URL(),URL('default','stage_manage'),[]),
   (T('Clouds'),URL('default','cloud_manage')==URL(),URL('default','cloud_manage'),[]),
   (T('Platform'),URL('default','platform_manage')==URL(),URL('default','platform_manage'),[]),
   (T('Library Types'),URL('default','library_type_manage')==URL(),URL('default','library_type_manage'),[]),
   (T('Archives'),URL('default','archives')==URL(),URL('default','archives'),[])
    ] ) )

