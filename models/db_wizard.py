### we prepend t_ to tablenames and f_ to fieldnames for disambiguity

db.define_table( "t_library_type" , 
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_description', type='text',
          label=T('Name')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table( 't_sample_tracking' ,
    Field('f_key', type='string',
          label=T('Bionimbus Key Id')),
    Field('f_date', type='string',
          label=T('Key Generation Date')),
    Field('f_project', type='string',
          label=T('Project')),
    Field('f_work_requested', type='string',
          label=T('Work Requested')),
    Field('f_current_status', type='string',
          label=T('Current Status')),
    Field('f_queued', type='string',
          label=T('Queued')),
    Field('f_billing_status', type='string',
          label=T('Billing Status (Tifani/Erin: please enter any additional work performed here that was not in request otherwise enter nothing)')),
    Field('f_facility', type='string',
          label=T('Sequencing Facility')),
    Field('f_seq_filenames', type='string',
          label=T('Sequence Filenames')),
    Field('f_ref_lib_map_out', type='string',
          label=T('Reference library to map output')),
    Field('f_request_id', type='string',
          label=T('Request ID')),
    Field('f_request_id_date', type='string',
          label=T('Request ID Date')),
    Field('f_user_name', type='string',
          label=T('User Name')),
    Field('f_institution', type='string',
          label=T('Institution')),
    Field('f_rec_date', type='string',
          label=T('Recieved Sample Date')),
    Field('f_sample_type', type='string',
          label=T('Recieved Sample Type ((Nucleic Acid or Library)')),
    Field('f_library_type', type='string',
          label=T('Library Type')),
    Field('f_material', type='string',
          label=T('Biological Material')),
    Field('f_Protocol', type='string',
          label=T('Library Protocol')),
    Field('f_multi_or_single', type='string',
          label=T('Multiple or Singleplex Lane Requested')),
    Field('f_run_type_req', type='string',
          label=T('Run Type Requested')),
    Field('f_run_type_req', type='string',
          label=T('Run Type Requested')),
    Field('f_lanes_per_sample', type='string',
          label=T('# of lanes per sample ( e.g. 0.25 ; 0.5 ; 1 ; 4 etc.)')),
    Field('f_additional_instructions' , type = 'text' , 
          label=T('Additional instructions from user') ),
    Field('f_short_QC' , type = 'string' ,
          label=T('User requesting a Short-cycle QC Run?') ),
    Field('f_reads_per_sample' , type = 'string' ,
          label=T('Desired # of Reads per sample') ),
    Field('f_index_tag_name' , type = 'string' ,
          label=T('Index Tag Name (IL1-12 or TS1-24)') ),


    Field('f_index_tag_name' , type = 'string' ,
          label=T('Index Tag Name (IL1-12 or TS1-24)') ),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table( 't_sample_state_list' ,
    Field('f_name' , type = 'string' ,
          label=T('Name') ),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table( 't_sample_state' ,
    Field('f_bionimbus_id', type='string',
          label=T('Bionimbus ID'),requires=[IS_IN_DB(db,"t_experiment_unit.f_bionimbus_id",'%(f_bionimbus_id)s')]),
    Field('f_state' , type = db.t_sample_state_list ,
          label=T('State') ),
    Field('f_updated' , type = 'datetime' ,
          label=T('Updated') ),

    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)


    
#db.t_sample_tracking.drop()   

args = [ Field('f_name', type='string',
          label=T('Name')),
    auth.signature ]

db.define_table( 't_platform2' ,
    *args , 
    format='%(f_name)s',
    migrate=settings.migrate)



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
    Field('f_list', type='string',requires = IS_IN_SET([ 'Key Creation' , 'Import' , 'admin' , 'Import Report' ]),
          label=T('List')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)


db.define_table('t_stage',
    Field('f_name', type='string',
          label=T('Name')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)




########################################
db.define_table('t_organism',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_common_name', type='string',
          label=T('Scientific Name')),
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
    Field('f_cloud', type='reference t_cloud',ondelete='set null',
          label=T('Cloud')),
    Field('f_organism', type='reference t_organism',ondelete='set null',
          label=T('Organism')),
    Field('f_platform', type='reference t_platform',ondelete='set null',
          label=T('Platform')),
    Field('f_pi', type='reference auth_user',ondelete='set null',
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
    format='%(f_filename)s',
    migrate=settings.migrate)

db.define_table('t_file_archive',db.t_file,Field('current_record','reference t_file',readable=False,writable=False),migrate=settings.migrate)

#try:
  #db.executesql( "create index bn_file_index on t_file(f_bionimbus_id)" )
  #db.commit()
#except:
  #pass
  #index alreafy exists
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


eu_fields = [ Field('f_name', type='string',
          label=T('Name')),
    Field('f_bionimbus_id', type='string', #unique=True,
          label=T('Bionimbus Id'),writable=False),
    Field('f_sample_state', type=db.t_sample_state_list,
          label=T('Sample State'),writable=False),
    Field('f_sample_state_updated', type='datetime',
          label=T('Sample State Updated'),writable=False),

    Field('f_project', db.t_project,
          label=T('Project')),
    Field('f_library_type', db.t_library_type,ondelete='set null',
          label=T('Library Type')),
    Field('f_subproject', db.t_subproject,
          label=T('Subproject'),default=1),
    Field('f_organism', type='reference t_organism',ondelete='set null',
          label=T('Organism')),
    Field('f_stage', type='reference t_stage',ondelete='set null',
          label=T('Stage')),
    Field('f_sample', type='string',
          label=T('Sample')),
    Field('f_experiment', type='string',
          label=T('Experiment')),
    Field('f_agent', type='string',
          label=T('Antibody')),
    Field('f_treatment', type='string',
          label=T('Treatment')),
    Field('f_barcode', type='string',
          label=T('Barcode')),
    Field('f_protein', type='string',
          label=T('Protein')),
    Field('f_reads', type='string',
          label=T('Reads')),
    Field('f_read_length', type='string',
          label=T('Read Length')),
    Field('f_lib_prep_protocol', type='string',
          label=T('Library Prep Protocol')),
    Field('f_desired_multiplexing', type='string',
          label=T('Desired Multiplexing')),
    Field('f_read_type' , type = 'string',
          label=T('Read Type')),
    Field('f_prep_preformed_by', type='string',
          label=T('Prep Performed by')),
    Field('f_desired_minimum_reads', type='string',
          label=T('desired minimum reads')),
    Field('f_whole_exome_custom_capture', type='string',
          label=T('Whole Exome Custom Capture')),
    Field('f_capture_protocol', type='string',
          label=T('Capture Protocol')),
    Field('f_capture_size', type='string',
          label=T('Capture Size (GB)')),
    Field('f_strain', type='string',
          label=T('Strain')),
    Field('f_tissue', type='string',
          label=T('Tissue')),
    Field('f_source', type='string',
          label=T('Source')),
    Field('f_replicate', type='string',
          label=T('Replicate')),
    Field('f_target_symbol', type='string',
          label=T('Target Symbol')),
    Field('f_target_ID', type='string',
          label=T('Target ID')),
    Field('f_fb_wb_ID', type='string',
          label=T('Flybase/Wormbase ID')),
    Field('f_is_public' , type = 'boolean' ,
          label=T('Public')),
    Field('f_import_id' , type = 'integer' ,
          label=T('Import ID'),writable=False),
    Field('f_spreadsheet' , type = 'integer' ,
          label=T('Spreadsheet'),writable=False)
]


cg_fields_def = [
    [ 'f_alias' , 'Alias' ] , 
    [ 'f_aliquot_id' , 'Aliquot ID' ] , 
    [ 'f_analysis_accession' , 'Analysis Accession' ] , 
    [ 'f_analysis_id' , 'Analysis ID' ] , 
    [ 'f_analysis_type' , 'Analysis Type' ] , 
    [ 'f_analyte_code' , 'Analyte Code' ] , 
    [ 'f_center_name' , 'Center Name' ] , 
    [ 'f_disease_abbr' , 'Disease Abbreviation' ] , 
    [ 'f_filename' , 'Filename' ] ,
    [ 'f_last_modified' , 'Last Modified' ] , 
    [ 'f_library_strategy' , 'Library Strategy' ] , 
    [ 'f_participant_id' , 'Participant ID' ] , 
    [ 'f_platform' , 'Platform' ] , 
    [ 'f_sample_accession' , 'Sample Accession' ] , 
    [ 'f_sample_id' , 'Sample ID' ] , 
    [ 'f_sample_type' , 'Sample Type' ] , 
    [ 'f_xml_text' , 'Search XML Text' ] , 
    [ 'f_state' , 'State' ] , 
    [ 'f_study' , 'Study' ] , 
    [ 'f_tss_id' , 'Tissue Source Site' ] , 
    [ 'f_title' , 'Title' ] ]


for f in cg_fields_def:
  eu_fields.append( Field( f[0] , type='string' , label=f[1] ) )

eu_fields.append( auth.signature )


########################################
db.define_table('t_experiment_unit',
    *eu_fields , 
    format='%(f_name)s',
    migrate=settings.migrate)

db.t_experiment_unit.f_agent.widget = SQLFORM.widgets.autocomplete(
     request, db.t_experiment_unit.f_agent , id_field= db.t_experiment_unit.f_agent , distinct = True )

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
    Field( 'f_proj_subproj' ,  type = 'string' , label=T('Project/Subproject') , requires=IS_NOT_EMPTY() ) , 
    Field( 'f_platform' , type = 'reference t_platform' , label=T('Platform') ,ondelete='set null'),
    Field('f_organism', type='reference t_organism',ondelete='set null',
          label=T('Organism')),
    Field('f_stage', type='reference t_stage',ondelete='set null',
          label=T('Stage'),default=1),
    Field( 't_facility' ,  type = 'reference t_facility' , ondelete='set null', label=T('Facility')  , default = 1 ) ,
    Field( 'f_lanes_per_sample' , type = 'integer' , label=T('Samples requested per lane') ) , 
    Field( 'f_cycles_per_lane' , type = 'string' , label=T('Cycles requested per lane') ) ,
    Field( 'f_reference_library_to_map_output' , type = 'string' , label=T('Refrence library to map output') ) ,
    Field( 'f_comments' , type = 'text' , label=T('Comments') ) ,
    Field( 'f_added_to_tracking_sheet' , type = 'boolean' , label=T('Added to tracking sheet') , default = 'f' , writable = False , readable = False ) ,
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

db.define_table( "t_selected_files" ,
    Field('f_id', type=db.t_file,
          label=T('File')),
    Field('f_counts', type='bigint',
          label=T('Counts')),
    Field('f_size', type='bigint',
          label=T('Size')),
    Field('f_user', type=db.auth_user,
          label=T('User')),
    auth.signature,
    migrate=settings.migrate)

db.define_table( "t_dropbox_keys" ,
    Field('f_hash', type="string",
          label=T('Hash' ) , 
          unique=True),
    auth.signature,
    migrate=settings.migrate)

db.define_table( "t_dropbox_files" ,
    Field('f_dropbox', type=db.t_dropbox_keys,
          label=T('Key')),
    Field('f_file', type=db.t_file,
          label=T('File')),
    auth.signature,
    migrate=settings.migrate)



