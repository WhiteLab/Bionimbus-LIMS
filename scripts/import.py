import sys
import os

from applications.Bionimbus.modules.file_location import generate_name

def run( str ):
  print str
  return os.popen( str ).readlines()
  

potentials = run( 'find /XRaid/bridge/' )

try:
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

     id = db.t_file.insert( f_path = file , f_bionimbus_id = bn_id )

     newpath,newname = generate_name( id , bn_id , fn )
     print "going to import" , file , newpath , newname
     run( "mkdir -p " + newpath )
     run( "ln " + fullpath + " " + newname )
     db( db.t_file.id == id ).update( f_newpath = newname , f_filename = file )
     print "**** fin!" 

finally:
  db.rollback()


