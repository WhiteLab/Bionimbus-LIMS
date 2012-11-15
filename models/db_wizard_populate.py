from gluon.contrib.populate import populate
#if db(db.auth_user).isempty():
#     populate(db.auth_user,10)
#     populate(db.t_sample,10)
#     populate(db.t_users,10)
#     populate(db.t_agent,10)
#     populate(db.t_organism,10)
#     populate(db.t_project,10)
#     populate(db.t_file,10)
#     populate(db.t_experiment_unit,10)

if db(db.t_platform).isempty():
      db.t_platform.insert( f_name = '454' )
      db.t_platform.insert( f_name = 'Illumina-HiSeq' )
      #db.t_platform.insert( f_name = 'Illumina-MiSeq' )
     
