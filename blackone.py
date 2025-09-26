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
	
idno = idno.strip()

if 'start' in field :

	startdate = field['start'].value
	
else:
	
	startdate = today

if 'end' in field :

	enddate = field['end'].value

else:

	enddate = today

if 'recur' in field :

	recur = field['recur'].value
	
else:
	
	recur = ''

if 'type' in field :

	type = field['type'].value
	
else:
	
	type = ''

if 'warning' in field :

	warning = field['warning'].value
	
else:
	
	warning = ''
	
    
if 'status' in field :

	status = field['status'].value
	
else:
	
	status = 'Active'
        
if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )


	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :

		cursor2.execute("update blackres set car = '%s', start = '%s', end = '%s', recur = '%s', type = '%s', warning = '%s', status='%s' \
		where idno = '%s'" % ( car, startdate, enddate, recur, type, warning, status, idno ) )
	
	pagename = '<center><b>BlackOut Reservations Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()

	cursor.execute("select idno, car, start, end, recur, type, warning, status from blackres where idno = '%s'" % ( idno ) )

#	cursor.execute("select car, loc, phone, pass, type, seq, idno, status, wheels, comment from cars where car = '%s'" % ( car ) )
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
	
	
	maintext += '<table cellpadding=3 cellspacing=3>'
	maintext += '<tr><th bgcolor=yellow colspan=2>'
	maintext += 'BlackOut Reservations restrict users from reserving cars.</th></tr>'
#	maintext += '<tr><th bgcolor=yellow><b>If ...</b></th><th bgcolor=yellow><b>Then ...</b></th></tr>'
	
	maintext += '<tr><td>If Recur=Yearly and Type=4WD-Studs and Sep 15 - Apr 15,</td><td>destinations are only HP-Summit.</br>'
	maintext += '<tr><td>If Recur=Daily and Type=Shift-Car,</td></td><td>then only Shift Managers can reserve:<br>like Roth, Letawsky, Otsuki</td></tr>'
	maintext += '</table><br>'


	if numrows == 1 :
	
		row = cursor.fetchone()

		black_idno = row[0]
		black_car = row[1]
		black_start = str( row[2] )
		black_end = str( row[3] )
		black_recur = row[4]
		black_type = row[5]
		black_warning = row[6]
		black_status = row[7]
		black_status = black_status.strip()
		

#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' ) ) :

			maintext += "<form method=post action='blackone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( black_idno )
			maintext += "<tr><td class=right>Blackout IDNo:</td><td>%s</td></tr>" % ( black_idno ) 
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>Car:</td><td>%s</td></tr>" % ( black_car ) 
			maintext += "<tr><td class=right>StartDate:</td><td>%s</td></tr>" % ( black_start ) 
			maintext += "<tr><td class=right>EndDate:</td><td>%s</td></tr>" % ( black_end ) 
			maintext += "<tr><td class=right>Recur:</td><td>%s</td></tr>" % ( black_recur ) 
			maintext += "<tr><td class=right>Type:</td><td>%s</td></tr>" % ( black_type ) 
			maintext += "<tr><td class=right>Warning:</td><td>%s</td></tr>" % ( black_warning ) 
			maintext += "<tr><td class=right>Status:</td><td>%s</td></tr>" % ( black_status )

		else:

			recur1 = ( 'Daily', 'Yearly' )
			recurCtrl = '<select size=1 name=recur>'
			for recur2 in recur1 :
				if black_recur == recur2 :
					recurCtrl += '<option value=%s selected>%s' % ( recur2, recur2 )
				else:
					recurCtrl += '<option value=%s>%s' % ( recur2, recur2 )
			recurCtrl += '</select>'

			status1 = ( 'Active', 'Removed', 'Garage' )
			statusCtrl = '<select size=1 name=status>'
			for status2 in status1 :
				if black_status == status2 :
					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
				else:
					statusCtrl += '<option value=%s>%s' % ( status2, status2 )           
			statusCtrl += '</select>'
			
			type1 = ( '4WD-Studs', 'Shift-Car' )
			typeCtrl = '<select size=1 name=type>'
			for type2 in type1 :
				if black_type == type2 :
					typeCtrl += '<option value=%s selected>%s' % ( type2, type2 )
				else:
					typeCtrl += '<option value=%s>%s' % ( type2, type2 )
			typeCtrl += '</select>'


			maintext += "<form method=post action='blackone.py?idno=%s'><input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>" \
			% ( black_idno )
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>IDNo: </td><td>%s</td></tr>" % ( black_idno ) 
			maintext += "<tr><td class=right>Car:</td><td><input type=text name=car size=20 value='%s'></td></tr>" % ( black_car ) 
			maintext += "<tr><td class=right>StartDate:</td><td><input type=text name=start size=15 value='%s'></td></tr>" % ( black_start ) 
			maintext += "<tr><td class=right>EndDate:</td><td><input type=text name=end size=15 value='%s'></td></tr>" % ( black_end ) 
			maintext += "<tr><td class=right>Recur:</td><td>%s</td></tr>" % ( recurCtrl ) 
			maintext += "<tr><td class=right>Type:</td><td>%s</td></tr>" % ( typeCtrl ) 
			maintext += "<tr><td class=right>Warning:</td><td><input type=text name=warning size=30 value='%s'></td></tr>" % ( black_warning ) 
			maintext += "<tr><td class=right>Status:</td><td>%s</td></tr>" % ( statusCtrl ) 
			maintext += "</form>"

	maintext += "</table>"

else :

	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
