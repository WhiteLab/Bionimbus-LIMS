# -*- coding: utf-8 -*-
### required - do no delete

import os
import xlrd

from applications.Bionimbus.modules.permissions import is_user_admin
from applications.Bionimbus.modules.gui         import nameval_to_options

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
def project_manage():
    fields = [
             db.t_project.f_name 
           , db.t_project.f_organism 
           , db.t_project.f_pi  
           , db.t_project.f_public
           , db.t_project.f_cloud
             ]
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_project,fields = fields , 
                         #links = project_links , 
                         editable = editable , 
                         create = editable , 
                         onupdate = auth.archive , 
                         paginate = 1000 , 
                         maxtextlength = 150,
                         deletable = False)
    return locals()


@auth.requires_login()
def subproject_manage():
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_subproject.id <> 1 ,
                         editable = editable ,
                         create = editable ,
                         deletable = False)
    return locals()


def names_for_users():
  a = db.auth_user
  ifn = db( a ) .select()
  return [ ( row[ a.first_name ] + ' ' + row[ a.last_name ] , row[ a.id ] ) for row in ifn ]


@auth.requires_login()
def user_project_manage():
    arg = request.args( 0 )

    fields = [
             db.t_user_project.f_project_id
           , db.t_user_project.f_user_id
           , db.t_user_project.f_admin
             ]
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_user_project ,
                         create    = editable ,
                         editable  = editable ,
                         deletable = editable ,
                         paginate = 1000 ,
                         maxtextlength = 150,
                         fields    = fields )

    if arg == 'new':
      nfu = names_for_users()
      options = nameval_to_options( nfu )     
      form[1][0][1][1] = TD( SELECT( *options ,  _class="generic-widget" , _id="t_user_project_f_user_id" , _name="f_user_id" ) )
   
    return locals()

