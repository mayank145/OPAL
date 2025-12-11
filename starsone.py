#! /usr/local/python


#! /usr/bin/python

import os
import sys
import datetime
import dbconnect
import cgi
import cgitb; cgitb.enable();
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import http.cookies as Cookie
import shelve
#import logproc
import logproc3 as logproc
import random

method=os.environ.get("REQUEST_METHOD","")

field = cgi.FieldStorage()

dbconn=dbconnect.opalconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor2.execute("set autocommit = 1")
cursor3=db.cursor()

def getGroups ( starsuser ) :

	from ldap3 import Server, Connection, ALL

#	s = Server( host='squery.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	s = Server( host='sreg6.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	
	conn = Connection(s, auto_bind=True)
#conn.search('memberuid=winegar,ou=Group,dc=subaru,dc=nao,dc=ac,dc=jp', '(objectClass=*)' , 'SUBTREE', attributes=['dn'] )
	conn.search('ou=Group,dc=stars,dc=nao,dc=ac,dc=jp', '(memberuid=' +  starsuser + ')' , 'SUBTREE', attributes=['cn'] )

	groups = []

	for entry in conn.entries :
	
		group = str( entry['cn'] )
		groups.append ( group )
	
	maintext = '<table cellpadding=3 cellspacing=4><tr><th colspan=4 bgcolor=lime>STARS LDAP assigned GROUPS ( %s )</th></tr>' % ( len( groups ) ) 

	if len( groups ) > 0 :
	
		seq = 0
	
		for group in groups :
		
			seq += 1
	
#			memberuid, gecos, mail = getGecos( member )
			
			maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, group, group, group )

	else :
		
		maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( '0', 'none', 'none', 'none' )

	maintext += '</table>'
	
	return ( maintext )

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px; font-weight: bold }"
	css_text += "</style>"


	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

#def main() :

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')


if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

if 'first' in field :

	first = field['first'].value
	
else:
	
	first = 'none'

if 'last' in field :

	last = field['last'].value
	
else:
	
	last = '0'
	
if 'name2' in field :

	name2 = field['name2'].value

else:

	name2 = ''


if 'altname' in field :

	altname = field['altname'].value

else:

	altname = ''

if 'email' in field :

	email = field['email'].value
	
else:
	
	email = ''

if 'gid' in field :

	gid = field['gid'].value
	
else:
	
	gid = ''

if 'privy' in field :

	privy = field['privy'].value
	
else:
	
	privy = 'none'

if 'comment' in field :

	comment = field['comment'].value

else:

	comment = 'none'

if logproc.validCookie() :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )

	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar', 'koshida', 'moritani' )
#	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar' )
#	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar' )
	
	reserveAdmin = False 
		
	if username in admin_users :
	
		reserveAdmin = True 

	updateComment = 'No Update'
	
	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :
		
		
		if reserveAdmin == True :
		
			cursor2.execute("update users set first = '%s', last = '%s', username = '%s', altname = '%s', groupid = '%s', privy = '%s', email='%s', comment='%s' \
			where idno = '%s'" \
			% ( first, last, name2, altname, gid, privy, email, comment, idno ) )

#		else :

#			cursor2.execute("update users set hourin='%s', hourout='%s', destiny='%s', shifttype='%s', shiftdest where idno = '%s'" \
#			% ( hourin, hourout, destiny, car, idno ) )

			updateComment = 'Updated OK'

	if method == 'GET' and int( idno ) == 0 :
		
#		cursor2.execute("insert into users ( user, email, stnuser, privy, train, status, hourin, hourout, destiny, shiftin, shiftcar, shifttype, shiftdest ) values \
#		( 'newuser', 'newemail', 'newstn', 'user', 'P', 'Active', '08', '16', 'BHSB' )" )

		cursor2.execute("select number from counter where file = '%s'" % ( 'users' ) )
		numrows2 = cursor2.rowcount
		counted = cursor2.fetchone()
		newid = counted[0]
		nextid = int( newid ) + 1
		cursor2.execute("update counter set number = '%s' where file = '%s'" % ( nextid, 'users' ) )
#		letters = ( 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' )
		letters = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz'

		newpw = ''
		for i in random.sample( letters , 12 ) :
			newpw += i


#		newpw='abc'

		cursor2.execute("insert into users ( idno, first, last, username, altname, groupid, email, datein, pw, comment ) values \
		( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
		% ( newid, 'newFirst', 'newLast', 'newUsername', '', '', 'newEmail', today, newpw, '' ) )

#		idno2 = cursor2.lastrowid
		idno = newid
	
	
	pagename = '<center><b>STARS User Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'
	
#	cursor.execute("select user, email, stnuser, idno, privy, train, status from users where idno = %s") % ( idnoNum )

#	cursor.execute("select user from users where idno = '%s'") % ( idnoNum ) 
#	cursor.execute("select user, email, stnuser, idno, privy, train, status from users where user='winegar'") 
#	idno=2494
#	if idno=='0' :
	cursor.execute("select idno, first, last, username, altname, groupid, privy, datein, email, pw, comment from users where idno = '%s'" % ( idno ) ) 
