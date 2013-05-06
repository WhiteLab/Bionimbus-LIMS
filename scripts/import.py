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

path = '/XRaid/bridge/130418_SN484_0205_BD1L1AACXX/2013-25_130418_SN484_0205_BD1L1AACXX_7_1_sequence.txt.gz'
test_path = '/home/dave/tmp/'
#path = test_path

potentials = run( 'find ' + path  )

by_project = {}
fullreport = []

for file in potentials:
   file = file.strip()
   fullpath = file
   file = file.split( '/' )
   file = file[ -1 ] 
  
   already = db( db.t_file.f_filename == file ).select()

   if len( already ) == 0:
     
     justpath = fullpath.split( '/' )
     justpath = justpath[ : -1 ]
     justpath = '/'.join( justpath )

     if not os.path.exists( justpath + '/import.me' ):
       continue

     fn = file.split( '/' )[ -1 ]
     bn_id = fn.split( '_' )[ 0 ]
     
     row = db( db.t_experiment_unit.f_bionimbus_id == bn_id ).select()
     if len( row ) <> 1:
       #print "malformed bionimbus ID:" , bn_id 
       continue 

     fullreport.append( ( bn_id , fn ) )

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
   
     reads = file_len( fullpath ) / 4 
  
     db( db.t_file.id == id ).update( f_newpath = newname , f_filename = file  , f_reads = reads )
     print "**** fin!" 


for project in by_project.keys():
  paths = by_project[ project ]
  project,title = project.split( ',' )

  content = ''
  print "type =",title 

  extra = [ db.t_experiment_unit.f_bionimbus_id , db.t_file.f_path , db.t_file.f_reads ]

  extra += [ db.t_platform.f_name , 
             db.t_project.f_name , 
             db.t_organism.f_name , 
             db.t_stage.f_name , 
             db.t_facility.f_name , 
             db.t_keygen_spreadsheets.f_lanes_per_sample ,
             db.t_keygen_spreadsheets.f_cycles_per_lane , 
             db.t_keygen_spreadsheets.f_reference_library_to_map_output , 
             db.t_keygen_spreadsheets.f_comments ]

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
          db.t_experiment_unit.f_name
        , db.t_experiment_unit.f_agent
        , db.t_experiment_unit.f_is_public
    ]

  res = extra + res 

  db.t_project.f_name.label = 'Project'
  db.t_organism.f_name.label = 'Organism'
  db.t_stage.f_name.label    = 'Stage'
  db.t_facility.f_name.label    = 'Facility'
  db.t_platform.f_name.label    = 'Platform'

  print paths 
  for fpath in paths:
    row = db(
              ( db.t_file.f_path == fpath ) & ( db.t_experiment_unit.f_bionimbus_id == db.t_file.f_bionimbus_id ) ).select( 
     left = [ 
              db.t_project.on( db.t_experiment_unit.f_project      == db.t_project.id ) ,
              db.t_organism.on( db.t_experiment_unit.f_organism     == db.t_organism.id ) ,
              db.t_stage.on( db.t_experiment_unit.f_stage        == db.t_stage.id ) ,
              db.t_keygen_spreadsheets.on( db.t_experiment_unit.f_spreadsheet  == db.t_keygen_spreadsheets.id ) ,
              db.t_facility.on( db.t_keygen_spreadsheets.t_facility == db.t_facility.id ) ,
              db.t_platform.on( db.t_keygen_spreadsheets.f_platform == db.t_platform.id ) ] ) 
     
    if content == '':
      content = '<html><table border="3">'
      content += '<tr>'
      for r in res:
        content += '<td>' + r.label + '</td>'
      content += '</tr>\n\n'
   
    if len( row ) > 0:
      row = row[ 0 ] 
      content += '<tr>'
      for r in res:
        c = 'None'
        try:
          c = flatten( row[ r ] )
        except:
          pass
        content += '<td>' + c + '</td>'
      content += '</tr>\n\n'
    else:
      content += '<tr><td>'+fpath+'</td></tr>'

  content += '</table></html>'

  pname = db.t_project[ project ].f_name

  sendMailTo( db , 'dhanley@uchicago.edu' , "Files imported to " + pname , content , list = 'Import' , project = project )

fullLen = len( fullreport )
if fullLen > 0:
  report  = '<html>\n'
  report += '<table border="3">\n'
  report += 'Number of files: %d' % fullLen 
  report += '<br>\n'
  for row in fullreport:
    report += '<tr><td>%s</td><td>%s</td></tr>\n' % row 
  report += '</html>'
  sendMailTo( db , 'dhanley@uchicago.edu' , 'Import report' , report , list = 'Import Report' )

if path == test_path:
  db.rollback()
