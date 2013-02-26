
from gluon.html import OPTION


def nameval_to_options( namevals ):
  options = [ OPTION( "" , _value = "" ) ]
  for name , val in namevals:
    options.append( OPTION( name , _value = val ) )
  return options

def print_form_structure( form ):
  for f1i in range(len(form)):
    f1 = form[ f1i ]
    print "f1"
    for f2i in range(len(f1)):
      f2 = f1[ f2i ]
      print "f2"
      for f3i in range( len( f2 ) ):
        f3 = f2[ f3i ]
        print "f3"
        for f4i in range( len( f3 ) ):
          f4 = f3[ f4i ]
          print f1i , f2i , f3i , f4i , f4


