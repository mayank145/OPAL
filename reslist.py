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
cursor = db.cursor()
cursor2 = db.cursor()
cursor3 = db.cursor()

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

minus30 = datetime.timedelta( days = 30 )
then = now - minus30
month30 = then.strftime('%Y-%m-%d')

today=now.strftime('%Y-%m-%d')


if 'driver' in field :

 	driver2 = field['driver'].value
	
else:
	
#	driver = '.none'
	driver2 = 'None'

if 'date1' in field :

 	date1 = field['date1'].value
	
else:
	
#	driver = '.none'
	date1 = month30
	
if 'date2' in field :

 	date2 = field['date2'].value
	
else:
	
#	driver = '.none'
	date2 = today
	
	

driver2 = driver2.strip()

if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()

# driver4 = POST driver2
	
#	driver4 = driver2

	cursor3.execute("select user from users where stnuser = '%s'" % ( username ) )
	
	numrows3 = cursor3.rowcount
	
	if numrows3 == 1:
		
		users = cursor3.fetchone()
		
		real_username = users[0]
		real_username = real_username.strip()

# set driver2 ro LoginUser if POST driver <> login user and POST driver <> '.none.'
	
		if driver2 == 'None' :
			
			driver2 = real_username

#		else:
			
#			driver = driver2
	else:
		
		driver2 = username
		
				
#	driver = username
#	driver = driver.strip()
#	termlimit = str( now + term )
	
	pagename = '<center><b>Reservations Lists</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'


# Driver Spinner


	cursor3.execute( "select user from users order by user" )
	
	numrows3 = cursor3.rowcount

	driverSpin = '<select name=driver>'
	
	for result3 in cursor3.fetchall() :
	
		driver3 = result3[0]
		driver3 = driver3.strip()
	
		if driver3 == driver2 :
			
			driverSpin += "<option value='%s' selected>%s" % ( driver3, driver3 )
			
		else :
			
			driverSpin += "<option value='%s'>%s" % ( driver3, driver3 )
	
	driverSpin += '</select>'
	
	
	if driver2 == '.none' :

#		cursor.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, status, masterid, datea, datef, dateb, datec, dated, datee from res order by idno desc" )

		cursor.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, status, masterid, datea, datef, dateb, datec, dated, datee from res \
		where date >= '%s' and date <= '%s' order by datein desc"  % ( date1, date2 ) )

	else:
		
		
		inSearch = '%' + driver2 + '%'
		
#		cursor.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, status, masterid, datea, datef, dateb, datec, dated, datee from res where driver = '%s' \
#		or pass like '%s' or rpass like '%s' order by date desc" % ( driver, inSearch, inSearch ) )

		cursor.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, status, masterid, datea, datef, dateb, datec, dated, datee from res \
		where date >= '%s' and date <= '%s' and ( driver = '%s' or pass like '%s' or rpass like '%s' ) \
		order by datein desc" % ( date1, date2, driver2, inSearch, inSearch ) )
		
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
	
	maintext += "<form method=post action=reslist.py?> Select Driver/Pass (.none = All): %s | " % ( driverSpin )
#	maintext += dateTxt
	maintext += "DateIn: <input type=text name=date1 value=%s size=10> | DateOut: <input type=text name=date2 value=%s size=10>" % ( date1, date2 )

	maintext += " <input name=action type=submit value=Search></form>" 

	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>IDNo</th><th>Car</th><th>Date</th><th>ResIn</th><th>ResOut</th> \
	<th bgcolor=lime>Start-1</th><th bgcolor=lime>Arr-2</th><th bgcolor=lime>Dep-3</th><th bgcolor=lime>Arr-4</th><th bgcolor=lime>Dep-5</th><th bgcolor=lime>End-6</th><th>Overnight</th><th>Destiny</th><th>Driver</th><th>Pass</th><th>Hrs:Min:Sec</th></tr>'

	seq = 0

	for row in cursor.fetchall() :
		
		seq += 1

		res_idno = row[0]
		res_car = row[1]
		res_date = str( row[2] )
		res_datein = str( row[3] )
		res_dateout = str( row[4] )
		res_overnight = row[5]
		res_destiny = row[6]

		res_destiny = res_destiny.strip()

		res_driver = row[7]
		res_rdriver = row[8]
		res_pass = row[9]
		res_datea = row[13]
		res_datef = row[14]
		res_dateaS = str( row[13] )
		res_datefS = str( row[14] )

		res_dateb = row[15]
		res_datec = row[16]
		res_dated = row[17]
		res_datee = row[18]
		
		res_datebS = str( row[15] )
		res_datecS = str( row[16] )
		res_datedS = str( row[17] )
		res_dateeS = str( row[18] )
		
		
		dcodes = { 'B':'Base', 'H':'HP', 'S':'Sum', 'O':'Hilo', 'X':'None' }

