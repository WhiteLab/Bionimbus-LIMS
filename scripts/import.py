import sys
import os

from applications.Bionimbus.modules.file_location import generate_name
from applications.Bionimbus.modules.mail          import sendMailTo

from applications.Bionimbus.modules.cols import *

def flatten( x ):
  return str(x) 

def run( str ):
  print str
  return os.popen( str ).readlines()
 
def file_len( fname ):
  try:
    i = 0
    if fname.endswith( '.gz' ):
      cmd = "zcat "+fname
      print cmd 
      f = os.popen( cmd ) 
    else:
      f = open( fname ) 
    for i, l in enumerate(f):
      pass
    return i + 1
  except:
    return 0


path = '/XRaid/bridge/'
test_path = '/home/dave/tmp/'
#path = test_path

potentials = run( 'find ' + path  )

by_project = {}

for file in potentials:
   file = file.strip()
   fullpath = file
   file = file.split( '/' )
   file = file[ -1 ] 

   already = db( db.t_file.f_filename == file ).select()

   if len( already ) == 0:
     fn = file.split( '/' )[ -1 ]
     bn_id = fn.split( '_' )[ 0 ]
     
     row = db( db.t_experiment_unit.f_bionimbus_id == bn_id ).select()
     if len( row ) <> 1:
       #print "malformed bionimbus ID:" , bn_id 
       continue 
     row = row[ 0 ] 
     type = row[ db.t_experiment_unit.f_type ]
     if type == None:
       type = ''
     project = str( row[ db.t_experiment_unit.f_project ] ) + ',' + type

     if not by_project.has_key( project ):
       by_project[ project ] = []

     id = db.t_file.insert( f_path = file , f_bionimbus_id = bn_id )

     by_project[ project ].append( file )

     newpath,newname = generate_name( id , bn_id , fn )
     print "going to import" , file , newpath , newname
     run( "mkdir -p " + newpath )
     run( "ln " + fullpath + " " + newname )
   
     reads = file_len( file ) / 4 
  
     db( db.t_file.id == id ).update( f_newpath = newname , f_filename = file  , f_reads = reads )
     print "**** fin!" 


for project in by_project.keys():
  paths = by_project[ project ]
  project,title = project.split( ',' )

  content = ''
  print "type =",title 

  res = []
  if title == 'RNAseq':
    res = rna_cols(db)
  elif title == 'DNAseq':
    res = dna_cols(db)
  elif title == 'Exomes':
    res = exome_cols(db)
  elif title == 'ChiPseq':
    res = chipseq_cols(db)
  else:
    print "****unmatched type" , title
    res = [
          db.t_experiment_unit.f_bionimbus_id
        , db.t_experiment_unit.f_name
        , db.t_experiment_unit.f_project
        , db.t_experiment_unit.f_subproject
        , db.t_experiment_unit.f_agent
        , db.t_experiment_unit.f_organism
        , db.t_experiment_unit.f_is_public
    ] 
  res = [ db.t_file.f_path , db.t_file.f_reads ] + res

  print paths 
  for fpath in paths:
    row = db( ( db.t_experiment_unit.f_bionimbus_id == db.t_file.f_bionimbus_id ) & ( db.t_file.f_path == fpath ) ).select()
    row = row[ 0 ] 
    if content == '':
      content = '<table>'
      content += '<tr>'
      for r in res:
        content += '<td>' + r.label + '</td>'
      content += '<tr>'
    
    content += '<tr>'
    for r in res:
      content += '<td>' + flatten( row[ r ] ) + '<td>'
    content += '</tr>'

  content += '</table>'

  pname = db.t_project[ project ].f_name
  if path == test_path:
    print '--------'
    print
    print content
    print
  else:
    sendMailTo( db , 'dhanley@uchicago.edu' , "Files imported to " + pname , content , list = 'Import' , project = project )

db.rollback()

