#! /usr/local/python

#! /usr/bin/python

import os
import cgi
#import logproc
import http.cookies as Cookie
import datetime
#import logproc
import logproc3 as logproc
import dbconnect
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import html
import re
#import ldap

field = cgi.FieldStorage()

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor1=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()


dbconn2=dbconnect.opalconn()
db2=MySQLdb.connect( host=dbconn2[0], user=dbconn2[1], passwd=dbconn2[2], db=dbconn2[3] )

cursorOPAL=db2.cursor()

#referpage=cgi.os.environ['HTTP_REFERER']
#clientip=cgi.os.environ['REMOTE_ADDR']

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:14px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "tr:nth-child(even) { background: #CCC; }"
	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold }"
	css_text += "</style>"


	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY><center>"
	printpg += maintext
	printpg += "</center></BODY></HTML>"
	print( printpg )	


#if field.has_key('username'):

if 'username' in field:

	username = field['username'].value
	
else:
	
	username = 'None'

if 'pw' in field:

	pw = field['pw'].value
	
else:
	
	pw = 'None'

if 'logcrew' in field:

	logcrew = field['logcrew'].value
	
else:
	
	logcrew = 'WP'

username = username.strip()

failure = True

#if len ( username ) > 0 :

#	failure = True
		
#	if not pw == 'None' :

#		l = ldap.open('ldap.subaru.nao.ac.jp',389 )

#		loginline = "uid="+username+",ou=People,dc=subaru,dc=nao,dc=ac,dc=jp"

#		try:

#			l.simple_bind_s(loginline,passtext)

#		except:

	# ldap bind fail
#			result="Login/Password Failed or Account is Locked"
	#		LoginFailureMsg(result,clientip,'LDAP Login',usertext)
#		else:

#			failure = False
#			
#	else :
	
		 

cursor2.execute("select user, privy from users where stnuser = '%s' " % ( username ) )
numrows2 = cursor2.rowcount

if numrows2 == 1 :

	row = cursor2.fetchone()
	user_contact1 = row[0]
	user_privy = row[1]
else :

	user_contact1 = '.none'
	user_privy = 'none'

user_contact1 = user_contact1.strip()


instr2 = { 'COMICS':'COM', 'FOCAS':'FCS', 'IRCS':'IRC', 'IRCS+AO':'IRC', 'CHARIS':'CRS', 'HSC':'HSC', 'MOIRCS':'MCS', 'HDS':'HDS', 'IRD':'IRD', 'SUKA':'SUK', 'PFS':'PFS', 'SWIMS':'SWS', 'MIMIZUKU':'MMZ', 'VAMPIRES':'VMP', 'SCEXAO':'SCX', 'MKID':'MEC', '-None':'-None' }

writecookie = 'No'

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')

utcnow = datetime.datetime.utcnow()

now2 = now - datetime.timedelta( days = 1 )
yesterday=now2.strftime('%Y-%m-%d')

#if '.php' in referpage :
#if referpage[:-4] == '.php'and not username == 'None':
#if "?" in referpage :
	
if not logproc.validCookie() :

	writecookie = 'Yes'

	termhours = 15

	then = now + datetime.timedelta( hours = termhours ) 
	thenC = then.strftime('%Y-%m-%d %H:%M')
	
	utcthen = utcnow + datetime.timedelta( hours = termhours )

	newcookie=Cookie.SimpleCookie()
	newcookie[ 'username' ] = '%s' % ( username )
	newcookie[ 'username' ][ 'max-age' ] = termhours * 60 * 60

# expires in GMT

	newcookie[ 'username' ][ 'expires' ] = utcthen.strftime("%a, %d %b %Y %H:%M:%S GMT")
						
	term=str( termhours * 60 * 60 )
#	newcookie[ 'start' ] = '%s' % ( now )
	newcookie[ 'term' ] = '%s' % ( term )
	newcookie[ 'term' ][ 'expires' ] = utcthen.strftime("%a, %d %b %Y %H:%M:%S GMT")
	newcookie[ 'end' ] = '%s' % ( thenC )
	newcookie[ 'end' ][ 'expires' ] = utcthen.strftime("%a, %d %b %Y %H:%M:%S GMT")
	newcookie[ 'logcrew' ] = '%s' % ( logcrew )
	newcookie[ 'logcrew' ][ 'expires' ] = utcthen.strftime("%a, %d %b %Y %H:%M:%S GMT")
	newcookie[ 'opaluser' ] = '%s' % ( username )
	newcookie[ 'opaluser' ][ 'expires' ] = utcthen.strftime("%a, %d %b %Y %H:%M:%S GMT")
	print( newcookie )
	
else:

	username, end, term, logcrew2 = logproc.getUsername()

	thenC = end

#thenC = end

maintext = ''

if not username == 'None' :

	maintext = ''
	maintext += '<FONT SIZE=4><b>Summit Calendar, Logs, Cars<br><FONT SIZE=3>[ ' + username + ' expires: ' + thenC[5:16] + ' ]<br><br>'
#	maintext += '<br>writecookie: ' + writecookie + '<table>'


	now=datetime.datetime.now()
	today=now.strftime('%Y-%m-%d')

	now2 = now - datetime.timedelta( days = 1 )
	yesterday=now2.strftime('%Y-%m-%d')
	
#	username, end, term, logcrew2 = logproc.getUsername()
#	username2, end2, term2, logcrew2 = getUsername()


#	maintext += '<br>writecookie: ' + writecookie + '<table>'
	buttontxt = '<table cellpadding=4 cellspacing=4 border=2 rules=all><tr>'
#	maintext += '<tr><td><a href = ./loglist.py?>All Logs Listing</a></td></tr>' % ( username )
	buttontxt += '<td bgcolor=lime><b>Main Menu</b></td>'
	buttontxt += '<td bgcolor=yellow><a href = ./sumcal.py?>Calendar</a></td>'
	buttontxt += '<td bgcolor=yellow><a href = ./loglist.py?>Logs List</a></td>'
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s>Today - %s</a></td>" % ( today, today[5:7] + '/' + today[8:10] )
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s>Yesterday - %s</a></td>" % ( yesterday, yesterday[5:7] + '/' + yesterday[8:10] )

	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s&logcrew=%s>Today - %s</a></td>" % ( today, logcrew, today[5:7] + '/' + today[8:10] )
	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s&logcrew=%s>Yesterday - %s</a></td>" % ( yesterday, logcrew, yesterday[5:7] + '/' + yesterday[8:10] )

	buttontxt += '<td bgcolor=yellow><a href = ./itemsearch.py?>Search</a></td>'
	buttontxt += '<td bgcolor=yellow><a href = ../menu.php?>Old OPAL</a></td>'
	buttontxt += '<td bgcolor=yellow><a href = ./proplist.py?>Semester IDs</a></td>'
	buttontxt += '<td bgcolor=yellow><a href = ./resday.py?>Cars</a></td>'
	buttontxt += '<td bgcolor=yellow><a href = ./logout.py?>Logout</a></td></tr>'
	
	buttontxt += '</table><br>'

#	maintext += logproc.getMenu()
	maintext += buttontxt
	
	maintext += logproc.getCarMenu()
#	maintext += '<table cellpadding=3 cellspacing=3 border=2 rules=all>'
##	maintext += '<tr><td><a href = ./loglist.py?>All Logs Listing</a></td></tr>' % ( username )
#	maintext += '<tr><th bgcolor=yellow><a href = ./loglist.py?>All Logs</a></th>'
#	maintext += "<th bgcolor=yellow><a href = ./logone.py?date=%s>Tonight - %s</a></th>" % ( today, today[5:10] )
#	maintext += "<th bgcolor=yellow><a href = ./logone.py?date=%s>Last Night - %s</a></th>" % ( yesterday, yesterday[5:10] )
#	maintext += '<th bgcolor=yellow><a href = ./itemsearch.py?>Search</a></th></tr>'
#	maintext += '</table>'

	# trouble 8
	cursor1.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime from items \
	where date = '%s' and logcrew='WP' order by itemtime" % ( today ) )
	numrows1 = str( cursor1.rowcount )
	#numrows8_trouble = '0' 

	maintext += '<br><table cellpadding=3 cellspacing=3 border=2 rules=all><tr><th colspan=4 bgcolor=lime>Today WorkPlans - %s</th></tr>' % ( today )
	maintext += '<tr><th>Time</th><th>Title</th><th>Assigned</th><th>Reqs</th></tr>'
	
	for result in cursor1.fetchall() :
	
		item_idno = result[0]
		item_time = str( result[5] )
		item_time = item_time[11:16]
		item_title = result[6]
		item_assigned1 = result[13]
		item_endtime = str( result[14] )
		item_endtime = item_endtime[11:16]
		cursor2.execute("select code from itemreqs where planidno=%s" % ( item_idno ) )
		numrows2 = cursor2.rowcount

		reqtext = ''

		if numrows2 > 0 :
		
			for result2 in cursor2.fetchall() :
			
				reqtext += result2[0] + ' | '

