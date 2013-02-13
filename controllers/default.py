# -*- coding: utf-8 -*-
### required - do no delete

import os
import xlrd

from gluon.custom_import import track_changes; track_changes(True)

from applications.Bionimbus.modules.permissions import is_user_admin
from applications.Bionimbus.modules.permissions import get_experiment_visibility_query
from applications.Bionimbus.modules.permissions import experiment_project_join
from applications.Bionimbus.modules.permissions import can_user_access_bionimbus_id

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
def experiment_unit_manage():
    experiment_links = [
         lambda row: A('Download'    , _href=URL( "default" , "bn_download",             args=[row.f_bionimbus_id])),
         lambda row: A('Files'       , _href=URL( "default" , 'file_manage?keywords=t_file.f_bionimbus_id+=+"%s"' % row.f_bionimbus_id ) ) ,
        ]

    editable = True
    arg = request.args( 0 ) 

    if ( arg == 'view' ):
      experiment_links.append( lambda row: "http://www.opensciencedatacloud.org/keyservice/ark:/31807/bn%s" % row.f_bionimbus_id )
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
    
    fields = [ 
          db.t_experiment_unit.f_bionimbus_id
        , db.t_experiment_unit.f_name 
        , db.t_experiment_unit.f_project  
        , db.t_experiment_unit.f_agent  
        , db.t_experiment_unit.f_barcode  
        , db.t_experiment_unit.f_protein  
        , db.t_experiment_unit.f_is_public 
    ] 

    form = SQLFORM.grid( get_experiment_visibility_query( db , auth ) , 
                         left = experiment_project_join( db ) , 
                         fields = fields , 
                         links = experiment_links , 
                         editable = editable , 
                         onupdate = auth.archive , 
                         deletable = False , 
                         create = False 
                        )
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
  print "here!!!"
  id = request.args( 0 )
  row = db( db.t_experiment_unit.f_bionimbus_id == id ).select()
  row = row[ 0 ] 
  id = row[ db.t_experiment_unit.id ]
  return redirect( 'http://bc.bionimbus.org/Bionimbus/default/metadata_display/view/t_experiment_unit/' + str( id ) )



#def add_file_to_push_table( id ):
#  r = db( db.t_file.id == id ).select()
#  r = r[ 0 ] 
#  db.t_cloud_push.insert( f_from      = r.f_newpath , 
#                          f_to        = '/glusterfs/' + auth.user.username + '/' + r.f_filename , 
#                          f_synced    = 'n' )


#@auth.requires_login()
#def file_cloud_push():
#  args = request.env.path_info.split('/')[-1]
#  add_file_to_push_table( int( args ) )

#@auth.requires_login()
#def cloud_push():
#  bn_id = request.env.path_info.split('/')[-1]
#  print "Pushing to cloud ID: " , bn_id
#  rows = [ r.id for r in db(db.t_file.f_bionimbus_id==bn_id).select() ]
#  for r in rows:
#    print "For id" , bn_id , " pushing id " , r 
#    add_file_to_push_table( int( r ) )



def files_for( bn_id ):
  rows = [ r.f_newpath for r in db(db.t_file.f_bionimbus_id==bn_id).select() ]
  return rows

@auth.requires_login()
def bn_download():
  args = request.env.path_info.split('/')[3:]
  bn_id = args[ 1 ]

  if not can_user_access_bionimbus_id( bn_id , db , auth ):
    return HTML( "You don't have permissions to download that experiment" )  # + db._lastsql )

  rows = files_for( bn_id )
  #if len( rows ) == 0 or None in rows:
  #  response.flash = "Sorry, that experiment has no files" 
  #  return redirect(URL('experiment_unit_manage'))
  instream = os.popen( "tar --dereference -czf - " + " ".join( rows ) )
  response.headers[ 'Content-Type' ] = '.gz'
  response.headers[ 'Content-disposition' ] = 'attachment; filename=%s.tgz' % bn_id
  return response.stream( instream , chunk_size = 256 * 256 )


def spreadsheet_download():
  args = request.env.path_info.split('/')[3:]
  ss_id = int( args[ 1 ] )
  (filename,file) = db.t_keygen_spreadsheets.file.retrieve(db.t_keygen_spreadsheets[ss_id].file)
  response.headers[ 'Content-disposition' ] = 'attachment; filename=%s' % filename
  return response.stream( file )


@auth.requires_login()
def barcode_manage():
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_barcodes ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
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
    
    form = SQLFORM.grid( db.t_organism , 
                         fields    = fields , 
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         onupdate  = auth.archive 
                         )
    return locals()

@auth.requires_login()
def facility_manage():
    editable = is_user_admin( db , auth )

    form = SQLFORM.grid( db.t_facility ,
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
def file_manage():
    fields = [
              db.t_file.f_filename
            , db.t_file.f_bionimbus_id
            , db.t_file.f_size
             ]

    lefty = db.t_file.f_bionimbus_id == db.t_experiment_unit.f_bionimbus_id 

    form = SQLFORM.grid( get_experiment_visibility_query( db , auth ) & lefty ,
                         left          = experiment_project_join( db ) ,
                         fields        = fields ,
                         field_id      = db.t_file.id ,
                         maxtextlength = 200 , 
                         deletable     = False ,
                         editable      = False ,
                         links         = file_links ,
                         create        = False 
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
 
 
