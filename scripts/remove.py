import sys
import os

#
# System to remove files
# we need a way to remove files from bionimbus for the periodically occurring incorrect imports
#

def run( cmd ):
  os.popen( cmd ).readlines()

def rm( base , fn ):
  c = 'find %s -type f -name "%s" -exec rm -f {} \;' % ( base , fn )
  print c 
  run( c )

for f in sys.argv[1:]:
  f = f.split('/')[-1]
  rm( settings.data_import , f )
  rm( settings.data_target , f )
  rm( "/%s/data/Cistrack/" % settings.base_dir , f )
  rm( "/%s/bionimbus/" % settings.base_dir , f )
  rr = db( db.t_file.f_filename == f ).delete() 
