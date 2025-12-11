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
import logproc


method=os.environ.get("REQUEST_METHOD","")

field = cgi.FieldStorage()

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor2.execute("set autocommit = 1")

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


if 'car' in field :

	car = field['car'].value
	
else:
	
	car = 'J-01'

if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

if 'phone' in field :

	phone = field['phone'].value
	
else:
	
	phone = ''

if 'loc' in field :

	loc = field['loc'].value
	
else:
	
	loc = ''

if 'type' in field :

	type = field['type'].value
	
else:
	
	type = ''

if 'seq' in field :

	seq = field['seq'].value
	
else:
	
	seq = '00'
	
if 'wheels' in field :

	wheels = field['wheels'].value
	
else:
	
	wheels = '4WD'
    
if 'status' in field :

	status = field['status'].value
	
else:
	
	status = 'Active'

if 'pass2' in field :

	pass2 = field['pass2'].value

else:

	pass2 = '4'

if 'comment' in field :

	comment = field['comment'].value

else:

	comment = ''
	
if 'drivers' in field :

	drivers = field['drivers'].value

else:

	drivers = '+All,'
       
if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )


	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :

		cursor2.execute("update cars set car = '%s', loc = '%s', phone = '%s', seq = '%s', status='%s', wheels='%s', comment='%s', type='%s', drivers = '%s' \
		where idno = '%s'" \
		% ( car, loc, phone, seq, status, wheels, comment, type, drivers, idno ) )
	
	pagename = '<center><b>Cars Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'
	

	cursor.execute("select car, loc, phone, pass, type, seq, idno, status, wheels, comment, drivers from cars where idno = '%s'" % ( idno ) )
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
#	maintext += '<table cellpadding=3 cellspacing=3>'
	admin_users = ( 'winegar', 'noriko', 'letawsky', 'otsuki' )
	
	if numrows == 1 :
	
		row = cursor.fetchone()

		car_car = row[0]
		car_loc = row[1]
		car_phone = row[2]
		car_pass2 = str( row[3] )
		car_type = row[4]
		car_seq = row[5]
		car_idno = row[6]
		car_status = row[7]
		car_wheels = row[8]
		car_comment = row[9]
		car_drivers = row[10]
		

#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' ) ) :

			if username in admin_users :
				maintext += "<form method=post action='carone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( car_idno )
			
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>Car</td><td>%s</td></tr>" % ( car_car ) 
			maintext += "<tr><td class=right>Location</td><td>%s</td></tr>" % ( car_loc ) 
			maintext += "<tr><td class=right>Phone</td><td>%s</td></tr>" % ( car_phone ) 
			maintext += "<tr><td class=right>Passengers</td><td>%s</td></tr>" % ( car_pass2 ) 
			maintext += "<tr><td class=right>Type</td><td>%s</td></tr>" % ( car_type ) 
			maintext += "<tr><td class=right>Seq</td><td>%s</td></tr>" % ( car_seq ) 
			maintext += "<tr><td class=right>Status</td><td>%s</td></tr>" % ( car_status ) 
			maintext += "<tr><td class=right>Wheels</td><td>%s</td></tr>" % ( car_wheels ) 
			maintext += "<tr><td class=right>Comment</td><td>%s</td></tr>" % ( car_comment )
			maintext += "<tr><td class=right>Drivers</td><td>%s</td></tr>" % ( car_drivers )

		else:

			wheels1 = ( '2WD', '4WD', '4WD-Studs' )
			wheelsCtrl = '<select size=1 name=wheels>'
			for wheels2 in wheels1 :
				if car_wheels == wheels2 :
					wheelsCtrl += '<option value=%s selected>%s' % ( wheels2, wheels2 )
				else:
					wheelsCtrl += '<option value=%s>%s' % ( wheels2, wheels2 )
			wheelsCtrl += '</select>'

			status1 = ( 'Active', 'Removed', 'Garage' )
			statusCtrl = '<select size=1 name=status>'
			for status2 in status1 :
				if car_status == status2 :
					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
				else:
					statusCtrl += '<option value=%s>%s' % ( status2, status2 )           
			statusCtrl += '</select>'

			maintext += "<form method=post action='carone.py?idno=%s'><input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>" % ( car_idno )
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>Car</td><td><input type=text name=car size=10 value='%s'></td></tr>" % ( car_car ) 
			maintext += "<tr><td class=right>Location</td><td><input type=text name=loc size=20 value='%s'></td></tr>" % ( car_loc ) 
			maintext += "<tr><td class=right>Phone</td><td><input type=text name=phone size=20 value='%s'></td></tr>" % ( car_phone ) 
			maintext += "<tr><td class=right>Passengers</td><td><input type=text name=pass2 size=10 value='%s'></td></tr>" % ( car_pass2 ) 
			maintext += "<tr><td class=right>Type</td><td><input type=text name=type size=20 value='%s'></td></tr>" % ( car_type ) 
			maintext += "<tr><td class=right>Seq</td><td><input type=text name=seq size=5 value='%s'></td></tr>" % ( car_seq ) 
			maintext += "<tr><td class=right>Status</td><td>%s</td></tr>" % ( statusCtrl ) 
			maintext += "<tr><td class=right>Wheels</td><td>%s</td></tr>" % ( wheelsCtrl ) 
			maintext += "<tr><td class=right>Comment</td><td><input type=text name=comment size=100 value='%s'></td></tr>" % ( car_comment ) 
			maintext += "<tr><td class=right>Drivers</td><td><input type=text name=drivers size=100 maxsize=150 value='%s'></td></tr>" % ( car_drivers ) 
			maintext += "</form>"

	maintext += "</table>"

else :

	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
