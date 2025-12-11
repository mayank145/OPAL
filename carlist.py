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

field = cgi.FieldStorage()

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
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

if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
	
	pagename = '<center><b>Cars Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

	cursor.execute("select car, loc, phone, pass, type, seq, status, wheels, idno, drivers from cars order by seq")
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
	maintext += '<br><b>Cars Listing</b><br>'
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>Car</th><th>Loc</th><th>Phone</th><th>Pass</th><th>Type</th><th>Status</th><th>Wheels</th><th>Drivers</th></tr>'

	for row in cursor.fetchall() :

		car = row[0]
		loc = row[1]
		phone = row[2]
		pass2 = str( row[3] )
		type = row[4]
		seq = row[5]
		status = row[6]
		wheels = row[7]
		car_idno = row[8]
		car_drivers = row[9]
		
		maintext += "<tr><td>%s</td><td><a href=carone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
		% ( seq, car_idno, car, loc, phone, pass2, type, status, wheels, car_drivers  )

	maintext += "</table>"

	maintext += "<br><b>BlackOuts Listing</b></br>"

	cursor2.execute("select idno, car, start, end, recur, type, warning, status from blackres order by idno")
	numrows2=cursor.rowcount
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3>'
	'<tr><th>IDNo</th><th>Car</th><th>Start</th><th>End</th><th>Recur</th><th>Type</th><th>Warning</th><th>Status</th></tr>'


	for row in cursor2.fetchall() :

		black_idno = row[0]
		black_car = row[1]
		black_start = str( row[2] )
		black_end = str( row[3] )
		black_recur = row[4]
		black_type = row[5]
		black_warning = row[6]
		black_status = row[7]
		
		maintext += "<tr><td>%s</td><td><a href=blackone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
		% ( black_idno, black_idno, black_car, black_start, black_end, black_recur, black_type, black_warning, black_status  )

	maintext += "</table>"



else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
