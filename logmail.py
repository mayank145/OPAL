#! /usr/bin/python

import os
import sys
import datetime
import dbconnect
import cgi
import cgitb; cgitb.enable();
import MySQLdb
import logproc

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()
cursor5=db.cursor()
cursor6=db.cursor()
cursor7=db.cursor()

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
#	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

#def main() :

# MariaDB [sumlogs]> desc days;
# +---------+--------------+------+-----+---------+----------------+
# | Field   | Type         | Null | Key | Default | Extra          |
# +---------+--------------+------+-----+---------+----------------+
# | idno    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | date    | date         | YES  | MUL | NULL    |                |
# | day     | char(10)     | YES  |     | NULL    |                |
# | to1     | char(20)     | YES  |     | NULL    |                |
# | to1loc  | char(20)     | YES  |     | NULL    |                |
# | to2     | char(20)     | YES  |     | NULL    |                |
# | to2loc  | char(20)     | YES  |     | NULL    |                |
# | io1     | char(20)     | YES  |     | NULL    |                |
# | io1loc  | char(20)     | YES  |     | NULL    |                |
# | io2     | char(20)     | YES  |     | NULL    |                |
# | io2loc  | char(20)     | YES  |     | NULL    |                |
# | dc1     | char(40)     | YES  |     | NULL    |                |
# | dc2     | char(40)     | YES  |     | NULL    |                |
# | toin    | datetime     | YES  |     | NULL    |                |
# | toout   | datetime     | YES  |     | NULL    |                |
# | ioin    | datetime     | YES  |     | NULL    |                |
# | ioout   | datetime     | YES  |     | NULL    |                |
# | dcin    | datetime     | YES  |     | NULL    |                |
# | dcout   | datetime     | YES  |     | NULL    |                |
# | sky     | char(20)     | YES  |     | NULL    |                |
# | seeing  | char(20)     | YES  |     | NULL    |                |
# | temp    | char(20)     | YES  |     | NULL    |                |
# | wind    | char(20)     | YES  |     | NULL    |                |
# | humid   | char(20)     | YES  |     | NULL    |                |
# | comment | varchar(100) | YES  |     | NULL    |                |
# +---------+--------------+------+-----+---------+----------------+
# 25 rows in set (0.00 sec)


now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

today2 = datetime.date.today()
tmrw = today2 + datetime.timedelta( days = 1 )
tmrw_txt = tmrw.strftime('%Y-%m-%d')

#username, end, term = logproc.getUsername()
username = 'winegar'

if field.has_key('logdate'):

	logdate = field['logdate'].value
	
else:
	
	logdate = today
	
date=date.strip()
	
if field.has_key('logcrew'):

	logcrew = field['logcrew'].value
	
else:
	
	logcrew = 'TO'


		
pagename = '<center><b>Summit Log Email - ' + logdate + '</b><br>' + '[ ' + username + ' ' + logcrew + ' expires: ' + end + ' ]<br><br><a href=loglist.py>Return to LogList</a><br></center>'
#pagename = '<center><b>Summit Log - ' + date + '</b><br>' + '[ ' + username + ' ' + ' ]<br><br><a href=loglist.py>Return to LogList</a><br></center>'

maintext = pagename

#maintext = ''

cursor.execute("select date, day, dc1, dc2, dcout, to1, toout, io1, ioout, idno, to1loc, \
to2loc, io1loc, io2loc, to2, io2, sky, seeing, temp, wind, humid, comment, dcin, toin, ioin from days where date = '%s' " % ( logdate ) )
#cursor2.execute("select date, day from days where date = '%s' " % ( date1 ) )
numrows = cursor.rowcount
#numrows = 0
maintext += 'rows: ' + str( numrows ) + '<br>' + logdate
#maintext += "<form method=post action='./logone.py?'>"

# outside frame
maintext += 'SciOps Night Log - %s' % ( logdate )

# left column
maintext += '<tr><td valign=top>'

if numrows == 1 :

	row = cursor.fetchone()
	
	date = str( row[0] )
	day = row[1]


	dc1 = row[2]
	dc2 = row[3]
	dcout = str( row[4] )
	dcout = dcout[5:16]
	
	dcin = str( row[22] )
	dcin = dcin[5:16]

	to1 = row[5]
	
	toout = str( row[6] )
	toout = toout[5:16]
	
	toin = str( row[23] )
	toin = toin[5:16]

	to1loc = str( row[10] )

	to2 = row[14]
	to2loc = str( row[11] )


	io1 = row[7]
	
	ioout = str( row[8] )
	ioout = ioout[0:16]

	ioin = str( row[24] )
	ioin = ioin[5:16]
	
	io1loc= str( row[12] )
	
	io2 = row[15]
	io2loc = str( row[13] )
	
	
	idno = str( row[9] )

	sky = row[16]
	seeing = row[17]
	temp = row[18]
	wind = row[19]
	humid = row[20]
	comment = row[21]
	
