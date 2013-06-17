#!/usr/bin/python

import os
import sqlite3
import time
import sys
import ConfigParser
import random

config = ConfigParser.RawConfigParser()
config.read('import.config')

dist = config.get( 'main' , 'dist' )
api_key = config.get( 'main' , 'api_key' )
api_url = config.get( 'main' , 'api_url' )

sys.path.append( dist )
sys.path.insert( 0, os.path.dirname( __file__ ) )
from common import submit, display

connection=sqlite3.connect("filedatabase.db")
cursor=connection.cursor()

def run( cmd ):
  """Run a shell action"""
  print cmd
  fh = os.popen( cmd , "r" )
  lines = fh.readlines()
  return lines

#get a list of all the libraries from the web server
#todo: only do this if there is a new file to import 
libs = []
projects = []

def read_libs():
  global libs
  global projects 
  libs = display(api_key, api_url + 'libraries', return_formatted=False)
  print libs
  print
  print
  projects = [ x[ 'name' ] for x in libs ]
  print "projects " , projects
 

read_libs()

folders = {}

def galaxy_ize( path ):
  "Galaxy handles folders and paths in a really stupid way.  Do it their dumb way. If there's more than one /, remove the last one."
  if path.count( "/" )  > 1: 
    path=path[:-1]
  return path


def read_folders():
  """Call the galaxy web server via their API, and get a list of server contents.  Only keep the folders, and make a hash
     that maps folders to their API keys, so we can import simply"""
  for lib in libs:
    print lib
    libname = lib[ 'name' ]
    id = lib[ 'id' ]
    l2 = display(api_key, api_url + 'libraries/%s/contents' % id , return_formatted=False )
    for l in l2:
      if l['type'] == 'folder':
        folders[ libname + l[ 'name' ] ] = l[ 'id' ]

def create_new_projects():
  pfolders = os.popen( 'ls /XRaid/share/public/' ).readlines()
  newOnes = False
  for pf in pfolders:
    pf = pf.strip()
    print 'pf' , pf
    print 'projcts here' , projects

    if pf in projects:
      print ' already exists'
    else:
      cmd = './library_create_library.py ' + pf
      print cmd
      os.popen( cmd ).readlines()
      newOnes = True
  if newOnes:
    read_libs()

def create_path( path ):
  """this is a little complicated.  If there is a new path in the import directory, create it on the server.
     however the new path may be nested, and with the given API's there is no way to do that in one shot.  You need
     to create a folder, find its id, then make the subfolder, etc.  So this creates a long path recursively."""
  ( parent_path , sep , new_folder_name ) = path[:-1].rpartition( '/' )
  parent = parent_path + sep
  if parent == '':
    raise "bogus"
  print "parent , new : " , parent , "," , new_folder_name 
  if not folders.has_key( parent ):
    #if the parent doesn't exist, create it recursively, then create the child ( me ) 
    create_path( parent )
  parent_id = folders[ parent ] 
  data = {}
  data[ 'folder_id' ] = parent_id
  data[ 'name' ] = new_folder_name
  data[ 'create_type' ] = 'folder'
  data[ 'description' ] = ''
  url = api_url + "libraries/" + parent_id + "/contents"
  #print data
  submit( api_key, url , data , return_formatted = False )
  read_folders()

def get_id_for( path ):
  """given a path   (module + folder(s) ) find its id, creating it if necessary."""
  path = path + "/"
  print path
  print folders
  if not folders.has_key( galaxy_ize( path ) ):
    create_path( path )
  return folders[ galaxy_ize( path  ) ] 


#before starting the main loop, fetch a list of folders from the webserver. 
#TODO: only do this if there is a new file to import. 
read_folders()
create_new_projects()

def import_cycle():
  #find all non-hidden real files. 
  ls = run( "find -L import/ \( ! -regex '.*/\..*' \) -type f" )
  random.shuffle( ls )
  if len(ls)>51:
    ls = ls[ : 50 ]

  for filepath in ls:
    filepath = filepath.strip()
    if os.path.isfile( filepath ):
      dir = filepath.split("/")
      dir = dir[ 2 : -1 ]
      dir = "/".join( dir )
      print "dir " , dir
      cursor.execute( "select * from files_imported where path='%s'" % filepath )
      results = cursor.fetchall()
      if len( results ) == 0:
        print "importing " , filepath , dir
        library_id = get_id_for( dir )
        print "library_id : " , library_id 
        connection.commit()
        id = cursor.lastrowid
        just_dir = dir
        #run( "mkdir -p hard_links/" + just_dir )
        pathless = "/".join( filepath.split("/")[2:] )
        #run( "ln -s %s hard_links/%s" % ( filepath , pathless ) )
        #hard_fullpath = os.path.abspath( "hard_links/%s" % pathless )
        run( "mkdir -p soft_links/" + just_dir )
        run( "ln -s %s soft_links/%s" % ( os.path.abspath( filepath ) , pathless ) )
        soft_fullpath = os.path.abspath( "soft_links/%s" % pathless ) 
        
        data = {}
        data['folder_id'] = library_id
        data['file_type'] = 'auto'
        data['dbkey'] = ''
        data['upload_option'] = 'upload_paths'
        data['filesystem_paths'] = soft_fullpath
        data['create_type'] = 'file'
	data['link_data_only'] = 'link_to_files'
        #data['server_dir'] = '/'.join( path.split('/')[:-1] )
        url = api_url + "libraries/%s/contents" % library_id
        print url 
        print data
        libset = submit(api_key, url , data, return_formatted = False)
        cursor.execute( "insert into files_imported(path,importtime) values('%s',datetime('now'))" % filepath )
        connection.commit()
        print libset
      else:
        print "File already imported" , filepath

import_cycle()

