import os 

def generate_name( i , bn_id , fn ):
  newpath = '/XRaid/bionimbus'
  ( year , index ) = bn_id.split( '-' )
  index = str( i ) 
  newpath += '/' + year
  while len( index ) > 0:
    l = min( len( index ) , 2 )
    ( first , rest ) = index[ :l ] , index[ l: ]
    newpath += '/' + first
    index = rest
  return newpath , newpath + "/" + fn

