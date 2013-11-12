

from xml.dom import minidom


def get( part , key ):
  "Given an XML node, take the content ( stuff between the tags ) and concaenate the parts into a string"
  buf = ''
  segs = part.getElementsByTagName(key)
  for seg in segs:
   try:
    #get the actual text content of the node
    snv = seg.childNodes[0].nodeValue
    if snv <> None:
      buf = buf + snv
   except:
    #Could be an exception in some cases, but in that case, not adding the string is fine 
    pass
  return buf

#open the cghub XML
xmldoc = minidom.parse( 'cghub.xml' )

#get the results section, which is almost the whole document
itemlist = xmldoc.getElementsByTagName('Result')

print "there are" , len(itemlist) , "results" 
base = 1  # we use this for computing id's in a sequence for testing.  
          # TODO: call the real key gen service 

for item in itemlist:
  print '------------------------------------------'
  d = {} #a hash of the fields of the genome
  for cg in cg_fields_def:
    #get the names 
    fullname = cg[ 0 ]
    name = fullname[ 2: ] 
    d[ fullname ] = get( item , name )
  #print d 
  d[ 'f_library_type' ] = 5 
  #todo: undo this hardcoding, look up the library type

  bn_id = '2013-C' + str( base )
  #todo: call key service 

  d[ 'f_bionimbus_id' ] = bn_id
  base = base + 1 

  #create the experiment
  db.t_experiment_unit.insert( **d )

  #there are one or more files associated with the genome.  Loop through them an insert them in the file table
  #todo: check the file size and cheksum, if they are present
  files = item.getElementsByTagName('file')
  for file in files:
    fn = get( file , 'filename' )
    fs = get( file , 'filesize' )
    cs = get( file , 'checksum' )
    db.t_file.insert( f_bionimbus_id = bn_id , f_filename = fn , f_size = int(fs) )
      

