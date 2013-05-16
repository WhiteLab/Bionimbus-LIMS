import sys
import os

from applications.Bionimbus.modules.file_location import generate_name

def run( str ):
  print str
  os.popen( str ).readlines()

for ss in db( db.t_keygen_spreadsheets ).select():
  if ss.f_added_to_tracking_sheet <> True:
    args = [] 
    sheet_id = ss.id
    print "sheet id" , sheet_id
    ids = db( ( db.t_experiment_unit.f_spreadsheet == sheet_id ) 
              & ( db.t_project.id == db.t_experiment_unit.f_project ) 
            ).select()
    for id in ids:
      args.append( id[ db.t_experiment_unit.f_bionimbus_id ] )
      args.append( id[ db.t_project.f_name ] )
    if len( args ) > 0:
      arg = " ".join( args )
      os.popen( "~/write_ids_to_tracking_sheet.pl " + arg ).readlines()
    db( db.t_keygen_spreadsheets.id == sheet_id ).update( f_added_to_tracking_sheet = True )
