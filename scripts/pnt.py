
import pyinotify
import os

base_directory = '/home/ubuntu/FILES/' # must not have trailing slash 

while( base_directory[ -1 ] == '/' ):
  base_directory = base_directory[ : -1 ] 
base_length = len( base_directory.split( '/' ) )

manifest_hash = {}


import sqlite3
conn = c = None
def find_file( user , id ):
  global conn , c 
  #print 'ff' , user , id 
  if c == None:
    conn = sqlite3.connect( 'cloud_drive.db' )
    c = conn.cursor()
    try:
      c.execute( 'create table cdm ( user , id , kind , path )' )
      c.commit()
    except:
      pass
  ki = ( user , id )
  #print ki 
  rows = c.execute( 'select kind,path from cdm where user = ? and id = ? ' , ki )
  row = rows.fetchone()
  print row
  return row[0],row[1]


def mount_file( kind , basepath , file_from ):
   ff = file_from.split( '/' )
   fn = ff[ -1 ]
   print 'ln -s %s %s/%s' % ( file_from , basepath , fn )

def handle_manifest_close( cwp ):
  pathparts = cwp.split( '/' )
  path = pathparts[ base_length : -1 ]

  # No manifest in the base directory
  if len( path ) == 0:
    return 

  # this is the user we will check for 
  user = path[ 0 ] 
  
  key = '/'.join( path ) 

  path_to_manifest = '/'.join( pathparts[ : -1 ] )

  #print 'opening' , cwp 
  manifest_ids = open( cwp ).readlines()
  #print manifest_ids

  new_manifest = {}
  for id in manifest_ids:
    new_manifest[ id.strip() ] = []

  if not manifest_hash.has_key( key ):
    manifest_hash[ key ] = {}
  old_manifest = manifest_hash[ key ]

  for oldie in old_manifest.keys():
    if not new_manifest.has_key( oldie ):
      file_file( user , oldie )
      print "deleting file" , oldie

  for newbie in new_manifest.keys():
    if not old_manifest.has_key( newbie ):
      kind , path = find_file( user , newbie )
      mount_file( kind , path_to_manifest , path )
    

  manifest_hash[ key ] = new_manifest




# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()

mask = pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        cwp = event.pathname
        print "closing" , cwp
        if cwp.endswith( 'MANIFEST' ):
          handle_manifest_close( cwp )

    def process_IN_DELETE(self, event):
        pass
        print "Removing:", event.pathname
    
    def process_IN_CREATE(self, event):
        path = event.pathname
        if os.path.isdir( path ):
          print "adding path" , path
          wdd = wm.add_watch( path , mask, rec = True )

#on startup look for all manifest files; thereater look for modified ones

fs = os.popen( "find %s -name MANIFEST" % base_directory ).readlines()
for f in fs:
  f = f.strip()
  print f 
  handle_manifest_close( f )


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch( base_directory , mask, rec = True )

notifier.loop()
