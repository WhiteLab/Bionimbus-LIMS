

from xml.dom import minidom


def get( part , key ):
  buf = ''
  segs = part.getElementsByTagName(key)
  for seg in segs:
   try:
    snv = seg.childNodes[0].nodeValue
    if snv <> None:
      buf = buf + snv
   except:
    pass
  return buf

xmldoc = minidom.parse( 'cghub.xml' )
itemlist = xmldoc.getElementsByTagName('Result')
print "there are" , len(itemlist) , "results" 
base = 1
for item in itemlist:
  print '------------------------------------------'
  d = {}
  for cg in cg_fields_def:
    fullname = cg[ 0 ]
    name = fullname[ 2: ] 
    d[ fullname ] = get( item , name )
  print d 
  d[ 'f_library_type' ] = 5 
  bn_id = '2013-C' + str( base )
  d[ 'f_bionimbus_id' ] = bn_id
  base = base + 1 
  db.t_experiment_unit.insert( **d )

  files = item.getElementsByTagName('file')
  for file in files:
    fn = get( file , 'filename' )
    fs = get( file , 'filesize' )
    cs = get( file , 'checksum' )
    db.t_file.insert( f_bionimbus_id = bn_id , f_filename = fn , f_size = int(fs) )
      

