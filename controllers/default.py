# -*- coding: utf-8 -*-
### required - do no delete

import os
import xlrd

from gluon.custom_import import track_changes; track_changes(True)

from applications.Bionimbus.modules.permissions import is_user_admin
from applications.Bionimbus.modules.permissions import get_experiment_visibility_query
from applications.Bionimbus.modules.permissions import experiment_project_join
from applications.Bionimbus.modules.permissions import can_user_access_bionimbus_id

from applications.Bionimbus.modules.cols import *

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
def my_experiments():
  return experiment_unit_manage( public = False )

@auth.requires_login()
def public_experiments():
  return experiment_unit_manage( public = True )

basic_experiment_fields = [
          db.t_experiment_unit.f_bionimbus_id
        , db.t_experiment_unit.f_name
        , db.t_experiment_unit.f_project
        , db.t_experiment_unit.f_subproject
        , db.t_experiment_unit.f_agent
        , db.t_experiment_unit.f_organism
        , db.t_experiment_unit.f_is_public
    ]

extracols = [ db.t_experiment_unit.f_bionimbus_id ,
              db.t_experiment_unit.f_library_type ,
              db.t_experiment_unit.f_project ,
              db.t_experiment_unit.f_subproject ]

@auth.requires_login()
def my_ChipSeq():
  cols = extracols + chipseq_cols(db)
  return experiment_unit_manage( False , cols , 'ChIP-seq' )

@auth.requires_login()
def my_Exomes():
  cols = extracols + exome_cols(db)
  return experiment_unit_manage( False , cols , 'Exome' )

@auth.requires_login()
def my_DNAseq():
  cols = extracols + dna_cols(db)
  return experiment_unit_manage( False , cols , 'DNAseq' )

@auth.requires_login()
def my_RNAseq():
  cols = extracols + rna_cols(db)
  return experiment_unit_manage( False , cols , 'RNAseq' )


@auth.requires_login()
def selected_files():
  arg = request.args( 0 )
  q = db.t_selected_files.f_user == auth.user_id
  if arg == 'clear':
    clearSelected()
    response.flash = 'cleared'
  form = SQLFORM.grid( q , 
                       fields = [ db.t_selected_files.f_id , db.t_selected_files.f_counts , db.t_selected_files.f_size ] ,
                       editable = False ,
                       #deletable = False ,
                       searchable = False , 
                       create = False ,
                       paginate = 100 ,
                       maxtextlength = 150 ,
                       user_signature=False
                     )
  if arg == 'make':
    key = boxFor()
    u = URL( "default/dropbox" , key , scheme=True )
    form[0].insert( 0 , u )
  return locals()


@auth.requires_login()
def clearSelected():
  db( db.t_selected_files.f_user == auth.user_id ).delete()
 
import string
import random
def generate_key( length = 6 ):
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  return ''.join(random.sample(chars*length,length))

def boxFor():
  # try to insert random keys until one inserts successfully,
  # the database's uniqueness constraint doing the lifting. Save the insert id
  box_id = None
  iters = 0
  while box_id == None and iters < 10:
    try:
      hash = generate_key()
      box_id = db.t_dropbox_keys.insert( f_hash = hash )
    except:
      print hash , "seems to be a duplicate"
    iters = iters + 1 
  
  print "hash" , hash

  # insert files into the dropbox content table

  files = db( db.t_selected_files.f_user == auth.user_id ).select()
  print "files" , files 

  fids = []
  for file in files:
    fids.append( file[ db.t_selected_files.f_id ] )
  print "fids" , fids

  for fid in fids:
    print "fid" , fid 
    db.t_dropbox_files.insert( f_dropbox = box_id , f_file = fid )
    
  # return a URL for the user
  clearSelected()
  return hash