#		else:
#			reqtext += 'None'
	
		maintext +=  '<tr><td><FONT SIZE=3>%s-%s</td><td><FONT SIZE=3>%s</td><td><FONT SIZE=3>%s</td><td><FONT SIZE=3>%s</td></tr>' %  ( item_time, item_endtime, item_title, item_assigned1, reqtext )
	
	maintext += '</table>'
	

	cursorOPAL.execute("select propid, instr, last, observers, remote, staff, idno, order1 from alloc where datein = '%s' and cal = 'Y' order by order1" % ( today ) )
	numrowsOPAL = cursorOPAL.rowcount
	
#	numrowsOPAL = 0
		
	maintext += "<br><table cellpadding=3 cellspacing=3><tr><th colspan=3 bgcolor=lime><FONT SIZE=3>Tonights Observations - %s - [ %s ]</th></tr>" % ( today, str( numrowsOPAL ) )			

	if numrowsOPAL > 0 :
	
#		opal_text = ''
		
		for resultOPAL in cursorOPAL.fetchall() :
		
			alloc_instr = resultOPAL[1]
			alloc_instr = alloc_instr.strip()
			observers = resultOPAL[3]
			remote = resultOPAL[4]
			staff = resultOPAL[5]
			allocidno = str( resultOPAL[6] )
			alloc_order = resultOPAL[7]
			alloc_order = alloc_order.strip()
			
			ordertable ='<table border=1 rules=all><tr>'
			
			if '1' in alloc_order:
			
				ordertable += '<td bgcolor=pink>1</td>'
			else:
				ordertable += '<td>&nbsp;</td>'
				
			if '2' in alloc_order:
			
				ordertable += '<td bgcolor=pink>2</td>'
			else:
				ordertable += '<td>&nbsp;</td>'
			
			if '3' in alloc_order:
			
				ordertable += '<td bgcolor=pink>3</td>'
			else:
				ordertable += '<td>&nbsp;</td>'

			if '4' in alloc_order:
			
				ordertable += '<td bgcolor=pink>4</td>'
			else:
				ordertable += '<td>&nbsp;</td>'
				
			ordertable += '</tr></table>'
			
		
			instrOPAL = instr2 [ alloc_instr ]

			maintext += '<tr><td><FONT SIZE=3><a href=allocone.py?idno=' + allocidno + '&date=' + today + '>' + resultOPAL[0][0:10] + '</a></td><td><FONT SIZE=3>' +  instrOPAL + ' (' +  resultOPAL[2]+ ')</td><td><FONT SIZE=3>' + ordertable + '</td></tr>'

			staffstring=''
			
			if len( observers ) > 0 or len( remote ) > 0 or len( staff ) > 0 :

#				maintext += '<tr><td colspan=2><FONT SIZE=2>'
					
				if len( observers ) > 0 :
					staffstring += 'Observers: '+ observers + ' | ' 

				if len( remote ) > 0 :
					staffstring += 'SAs: '+ remote + ' | ' 

				if len( staff ) > 0 :
					staffstring += 'Operators: '+ staff + '' 
				
#				maintext += '</td></tr>'

				maintext += '<tr><td colspan=3><FONT SIZE=3>'+ staffstring + ' </td></tr>'
#			maintext += '<tr><td colspan=3><hr></td></tr>'
			
			

	
	maintext += '</table>'
#	maintext += '<img src=./seats0.jpg>'



	
else:
	maintext += 'None name'

printHTML( maintext )