#	cursor.execute("select user, email, stnuser, idno, privy, train, status from users where user = '%s'") % ( 'winegar' )

	numrows = cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'+ updateComment
#	maintext += '<table cellpadding=3 cellspacing=3>'

	test = False
#	if False :
#	if test == True:
	if numrows == 1 :
	
		row = cursor.fetchone()

		user_idno = row[0]
		user_first = row[1]
		
		user_last = row[2]
		user_username = row[3]
		
		user_altname = row[4]
		user_groupid = row[5]
		
		user_privy = row[6]
		user_datein = row[7]
		user_email = row[8]
		
#		user_pw = row[9]
		user_pw = 'thinCigar' + str( idno )
		user_comment = row[10]

				
		safeGets = ( 'Save', 'Cancel' )

#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

		if method == 'GET' or ( method == 'POST' and field['action'].value in safeGets ) :
			
			maintext += "<form method=post action='starsone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( user_idno )
			maintext += '<b>STARS User Display</b><br>'
			
			maintext += '<table cellpadding=3 cellspacing=3><td valign=top>'
			
			
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( user_idno ) 
			maintext += "<tr><td class=right>First:</td><td>%s</td></tr>" % ( user_first ) 
			maintext += "<tr><td class=right>Last:</td><td>%s </td></tr>" % ( user_last ) 
			maintext += "<tr><td class=right>STARS Username:</td><td><FONT SIZE=+1><b>%s</b></FONT></td></tr>" % ( user_username ) 
			maintext += "<tr><td class=right>STN Username:</td><td>%s</td></tr>" % ( user_altname ) 
			maintext += "<tr><td class=right>Email:</td><td>%s</td></tr>" % ( user_email ) 
			maintext += "<tr><td class=right>GroupID:</td><td>%s</td></tr>" % ( user_groupid ) 
			maintext += "<tr><td class=right>Privilege:</td><td>%s</td></tr>" % ( user_privy ) 
			maintext += "<tr><td class=right>DateIn:</td><td>%s</td></tr>" % ( user_datein ) 
			maintext += "<tr><td class=right>1st PW:</td><td>%s</td></tr>" % ( user_pw ) 
			maintext += "<tr><td class=right>Comment:</td><td>%s</td></tr>" % ( user_comment ) 
			
			if reserveAdmin == True :

				maintext += "<tr><td colspan=2 class=center><a href=propone.py?idno=0&uid=%s>Make New PropID for PI - %s</a></td></tr>" \
				% ( user_idno, user_username + ' - ' + user_first + ' ' + user_last  ) 

				maintext += "<tr><td colspan=2>STAUtRegistUser -a -u 00000 -c '%s %s' -M %s -p %s -G %s %s</td></tr>" \
				% ( user_first, user_last, user_email, user_pw, user_groupid, user_username ) 
			
			maintext += "</table>"
			maintext += "</td><td valign=top><FONT SIZE=+1>LDAP Groups - <b>%s</b></FONT><br>" % ( user_username )
			maintext += getGroups ( user_username )
			maintext += "</tablw>"
			
		else:
			
			privy1 = ( 'none', 'admin', 'subaru' )
			
			privyCtrl = '<select size=1 name=privy>'
			
			for privy2 in privy1 :
				
				if user_privy == privy2 :
					
					privyCtrl += '<option value=%s selected>%s' % ( privy2, privy2 )
				
				else:
					
					privyCtrl += '<option value=%s>%s' % ( privy2, privy2 )
			
			privyCtrl += '</select>'
			
			maintext += "<form method=post action='starsone.py?idno=%s'><input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>" \
			% ( user_idno )

			maintext += '<b>STARS User Edit</b><br>'
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( user_idno  ) 
			maintext += "<tr><td class=right>First:</td><td><input type=text name=first size=40 value='%s'></td></tr>" % ( user_first  ) 
			maintext += "<tr><td class=right>Last:</td><td><input type=text name=last size=40 value='%s'></td></tr>" % ( user_last ) 
			maintext += "<tr><td class=right>STARS Username</td><td><input type=text name=name2 size=20 value='%s'></td></tr>" % ( user_username  ) 
			maintext += "<tr><td class=right>STN Alt UserName</td><td><input type=text name=altname size=20 value='%s'></td></tr>" % ( user_altname ) 
			maintext += "<tr><td class=right>Email</td><td><input type=text name=email size=40 value='%s'></td></tr>" % ( user_email  ) 
			maintext += "<tr><td class=right>1st SemID:</td><td><input type=text name=gid size=20 value='%s'></td></tr>" % ( user_groupid ) 
			maintext += "<tr><td class=right>Privilege:</td><td>%s | none admin user</td></tr>" % ( privyCtrl ) 
			maintext += "<tr><td class=right>Comment:</td><td><input type=text name=comment size=20 value='%s'></td></tr>" % ( user_comment ) 

			maintext += "</table>"
			maintext += "</form>"
		
	else:
		
		maintext+="No user for IDNO: " + str( idno ) + "<br>"

else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )

