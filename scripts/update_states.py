import sys
import os

####
# 
# look for states in the updated states table that are newer than the newst state
# in the unit table. Copy those over. 
#
####

newest_eu_state = db.t_experiment_unit.f_sample_state_changed.max()
after_this = db().select( newest_eu_state ).first()[ newest_eu_state ]

ss = db.t_sample_state

if after_this == None:
  res = db( ss ).select( orderby = ss.f_updated )
else:
  res = db( ss.f_updated > after_this ).select( orderby = ss.f_updated )

for r in res:
  (key,state,time) = r[ ss.f_bionimbus_id ] , r[ ss.f_state ] , r[ ss.f_updated ]  
  db( db.t_experiment_unit.f_bionimbus_id == key ).update( f_sample_state = state , f_sample_state_changed = time )

#files = db(db.t_file.f_size == None ).select()
#for f in files:
# try:
#  rpath = os.path.realpath(f.f_newpath)
#  size = os.path.getsize( rpath )
#  db( db.t_file.id == f.id ).update( f_size = size )
#  print "Set" , rpath , "to size" , size 
# except:
#  print rpath, "is missing" 
