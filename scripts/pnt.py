
import pyinotify
import os

base_directory = '/home/ubuntu/FILES' # must not have trailing slash 

base_length = len( base_directory.split( '/' ) )

manifest_hash = {}

def handle_manifest_close( cwp ):
  pathparts = cwp.split( '/' )
  path = pathparts[ base_length : -1 ]

  # No manifest in the base directory
  if len( path ) == 0:
    return 

  # this is the user we will check for 
  user = path[ 0 ] 
  
  key = '/'.join( path ) 

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
      print "deleting file" , oldie

  for newbie in new_manifest.keys():
    if not old_manifest.has_key( newbie ):
      print "adding file" , newbie 

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
        #print "Removing:", event.pathname
    
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
