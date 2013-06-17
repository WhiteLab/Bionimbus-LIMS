#!/usr/bin/env python

import ConfigParser
import os, sys

config = ConfigParser.RawConfigParser()
config.read('dropbox.config')

dist = config.get( 'main' , 'dist' )
api_key = config.get( 'main' , 'api_key' )
api_url = config.get( 'main' , 'api_url' )

sys.path.append( dist )
sys.path.insert( 0, os.path.dirname( __file__ ) )

from common import submit

try:
    data = {}
    data[ 'name' ] = sys.argv[1]
except IndexError:
    print 'usage: %s key url name [description] [synopsys]' % os.path.basename( sys.argv[0] )
    sys.exit( 1 )
try:
    data[ 'description' ] = sys.argv[4]
    data[ 'synopsis' ] = sys.argv[5]
except IndexError:
    pass

url = api_url + '/libraries'
print api_key
print url
submit( api_key , url , data , return_formatted = False)
