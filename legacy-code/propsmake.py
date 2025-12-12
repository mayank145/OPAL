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

import random


method=os.environ.get("REQUEST_METHOD","")
#method='GET'

field = cgi.FieldStorage()

dbconn=dbconnect.opalconn()
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


if 'sem' in field :

	sem = field['sem'].value
	
else:
	
	sem = 'S99A'

if 'type' in field :

	type = field['type'].value
	
else:
	
	type = 'EN'
	

if 'propseq' in field :

	propseq = field['propseq'].value
	
else:
	
	propseq = 'o24201'

if 'makenum' in field :

	makenum = field['makenum'].value

else:

	makenum = '1'

if 'sdate' in field :

	sdate = field['sdate'].value
	
else:
	
	sdate = today

        
#if logproc.validCookie() :

if True :

#	username, end, term, logcrew2 = logproc.getUsername()

	username='winegar'
	end='soon'
	term='3'
	logcrew='TO'

#	termlimit = str( now + term )

	post_text = 'start<br>' 

	if method == 'POST' and len ( sem ) == 4 :

		post_text += 'inside POST<br>' 

		useridno = '1414'
		username = 'starsopr'
		first = 'Operator'
		last = 'STARS'
		nseq = 0

		nsuffix = '1'
		
		sdate2 = sdate

		pregid = propseq[ 0:3 ]
			
		sufgid = propseq[ 3:6 ]

		cseq = sufgid
		
		if type == 'EN' :
		
#			cmdSelect = "select idno, propid, gid, instr, piidno, engseq, first, last, username, ulogin, public, \
#			eng, engseq, comment, stn_flag from props where sem ='S99A' and eng=1 and engseq is not null order by engseq" 
			cmdSelect = "select idno, propid, gid, instr, piidno, engseq, first, last, username, ulogin, public, \
			eng, engseq, coalesce( comment, '' ), coalesce( stn_flag, '0') from props where sem ='S24A' and eng=1 and engseq is not null order by engseq" 
			
			post_text += "in EN<br>"+ cmdSelect + "<br>"
			
			cursor2.execute(  cmdSelect ) 

			nseq = 0

#			if False:
			for rows in cursor2.fetchall() :

				nseq += 1

				idno = rows[0]
				propid = rows[1]
				gid = rows[2]
				instr = rows[3]
				useridno = rows[4]
				engseq = rows[5]
				first = rows[6]
				last = rows[7]
				username = rows[8]
				ulogin = rows[9]				
				public = rows[10]
				eng = rows[11]
				engseq = rows[12]
				comment = rows[13]
				stn_flag = rows[14]

				dateinArray = sdate2.split('-')

				datein3 = datetime.datetime( int( dateinArray[0] ) , int( dateinArray[1] ), int( dateinArray[2] ) )

				if nseq > 1 :
				
					addDay = datetime.timedelta ( days = 1 )
					newDate = datein3 + addDay
				
				else :
					newDate = datein3

				nextDay = newDate.strftime('%Y-%m-%d')
				sdate2 = nextDay
	#			nextDay = today

				datein = nextDay

				dateout = nextDay

				nights='1'

				gid = 'o' + sem[ 1:3 ]  + engseq
				
				post_text += "PID: %s GID: %s INSTR: %s PIIDNO: %s ENGSEQ: %s NewGID %s<br>" \
				% ( propid, gid, instr, useridno, engseq, gid )

				propid = sem + '-EN' + engseq[ 1:3 ]

				pepA = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', \
				'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' ]

				newpep = ''

				for i in random.sample( pepA , 12 ) :
					newpep += i

				cmdIdno = "select number from counter where file = '%s'" % ( 'props' )
				cursor2.execute(  cmdIdno )
				rowIdno = cursor2.fetchone()
				nidno = rowIdno[0]
				nextIdno = nidno + 1
				cmdIdno = "update counter set number = %s where file = '%s'" % ( nextIdno, 'props' )

				cursor2.execute(  cmdIdno )

				cmdInsert = "insert into props ( idno, propid, piidno, gid, nights, instr, datein, dateout, sem, \
				first, last, username, ulogin, pep, public, eng, engseq, comment, stn_flag  ) values \
				('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
				% ( nidno, propid, useridno, gid, nights, instr, datein, dateout, sem, first, last, username, \
				ulogin, newpep,  'OFF', eng, engseq, comment, '0' ) 

				post_text += 'Props Insert: ' + cmdInsert + "<br>"

				cursor2.execute(  cmdInsert )

				newpropidno = nidno

				cmdIdno = "select number from counter where file = '%s' " % ( 'alloc' )
				cursor2.execute(  cmdIdno )
				rowIdno = cursor2.fetchone()
				nidno = rowIdno[0]
				nextIdno = nidno + 1
				cmdIdno = "update counter set number = %s where file = '%s' " % ( nextIdno, 'alloc' )
				cursor2.execute(  cmdIdno )

				cmdInsert2 = "insert into alloc ( idno, propidno, datein, dateout, propid, gid, nights, instr, piidno, sem, \
				last, first, username, stn_flag, cal, order1, delivery, observers, remote, staff ) values \
				( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
				'%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
				% ( nidno, newpropidno, datein, dateout, propid, gid, nights, instr, useridno, sem, \
				last, first, username, 'N', 'Y', '1234', 'D', '', '', '' )

				post_text += 'Alloc Insert: ' + cmdInsert2  + "<br>"

				cursor2.execute(  cmdInsert2 )

				cmdUpdate = "update props set subidno='%s' where idno='%s' " % ( nidno, newpropidno )

				post_text += 'Props Update: ' + cmdUpdate + "<br>"

				cursor2.execute(  cmdUpdate )

