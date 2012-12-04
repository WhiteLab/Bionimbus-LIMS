import sys
import os

from applications.Bionimbus.modules.file_location import generate_name

def run( str ):
  print str
  return os.popen( str ).readlines()
  

potentials = run( 'find /XRaid/bridge/' )

for file in potentials:
   file = file.strip()
   already = db( db.t_file.f_path == file ).select()

   if len( already ) == 0:
     fn = file.split( '/' )[ -1 ]
     bn_id = fn.split( '_' )[ 0 ]
     
     id = db.t_file.insert( f_path = file , f_bionimbus_id = bn_id )
     if len( bn_id.split( '-' ) ) <> 2:
       print "malformed bionimbus ID:" , bn_id 
       continue 
     newpath,newname = generate_name( id , bn_id , fn )
     print file , newpath , newname
     run( "mkdir -p " + newpath )
     run( "ln " + file + " " + newname )
     db( db.t_file.id == id ).update( f_newpath = newname )
     db.commit()
     print "**** fin!" 
#   except:
#     pass

#files = db(db.t_file).select()
#for file in files:
#  rpath = os.path.realpath(file.f_path)
#  fn = rpath.split( '/' )[ -1 ]

#  newpath,newname = generate_name( file.id , file.f_bionimbus_id , fn )
  
#  run( "mkdir -p " + newpath )
#  run( "ln " + rpath + " " + newname )
#  db( db.t_file.id == file.id ).update( f_newpath = newname )
#  db.commit()