def add_bn_id( ids ):
  print "called add bm id's with" , ids 
  ids_to_add = []
  for id in ids:
    rows = db( ( db.t_experiment_unit.id == id ) & 
               ( db.t_experiment_unit.f_bionimbus_id == db.t_file.f_bionimbus_id ) ).select()
    for row in rows:
      ids_to_add.append( ( row[ db.t_file.id ] , row[ db.t_file.f_size ] ,row[ db.t_file.f_reads ] ) )
  print "id's to add:" , ids_to_add
  userid = auth.user_id

  for id,size,counts in ids_to_add:
    likethis = db( ( db.t_selected_files.f_id == id ) & ( db.t_selected_files.f_user == userid ) ).select()
    if len( likethis ) == 0:
      db.t_selected_files.insert( f_id = id , f_user = userid , f_size = size , f_counts = counts )
    else:
      print "didn't add duplicate:" , id , userid
  return redirect( URL( "selected_files" ) )

def fileRow( pub , row ):
  bn_id = row.f_bionimbus_id
  if len(db(db.t_file.f_bionimbus_id == bn_id ).select())>0:
    return A('Libraries'       , _href=URL( "default" , '%s_file_manage?keywords=t_file.f_bionimbus_id+=+"%s"' % (pub,bn_id) ) )

def downloadRow( row ):
  bn_id = row.f_bionimbus_id
  if len(db(db.t_file.f_bionimbus_id == bn_id ).select())>0:
    return A('Download'    , _href=URL( "default" , "bn_download",             args=[row.f_bionimbus_id]))

@auth.requires_login()
def experiment_unit_manage( public , fields = basic_experiment_fields , type = None ):
    if type<>None:
      type = db( db.t_library_type.f_name == type ).select()[0][ db.t_library_type.id]
    pub = 'my'
    if public:
      pub = 'public'
    experiment_links = [
         lambda row: downloadRow( row ),
         lambda row: fileRow( pub , row )
        ]

    editable = True
    arg = request.args( 0 ) 

    if ( arg == 'view' ):
      #experiment_links.append( lambda row: "http://www.opensciencedatacloud.org/keyservice/ark:/31807/bn%s" % row.f_bionimbus_id )
      if db.t_experiment_unit[ request.args[ 2 ] ].f_spreadsheet <> None:
        experiment_links.append( lambda row: A('Spreadsheet Download'    , _href=URL("default","spreadsheet_download",             args=[row.f_spreadsheet])))

    if ( arg == 'edit' ):
      if is_user_admin( db , auth ):
        editable = True
      else:    
        id = int( request.args( 2 ) )
        rows = db( ( db.t_user_project.f_user_id    == auth.user_id ) & ( db.t_experiment_unit.id == id ) ).select( db.t_experiment_unit.id , left = experiment_project_join(db) )
        if len(rows)<1:
          response.flash = "you can't edit that experiment"
          editable = False
        else:
          editable = True 
    
    #if arg == 'csv':
    #  form = SQLFORM.grid( db.t_experiment_unit )
    #  return locals()

    if public == True:
      q = db.t_experiment_unit.f_is_public == 't'
    else:
      if is_user_admin( db , auth ):
        q = db.t_experiment_unit.id <> -1 
      else:
        q = ( db.t_experiment_unit.f_project == db.t_user_project.f_project_id ) & ( db.t_user_project.f_user_id == auth.user_id )

    if type <> None:
      q = q & ( db.t_experiment_unit.f_library_type == type )

    form = SQLFORM.grid( q , 
                         fields = fields , 
                         links = experiment_links , 
                         editable = editable , 
                         onupdate = auth.archive , 
                         deletable = False , 
                         create = False , 
                         maxtextlength = 150,
                         paginate = 100 , 
                         selectable = lambda ids: add_bn_id(ids) ,
                        )
    #need this try-catch in case the table is empty, and therefore has no submit button
    try:
      form.element('.web2py_table input[type=submit]')['_value'] = T('Add To Dropbox')
    except:
      pass
    return locals()