# OT SV  OU 
		else :
		
			while nseq < int( makenum ) :

				nseq += 1 

				if ( nseq > 1 ) :

					cseq = str( int( cseq )  + 1 )
					nsuffix =  str( int( nsuffix ) + 1 ) 

				if int( cseq ) < 10  :

					cseq = '0' + cseq

				if int( nsuffix ) < 10  :

					nsuffix = '0' + nsuffix


				gid = pregid + cseq
	#			gid = 'o24201'

				propid = sem + '-' + type + nsuffix

	#			propid = sem + gid

	#			post_text += 'New PropID: ' + propid + '<br>' 

				dateinArray = sdate2.split('-')

				datein3 = datetime.datetime( int( dateinArray[0] ) , int( dateinArray[1] ), int( dateinArray[2] ) )

				addDay = datetime.timedelta ( days = 1 )
				newDate = datein3 + addDay

				nextDay = newDate.strftime('%Y-%m-%d')
				sdate2 = nextDay
	#			nextDay = today

				datein = nextDay

				dateout = nextDay

				ulogin = 'u' + gid[1:5]
				nights = '1'
				instr = 'MOIRCS'
				code = 'MCS'

				post_text += 'New Prop: ' + propid + ' gid: ' + gid + ' NewDate: ' + nextDay + '<br>' 

				pepA = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', \
				'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' ]

				newpep = ''

				for i in random.sample( pepA , 12 ) :
					newpep += i


				cmdIdno = "select number from counter where file = '%s'" % ( 'props' )
				cursor2.execute(  cmdIdno )
				rowIdno = cursor2.fetchone()
				nidno = rowIdno[0]
				nextIdno = nidno + 1
				cmdIdno = "update counter set number = %s where file = '%s'" % ( nextIdno, 'props' )

				cursor2.execute(  cmdIdno )

				cmdInsert = "insert into props ( idno, propid, piidno, gid, nights, instr, datein, dateout, sem, \
				first, last, username, ulogin, pep, public ) values \
				('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
				% ( nidno, propid, useridno, gid, nights, instr, datein, dateout, sem, first, last, username, \
				ulogin, newpep,  'OFF' ) 

				post_text += 'Props Insert: ' + cmdInsert
				cursor2.execute(  cmdInsert )

				newpropidno = nidno

				cmdIdno = "select number from counter where file = '%s' " % ( 'alloc' )
				cursor2.execute(  cmdIdno )
				rowIdno = cursor2.fetchone()
				nidno = rowIdno[0]
				nextIdno = nidno + 1
				cmdIdno = "update counter set number = %s where file = '%s' " % ( nextIdno, 'alloc' )
				cursor2.execute(  cmdIdno )

				cmdInsert2 = "insert into alloc ( idno, propidno, datein, dateout, propid, gid, nights, instr, piidno, sem, \
				last, first, username, stn_flag, cal, order1, delivery, observers, remote, staff ) values \
				( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
				'%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
				% ( nidno, newpropidno, datein, dateout, propid, gid, nights, instr, useridno, sem, \
				last, first, username, 'N', 'Y', '1234', 'D', '', '', '' )

				post_text += 'Alloc Insert: ' + cmdInsert2 

				cursor2.execute(  cmdInsert2 )

				cmdUpdate = "update props set subidno='%s' where idno='%s' " % ( nidno, newpropidno )

				post_text += 'Props Update: ' + cmdUpdate

				cursor2.execute(  cmdUpdate )


	#        		$result=mysql_query("insert into propinst (propidno, instr, propid, gid, code) values
	#			('$newpropidno','$instr','$propid','$gid','$code')");

	
	pagename = '<center><b>Make OPAL Semester IDs</b> | ' + username + " [" + end + ']<br><br>' 
	
