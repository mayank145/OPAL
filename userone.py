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

method=os.environ.get("REQUEST_METHOD","")

field = cgi.FieldStorage()

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor2.execute("set autocommit = 1")
cursor3=db.cursor()

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


if 'user' in field :

	user = field['user'].value
	
else:
	
	user = 'none'

if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

if 'email' in field :

	email = field['email'].value
	
else:
	
	email = ''

if 'stnuser' in field :

	stnuser = field['stnuser'].value
	
else:
	
	stnuser = ''

if 'privy' in field :

	privy = field['privy'].value
	
else:
	
	privy = 'none'

if 'train' in field :

	train = field['train'].value
	
else:
	
	train = 'P'


if 'status' in field :

	status = field['status'].value
	
else:
	
	status = 'Active'

if 'hourin' in field :

	hourin = field['hourin'].value
	
else:
	
	hourin = '18'  
	      
if 'hourout' in field :

	hourout = field['hourout'].value
	
else:
	
	hourout = '08'  

if 'destiny' in field :

	destiny = field['destiny'].value

else:

	destiny = 'BHSB'  

if 'car' in field :

	car = field['car'].value

else:

	car = 'J-01' 
#if logproc.validCookie() :
if 'shifttype' in field :

	shifttype = field['shifttype'].value

else:

	shifttype = 'Daytime' 

shifttype = shifttype.strip()

if 'shiftdest' in field :

	shiftdest = field['shiftdest'].value

else:

	shiftdest = 'BaseSum_Days-All'

if logproc.validCookie() :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )

	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar' )
#	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar' )
	
	reserveAdmin = False 
		
	if username in admin_users :
	
		reserveAdmin = True 

	updateComment = 'No Update'
	
	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :
		
		idno=idno.strip()
		user=user.strip()
		email=email.strip()
		stnuser=stnuser.strip()
		privy=privy.strip()
		train=train.strip()
		status=status.strip()
		car=car.strip()
		hourin=hourin.strip()
		if len( hourin ) == 1 :
			hourin = '0'+ hourin			
		hourout=hourout.strip()
		if len( hourout ) == 1 :
			hourout = '0'+ hourout			
		destiny=destiny.strip()
		shifttype=shifttype.strip()
		shiftdest=shiftdest.strip()
		
		if reserveAdmin == True :
		
			cursor2.execute("update users set user = '%s', email = '%s', stnuser = '%s', privy = '%s', train = '%s', status = '%s', hourin='%s', hourout='%s', \
			destiny='%s', shiftcar='%s', shifttype='%s', shiftdest='%s' where idno = '%s'" \
			% ( user, email, stnuser, privy, train, status, hourin, hourout, destiny, car, shifttype, shiftdest, idno ) )

		else :

			cursor2.execute("update users set hourin='%s', hourout='%s', destiny='%s', shifttype='%s', shiftdest where idno = '%s'" \
			% ( hourin, hourout, destiny, car, idno ) )

		updateComment = 'Updated OK'

	if method == 'GET' and int( idno ) == 0 and status == 'New' :
		
#		cursor2.execute("insert into users ( user, email, stnuser, privy, train, status, hourin, hourout, destiny, shiftin, shiftcar, shifttype, shiftdest ) values \
#		( 'newuser', 'newemail', 'newstn', 'user', 'P', 'Active', '08', '16', 'BHSB' )" )
		cursor2.execute("insert into users ( user, email, stnuser, privy, train, status, hourin, hourout, destiny, shiftin, shiftcar, shifttype, shiftdest ) values \
		( 'newuser', 'newemail', 'newstn', 'user', 'P', 'Active', '08', '16', 'BHSB', '2020-01-01', 'J-01', 'Daytime', 'BaseSum-Days_All' )" )

		idno = cursor2.lastrowid
		idno = str( idno )
	
	
	pagename = '<center><b>User Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'
	
	idnoNum = int( idno )
#	cursor.execute("select user, email, stnuser, idno, privy, train, status from users where idno = %s") % ( idnoNum )