def metadata_display():
    experiment_links = [
         lambda row: A('Download',_href=URL("default","bn_download",args=[row.f_bionimbus_id])),
         lambda row: A('Files'   ,_href=URL("default","file_manage" , args=[ '?keywords=t_file.f_bionimbus_id+%%3D+"%s"' % row.f_bionimbus_id ] ) ) ,
        ]

    experiment_links.append( lambda row: "http://www.opensciencedatacloud.org/keyservice/ark:/31807/bn2011-123%s" % row.f_bionimbus_id )

    fields = [
          db.t_experiment_unit.f_bionimbus_id
        , db.t_experiment_unit.f_name
        , db.t_experiment_unit.f_project
        , db.t_experiment_unit.f_agent
        , db.t_experiment_unit.f_barcode
        , db.t_experiment_unit.f_protein
        , db.t_experiment_unit.f_is_public
    ]

    form = SQLFORM.grid( db.t_experiment_unit ,
                         fields = fields ,
                         links = experiment_links ,
                         editable = False ,
                         onupdate = auth.archive ,
                         deletable = False ,
                         create = False ,
                         user_signature = False
                        )
    return locals()


def metadata():
  id = request.args( 0 )
  row = db( db.t_experiment_unit.f_bionimbus_id == id ).select()
  row = row[ 0 ] 
  id = row[ db.t_experiment_unit.id ]
  return redirect( 'https://bc.bionimbus.org/Bionimbus/default/metadata_display/view/t_experiment_unit/' + str( id ) )


def files_for( bn_id ):
  rows = [ r.f_newpath for r in db(db.t_file.f_bionimbus_id==bn_id).select() ]
  return rows

def download_fullpaths_tar( name , fullpaths ):
  instream = os.popen( "tar --dereference -czf - " + " ".join( fullpaths ) )
  response.headers[ 'Content-Type' ] = '.gz'
  response.headers[ 'Content-disposition' ] = 'attachment; filename=%s.tgz' % name
  return response.stream( instream , chunk_size = 256 * 256 )

@auth.requires_login()
def bn_download():
  args = request.env.path_info.split('/')[3:]
  bn_id = args[ 1 ]

  if not can_user_access_bionimbus_id( bn_id , db , auth ):
    return HTML( "You don't have permissions to download that experiment" )  # + db._lastsql )

  rows = files_for( bn_id )
  return download_fullpaths_tar( bn_id , rows )

@auth.requires_login()
def dropbox():
  key = request.args( 0 )
  files = db( ( db.t_dropbox_keys.f_hash == key ) & 
              ( db.t_dropbox_keys.id == db.t_dropbox_files.f_dropbox ) & 
              ( db.t_dropbox_files.f_file == db.t_file.id ) ).select( db.t_file.f_newpath )
  files = [ f[ db.t_file.f_newpath ] for f in files ]
  #return ",".join( files ) 
  return download_fullpaths_tar( key , files ) 

def spreadsheet_download():
  args = request.env.path_info.split('/')[3:]
  try:
    ss_id = int( args[ 1 ] )
    (filename,file) = db.t_keygen_spreadsheets.file.retrieve(db.t_keygen_spreadsheets[ss_id].file)
    response.headers[ 'Content-disposition' ] = 'attachment; filename=%s' % filename
    return response.stream( file )
  except:
    return HTML( "That key was not created with a spreadsheet" )

@auth.requires_login()
def cloud_manage():
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_cloud ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         #fields    = fields
                       )
    return locals()


@auth.requires_login()
def barcode_manage():
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_barcodes ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         paginate = 1000 ,
                         maxtextlength = 150,

                         #fields    = fields 
                       )
    return locals()

@auth.requires_login()
def mailing_list_manage():
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_mail_list ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         paginate = 1000 ,
                         maxtextlength = 150,
                         #fields    = fields
                       )
    return locals()


@auth.requires_login()
def mail_list():
    editable = True # is_user_admin()
    form = SQLFORM.grid( db.t_mail_list ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         #fields    = fields
                       )
    return locals()


@auth.requires_login()
def organism_manage():
    fields = [
              db.t_organism.f_name 
            , db.t_organism.f_common_name 
             ]
    editable = is_user_admin( db , auth )
    
    links = [
         lambda row: A('Libraries'       , _href=URL( "default" , 'my_experiments?keywords=t_experiment_unit.f_organism+=+"%d"' % (row[ db.t_organism.id ] ) ) ) ,
        ]

    form = SQLFORM.grid( db.t_organism , 
                         fields    = fields , 
                         create    = editable ,
                         editable  = editable ,
                         deletable = False ,
                         onupdate  = auth.archive ,
                         paginate = 1000 ,
                         maxtextlength = 150 ,
                         links = links 
                         )
    return locals()

