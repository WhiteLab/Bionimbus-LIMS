
def sendMailTo( db , me , subject , content , list = None , project = None ):

  addys = []
  if list <> None:
    a2 = db( ( db.auth_user.id == db.t_mail_list.f_user ) & ( db.t_mail_list.f_list == list ) ).select( db.auth_user.email )
    for a in a2:
      a = a[ db.auth_user.email ]
      addys.append( a )

  if project <> None:
    a2 = db( ( db.auth_user.id == db.t_user_project.f_user_id ) & ( db.t_user_project.f_project_id == project ) ).select( db.auth_user.email )
    for a in a2:
      addys.append( a[ db.auth_user.email ] )

  import smtplib
  from email.mime.text import MIMEText

  msg = MIMEText( content )
  msg[ 'Subject' ] = subject
  msg[ 'From'    ] = me
  msg[ 'To'      ] = ",".join( addys )

  server = smtplib.SMTP( '127.0.0.1' )
  server.sendmail( me , addys , msg.as_string() )