#	pagename += logproc.getMenu()

#	cursor.execute("select idno, car, start, end, recur, type, warning, status from blackres where idno = '%s'" % ( idno ) )

#	cursor.execute("select car, loc, phone, pass, type, seq, idno, status, wheels, comment from cars where car = '%s'" % ( car ) )
#	numrows=cursor.rowcount

	maintext = pagename 

	if method == 'GET' :

		maintext += "<form method=post action='propsmake.py?'><br>"

		maintext += "<table spacing=2 cellpadding=2>"
		maintext += "<td align=right>"
		maintext += " <FONT FACE='Arial,Helvetica' SIZE=2><b>Semester:</b></td>"
		maintext += "<td><FONT FACE='Arial,Helvetica' SIZE=2><INPUT type='text' name='sem' size=5 value=''></td></tr>"
		maintext += "<td align=right><FONT FACE='Arial,Helvetica' SIZE=2><b>SV/OT/EN:</b></td> \
		<td><FONT FACE='Arial,Helvetica' SIZE=2><INPUT type='text' name='type' size=10 value='OT'></td></tr>"

		maintext += "<td align=right><FONT FACE='Arial,Helvetica' SIZE=2><b>1st PropID:</b></td> \
		<td><FONT FACE='Arial,Helvetica' SIZE=2><INPUT type='text' name='propseq' size=10 value=''></td></tr>"

		maintext += "<td align=right><FONT FACE='Arial,Helvetica' SIZE=2><b>MakeNumber (max 99) :</b></td> \
		<td><FONT FACE='Arial,Helvetica' SIZE=2><INPUT type='text' name='makenum' size=2 value='20'></td></tr>"

		maintext += "<td align=right><FONT FACE='Arial,Helvetica' SIZE=2><b>StartDate:</b></td> \
		<td><FONT FACE='Arial,Helvetica' SIZE=2><INPUT type='text' name='sdate' size=10 value='%s'></td></tr>" % ( today )

		maintext += "</table><BR></td><td valign=top>"

		maintext += "</table><BR>"
		maintext += "<input type=submit name='action' value='Make Props'><br>"
		maintext += "</form>"

	else:

		maintext += 'POST: ' + post_text


else :

	maintext = logproc.returnLogin()

#maintext='Test Mode: call Tom!<br>'

printHTML( maintext )