@auth.requires_login()
def facility_manage():
    editable = is_user_admin( db , auth )

    form = SQLFORM.grid( db.t_facility ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = False ,
                         )
    return locals()

@auth.requires_login()
def platform_manage():
    editable = is_user_admin( db , auth )

    form = SQLFORM.grid( db.t_platform ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = False ,
                         )
    return locals()


@auth.requires_login()
def stage_manage():
    editable = is_user_admin( db , auth )

    form = SQLFORM.grid( db.t_stage.id <> 1 ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = False ,
                         paginate = 1000 ,
                         maxtextlength = 150,
                         )
    return locals()


@auth.requires_login()
def library_type_manage():
    editable = False # is_user_admin( db , auth )

    form = SQLFORM.grid( db.t_library_type ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         )
    return locals()




file_links = [
         lambda row: A('Download',_href=URL("default","file_download",args=[row.id]))
         #lambda row: A('Cloud Push',callback=URL('file_cloud_push',args=[row.id]),target="me")
        ]

@auth.requires_login()
def public_file_manage():
  return file_manage( public = True )

@auth.requires_login()
def my_file_manage():
  return file_manage( public = False)

def add_file_id( ids ):
  ids_to_add = []
  for id in ids:
    rows = db( 
               ( db.t_file.id == id ) ).select()
    for row in rows:
      ids_to_add.append( ( row[ db.t_file.id ] , row[ db.t_file.f_size ] ,row[ db.t_file.f_reads ] ) )
  print "id's to add:" , ids_to_add
  userid = auth.user_id

  for id,size,counts in ids_to_add:
    likethis = db( ( db.t_selected_files.f_id == id ) & ( db.t_selected_files.f_user == userid ) ).select()
    if len( likethis ) == 0:
      db.t_selected_files.insert( f_id = id , f_user = userid , f_size = size , f_counts = counts )
    else:
      print "didn't add duplicate:" , id , userid
  return redirect( URL( "selected_files" ) )



@auth.requires_login()
def file_manage( public ):
    fields = [
              db.t_file.f_filename
            , db.t_file.f_bionimbus_id
            , db.t_file.f_size
            , db.t_file.f_reads 
             ]

    if public == True:
      q = ( db.t_file.f_bionimbus_id == db.t_experiment_unit.f_bionimbus_id) & ( db.t_experiment_unit.f_is_public == 't' )
    else:
      if is_user_admin( db , auth ):
        q = db.t_file
      else:
        q = ( db.t_file.f_bionimbus_id == db.t_experiment_unit.f_bionimbus_id) & ( db.t_experiment_unit.f_project == db.t_user_project.f_project_id ) & ( db.t_user_project.f_user_id == auth.user_id )

    form = SQLFORM.grid( q , 
                         fields        = fields ,
                         field_id      = db.t_file.id ,
                         maxtextlength = 200 , 
                         deletable     = False ,
                         editable      = False ,
                         links         = file_links ,
                         create        = False ,
                         paginate = 1000 ,
                         selectable = lambda ids: add_file_id(ids) ,
                       )
    return locals()



@auth.requires_login()
def file_download():
  args = request.env.path_info.split('/')[3:]
  id = args[ 1 ]

  bn_id = db(db.t_file.id==id).select( db.t_file.ALL )

  bn_id = bn_id[ 0 ]   
  bn_id = bn_id[ db.t_file.f_bionimbus_id ]

  if not can_user_access_bionimbus_id( bn_id , db , auth ):
    return HTML( "You don't have permissions to download files for experiment " + bn_id )  # + db._lastsql )

  path = [ r.f_newpath for r in db(db.t_file.id==id).select() ]
  path = path[ 0 ] 
  parts = path.split( '/' )
  response.headers[ 'Content-Type' ] = '.gz'
  response.headers[ 'Content-disposition' ] = 'attachment; filename=%s' % parts[ -1 ] 
  return response.stream( path , chunk_size = 256 * 256 )
 
 
