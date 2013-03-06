#gent -*- coding: utf-8 -*-
### required - do no delete

import os
import xlrd
import sys
import traceback

from gluon.custom_import import track_changes; track_changes(True)

from applications.Bionimbus.modules.permissions import is_user_admin
from applications.Bionimbus.modules.permissions import get_experiment_visibility_query
from applications.Bionimbus.modules.permissions import experiment_project_join
from applications.Bionimbus.modules.permissions import can_user_access_bionimbus_id
from applications.Bionimbus.modules.gui         import nameval_to_options

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

def projects_for_user():
  d = db.t_user_project
  p = db.t_project
  pfu = db( ( d.f_user_id == auth.user_id ) &
            ( d.f_project_id == p.id      ) ).select()
  return [ ( row[ p.f_name ] , row[ p.id ] ) for row in pfu ]


templates = [ 'Samples_ChIPseq.xls' , 
              'Samples_DNAseq_Whole Genome2.xls' , 
              'Samples_DNAseq_Whole_Genome.xls' , 
              'Samples_RNAseq.xls' ]


def trimProject( form ):
  pfu = projects_for_user()
  options = nameval_to_options( pfu )
  form[0][0][1][0] = SELECT( *options ,  _class="generic-widget" , _id="t_keygen_spreadsheets_f_project" , _name="f_project" )


@auth.requires_login()
def keygen_spreadsheet():
  form = SQLFORM( db.t_keygen_spreadsheets )
  if form.process().accepted:
    id = int( form.vars.id )
    return process_key_spreadsheet( id )

  trimProject( form ) 

  for template in templates:
    st = "/Bionimbus/static/" + template
    l = A( template , _href = st ) 
    form[ 0 ].insert( 0 , l )
  return locals()

titles = [ 'dswg' , 'rnaseq' , 'dswg2' , 'CS' ]

def spreadsheet_to_matrix( fn ):
  book = xlrd.open_workbook( fn )
  title = None
  matrix = []
  for sheet_name in book.sheet_names():
    sh = book.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows):
      mr = []
      row = sh.row_values(rownum)
      for r in row:
        if title == None:
          title = str( r )
          title = title.split() 
          title = title[ 0 ] 
          if not title in titles:
            return 1 / 0 
        mr.append( str( r ) )
      matrix.append( mr )
  return title,matrix


def get_user_hash():
  au = db.auth_user
  users = db( au ).select(  )
  users = [ [ r[ au.id ] , r[ au.first_name ] + " " + r[ au.last_name ] ] for r in users ]

  uh = {} 

  for u in users:
    uh[ u[ 0 ] ] = u[ 1 ]
  return uh


def get_spreadsheet_info( id ):
  rows    = db(db.t_keygen_spreadsheets).select( )
  row     = rows.last()
  fn      = row.file
  project = row.f_project

  project = db( db.t_project.id == row.f_project ).select()
  project = project[ 0 ] 
  projectname = project[ db.t_project.f_name ]
  projectid   = project[ db.t_project.id ]

  title , matrix = spreadsheet_to_matrix( "applications/Bionimbus/uploads/" + fn )
  return row , fn , project , projectname , projectid , title , matrix


def make_slug( id , keys = None ):
  try:
    row , fn , project , projectname , projectid , title , matrix = get_spreadsheet_info( id )
  except:
    return HTML( "Error" )

  slug = [ ]
  table = []
  uh = get_user_hash()
  uh[ None ] = 'None'

  table.append( TR( LABEL( "Principal Investigator" ) ,
                    LABEL( uh[ project.f_pi ] ) ) )

  table.append( TR( LABEL( "Administrative/Accounts Payable" ) ,
                    LABEL( uh[ project.f_pi ] ) ) )

  table.append( TR( LABEL( "Requester" ) ,
                    LABEL( uh[ project.f_pi ] ) ) )

  table.append( TR( LABEL( "Project" ) ,
                    LABEL( projectname ) ) )

  organism = db( db.t_organism == project[ db.t_project.f_organism ] ).select( db.t_organism.f_name )  
  organism = organism[ 0 ] 
  organism = organism[ db.t_organism.f_name ]

  table.append( TR( LABEL( "Organism" ) ,
                    LABEL( organism ) ) )

  platform = db( db.t_platform == project[ db.t_project.f_platform ] ).select( db.t_platform.f_name )
  platform = platform[ 0 ]
  platform = platform[ db.t_platform.f_name ]

  table.append( TR( LABEL( "Platform" ) ,
                    LABEL( platform ) ) )

  table.append( TR( LABEL( "Library Preparation Type" ) , 
                    LABEL( row.f_library_prep_type ) ) )

  table.append( TR( LABEL( "Lanes required per sample" ) ,
                    LABEL( row.f_lanes_per_sample) ) )

  table.append( TR( LABEL( "Cycles required per lane" ) ,
                    LABEL( row.f_cycles_per_lane ) ) )

  table.append( TR( LABEL( "Refrence library to map output" ) ,
                    LABEL( row.f_reference_library_to_map_output ) ) )

  table.append( TR( LABEL( "Comments" ) ,
                    LABEL( row.f_comments ) ) )

  slug.append( TABLE( *table ) )

  x = 1
  table = []
  table.append( TR( "" , "name" , "biological material" , "Antibody/treatment" , "Experiment" , "Barcode" ) ) 
 
  for row in matrix[ 1: ]:
    values = extractRow( title , row )
    ar = []
    if keys:
      l = keys[ 0 ]
      keys = keys[ 1: ] 
    else:
      l = "Row " + str(x)
    ar.append( LABEL( l ) )
    x = x + 1 
    ar.append( values.name ) 
    ar.append( values.material )
    ar.append( values.antibody )
    ar.append( values.experiment )
    ar.append( values.barcode )
    table.append( TR( *ar ) )
  slug.append( TABLE( *table ,  _style='border:1px solid black' ) )
  return slug