#	cursor.execute("select user from users where idno = '%s'") % ( idnoNum ) 
#	cursor.execute("select user, email, stnuser, idno, privy, train, status from users where user='winegar'") 
	cursor.execute("select user, email, stnuser, idno, privy, train, status, hourin, hourout, destiny, shiftin, shiftcar, shifttype, shiftdest \
	 from users where idno = '%s'" % ( idno ) ) 
#	cursor.execute("select user, email, stnuser, idno, privy, train, status from users where user = '%s'") % ( 'winegar' )

	numrows = cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'+ updateComment
#	maintext += '<table cellpadding=3 cellspacing=3>'

	test = False

#	if test == True:
	if numrows == 1 :
	
		row = cursor.fetchone()

		users_user = row[0]
		users_user = users_user.strip()
		
		users_email = row[1]
		users_email = users_email.strip()
		
		users_stnuser = row[2]
		users_stnuser = users_stnuser.strip()
		
		users_idno = str( row[3] )
		users_idno = users_idno.strip()
		
		users_privy = row[4]
		users_privy = users_privy.strip()
		
		users_train = row[5]
		users_train = users_train.strip()
		
		users_status = row[6]
		users_status = users_status.strip()

		users_hourin = row[7]
		users_hourout = row[8]

		users_destiny = row[9]

		users_shiftin = row[10]
		users_shiftcar = row[11]
		users_shifttype = row[12]
		users_shiftdest = row[13]
		

#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' ) ) :
			
			maintext += "<form method=post action='userone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( users_idno )
			
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>User:</td><td>%s</td></tr>" % ( users_user ) 
			maintext += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( users_idno ) 
			maintext += "<tr><td class=right>Email:</td><td>%s</td></tr>" % ( users_email ) 
			maintext += "<tr><td class=right>STN-User:</td><td>%s </td></tr>" % ( users_stnuser ) 
			maintext += "<tr><td class=right>Privy:</td><td>%s </td></tr>" % ( users_privy ) 
			maintext += "<tr><td class=right>Summit Training:</td><td>%s | Passenger Driver-Summit Base None</td></tr>" % ( users_train ) 
			maintext += "<tr><td class=right>Status:</td><td>%s | Active Removed Temporary</td></tr>" % ( users_status ) 
			maintext += "<tr><td class=right>In|Out Defaults:</td><td>%s - %s</td></tr>" % ( users_hourin, users_hourout ) 
			maintext += "<tr><td class=right>Destiny Defaults:</td><td>%s</td></tr>" % ( users_destiny ) 
			maintext += "<tr><td class=right>Shift Type:</td><td>%s</td></tr>" % ( users_shifttype ) 
			maintext += "<tr><td class=right>Shift Destiny:</td><td>%s</td></tr>" % ( users_shiftdest ) 
			maintext += "<tr><td class=right>Shift Date:</td><td>%s</td></tr>" % ( users_shiftin ) 
			maintext += "<tr><td class=right>Shift Car:</td><td>%s</td></tr>" % ( users_shiftcar ) 
			
			maintext += "</table>"
			
		else:
			
			privy1 = ( 'none', 'admin', 'user', 'shift' )
			
			privyCtrl = '<select size=1 name=privy>'
			
			for privy2 in privy1 :
				
				if users_privy == privy2 :
					
					privyCtrl += '<option value=%s selected>%s' % ( privy2, privy2 )
				
				else:
					
					privyCtrl += '<option value=%s>%s' % ( privy2, privy2 )
			
			privyCtrl += '</select>'

			
			train1 = ( 'D', 'P', 'N', 'B' )
			
			trainCtrl = '<select size=1 name=train>'
			
			for train2 in train1 :
				
				if users_train == train2 :
					
					trainCtrl += '<option value=%s selected>%s' % ( train2, train2 )
				
				else:
					
					trainCtrl += '<option value=%s>%s' % ( train2, train2 )
			
			trainCtrl += '</select>'

			status1 = ( 'Active', 'Removed', 'Temporary' )
			
			statusCtrl = '<select size=1 name=status>'
			
			for status2 in status1 :
			
				if users_status == status2 :
			
					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
			
				else:
			
					statusCtrl += '<option value=%s>%s' % ( status2, status2 )           
			
			statusCtrl += '</select>'

			
			carCtrl = '<select size=1 name=car>'
			
			cursor3.execute("select car from cars order by seq")

			for raw in cursor3.fetchall() :
			
				if users_shiftcar == raw[0] :
		
					carCtrl += '<option value=%s selected>%s' % ( raw[0], raw[0] )
		
				else:
		
					carCtrl += '<option value=%s>%s' % ( raw[0], raw[0] )           
			
			carCtrl += '</select>'
				

			destinys = ( 'BaseSum_HP-Nights', 'BaseSum_HP-Nights_SA', 'BaseSum_No-HP-Nights', 'BaseSum_Days-All', 'BaseSum_Days-MonTh', 'BaseSum_Days-MonFr'  )
			
			destCtrl = '<select size=1 name=shiftdest>'
			
			for dest2 in destinys :
			
				if users_shiftdest == dest2 :
			
					destCtrl += '<option value=%s selected>%s' % ( dest2, dest2 )
			
				else:
			
					destCtrl += '<option value=%s>%s' % ( dest2, dest2 )           
			
			destCtrl += '</select>'

			overnights = ( 'Daytime', 'Overnight'  )
			
			overnightCtrl = '<select size=1 name=shifttype>'
			
			for overnight2 in overnights :
			
				if users_shifttype == overnight2 :
			
					overnightCtrl += '<option value=%s selected>%s' % ( overnight2, overnight2 )
			
				else:
			
					overnightCtrl += '<option value=%s>%s' % ( overnight2, overnight2 )           
			
			overnightCtrl += '</select>'
			
			maintext += "<form method=post action='userone.py?idno=%s'><input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>" % ( users_idno )
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>User:</td><td><input type=text name='user' size=20 value='%s'></td></tr>" % ( users_user  ) 
			maintext += "<tr><td class=right>Email:</td><td><input type=text name='email' size=40 value='%s'></td></tr>" % ( users_email  ) 
			maintext += "<tr><td class=right>STN-User:</td><td><input type=text name='stnuser' size=20 value='%s'>  | STN Username</td></tr>" % ( users_stnuser ) 
