
import pyinotify
import os
import sys
sys.path.append( '.' )
import tukey

# the one setting.  Where the files go
base_directory = '/home/ubuntu/FILES/' # must not have trailing slash 

# where to look for the gluster files
gluster_base = '/glusterfs'
swift_base   = '/home/ubuntu/cloudfuse/mnt'

# in case there is a trailing slash, strip it/them
while( base_directory[ -1 ] == '/' ):
  base_directory = base_directory[ : -1 ] 

# we need to know how many parts there are in the 
base_length = len( base_directory.split( '/' ) )


# this keeps a hash of previous manifests per directory, so we can quickly detect differences upon change
manifest_hash = {}


#
# this is a stub database for mapping id's to paths
# for a user and an ID.  It is here for both testing, and in case
# we ever need to serve files based on ID's without the 
# tukey system present
#
import sqlite3
# the two persistent globals
conn = c = None



def find_file_sqlite( user , id ):
  global conn , c 
  # if there's no database connection, make the connection, and try to make
  # the one table we use.  Instead of testing for the table, just make it, 
  # and catch and ignore the "table already exists" exception
  if c == None:
    conn = sqlite3.connect( 'cloud_drive.db' )
    c = conn.cursor()
    try:
      c.execute( 'create table cdm ( user , id , kind , path )' )
      c.commit()
    except:
      pass

  # see if the file exists and is visible for the user. If so, return the kind and 
  rows = c.execute( 'select kind,path from cdm where user = ? and id = ? ' , ( user , id ) )
  for row in rows:
    row = rows.fetchone()
    yield row[0],row[1]


def file_file_tukey( user , id ):
  print "looking for " , id , " with tukey"
  md = tukey.get_path_for_id( id )
  return [ [ md[ 'type' ] , md[ 'filepath' ] ] ]

def find_file( user , id ):
  #find_file_sqlite( user , id )
  return file_file_tukey( user , id )


def run( str ):
  print "Running" , str
  os.popen( str ).readlines()



def mount_file( kind , basepath , file_from ):
 ff = file_from.split( '/' )
 fn = ff[ -1 ]
 #used an IF here to accoutn for different mounting procedures
 if kind == 'gluster':
   run( 'ln -s %s/%s %s/%s' % ( gluster_base , file_from , basepath , fn ) )
 elif kind == 'swift':
   run( 'ln -s %s/%s %s/%s' % ( swift_base , file_from , basepath , fn ) )



def handle_manifest_close( cwp ):
  pathparts = cwp.split( '/' )
  path = pathparts[ base_length : -1 ]

  # No manifest in the base directory
  if len( path ) == 0:
    return 

  # this is the user we will check for 
  user = path[ 0 ] 
 
  # the relative directory of the manifest ( offset from base_path ) 
  # it's out key to check for the previous path of the manifest 
  key = '/'.join( path ) 

  # The full path to the manifest, minuts the manifest itself.
  # We use this so we know where to put the files 
  path_to_manifest = '/'.join( pathparts[ : -1 ] )

  # grab the contents of the manifest file. Should be a lot of ID's 
  manifest_ids = open( cwp ).readlines()

  # load the contents of the manifest into a dictionary 
  new_manifest = {}
  for id in manifest_ids:
    new_manifest[ id.strip() ] = []

  # is there is no previous manifest dictionary, create a blank one. 
  # then set the old manifest directory
  if not manifest_hash.has_key( key ):
    manifest_hash[ key ] = {}
  old_manifest = manifest_hash[ key ]

  # for every file from the old manifest not present in the new manifest, delete it 
  for oldie in old_manifest.keys():
    if not new_manifest.has_key( oldie ):
      try:
        for kind , path in find_file( user , oldie ):
          os.unlink( "%s/%s" % ( path_to_manifest , path.split( '/' )[ -1 ] ) )
        print "unlink %s/%s" % ( path_to_manifest , path.split( '/' )[ -1 ] ) 
      except:
        pass

  # every file in the new manifest that doesn't appear in old one, if we can get its info
  # ( valid key, and we have access ) we mount it 
  for newbie in new_manifest.keys():
    if not old_manifest.has_key( newbie ):
      print "newbie:" , newbie
      ff = find_file( user , newbie )
      print ff
      for kind , path in ff:
        print kind , path 
        mount_file( kind , path_to_manifest , path )
    
  #replace the old manifest with the new one. 
  manifest_hash[ key ] = new_manifest




# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE  # watched events

#handle the events of files being created and deleted 
class EventHandler(pyinotify.ProcessEvent):
    # catch file closes.  If it's the manifest, process it 
    def process_IN_CLOSE_WRITE(self, event):
        cwp = event.pathname
        print "closing" , cwp
        if cwp.endswith( 'MANIFEST' ):
          handle_manifest_close( cwp )

    # files being deleted.  TODO: remove inotify, remove manifest if the directory is gone, etc. 
    def process_IN_DELETE(self, event):
        pass
        #print "Removing:", event.pathname
    
    # look at file creation. If it's a directory, add an inotify watch for it
    def process_IN_CREATE(self, event):
        path = event.pathname
        if os.path.isdir( path ):
          print "adding path" , path
          wdd = wm.add_watch( path , mask, rec = True )



# on startup look for all manifest files; use them to create hashes
fs = os.popen( "find %s -name MANIFEST" % base_directory ).readlines()
for f in fs:
  f = f.strip()
  handle_manifest_close( f )



# create the event handle, and add it to the inotify watch
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch( base_directory , mask, rec = True )



# start watching files 
notifier.loop()
