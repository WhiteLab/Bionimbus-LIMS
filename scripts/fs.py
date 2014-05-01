import os


##########
#
# route files to the right cloud directory
#
##########

#
# TODO: erase files that are there that should not be.
# the main use case for this is files going away because permissions have changed
#

def run( str ):
  os.popen( str ).readlines()

def PAL( id , p_name , is_pub , really_at , fn , cloud ):
  if fn == None:
    fn = really_at.split( '/' )
    fn = fn[ -1 ]
    db( db.t_file.id == id ).update( f_filename = fn )
  goesto = cloud
  p_name = ( '%s/%s/' % ( settings.data_target , goesto ) ) + p_name.replace( ' ' , '_' ) + '/' + fn
  p_path = p_name.split( '/' )
  p_path = p_path[ : -1 ]
  p_path = '/'.join( p_path )
  if not os.path.exists( p_path ):
    cmd = 'mkdir -p ' + p_path
    run( cmd  )
  print really_at , p_name 
  if not os.path.exists( p_name ):
    cmd = 'ln ' + really_at + ' ' + p_name
    run( cmd )

rows = db( ( db.t_project.id                     == db.t_experiment_unit.f_project ) &
           ( db.t_project.f_cloud                == db.t_cloud.id ) & 
           ( db.t_experiment_unit.f_bionimbus_id == db.t_file.f_bionimbus_id ) ).select( )

for row in rows:
  PAL( row[ db.t_file.id ] , 
                                       row[ db.t_project.f_name ] , row[ db.t_experiment_unit.f_is_public  ] , 
                                       row[ db.t_file.f_newpath ] , row[ db.t_file.f_filename ] , row[ db.t_cloud.f_folder ] )
