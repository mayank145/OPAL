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

if 'letter' in field :

	letter = field['letter'].value
	
else :
	
	letter = 'all'
	
letter2 = letter + '%'

	
if 'propidno' in field :

	propidno = field['propidno'].value
	
else :

	propidno = '0'

#propidno2 = int( propidno )

#def main() :




if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()

	pagename = '<center><b>STARS Users Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'


#	cursor.execute("select idno, propidno, allocidno, date, instr, ss, last, first, propid, focus, arrive, \
#	ag, sv, adc, imr, cal, flats, polar, ao, irm2, pmdusk, \
#	pmdome, amdawn, amdome, flatrun, calrun, comments, calcomm, imrcomm, day, gid, \
#	pmcomm, amcomm, observers, obsarrive, location, sh, chop, m2, m3, \
#	adccomm, amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, program, \
#	ordering, wpulgs, ocs, m2offset, others, alloc, confirm, ao2, queue, agcomm \
#	from tsr order by date desc") % ( year )

	if letter == 'all' :

		cursor.execute("select idno, first, last, email, username, altname, privy from users order by last, first")

	else :

		cursor.execute("select idno, first, last, email, username, altname, privy from users where last like '%s' order by last, first" % ( letter2 ) )
	
#	cursor2.execute("select substr(date,1,4) from tsr group by substr(date,1,4) desc" )
#	year_spin = "<select name='%s' size=1>" % ( 'year' )''
	letter_spin = ""
#	seq = 0
	letters = ( 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' )
#	'a','c','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' )
	
	for lett in letters :
#		seq += 1
		letter_spin += "<a href=starslist.py?letter=%s>%s</a> | " % ( lett, lett )
#		if seq == 10 or seq==20 or seq==30 or seq==40 :
#			year_spin += "| <br>"
#	year_spin += "</select>"
	
	

	
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
	maintext += '<br><b>STARS Users Listing</b><br>'
	maintext += '<br><b>Last: %s<br>New: <a href=starsone.py?idno=%s>+Add New User</a></b><br><br>' % ( letter_spin, '0' )
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>Last</th><th>First</th><th>Email</th> \
	<th>STARS-Name</th><th>STN-Name</th><th>Privy</th></tr>'
	
	seq = 0

	for row in cursor.fetchall() :

		seq += 1

		user_idno = row[0]
		user_first = row[1]
		user_last = row[2]
		user_email = row[3]
		user_username = row[4]
		user_altname = row[5]		
		user_privy = row[6]
#		tsr_ag = row[11]
		
#		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_datein, prop_last, prop_cal )
		bgcolor = 'white'

#		if tsr_date == today :
		
#			bgcolor = 'lime'
			
#		maintext += "<tr><td>%s</td><td><a href=userone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( seq, user_idno, user_last, user_first, user_email, user_username, user_privy )

		if int( propidno ) > 0 :

#		if propidno2 > 0 :
#		if True :
			maintext += "<tr><td>%s</td><td>( Assign-PI ): <a href=propone.py?idno=%s&uid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
			% ( seq, propidno, user_idno, user_last, user_first, user_email, user_username, user_altname, user_privy )

#		else :

#			maintext += "<tr><td>%s</td><td><a href=starsone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#			% ( seq, user_idno, user_last, user_first, user_email, user_username, user_altname, user_privy )
		
		else :

			maintext += "<tr><td>%s</td><td><a href=starsone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
			% ( seq, user_idno, user_last, user_first, user_email, user_username, user_altname, user_privy )
		
	maintext += "</table>"




else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
