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

from ldap3 import Server, Connection, ALL


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
	printpg += "</HEAD><BODY><CENTER>"
	printpg += maintext
	printpg += "</CENTER></BODY></HTML>"
	print( printpg )	


now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')
year = today[0:4]

#currentSem = logproc.getSemID ( today )

if 'letter' in field :

	letter = field['letter'].value
	
else :
	
	letter = 'A'
	
letter2 = ' ' + letter

	
#def main() :




if logproc.validCookie() :
#if True :

#	username, end, term, logcrew2 = logproc.getUsername()

#	pagename = '<center><b>STARS LDAP Listing</b> | ' + username + " [" + end + ']<br><br>' 
	pagename=''
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'


#	cursor.execute("select idno, propidno, allocidno, date, instr, ss, last, first, propid, focus, arrive, \
#	ag, sv, adc, imr, cal, flats, polar, ao, irm2, pmdusk, \
#	pmdome, amdawn, amdome, flatrun, calrun, comments, calcomm, imrcomm, day, gid, \
#	pmcomm, amcomm, observers, obsarrive, location, sh, chop, m2, m3, \
#	adccomm, amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, program, \
#	ordering, wpulgs, ocs, m2offset, others, alloc, confirm, ao2, queue, agcomm \
#	from tsr order by date desc") % ( year )
	letter_spin = ""
	letter_spin2 = ""
#	seq = 0
	letters = ( 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' )
	lettersLC = ( 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' )
	
	for lett in letters :
#		seq += 1
		letter_spin += "<a href=ldaplist.py?letter=%s>%s</a> | " % ( lett, lett )
	
	for lett in lettersLC :
	#		seq += 1
		letter_spin2 += "<a href=ldaplist.py?letter=%s>%s</a> | " % ( lett, lett )
	#num
#numrows=cursor.rowcount
	maintext = pagename 
	#maintext += 'rows: ' + str( numrows ) + '<br>'
	maintext += '<br><b>STARS LDAP Users Listing</b><br><br>'
	maintext += 'Last Name (Upper): ' + letter_spin + '<br>'
	maintext += 'User Name (lower): ' + letter_spin2 + '<br><br>'
	 
	 
	#maintext += '<br><b>Last: %s<br>New: <a href=starsone.py?idno=%s>+Add New User</a></b><br><br>' % ( letter_spin, '0' )
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>UserName</th><th>FullName</th><th>Email</th></tr>'

	seq = 0



#	s = Server( host='squery.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	s = Server( host='sreg6.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )

	conn = Connection(s, auto_bind=True)
#conn.search('memberuid=winegar,ou=Group,dc=subaru,dc=nao,dc=ac,dc=jp', '(objectClass=*)' , 'SUBTREE', attributes=['dn'] )
	conn.search('ou=people,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=*)' , 'SUBTREE', attributes=['cn', 'gecos', 'mail'] )

	members = []


	for entry in conn.entries :
	
		
		cn = str( entry['cn'] )
		gecos = str( entry['gecos'] )
		gecos2 = gecos.upper()
		mail = str( entry['mail'] )
		
		cursor.execute("select idno, username from users where username = '%s'" % ( cn ) )
		numrows = cursor.rowcount
		
		starsidno = 0
		
		if numrows == 1 :

			rows = cursor.fetchone()
			starsidno = rows[0]

		if letter in letters:
#			maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, 'uppercase', gecos, mail )

			if letter2 in gecos2 :

				seq += 1
				members.append ( cn )
				maintext += '<tr><td>%s</td><td><a href=starsone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td></tr>' % ( seq, starsidno, cn, gecos, mail )

		else :
#			maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, 'lowercase', gecos, mail )
		
			if cn[0:1] == letter :

				seq += 1
				members.append ( cn )
				maintext += '<tr><td>%s</td><td><a href=starsone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td></tr>' % ( seq, starsidno, cn, gecos, mail )
			
	
#	maintext += '<table cellpadding=3 cellspacing=4><tr><th colspan=4 bgcolor=lime>STARS LDAP assigned USERS ( %s )</th></tr>' % ( len( members ) ) 
	print("members: " + str( members ))#		maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( '0', 'none', 'none', 'none' )

	maintext += '</table>'


#	if letter == 'all' :
#		cursor.execute("select idno, first, last, email, username, altname, privy from users order by last, first")
#	else :
#		cursor.execute("select idno, first, last, email, username, altname, privy from users where last like '%s' order by last, first" % ( letter2 ) )
	
#	cursor2.execute("select substr(date,1,4) from tsr group by substr(date,1,4) desc" )
#	year_spin = "<select name='%s' size=1>" % ( 'year' )''

#		if seq == 10 or seq==20 or seq==30 or seq==40 :
#			year_spin += "| <br>"
#	year_spin += "</select>"
	


else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
