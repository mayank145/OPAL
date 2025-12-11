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
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 16px }"
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


now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')
year = today[0:4]

#currentSem = logproc.getSemID ( today )

if 'year' in field :

	year = field['year'].value
	


	
#def main() :




if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()

	pagename = '<center><b>Telescope Setup Request ( TSR ) Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'


#	cursor.execute("select idno, propidno, allocidno, date, instr, ss, last, first, propid, focus, arrive, \
#	ag, sv, adc, imr, cal, flats, polar, ao, irm2, pmdusk, \
#	pmdome, amdawn, amdome, flatrun, calrun, comments, calcomm, imrcomm, day, gid, \
#	pmcomm, amcomm, observers, obsarrive, location, sh, chop, m2, m3, \
#	adccomm, amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, program, \
#	ordering, wpulgs, ocs, m2offset, others, alloc, confirm, ao2, queue, agcomm \
#	from tsr order by date desc") % ( year )

	cursor.execute("select idno, propidno, allocidno, date, instr, ss, last, first, propid, focus, arrive, sslist \
	from tsr where substr(date,1,4) = '%s' order by date desc" % ( year ) )
	
	cursor2.execute("select substr(date,1,4) from tsr group by substr(date,1,4) desc" )
#	year_spin = "<select name='%s' size=1>" % ( 'year' )''
	year_spin = ""
	seq = 0
	for row2 in cursor2.fetchall() :
		seq += 1
		year_spin += "<a href=tsrlist.py?year=%s>%s</a> | " % ( row2[0], row2[0] )
		if seq == 10 or seq==20 or seq==30 or seq==40 :
			year_spin += "| <br>"
#	year_spin += "</select>"
	
	

	
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
	maintext += '<br><b>TSRs Listing</b><br>'
	maintext += '<br><b>Years: %s</b><br>' % ( year_spin )
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>PropID</th><th>Instr</th><th>Date</th> \
	<th>Focus</th><th>PI First</th><th>PI Last</th><th>Arrive</th><th>SAs</th></tr>'
	
	seq = 0

	for row in cursor.fetchall() :

		seq += 1

		tsr_idno = str( row[0] )
		tsr_propidno = row[1]
		tsr_allocidno = row[2]
		tsr_date = row[3]
		tsr_instr = row[4]
		tsr_ss = row[5]
		
		tsr_last = row[6]
		tsr_first = row[7]
		tsr_propid = row[8]
		tsr_focus = row[9]
		tsr_arrive = row[10]
		tsr_sslist = row[11]
#		tsr_ag = row[11]
		
#		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_datein, prop_last, prop_cal )
		bgcolor = 'white'

		if tsr_date == today :
		
			bgcolor = 'lime'
			
		maintext += "<tr><td>%s</td><td><a href=tsrone.py?idno=%s>%s</a></td><td>%s</td><td bgcolor=%s>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
		% ( seq, tsr_idno, tsr_propid, tsr_instr, bgcolor, tsr_date, tsr_focus, tsr_first, tsr_last, tsr_arrive, tsr_sslist )

	maintext += "</table>"




else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
