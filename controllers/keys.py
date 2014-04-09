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

sheets = [
  'rnaseq' ,
  'dswg2' ,
  'dswg' ,
  'cs' ]

@service.xmlrpc
def generate_key(  ):
    now = datetime.datetime.now()
    year = now.year
    iters = 0
    bn_id = None
    print "in keygen"
    while (iters < 10) & (bn_id == None):
        print "**"
        max = db.t_keys.f_index.max()
        maxid = db(db.t_keys.f_year == year ).select(max).first()[ max ]
        if maxid == None:
            maxid = 1
        else:
            maxid = maxid + 1
        try:
            bn_id = "%d-%d" % ( year , maxid )
            print "trying to insert" , bn_id
            db.t_keys.insert( f_year = year , f_index = maxid )
            db.commit()
        except:
            print "exception!"
            traceback.print_exc(file=sys.stdout)
            iters = iters + 1
            bn_id = None
    print "returning" , bn_id
    return bn_id

def key_to_id( key ):
    y,i = key.split( '-' )
    y,i = int(y) , int(i)
    print "y,i" , y , i
    id = db( ( db.t_keys.f_year == y )  & ( db.t_keys.f_index == i ) ).select()
    print "result of ID query"
    id = id[ 0 ]
    id = id[ 'id' ]
    return id

@service.xmlrpc
def add_metadata_to_key( key , kv_pairs ):
    id = key_to_id( key )
    for k,v in kv_pairs:
        db.t_key_metadata.insert( f_key = id , f_metadata_key = k , f_value = v )

@service.xmlrpc
def metadata_for_key( key ):
    id = key_to_id( key )
    kvp = db( db.t_key_metadata.f_key == id ).select()
    res = []
    for kv in kvp:
        res.append( ( kv[ 'f_metadata_key' ] , kv[ 'f_value' ] ) )
    return res

@service.xmlrpc
def does_key_exist( key ):
    try:
        id = key_to_id( key )
        return True
    except:
        return False



rpc_return_fields = [ db.t_experiment_unit.f_bionimbus_id ,
                      db.auth_user.first_name ,
                      db.auth_user.last_name ,
                      db.t_experiment_unit.created_on ,
                      db.t_library_type.f_name ,
                      db.t_project.f_name
]

def flatify( re ):
    l = []
    for r in re:
        l.append( [ r[f] for f in rpc_return_fields ] )
    l.reverse()
    return l

@service.xmlrpc
def recent_keys( count ):
    re = db( ( db.t_experiment_unit.created_by == db.auth_user.id ) &
            ( db.t_experiment_unit.f_library_type == db.t_library_type.id ) &
            ( db.t_experiment_unit.f_project == db.t_project.id ) ).select( *rpc_return_fields ,
                                                                            orderby = ~db.t_experiment_unit.id ,
                                                                            limitby = ( 0 , count ) )
    return flatify( re )

@service.xmlrpc
def keys_after_date( adate ): 
    re = db( ( db.t_experiment_unit.created_by == db.auth_user.id ) &
            ( db.t_experiment_unit.f_library_type == db.t_library_type.id ) &
            ( db.t_experiment_unit.f_project == db.t_project.id ) &
            ( db.t_experiment_unit.created_on > adate ) ).select( *rpc_return_fields ,
                                                                            orderby = ~db.t_experiment_unit.id 
                                                                            #limitby = ( 0 , count ) 
                                                                )
    return flatify( re )

def call():
    return service()
