# -*- coding: utf-8 -*-
### required - do no delete

import os
import xlrd
import datetime
import traceback
import sys

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

service = Service()

# return a list of possible states, 
# then a list of the states of the keys 
@service.xmlrpc
def get_states( keys ):
    ssl = db.t_sample_state_list
    states = db( ssl ).select( ssl.id , ssl.f_name )
    sl = []
    for s in states:
      sl.append( ( s[ ssl.id ] , s[ ssl.f_name ] ) )

    ksl = []
    ss = db.t_sample_state
    for key in keys:
      sl = []
      states = db( ss.f_bionimbus_id == key ).select()
      for s in states:
        sl.append( [ s[ ss.f_bionimbus_id ] , s[ ss.f_state ] , s[ ss.f_updated ] ] )
      ksl.append( sl ) 
    return sl #,ksl
 
# add to states
@service.xmlrpc
def set_states( keys_and_states ):
  now = datetime.datetime.now()
  for key,state in keys_and_states:
    db.t_sample_state.insert( f_bionimbus_id = key , f_state = state , f_updated = now )

def call():
    return service()
