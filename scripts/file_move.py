import sys
import os

from applications.Bionimbus.modules.file_location import generate_name

def run( str ):
  print str
  os.popen( str ).readlines()

files = db(db.t_file).select()
for file in files:
  rpath = os.path.realpath(file.f_path)
  fn = rpath.split( '/' )[ -1 ]

  newpath,newname = generate_name( file.id , file.f_bionimbus_id , fn )
  
  run( "mkdir -p " + newpath )
  run( "ln " + rpath + " " + newname )
  db( db.t_file.id == file.id ).update( f_newpath = newname )
  db.commit()
