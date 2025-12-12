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

field = cgi.FieldStorage()

dbconn=dbconnect.opalconn()
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

	
#
#def main() :

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')
oneday = datetime.timedelta( days = 1 )
yday = now - oneday

yday2 = yday.strftime('%Y-%m-%d')

#twoWeeks =  datetime.timedelta( days = 14 )
#maxView = today + twoWeeks
 

if 'date' in field :

	date = field['date'].value

else:

	date = yday2

if 'order' in field :

	order = field['order'].value

else:

	order = 'date'


if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	username = 'winegar'	
#	end = 'none'
	pagename = '<center><b>Observer ZOOMIDs Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'

	orderby = " limit 32 "
	orderby=''
#	if order == 'semid' :

#		orderby = "order by gid"
		
#	if order == 'propid' :

#		orderby = "order by propid"
	
#	if order == 'instr' :

#		orderby = "order by instr, datein"
		
#	cursor.execute("select idno, propid, piidno, gid, instr, sem, datein, first, last, username from props where sem='%s' %s" % ( sem, orderby ) )

	cursor2.execute("select sem from props group by sem desc" )
#	year_spin = "<select name='%s' size=1>" % ( 'year' )''
	year_spin = ""
	seq = 0
	for row2 in cursor2.fetchall() :
		seq += 1
		year_spin += "<a href=zoomlist.py?sem=%s>%s</a>  " % ( row2[0], row2[0] )
		if seq == 15 or seq==30 or seq==45 or seq==60 :
			year_spin += "| <br>"
	
	
#	year_spin += "</select>"


	maintext = pagename 


	maintext += '<br><b>ZoomIDs Listing</b><br>'

	maintext += year_spin + '<br>'
	
	if date == yday2 :

		cursor.execute("select date, day, zoomid, zoompw, join_url from days where date > '%s' limit 60" % ( yday2 ) )
				
	
#	cursor.execute("select idno, propid, piidno, gid, instr, sem, datein, first, last, username from props order by datein")
		numrows=cursor.rowcount

		maintext += 'rows: ' + str( numrows ) + '<br>'
	
		maintext += '<table rules=all border=2 cellpadding=5 cellspacing=5><tr><th>Seq</th><th>Date</th><th>Day</th><th>ZoomID</th><th>ZoomPW</th><th>Join_URL</th></tr>'
	
		seq = 0

		for row in cursor.fetchall() :

			seq += 1

			days_date = str( row[0] )
			days_day = row[1]
			days_zoomid = row[2]
			days_zoompw = row[3]
			days_joinurl = row[4]		
	#		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
	#		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_datein, prop_last, prop_cal )

			maintext += "<tr><td>%s</td><td><a href=zoomlist.py?date=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td><font size=-1><a href=%s>%s</a></font></td></tr>" \
			% ( seq, days_date, days_date, days_day[0:3],  days_zoomid, days_zoompw, days_joinurl, days_joinurl   )

		maintext += "</table>"

	else :

		cursor.execute("select date, day, zoomid, zoompw, join_url from days where date = '%s'" % ( date ) )
				
	
#	cursor.execute("select idno, propid, piidno, gid, instr, sem, datein, first, last, username from props order by datein")
		numrows=cursor.rowcount
	
#		maintext += '<table rules=all border=2 cellpadding=5 cellspacing=5><tr><th>Seq</th><th>Date</th><th>Day</th><th>ZoomID</th><th>ZoomPW</th><th>Join_URL</th></tr>'
		maintext += '<table rules=all border=2 cellpadding=5 cellspacing=5><tr><th>Desc</th><th>Value</th></tr>'
	
		seq = 0

		row = cursor.fetchone()

		days_date = str( row[0] )
		days_day = row[1]
		days_zoomid = row[2]
		days_zoompw = row[3]
		days_joinurl = row[4]		
#		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_datein, prop_last, prop_cal )

		maintext += "<tr><td>%s</td><td>%s %s</td></tr>" % ( 'Date:', days_date, days_day[0:3] )
		
		maintext += "<tr><td>ZoomID/PW</td><td>%s / %s</td></tr>" % ( days_zoomid, days_zoompw )
		maintext += "<tr><td>Join_URL</td><td><a href='%s'>%s</a></td></tr>" % ( days_joinurl, days_joinurl )

		maintext += "</table>"
	
	



else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
