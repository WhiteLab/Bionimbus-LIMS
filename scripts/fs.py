import os

def run( str ):
  print str
  os.popen( str ).readlines()

def PAL( p_name , is_pub , really_at , fn ):
  p_name = '/XRaid/share/' + p_name.replace( ' ' , '_' ) + '/' + fn
  p_path = p_name.split( '/' )
  p_path = p_path[ : -1 ]
  p_path = '/'.join( p_path )
  if not file.exists( p_path ):
    cmd = 'mkdir -p ' + p_path
    run( cmd  )
  if not file.exists( p_name ):
    cmd = 'ln ' + really_at + ' ' + p_name
    run( cmd )

rows = db( ( db.t_project.id == db.t_experiment_unit.f_project ) &
           ( db.t_experiment_unit.f_bionimbus_id == db.t_file.f_bionimbus_id ) ).select()

for row in rows:
  PAL( row[ db.t_project.f_name ] , row[ db.t_experiment_unit.f_is_public  ] , 
                                       row[ db.t_file.f_newpath ] , row[ db.t_file.f_filename ] )
