

#def publish():
#  paths = run_sql( "select * from Cloud_Deployment where synced='n'" )
#
#  for path in paths:
#    (id,from_path,to_path) = path[ :3 ]
#    linkey = "/glusterfs" + from_path 
#    os.popen( "mkdir -p " + to_path ).readlines()
#
#    if os.path.exists( linkey ):
#      cmd = "ln -s '" + linkey + "'  '" + to_path + "'"
#    else:
#      cmd = "cp '" + from_path + "' '" + to_path + "'"
#    print cmd 
#    os.popen( cmd ).readlines()
#    run_sql( "update Cloud_Deployment set synced='y' where id = " + str( id  ) )
#
#publish()

import os

cp = db.t_cloud_push 

rows = db( cp.f_synced == 'n' ).select()
for r in rows:
  (id,f,t) = r[ cp.id ] , r[ cp.f_from ] , r[ cp.f_to ]  
  cmd = "rsync '" + f + "' '" + t + "'"
  print cmd 
  os.popen( cmd , "r" ).readlines()
  db( cp.id == id ).update( f_synced = 'y' )
