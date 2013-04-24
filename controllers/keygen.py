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

from applications.Bionimbus.modules.cols import * 

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

def comma_or_nought( itm ):
  if itm == None:
    return '' 
  return ' ( %s ) ' % itm 

def projects_for_user():
  d = db.t_user_project
  p = db.t_project
  sub = db.t_subproject
  lefty = sub.on( p.id == sub.f_parent )
  pfu = db( ( d.f_user_id == auth.user_id ) &
            ( d.f_project_id == p.id      ) ).select( left = lefty )
  return [ ( row[ p.f_name ] + comma_or_nought( row[ sub.f_name ] ) ,
             str( row[ p.id ] ) + ',' + str( row[ sub.id ] ) 
           ) for row in pfu ]


templates = [ 'Samples_ChIPseq.xls' , 
              'Samples_Exomes.xls' ,
              'Samples_DNAseq_Whole_Genome.xls' , 
              'Samples_RNAseq.xls' ]


def trimProject( form ):
  pfu = projects_for_user()
  options = nameval_to_options( pfu )
  form[0][0][1][0] = SELECT( *options ,  _class="generic-widget" , 
                             _id="t_keygen_spreadsheets_f_proj_subproj" , _name="f_proj_subproj" )


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

titles = [ 'dswg' , 'rnaseq' , 'dswg2' , 'CS' , 
           'ChiPseq' , 'Exome' , 'DNA' , 'RNA' ]


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
            print "Invalid title '%s' " % title
            raise "Invalid spreadsheet" 
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
  rows     = db(db.t_keygen_spreadsheets).select( )
  row      = rows.last()
  fn       = row.file
  psp      = row.f_proj_subproj
  organism = row.f_organism 
  stage    = row.f_stage

  psp = psp.split( ',' )
  projectid = int( psp[ 0 ] ) 
  project = db.t_project[ projectid ]
  projectname = project[ db.t_project.f_name ]
  
  subproject  = None
  try:
    subproject = int( psp[ 1 ] )
    subproj_name = db.t_subproject[ subproject ][ db_t_subproject.f_name ]
    projectname += " ( %s ) " % subproj_name
  except:
    pass

  title , matrix = spreadsheet_to_matrix( "applications/Bionimbus/uploads/" + fn )
  
  tab = { 'dswg'   : 'DNAseq' , 
          'dswg2'  : 'DNAseq' ,
          'rnaseq' : 'RNAseq' , 
          'CS'     : 'ChIP-seq' ,  
          'ChiPseq': 'ChIP-seq' , 
          'RNA'    : 'RNAseq' , 
          'Exome'  : 'Exome' , 
          'DNA'    : 'DNAseq' } 

  lib_type = tab[ title ] 
  lib_type = db(  db.t_library_type.f_name == lib_type ).select().first().id

  return row , fn , project , projectname , projectid , title , matrix , organism , stage , subproject , lib_type 


def make_slug( id , keys = None ):
  row , fn , project , projectname , projectid , title , matrix , organism , stage , subproject , lib_type = get_spreadsheet_info( id )

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

  if subproject <> None:
    table.append( TR( LABEL( "Subproject" ) ,
                      LABEL( db.t_subproject[ subproject ].f_name ) ) )

  library_name = db.t_library_type[ lib_type ].f_name

  table.append( TR( LABEL( "Library type" ) , 
                    LABEL( library_name ) ) )

  table.append( TR( LABEL( "Organism" ) ,
                    LABEL( db.t_organism[ organism ].f_name ) ) )

  platform = db( db.t_platform == project[ db.t_project.f_platform ] ).select( db.t_platform.f_name )
  platform = platform[ 0 ]
  platform = platform[ db.t_platform.f_name ]

  table.append( TR( LABEL( "Platform" ) ,
                    LABEL( platform ) ) )

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
 
  for row in matrix[ 1: ]:
    values = extractRow( title , row )
    if table == []:
      table.append( TR( *( [ "*" ] + [ v[ 0 ] for v in values ] ) ) )

    ar = []
    if keys:
      l = keys[ 0 ]
      keys = keys[ 1: ] 
    else:
      l = "Row " + str(x)
    ar.append( LABEL( l ) )
    x = x + 1 
    for v in values:
      ar.append( v[ 2 ] )
    table.append( TR( *ar ) )
  slug.append( TABLE( *table ,  _style='border:1px solid black' ) )
  return slug


def process_key_spreadsheet( id ):
  slug = make_slug( id )
  slug.append( INPUT( value = 'Create Keys' , _type = 'submit' , _action = URL( 'page_two' ) )  )
  form = FORM( _action = 'create_keys/' + str( id ) , *slug)
  return locals()


