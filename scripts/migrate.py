#!/usr/bin/python

import os
import sys
import pg

connection = pg.connect( 'cistrackdb' , 'localhost', -1 , None , None , 'dstn' , 'cisdstn' )
connection2= pg.connect( 'bionimbus'  , 'localhost', -1 , None , None , 'dstn' , 'cisdstn' )

# TODO: insert using DAL 

def run_sql( c , sql ):
  print sql , ";"
  r = None
  res = c.query( sql )
  if res <> None:
    r = res 
    if type(r) <> type(''):
      r = res.getresult()
  return r

def setter( field , table ):
  id = run_sql( connection2 , "select max(id) from " + table )[0][0]
  run_sql( connection2 , "SELECT pg_catalog.setval('%s', %d)" % ( field , id ) )
  

def foo( a ):
  if a == None:
    a = 'NULL'
  else:
    try:
      a = a.replace( "'" , "''")
      a = "'" + a + "'" 
    except:
      a = str(a) 
  return a 

def convert( q , t2 , cs2 ):
  run_sql( connection2 , "begin" ) 
  run_sql( connection2 , "delete from " + t2 )
  print q 
  rows = run_sql( connection , q )
  for row in rows:
    row = [ foo( a ) for a in row ] 
    q = 'insert into ' + t2 + '(' + ",".join(cs2) + ') values ( ' + ",".join( row ) + ' ) '
    run_sql( connection2 , q  ) 
  run_sql( connection2 , 'commit' ) 

convert( 'select orgid,commonname,speciesname from organism' , 't_organism' , [ 'id' , 'f_name' , 'f_common_name' ] )
setter( 't_organism_id_seq' , 't_organism' )

convert( 'select projectid,projectname,projectpath,projectdescription,organismid from project' , 't_project' , [ 'id' , 'f_name' , 'f_path' , 'f_description' , 'f_organism' ] )
setter( 't_project_id_seq' , 't_project' )


convert( 'select id,name,cistrack_id,sampleid,projectid,agent  from experiment_unit' , 't_experiment_unit' , [ 'id' , 'f_name' , 'f_bionimbus_id' , 'f_sample' , 'f_project' , 'f_agent' ] )
#run_sql( connection2 , 'update t_experiment_unit set f_agent = ( select id from t_agent where f_name = f_agent_text_tmp )' )
ids = run_sql( connection , "select id from experiment_unit join users_for_supergroup on supergroup_id = supergroup where username = 'guest'" )
for id in ids:
  id = id[ 0 ] 
  q = "update t_experiment_unit set f_is_public = 'T' where id = %d" % id 
  run_sql( connection2 , q ) 
run_sql( connection2 , "SELECT setval('t_experiment_unit_id_seq', (SELECT MAX(id) FROM t_experiment_unit)+1)" )
run_sql( connection2 , "delete from t_keys" )
keys = run_sql( connection2 , "select f_bionimbus_id from t_experiment_unit" )
for key in keys:
 try:
  key = key[ 0 ] 
  print key 
  y,i = key.split( '-' )
  y,i = int(y) , int(i)
  run_sql( connection2 , "insert into t_keys(f_year,f_index) values(%d,%d)" % ( y , i ) ) 
 except:
  pass

convert( 'select datafileid,cistrack_id,path,size from data_digest' , 't_file' , [ 'id' , 'f_bionimbus_id' , 'f_path' , 'f_size' ] )

ip = run_sql( connection2 , "select id , f_path from t_file" )
for (id,path) in ip:
  run_sql( connection2 , "update t_file set f_filename = '%s' where id = %d" % ( path.split( '/' )[ -1 ] , id ) )

#convert( "select userid, username,password,lastlogintime,is_superuser, firstname || ' ' || lastname , address , email , phone from login join personnel on login.userid = personnel.personnelid" , 't_users' , 
#               [ 'id' , 'f_username' , 'f_password' , 'f_lastlogin' , 'f_superuser' , 'f_name' , 'f_address' , 'f_email' , 'f_phone'] )