# items query

# all 3
	cursor3.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user from items where date = '%s' order by itemtime" % ( date ) )
	numrows3_all = str( cursor3.rowcount ) 

# dc 4
	cursor4.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user from items where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'DC' ) )
	numrows4_dc = str( cursor4.rowcount )
# wp 5	
	cursor5.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user from items where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'WP' ) )
	numrows5_wp = str( cursor5.rowcount )
# to 6
	cursor6.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user from items where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'TO' ) )
	numrows6_to = str( cursor6.rowcount )
	
# crew section

	if method == 'GET' or method == 'POST'  : 
#	if  method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter' ) : 

		types = ( 'Comment', 'Trouble', 'Summary', 'Warning' )

		subsystems = ( 'None', 'Tel', 'Inst', 'SOSS', 'Weather', 'Operations', 'Others', '' )
		
		statii = ( 'Completed', 'Cancel', 'Incomplete' )
		
		status2 = "<select name=status size=1>"
		for stati in statii :
			if stati == 'status' :
				status2 += "<option value=%s selected>%s" % ( stati, stati )
			else:
				status2 += "<option value=%s>%s" % ( stati, stati )
		
		status2 += "</select>"

		logtypes2 = "<select name=type size=1><option value='Comment' selected>Comment<option value='Error'>Error<option value='Warning'>Warning</select>"
		subsystems2 = "<select name=subsystem size=1><option value='None' selected>None<option value='Tel'>Tel<option value='Inst'>Inst"
		subsystems2 += "<option value=SOSS>SOSS<option value=Weather>Weather<option value=Operations>Operations<option value=Other>Other</select>"


		formtxt = "<center><form method=post action='./logone.py?'><input type=submit name=action value='Edit'>"
		formtxt += "<input type=hidden name=date value='%s'></center><br></form>" % ( date ) 
# Crews		
		crewtxt = ''
		crewtxt += '<table cellpadding=5 cellspacing=5><tr>'
		crewtxt += '<td colspan=4 align=left bgcolor=lightgray><b>Day Crew</b> || In: %s | Out: %s |</td></tr>' % ( dcin, dcout )
		crewtxt += '<td bgcolor=lime>DC1: </td><td colspan=3>' + dc1 + '</td></tr>'
		crewtxt += '<td bgcolor=lime>DC2: </td><td colspan=3>' + dc2  + '</td></tr>'
		crewtxt += '<td colspan=4 align=left bgcolor=lightgray><b>Night Crew</b> || In: %s | Out: %s |</td></tr>' % ( toin, toout )
		crewtxt += '<td bgcolor=lime>TO1: </td><td>' + to1 + ' @ '+ to1loc + ' | </td><td bgcolor=lime>IO1: </td><td>' + io1 + ' @ '+ io1loc + ' | </td></tr>'
		crewtxt += '<td bgcolor=lime>TO2: </td><td>' + to2 + ' @ '+ to2loc + ' | </td><td bgcolor=lime>IO2: </td><td>' + io2 + ' @ '+ io2loc + ' | </td></tr>'
		crewtxt += '</table>'
		
		dcentry = "<form method=post action=./logone.py?date=%s><input type=hidden name=logcrew value='DC' size=3><table>" % ( date )
		dcentry += "<tr><td colspan=2 bgcolor=lightgray>Day Crew - Item Entry | <input type=submit name=action value='Enter'></td></tr>"
