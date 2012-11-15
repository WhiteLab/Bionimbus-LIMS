

def experiment_project_join( db ):
  return db.t_user_project.on( db.t_user_project.f_project_id == db.t_experiment_unit.f_project )



def is_user_admin( db , auth ):
  rows = db( 
          ( db.auth_user.id       == auth.user_id) & 
          ( db.auth_user.is_admin == True ) 
    ).select()
  return len( rows ) > 0



def get_experiment_visibility_query( db , auth ):
  if is_user_admin( db , auth ):
    evq = db.t_experiment_unit.id > -1
  else:
    evq =  ( ( db.t_experiment_unit.f_is_public == True ) |
             ( db.t_user_project.f_user_id    == auth.user_id ) )
  return evq


def can_user_access_bionimbus_id( bn_id , db , auth ):
  q = ( db.t_experiment_unit.f_bionimbus_id == bn_id ) & get_experiment_visibility_query( db , auth )
  r = db(q).select( db.t_experiment_unit.ALL , left = experiment_project_join( db ) )
  return len(r) != 0


def can_user_access_group( user , group ):
  q = ( db.t_experiment_unit.f_bionimbus_id == group ) & get_experiment_visibility_query( db , auth )
  r = db(q).select( db.t_experiment_unit.ALL , left = experiment_project_join( db ) )
  return len(r) != 0

