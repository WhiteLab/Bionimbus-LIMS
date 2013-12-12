

import os
import json

tool = """{
              "username": "USER",
              "protocol": "ssh",
              "filepath": "PATH",
              "tenant_name": "USER",
              "type" : "TYPE" , 
              "acl": [{
                  "grantee": {
                      "type": "username",
                      "id": "USER"
                  },
                  "permission": "full_control"
              },
              {
                  "grantee": {
                      "type": "tenant_name",
                      "id": "USER"
                  },
                  "permission": "full_control"
              }],
              "cloud_name": "sullivan",
              "metadata_server": ""}"""

def get_path_for_id( id ):
  inf = os.popen( "curl http://172.16.1.76:8774/ids/v0/%s" % id ).readlines()
  h = json.loads( inf[ 0 ] )
  return h

