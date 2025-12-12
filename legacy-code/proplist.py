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


if 'sem' in field :

	sem = field['sem'].value

else:

	sem = logproc.getSemID ( today )

#	sem = 'S22B'

if 'order' in field :

	order = field['order'].value

else:

	order = 'date'


if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	username='winegar'	
#	end='none'
	pagename = '<center><b>Proposals Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'

	orderby = "order by datein"

	if order == 'semid' :

		orderby = "order by gid"
		
	if order == 'propid' :

		orderby = "order by propid"
	
	if order == 'instr' :

		orderby = "order by instr, datein"
		
	cursor.execute("select idno, propid, piidno, gid, instr, sem, datein, first, last, username from props where sem='%s' %s" % ( sem, orderby ) )
				
	
#	cursor.execute("select idno, propid, piidno, gid, instr, sem, datein, first, last, username from props order by datein")
	numrows=cursor.rowcount


	cursor2.execute("select sem from props where sem is not null group by sem desc" )
#	year_spin = "<select name='%s' size=1>" % ( 'year' )''
	year_spin = ""
	seq = 0
	for row2 in cursor2.fetchall() :
		seq += 1
		year_spin += "<a href=proplist.py?sem=%s>%s</a>  " % ( row2[0], row2[0] )
		if seq == 15 or seq==30 or seq==45 or seq==60 :
			year_spin += "| <br>"
		
		
#	year_spin += "</select>"
	

	maintext = pagename 
	
	maintext += 'rows: ' + str( numrows ) + '<br>'
	
	maintext += '<br><b>Proposals Listing</b><br>'

	maintext += year_spin + '<br>'
	
	maintext += 'OrderBy: <a href=proplist.py?sem=%s&order=date>Date</a> | ' % ( sem )
	maintext += '<a href=proplist.py?sem=%s&order=propid>PropID</a> | ' % ( sem )
	maintext += '<a href=proplist.py?sem=%s&order=semid>SemID</a> | ' % ( sem )
	maintext += '<a href=proplist.py?sem=%s&order=instr>Instr</a> | <br> ' % ( sem )

	

	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>PropID</th><th>Instr</th><th>Date</th><th>SemID</th><th>PI First</th><th>PI Last</th><th>Sem</th></tr>'
	
	seq = 0

	for row in cursor.fetchall() :

		seq += 1

		prop_idno = str( row[0] )
		prop_propid = row[1]
		prop_piidno = str( row[2] )
		prop_gid = row[3]
		prop_instr = row[4]
		prop_sem = row[5]
		prop_datein = row[6]
		prop_first = row[7]
		prop_last = row[8]
		prop_username = row[9]
		
#		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_datein, prop_last, prop_cal )

		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_gid, prop_first, prop_last, prop_sem )

	maintext += "</table>"




else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