basic_lookup = [ [ 'Name'       , 'f_name'       , None ] ,
                 [ 'Material'   , 'f_sample'   , None ] , 
                 [ 'Experiment' , 'f_experiment' , None ] ,
                 [ 'Antibody'   , 'f_agent'   , None ] , 
                 [ 'Barcode'    , 'f_barcode'    , None ] ]

import copy

def old_sheet( indexes , row ):
  res = copy.deepcopy( basic_lookup )
  for a in range(0,5):
    res[ a ][ 2 ] = row[ indexes[ a ] ]
  return res

def unswizzle( title , map , values ):
  tt = db.t_experiment_unit.f_type

  res = [ [ tt.label , tt.name , title ] ]
  for (db_key,value) in zip( map , values ):
    print db_key
    rr = [ db_key.label , db_key.name , value ]
    res.append( rr )
  return res 

def extractRow( title , row ):
  r = row
  res = None

  if title == 'dswg':
    res = old_sheet( [ 0 , 1 , 2 , 4 , 7 ] , row )

  if title == 'dswg2':
    res = old_sheet( [ 0 , 1 , 3 , 5 , 8 ] , row ) 

  if title == 'CS':
    res = old_sheet( [ 0 , 1 , 3 , 4 , 9 ] , row )

  if title == 'rnaseq':
    res = old_sheet( [ 0 , 1 , 3 , 5 , 8 ] , row )
  
  #### NEW SPREADSHEETS 

  if title == 'RNA': 
    res = unswizzle( 'RNAseq' , rna_cols(db) , row )
  if title == 'DNA':
    res = unswizzle( 'DNAseq' , dna_cols(db) , row )
  if title == 'Exome':
    res = unswizzle( 'Exomes' , exome_cols(db) , row )
  if title == 'ChiPseq':
    res = unswizzle( 'ChiPseq' , chipseq_cols(db) , row )
  if res == None:
    raise Exception( "Invalid spreadsheet " + title  )
  
  return res

def generate_a_key(  ):
    now = datetime.datetime.now()
    year = now.year
    iters = 0
    bn_id = None
    print "in keygen"
    while (iters < 10) & (bn_id == None):
      print "**"
      max = db.t_keys.f_index.max()
      maxid = db(db.t_keys.f_year == year ).select(max).first()[ max ]
      if maxid == None:
        maxid = 1
      else:
        maxid = maxid + 1
      try:
        bn_id = "%d-%d" % ( year , maxid )
        print "trying to insert" , bn_id
        db.t_keys.insert( f_year = year , f_index = maxid )
        db.commit()
      except:
        print "exception!"
        traceback.print_exc(file=sys.stdout)
        iters = iters + 1
        bn_id = None
    print "returning" , bn_id
    return bn_id


#import xmlrpclib
import datetime
def generate_key( values ):
  #server=xmlrpclib.ServerProxy( 'https://bc.bionimbus.org/Bionimbus/keys/call/xmlrpc' )
  #key = server.generate_a_key()

  key = generate_a_key()
  values[ 'f_bionimbus_id' ] = key
  id = db.t_experiment_unit.bulk_insert( [values] )

  return key


from applications.Bionimbus.modules.mail import sendMailTo



@auth.requires_login()
def create_keys():
  id = int( request.args( 0 ) )
  row , fn , project , projectname , projectid , title , matrix , organism , stage , subproject , lib_type  = get_spreadsheet_info( id )

  keys = ""
  keylist = []

  for row in matrix[ 1: ]:
    _values = extractRow( title , row )
    values = {}
    for v in _values:
      values[ v[1] ] = v[2]
    
    hash = { 'f_organism' : organism , 
             'f_stage'    : stage , 
             'f_project'  : projectid , 
             'f_subproject' : subproject ,
             'f_import_id'  : id , 
             'f_spreadsheet' : id 
    }

    key = generate_key( dict( values.items() + hash.items() ) ) 
     
    keylist.append( key )
    keys = keys + " " + key + ' "' + projectname + '" '
  
  #db.executesql( 'update t_experiment_unit set f_organism = t_project.f_organism from t_project where t_experiment_unit.f_project = t_project.id and t_experiment_unit.f_organism is null' )
  #add to google doc 
  os.popen( "~/write_ids_to_tracking_sheet.pl " + keys ).readlines()

  u = URL( 'default' , 'my_experiments?keywords=t_experiment_unit.f_import_id+=+"%d"' % id )

  slug = make_slug( id , keys = keylist ) 
  msg  = "<html>" + FORM( *slug ).xml() + "</html>"
  
  print msg 
  msg = msg.replace( '</tr>' , '</tr>\n' )
  
  sendMailTo( db , 'dhanley@uchicago.edu' , "Keys created in project " + projectname  , msg , list = 'Import' , project = projectid )
  return redirect( u )
