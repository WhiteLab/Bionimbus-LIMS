import sys
import os

#
# System to remove files
#

def run( cmd ):
  os.popen( cmd ).readlines()

def rm( base , fn ):
  c = 'find %s -type f -name "%s" -exec rm -f {} \;' % ( base , fn )
  print c 
  run( c )

for f in sys.argv:
  f = f.split('/')[-1]
  rm( "/XRaid/bridge/" , f )
  rm( "/XRaid/share/" , f )
  rm( "/XRaid/data/Cistrack/" , f )
  rm( "/XRaid/bionimbus/" , f )
  rr = db( db.t_file.f_filename == f ).delete() 