def process_key_spreadsheet( id ):
  slug = make_slug( id )
  slug.append( INPUT( value = 'Create Keys' , _type = 'submit' , _action = URL( 'page_two' ) )  )
  form = FORM( _action = 'create_keys/' + str( id ) , *slug)
  return locals()

class Bunch:
  def __init__(self, **kwds):
    self.__dict__.update(kwds)

def extractRow( title , row ):
  r = row # [ INPUT( _value = x ) for x in row ]

  if title == 'dswg':
    return Bunch( name       = r[ 0 ] ,
                  material   = r[ 1 ] ,
                  antibody   = r[ 2 ] ,
                  experiment = r[ 4 ] , 
                  barcode    = r[ 7 ] )
  if title == 'dswg2':
    return Bunch( name       = r[ 0 ] ,
                  material   = r[ 1 ] ,
                  antibody   = r[ 3 ] ,
                  experiment = r[ 5 ] ,
                  barcode    = r[ 8 ] )
  if title == 'CS':
    return Bunch( name       = r[ 0 ] ,
                  material   = r[ 1 ] ,
                  experiment = r[ 3 ] , 
                  antibody   = r[ 4 ] ,
                  barcode    = r[ 9 ] )
  if title == 'rnaseq':
     return Bunch( name       = r[ 0 ] ,
                   material   = r[ 1 ] ,
                   antibody   = r[ 3 ] ,
                   experiment = r[ 5 ] , 
                   barcode    = r[ 8 ] )

  
  raise Exception("Invalid spreadsheet")


import xmlrpclib
def generate_key( name , agent , sample , import_id , project , barcode , spreadsheet_id ):
  server=xmlrpclib.ServerProxy( 'https://bc.bionimbus.org/Bionimbus/keys/call/xmlrpc' )
  key = server.generate_key()
  id = db.t_experiment_unit.insert( f_name = name , 
                                    f_agent = agent ,
                                    f_bionimbus_id = key ,
                                    f_project = project ,
                                    f_sample = sample ,
                                    f_barcode = barcode , 
                                    f_import_id = import_id ,
                                    f_spreadsheet = spreadsheet_id )
  return key


from applications.Bionimbus.modules.mail import sendMailTo



@auth.requires_login()
def create_keys():
  id = int( request.args( 0 ) )
  row , fn , project , projectname , projectid , title , matrix = get_spreadsheet_info( id )

  keys = ""
  keylist = []

  for row in matrix[ 1: ]:
    values = extractRow( title , row )
    key = generate_key( values.name , values.antibody , values.material , id , project , values.barcode , id )
    keylist.append( key )
    keys = keys + " " + key + ' "' + projectname + '" '

  #add to google doc 
  os.popen( "~/write_ids_to_tracking_sheet.pl " + keys ).readlines()

  u = URL( 'default' , 'experiment_unit_manage?keywords=t_experiment_unit.f_import_id+=+"%d"' % id )

  slug = make_slug( id , keys = keylist ) 
  msg  = "<html>" + FORM( *slug ).xml() + "</html>"
  
  print msg 

  sendMailTo( db , 'dhanley@uchicago.edu' , "Keys created in project " + projectname  , msg , list = 'Import' , project = projectid )
  return redirect( u )