#				ds = res_destiny.split()

		aDepart = dcodes [ res_destiny[0] ]
		bArrive = dcodes [ res_destiny[1] ]
		dArrive = dcodes [ res_destiny[2] ]
		fArrive = dcodes [ res_destiny[3] ]

		if bArrive == 'None' :
			
			bArrive = '-'
			
		if dArrive == 'None' :
			
			dArrive = '-'
#					destinyString += eArrive + '-' 
		
		if res_dateaS == 'None' :
			
			res_dateaS = '000000'
			

		if res_datefS == 'None' :
			
			res_datefS = '000000'

		if res_dateeS == 'None' :
			
			res_dateeS = '000000'
			
		hours = 0
		
		inYear = res_dateaS[0:4]
		
		outYear = res_datefS[0:4]
		
		dYear = res_datedS[0:4]

		eYear = res_dateeS[0:4]
		
		hours = 0
		minutes = 0
		seconds = 0

		hours2 = 0
		minutes2 = 0
		seconds2 = 0
		
		if int( inYear ) > 0 and int( outYear ) > 0 :
			
			elapsed = res_datef - res_datea
			
			hours, minutes, seconds = str( elapsed ).split(':')
					
			if res_destiny == 'HSHB' and int ( dYear ) > 0 and int( eYear ) > 0 :

				elapsed = res_dated - res_datea

				hours, minutes, seconds = str( elapsed ).split(':')

				elapsed2 = res_datef - res_datee
			
				hours2, minutes2, seconds2 = str( elapsed2 ).split(':')

#			hourcount = minutes * 50
#		if int(outYear) > 0 :
#			hours = elapsed.total_seconds() / 3600
			
#			minutesS = str( minutes )
			
#			hoursDuration = int(hours // (60*60))
			
#			hoursD = hoursDuration
#			hoursS = hoursS[0:5]
		
		dateAtxt = "<b>" + aDepart + "</b><br>"
		dateAtxt += res_dateaS[5:10] + "<br>"
		dateAtxt += res_dateaS[11:16] + "<br>"


		dateBtxt = "<b>" + bArrive + "</b><br>"
		dateBtxt += res_datebS[5:10] + "<br>"
		dateBtxt += res_datebS[11:16] + "<br>"

		dateCtxt = "<b>" + bArrive + "</b><br>"
		dateCtxt += res_datecS[5:10] + "<br>"
		dateCtxt += res_datecS[11:16] + "<br>"

		dateDtxt = "<b>" + dArrive + "</b><br>"
		dateDtxt += res_datedS[5:10] + "<br>"
		dateDtxt += res_datedS[11:16] + "<br>"

		dateEtxt = "<b>" + dArrive + "</b><br>"
		dateEtxt += res_dateeS[5:10] + "<br>"
		dateEtxt += res_dateeS[11:16] + "<br>"

		dateFtxt = "<b>" + fArrive + "</b><br>"
		dateFtxt += res_datefS[5:10] + "<br>"
		dateFtxt += res_datefS[11:16] + "<br>"
		
#		maintext += "<tr><td>%s</td><td><a href=resone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td> \
#		<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s:%s:%s</td></tr>" \
#		% ( seq, res_idno, res_idno, res_car, res_date[2:10], res_datein[2:16], res_dateout[2:16], res_dateaS[11:16], res_dateb[11:16], \
#		res_datec[11:16],res_dated[11:16],res_datee[11:16],res_datefS[11:16], res_overnight, res_destiny, res_driver, res_pass, hours, minutes, seconds )
		if res_destiny == 'HSHB' :

			maintext += "<tr><td>%s</td><td><a href=resone.py?idno=%s>%s</a></td><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td> \
			<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>HP-HP: %s:%s:%s<br>HP-Base: %s:%s:%s</td></tr>" \
			% ( seq, res_idno, res_idno, res_car, res_date[2:10], res_datein[5:16], res_dateout[5:16], dateAtxt, dateBtxt, \
			dateCtxt, dateDtxt, dateEtxt, dateFtxt, res_overnight, res_destiny, res_driver, res_pass, hours, minutes, seconds, hours2, minutes2, seconds2 )
			
		else :
			
			maintext += "<tr><td>%s</td><td><a href=resone.py?idno=%s>%s</a></td><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td> \
			<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s:%s:%s</td></tr>" \
			% ( seq, res_idno, res_idno, res_car, res_date[2:10], res_datein[5:16], res_dateout[5:16], dateAtxt, dateBtxt, \
			dateCtxt, dateDtxt, dateEtxt, dateFtxt, res_overnight, res_destiny, res_driver, res_pass, hours, minutes, seconds )

	maintext += "</table>"
else :

	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