#		dcentry += "<tr><td>Time:</td><td>%s Type: %s DownTimeMin: %s Subsystem: %s Crew: %s</td></tr>" % ( itemtime, type, downtime, subsystem, logcrew )
		dcentry += "<tr><td>Title:</td><td><input type=text name=itemtitle value='%s' size=80></td></tr>" % ( itemtitle )
		dcentry += "<tr><td valign=top>Text:</td><td><textarea name=itemtext rows=10 cols=80>%s</textarea></td></tr>" % ( itemtext )		
		dcentry += "<tr><td valign=top>Time:</td><td><input type=text name=itemtime value='00:00' size=3> || "
		dcentry += "Type: " + logtypes2 + " || Status: " + status2 + "</td></tr>"

		dcentry += "</table></form>"


		toentry = "<form method=post action=logone.py?date=%s><input type=hidden name=logcrew value='TO' size=3><table>" % ( date )
		toentry += "<tr><td colspan=2 bgcolor=lightgray>Night Crew - Item Entry | <input type=submit name=action value='Enter'></td></tr>"
		toentry += "<tr><td>Title:</td><td><input type=text name=itemtitle value='%s' size=80></td></tr>" % ( itemtitle )
		toentry += "<tr><td valign=top>Text:</td><td><textarea name=itemtext rows=10 cols=80>%s</textarea></td></tr>" % ( itemtext )		
		toentry += "<tr><td valign=top>Time:</td><td><input type=text name=itemtime value='00:00' size=3> || "
		toentry += "Type: " + logtypes2 + " || DownTimeMin: <input type=text name=downtime value='0' size=1> || Subsystem: " + subsystems2 + "</td></tr>"
		toentry += "</table></form>"
		


		alllog = ''
		
		if numrows3_all > 0 :
		
			alllog += '<table>'
			for row in cursor3.fetchall() :

				item_idno = row[0]
				loglogcrew = row[4]
				logtime = str( row[5] )
				logtime = logtime[11:16]
				logtitle = row[6]
				logtext = row[7]
				logtype = row[8]
				logdowntime = row[9]
				logsubsystem = row[10]		
				logstatus= row[11]		
				loguser = row[12]		

				alllog += '<tr><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>[ %s ]</td><td valign=top><b>%s</b><br>Text: %s</td></tr>' % ( item_idno, logtime, loglogcrew, logtitle, logtext )

			alllog += '</table>' 
		else:
			alllog += 'No Items for All Logs'


		dclog = ''
		
		if numrows4_dc > 0 :
		
			dclog += '<table>'
			for row in cursor4.fetchall() :

				item_idno = row[0]
				logtime = str( row[5] )
				logtime = logtime[11:16]
				logtitle = row[6]
				logtext = row[7]
				logtype = row[8]
				logdowntime = row[9]
				logsubsystem = row[10]
				logstatus= row[11]		
				loguser = row[12]		

				dclog += '<tr><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>[ %s ]</td><td valign=top><FONT SIZE=3><b>%s</b><br>Text: %s</td></tr>' % ( item_idno, logtime, logcrew, logtitle, logtext )

			dclog += '</table>' 
		else:
			dclog += 'No Items for DC Logs'


		tolog = ''
		
		if numrows6_to > 0 :
		
			tolog += '<table>'
			for row in cursor6.fetchall() :

				item_idno = row[0]
				logtime = str( row[5] )
				logtime = logtime[11:16]
				logtitle = row[6]
				logtext = row[7]
				logtype = row[8]
				logdowntime = row[9]
				logsubsystem = row[10]
				logstatus= row[11]		
				loguser = row[12]		

				tolog += '<tr><td valign=top><a href=itemone.py?idno=%s><FONT SIZE=2>%s</a></td><td valign=top>[ %s ]</td><td valign=top><FONT SIZE=3><b>%s</b><FONT SIZE=2> ( %s )<br>Text: %s<br>Type: %s || Status: %s || Subsystem: %s || DownTimeMin: %s</td></tr>' % ( item_idno, logtime, logcrew, logtitle, loguser, logtext, logtype, logstatus, logsubsystem, logdowntime )

			tolog += '</table>' 

		else:
			tolog += 'No Items for TO Logs'

# left column end - start right column


# buttons for DC-Night-WP

		buttontxt = '<center><table cellspacing=5 cellpadding=5 rules=all border=1>'

		if logcrew == 'All' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>All - %s</a></td>' % ( 'pink', date, 'All', numrows3_all  )
		else:	
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>All - %s</a></td>' % ( 'yellow', date, 'All', numrows3_all )  

		if logcrew == 'DC' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>DayCrew - %s</a></td>' % ( 'pink', date, 'DC', numrows4_dc ) 
		else:
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>DayCrew - %s</a></td>' % ( 'yellow', date, 'DC', numrows4_dc ) 
				
		if logcrew == 'WP' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>WorkPlan - %s</a></td>' % ( 'pink', date, 'WP', numrows5_wp ) 
		else: 
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>WorkPlan - %s</a></td>' % ( 'yellow', date, 'WP', numrows5_wp ) 
		
		if logcrew == 'TO' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>Night - %s</a></td>' % ( 'pink', date, 'TO', numrows6_to )
		else:
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>Night - %s</a></td>' % ( 'yellow', date, 'TO', numrows6_to )  
					

		buttontxt += '</table></center><br>'

