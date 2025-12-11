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

if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )
	
	pagename = '<center><b>Users Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

#MariaDB [sumlogs]> desc users;
#+---------+----------+------+-----+---------+----------------+
#| Field   | Type     | Null | Key | Default | Extra          |
#+---------+----------+------+-----+---------+----------------+
#| user    | char(30) | YES  |     | NULL    |                |
#| email   | char(40) | YES  |     | NULL    |                |
#| stnuser | char(40) | YES  |     | NULL    |                |
#| idno    | int(11)  | NO   | PRI | NULL    | auto_increment |
#| privy   | char(10) | YES  |     | NULL    |                |
#| train   | char(1)  | YES  |     | NULL    |                |
#| status  | char(10) | YES  |     | NULL    |                |
#+---------+----------+------+-----+---------+----------------+

	maintext = pagename 

	cursor2.execute("select user, email, stnuser, idno, privy, train, status, hourin, hourout, destiny from users where stnuser='%s' order by user" % ( username ))
	numrows2 = cursor.rowcount
	if numrows2 == 1 :
	
		raw=cursor2.fetchone()
		username_user = raw[0]
		username_email = raw[1]
		username_stnuser = raw[2]
		maintext += "Users Table: Found!<br> user: %s email: %s stnuser: %s<br>" % ( username_user, username_email, username_stnuser )
	
	else :
		
		maintext += "Users Table: Not Found!<br> username: %s<br>" % ( username )


	cursor.execute("select user, email, stnuser, idno, privy, train, status, hourin, hourout, destiny, shiftin, shiftcar, shifttype, shiftdest \
	 from users order by user")
	numrows = cursor.rowcount
	maintext += 'rows: ' + str( numrows ) + '<br>'
	maintext += "Add User: <a href=userone.py?idno=0&status=New>+Add</a><br>"
	
	
	
	
		
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>IDNo</th><th>User</th><th>Email</th><th>STN-User</th><th>Privy</th> \
	<th>Train</th><th>Status</th><th>In|Out</th><th>Destiny</th><th>ShiftType</th><th>ShiftDest</th><th>ShiftIn</th><th>ShiftCar</th></tr>'

	for row in cursor.fetchall() :

		users_user = row[0]
		users_email = row[1]
		users_stnuser = row[2]
		users_idno = str( row[3] )
		users_privy = row[4]
		users_train = row[5]
		users_status = row[6]
		users_hourin = row[7]
		users_hourout = row[8]
		users_destiny = row[9]

		users_shiftin = row[10]
		users_shiftcar = row[11]
		users_shifttype = row[12]
		users_shiftdest = row[13]
		
#		maintext += "<tr><td>%s</td><td><a href=userone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( users_idno, users_idno, users_user, users_email, users_stnuser, users_privy, users_train, user_status  )
		maintext += "<tr><td>%s</td><td><a href=userone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s - %s</td><td>%s</td> \
		<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
		% ( users_idno, users_idno, users_user, users_email, users_stnuser, users_privy, users_train, users_status, users_hourin, users_hourout, users_destiny, \
			users_shifttype, users_shiftdest, users_shiftin, users_shiftcar )

	maintext += "</table>"
else :
        maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