#			maintext += "<tr><td class=right>Privy</td><td><input type=text name=privy size=10 value='%s'></td></tr>" % ( users_privy  ) 
#			maintext += "<tr><td class=right>Train</td><td><input type=text name=type size=20 value='%s'></td></tr>" % ( users_train ) 
			maintext += "<tr><td class=right>Privilege:</td><td>%s | none admin user</td></tr>" % ( privyCtrl ) 
			maintext += "<tr><td class=right>Summit Training:</td><td>%s Passenger Driver-Summit Base None</td></tr>" % ( trainCtrl ) 
#			maintext += "<tr><td class=right>Wheels</td><td>%s</td></tr>" % ( car_wheels ) 
			maintext += "<tr><td class=right>Status</td><td>%s | Active Removed Temporary</td></tr>" % ( statusCtrl ) 
			maintext += "<tr><td class=right>In|Out Defaults:</td><td><input type=text name='hourin' size=10 value='%s'> - \
			<input type=text name='hourout' size=10 value='%s'></td></tr>" % ( users_hourin, users_hourout  ) 
			maintext += "<tr><td class=right>Destiny Default:</td><td><input type=text name=destiny size=10 value='%s'></td></tr>" % ( users_destiny  ) 
			maintext += "<tr><td class=right>Shift Type:</td><td>%s</td></tr>" % ( overnightCtrl  ) 
			maintext += "<tr><td class=right>Shift Destiny:</td><td>%s</td></tr>" % ( destCtrl  ) 
			maintext += "<tr><td class=right>Shift Car:</td><td>%s</td></tr>" % ( carCtrl  ) 

			maintext += "</table>"
			maintext += "</form>"
		
	else:
		
		maintext+="No user for IDNO: " + str( idno ) + "<br>"

else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )

