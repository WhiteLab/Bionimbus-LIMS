import sys
import os

from applications.Bionimbus.modules.file_location import generate_name

def run( str ):
  print str
  os.popen( str ).readlines()

files = db(db.t_file.f_newpath == None ).select()
for f in files:
  rpath = os.path.realpath(f.f_path)
  #print "rpath:" , rpath 

  fn = rpath.split( '/' )[ -1 ]
  #print "fn" , fn 
  
  newpath,newname = generate_name( f.id , f.f_bionimbus_id , fn )
 
  #print "newpath , newname:", newpath , newname 

  if not os.path.exists( newpath ): 
    print "making" 
    run( "mkdir -p " + newpath )
  #else:
  #  print "path is already there" 

  #if not os.path.exists( newname ):
  run( "ln " + rpath + " " + newname )
  db( db.t_file.id == f.id ).update( f_newpath = newname )
  db.commit()
