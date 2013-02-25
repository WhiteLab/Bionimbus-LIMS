import sys
import os

from applications.Bionimbus.modules.file_location import generate_name
from applications.Bionimbus.modules.mail          import sendMailTo

def run( str ):
  print str
  return os.popen( str ).readlines()
 
def file_len( fname ):
    i = 0
    with os.popen("zcat "+fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

potentials = run( 'find /XRaid/bridge/' )

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
     
     ids = db( db.t_experiment_unit.f_bionimbus_id == bn_id ).select()
     if len( ids ) <> 1:
       #print "malformed bionimbus ID:" , bn_id 
       continue 
     id = ids[ 0 ] 
     project = id[ db.t_experiment_unit.f_project ]

     if not by_project.has_key( project ):
       by_project[ project ] = []

     by_project[ project ].append( ( file , fn ) ) 

     id = db.t_file.insert( f_path = file , f_bionimbus_id = bn_id )

     newpath,newname = generate_name( id , bn_id , fn )
     print "going to import" , file , newpath , newname
     run( "mkdir -p " + newpath )
     run( "ln " + fullpath + " " + newname )
     db( db.t_file.id == id ).update( f_newpath = newname , f_filename = file )
     print "**** fin!" 

for project in by_project.keys():
  files2 = by_project[ project ]
  files = []
  for file,fn in files2:
    f = "%s ( %d reads )" % ( fn , file_len( file ) )

  pname = db.t_project[ project ].f_name
  sendMailTo( db , 'dhanley@uchicago.edu' , "Files imported to " + pname , "\n".join( files ) , list = 'Import' , project = project )


