# -*- coding: utf-8 -*-
### required - do no delete

import os
import xlrd

from applications.Bionimbus.modules.permissions import is_user_admin

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
             ]
    editable = is_user_admin( db , auth )
    form = SQLFORM.grid( db.t_project,fields = fields , 
                         #links = project_links , 
                         editable = editable , 
                         create = editable , 
                         onupdate = auth.archive , 
                         deletable = False)
    return locals()

@auth.requires_login()
def user_project_manage():
    arg = request.args( 0 )

    print "\n\n**Request:\n" , request , "\n\n"

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
                         fields    = fields )
    return locals()