# 1-2 column break

		columntxt = '</td><td valign=top>'
		
# Weather

		weathertxt = '<table cellpadding=3 cellspacing=3><tr><td colspan=10 align=left bgcolor=lightgray><b>Weather</b> ||</td><tr>'
		weathertxt += '<td align=right bgcolor=lime>Sky: </td><td>' + sky + ' | </td><td bgcolor=lime>Seeing: </td><td>' + seeing + ' | </td><td bgcolor=lime>Temp: </td><td>' + temp + ' | </td><td bgcolor=lime>Wind: </td><td>' + wind + ' | </td><td bgcolor=lime>Humid: </td><td>' + humid + ' | </td></tr>'
		weathertxt += '<tr><td align=right bgcolor=lime>Comment:</td><td>' + comment + ' | </td>'
		weathertxt += '</tr></table>'


		cursor2.execute("select idno, dayidno, date, day, seq, instr, alloc, pi, ao1, ao2, intime, \
		outtime, obs1, obs2, obs3, obs1loc, obs2loc, obs3loc, ss, ssloc, others1, \
		others2, others1loc, others2loc, gid, propid from progs where date = '%s' order by seq" % ( date ) )
# Programs		
		progtxt = "<table cellpadding=3 cellspacing=3><tr><td colspan=5 bgcolor=lightgray><b>Observation Programs</b> || <a href=progone.py?date=%s&seq=0>Add Program</a></td></tr>" % ( date )
		
		numrows2 = cursor2.rowcount
				
		if numrows2 > 0 :

			for raw in cursor2.fetchall() :
		
				progidno = raw[0]
				seq = raw[4]
				
				instr = raw[5]	
				alloc = raw[6]
				pi = raw[7]
				ao1 = raw[8]	
				ao2 = raw[9]
				intime = str( raw[10] )	
				outtime = str( raw[11] )
				obs1 = raw[12]
				obs2 = raw[13]	
				obs3 = raw[14]
				obs1loc = raw[15]
				obs2loc = raw[16]	
				obs3loc = raw[17]
				ss = raw[18]
				ssloc = raw[19]
				others1 = raw[20]
				others2 = raw[21]
				others1loc = raw[22]
				others2loc = raw[23]
				gid = raw[24]
				propid = raw[25]

				progtxt += '<tr><td valign=top><a href=progone.py?idno=%s>Program %s</a></td>' % ( progidno, seq ) 
				progtxt += '<td>Instr: %s | Allocation: %s | PI: %s<br>AO1/2: %s / %s<br>' % ( instr, alloc, pi, ao1, ao2 ) 
				progtxt += 'GID: %s | PropID: %s<br>' % ( gid, propid ) 
				progtxt += 'StartTime: %s | EndTime: %s<br>' % ( intime, outtime ) 
				progtxt += 'Observers 1: %s | Location:  %s<br>' % ( obs1, obs1loc ) 
				progtxt += 'Observers 2: %s | Location:  %s<br>' % ( obs2, obs2loc ) 
				progtxt += 'Observers 3: %s | Location:  %s<br>' % ( obs3, obs3loc ) 
				progtxt += 'SA: %s | Location:  %s<br>' % ( ss, ssloc ) 
				progtxt += 'Others 1: %s | Location:  %s<br>' % ( others1, others1loc ) 
				progtxt += 'Others 2: %s | Location:  %s<br>' % ( others2, others2loc ) 
				progtxt += '</td></tr>' 
			
			
		else:
			progtxt += '<td colspan=5>No Programs for %s</td></tr>' % ( date ) 
			
					
		progtxt += '</table><br>'

# end right column

		progtxt += '</td></tr></table>'
		
#		maintext = maintext + crewtxt + buttontxt + weathertxt + progtxt

		if logcrew == 'All' :
		
			buttontxt += '<hr>' + alllog

		if logcrew == 'DC' :
		
			buttontxt += dcentry + '<hr>' + dclog
		
		if logcrew == 'TO' :
			
			buttontxt += toentry + '<hr>' + tolog
		
		maintext = maintext + buttontxt + columntxt + formtxt + crewtxt + weathertxt + progtxt
#		maintext = maintext

#	if  method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter' ) : 


else :

	maintext += '<tr><td colspan=8>No SummitLog Available for' + date + '</td></tr>'
	
maintext += '</table>'

maintext = 'tom' + logdate + ' '
printHTML( maintext )
	
