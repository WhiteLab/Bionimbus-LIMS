### we prepend t_ to tablenames and f_ to fieldnames for disambiguity



db.define_table( 't_platform' , 
    Field('f_name', type='string',
          label=T('Name')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)


db.define_table( 't_cloud' ,
    Field('f_name', type='string',
          label=T('Name')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)


########################################
db.define_table('t_mail_list',
    Field('f_user', type='reference auth_user',
          label=T('User')),
    Field('f_list', type='string',requires = IS_IN_SET([ 'Key Creation' , 'Import' , 'admin' ]),
          label=T('List')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)




########################################
db.define_table('t_organism',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_common_name', type='string',
          label=T('Common Name')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_organism_archive',db.t_organism,Field('current_record','reference t_organism',readable=False,writable=False),migrate=settings.migrate)



########################################
db.define_table('t_project',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_description', type='string',
          label=T('Description')),
    Field('f_public', type='boolean',
          label=T('Public?')),
    Field('f_cloud', type='reference t_cloud',
          label=T('Cloud')),
    Field('f_organism', type='reference t_organism',
          label=T('Organism')),
    Field('f_platform', type='reference t_platform',
          label=T('Platform')),
    Field('f_pi', type='reference auth_user',
          label=T('Pi')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_project_archive',db.t_project,Field('current_record','reference t_project',readable=False,writable=False),migrate=settings.migrate)

db.define_table('t_subproject',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_parent', type='reference t_project',
          label=T('Parent Project')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)


########################################
db.define_table('t_file',
    Field('f_path', type='string',
          label=T('Path')),
    Field('f_filename', type='string',
          label=T('Filename')),
    Field('f_newpath', type='string',
          label=T('New Path')),
    Field('f_bionimbus_id', type='string',
          label=T('Bionimbus Id')),
    Field('f_size' , type = 'string' , 
          label=T('File size') ) , 
    Field( 'f_reads' , type = 'bigint' , 
          label=T('Reads') ) , 
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_file_archive',db.t_file,Field('current_record','reference t_file',readable=False,writable=False),migrate=settings.migrate)


########################################
db.define_table( 't_user_project' ,
    Field('f_project_id' , type = 'reference t_project' , 
           label=T('Project') ) , 
    Field('f_user_id' , type = 'reference auth_user' ,
           label=T('Users') ) ,
    Field('f_admin' , type = 'boolean' ,
           label=T('Is administrator') ) ,
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

def id_to_fullname( id , row ):
  id = row[ db.t_user_project.f_user_id ]
  r2 = db.auth_user[ id ]
  return r2.first_name + ' ' + r2.last_name 

db.t_user_project.f_user_id.represent = id_to_fullname


########################################
db.define_table('t_experiment_unit',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_bionimbus_id', type='string', #unique=True,
          label=T('Bionimbus Id')),
    Field('f_project', db.t_project,
          label=T('Project')),
    Field('f_subproject', db.t_subproject,
          label=T('Subproject')),
    Field('f_organism', type='reference t_organism',
          label=T('Organism')),
    Field('f_sample', type='string',
          label=T('Sample')),
    Field('f_agent', type='string',
          label=T('Antobody/Treatment')),
    Field('f_barcode', type='string',
          label=T('Barcode')),
    Field('f_protein', type='string',
          label=T('Protein')),
    Field('f_is_public' , type = 'boolean' , 
          label=T('Public')),
    Field('f_import_id' , type = 'integer' ,
          label=T('Import ID')),
    Field('f_spreadsheet' , type = 'integer' ,
          label=T('Spreadsheet')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_experiment_unit_archive', 
    Field('f_name', type='string',
          label=T('Name')),
    Field('current_record','reference t_experiment_unit',
          readable=False,writable=False),
    Field('f_bionimbus_id', type='string', 
          label=T('Bionimbus Id')),
    Field('f_project', db.t_project,
          label=T('Project')),
    Field('f_sample', type='string',
          label=T('Sample')),
    Field('f_agent', type='string',
          label=T('Agent')),
    Field('f_barcode', type='string',
          label=T('Barcode')),
    Field('f_protein', type='string',
          label=T('Protein')),
    Field('f_is_public' , type = 'boolean' ,
          label=T('Public')),
    migrate=settings.migrate
     )

db.define_table( 't_barcodes' ,
        Field('f_name', type='string',
          label=T('Name'),unique=True),
        Field('f_sequence', type='string',
          label=T('Sequence'),unique=True),migrate=settings.migrate)

db.define_table('t_facility',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_contact', type='text',
          label=T('Contact Information')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)


db.define_table('t_keygen_spreadsheets', 
    Field( 'f_proj_subproj' ,  type = 'string' , label=T('Project/Subproject')  ) , 
    Field( 'f_platform' , type = 'reference t_platform' , label=T('Platform') ) ,
    Field('f_organism', type='reference t_organism',
          label=T('Organism')),
    Field( 'f_library_prep_type' , type = 'string' , label=T('Library Preparation Type') , 
            requires = IS_IN_SET([  'DNAseq' , 'ChIP-seq' , 'Paired-end' , 'RNAseq' , '16s' ]) ) ,
    Field( 't_facility' ,  type = 'reference t_facility' , label=T('Facility')  ) ,
    Field( 'f_lanes_per_sample' , type = 'integer' , label=T('Samples requested per lane') ) , 
    Field( 'f_cycles_per_lane' , type = 'string' , label=T('Cycles requested per lane') ) ,
    Field( 'f_reference_library_to_map_output' , type = 'string' , label=T('Refrence library to map output') ) ,
    Field( 'f_comments' , type = 'text' , label=T('Comments') ) ,
    Field('file','upload', requires = IS_NOT_EMPTY() ) , 
    migrate=settings.migrate )



#
#  Key models
#


db.define_table( 't_keys' ,
        Field('f_year', type='integer',
          label=T('year')),
        Field('f_index', type='integer',
          label=T('index')),
        migrate=settings.migrate  
)

db.define_table( 't_key_metadata' ,
        Field('f_key', type='reference t_keys',
          label=T('key')),
        Field('f_metadata_key', type='string',
          label=T('metadata key')) ,
        Field('f_value', type='string',
          label=T('value')) ,
       migrate=settings.migrate
)
