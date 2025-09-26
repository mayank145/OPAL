#! /usr/local/python

# Thomas Willis Winegar - Subaru Telescope May 2021
# Car Times is the Login Required general use page for updating Times in transit
# It is limited to Current Date and Time, refreshes every two min
# see Car Times OPEN restimesOpen.py for the Login version

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
import logproc3 as logproc

field = cgi.FieldStorage()
method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor = db.cursor()
cursor2 = db.cursor()
cursor3 = db.cursor()
cursor4 = db.cursor()
cursor5 = db.cursor()
cursor6 = db.cursor()
cursor7 = db.cursor()
cursor3.execute("set autocommit = 1")
cursor4.execute("set autocommit = 1")

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
dt = now.strftime('%Y-%m-%d %H:%M:%S')

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "th.center { background-color: lemonchiffon; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
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
#	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
# refresh 300 secs 5 min
	printpg += "<META HTTP-EQUIV='refresh' CONTENT='300'>"

	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

def getWeather( today2, yesterday2, yesterday4, deg ) :

#	weatherFile = './weather2.txt'
	weatherFile = './weather.txt'
	weatherData = ''	
	weatherLog2 = ''
#	hourin = dt[11:13]
#	source='Keck'

	source='Subaru'
	maintable = '<table><td><FONT SIZE=+1><center><b>Summit Weather - %s</font></b> | <a href=restimes.py?>&deg;C</a> | <a href=restimes.py?deg=F>&deg;F</a></b><br>' % ( source )
	
	if os.path.exists( weatherFile ) :
		weatherWritten = os.path.getmtime( weatherFile )
#		weatherWritten2 = str( weatherWritten ) 
		weatherWritten2 = datetime.datetime.fromtimestamp( weatherWritten )  
		weatherWritten4 = weatherWritten2.strftime('%H:%M')  
#		weatherWritten3 = weatherWritten2.strftime('%Y-%m-%d %H:%M')  
		weatherage = now - weatherWritten2
		weatherAge2 = weatherage.total_seconds()
#		weatherMin =  weatherAge2 / 60  				 
		weatherMin =  int( weatherAge2 ) 				 
		weatherString = str(weatherMin) + 's'

#		weatherMin = round (weatherMin, 0 )				 
		if weatherMin > 120 :

			weatherMin = int( weatherMin / 60 )
			weatherString = str( weatherMin ) + 'm'

#		weatherWritten3 = 'collected '+ str(weatherMin) + 's before refresh'	
		weatherWritten3 = 'collected '+ weatherString + ' before refresh at ' + weatherWritten4	
#		maintable += 'Weather File EXISTS at weather.txt<br>'
		FILE1 = open( weatherFile, "r" )
		tempData = FILE1.readline()
		rhData = FILE1.readline()
		hstData = FILE1.readline()
		FILE1.close()
		
		
		hstData2 = hstData.strip()
#		hstData2 = hstData.strip()
		
		tempData2=tempData[6:]
		tempData2=tempData2.strip()
#		tempData3 = int( tempData2 )
		rhData2=rhData[4:]
		rhData2=rhData2.strip()
#		rhData3 = int( rhData2 )
		
		weatherAlarm = 'Alarms: '
		
		currTemp2 = float ( tempData2 )
		avgF = ( currTemp2 * 1.8 ) + 32
		avgFRound = round( avgF, 1 )
		
		rhInt = int( rhData2 )
		
		Tdp = currTemp2 - ( ( 100 - rhInt ) / 5 )
#		Tdp = currTemp2 - ( ( 103 - rhInt ) / 5 )
		TdpRound = round( Tdp, 1 )
		
		
		dewpoint = str( TdpRound )
		
#		weatherAlarm = 'Temp: <b>' + tempData2 + '</b> C | RH: <b>' + rhData2 + '</b>% |<br>'  + " <br>"
		if deg == 'C' :
		
#			maintable += '<FONT SIZE=+1>Temp:</font> <FONT SIZE=+2><b>' + tempData2 + '</b>&deg;</font>C | <FONT SIZE=+2><b>'+ str( avgFRound )+ '</b>&deg;</font>F | RH: <FONT SIZE=+2><b>' + rhData2 + '</b></font> %<br>'  + hstData2 + " DewPoint: " + dewpoint + "&deg; C<br></font>"
			maintable += '<FONT SIZE=+1>Temp:</font> <FONT SIZE=+2><b>' + tempData2 + '</b>&deg;</font>C | <FONT SIZE=+2><b>'+ str( avgFRound )+ '</b>&deg;</font>F | <FONT SIZE=+1>RH:</font> <FONT SIZE=+2><b>' + rhData2 + '</b></font> %<br>'  \
			+ hstData2 + "</font>"

		else :
		
#			maintable += '<FONT SIZE=+1>Temp:</font> <FONT SIZE=+2><b>'+ str( avgFRound ) + '</b>&deg;</font>F | <FONT SIZE=+2><b>' + tempData2 + '</b>&deg;</font>C | RH: <FONT SIZE=+2><b>' + rhData2 + '</b></font> %<br>'  \
#			+ hstData2  + " DewPoint: " + dewpoint +"&deg; C<br></font>"
			maintable += '<FONT SIZE=+1>Temp:</font> <FONT SIZE=+2><b>'+ str( avgFRound ) + '</b>&deg;</font>F | <FONT SIZE=+2><b>' + tempData2 + '</b>&deg;</font>C | <FONT SIZE=+1>RH:</font> <FONT SIZE=+2><b>' + rhData2 + '</b></font> %<br>'  \
			+ hstData2  + "</font>"
#
		maintable += '<font size=-1><i>' + weatherWritten3 + '</i>'
		weatherData = 'TEST: ' + "<br>"
	else :

		maintable += 'No Weather File at weather.txt'

#	maintable += '<font size=-1><i>' + weatherWritten3 + '</i>'
	maintable += '</center></td><td valign=top>'

		
	weatherLog = '/var/www/html/sumlogs/weather/' + today2 + '.txt'
#	weatherLog = '/var/www/html/sumlogs/weather/tom.txt'

	hourin = '01'
	maintable += '<table cellpadding=2 cellspacing=2 border=2 rules=all>'
	maintable += '<tr><th>1-Day History</th><th>Hours</th><th>0</th><th>2</th><th>4</th><th>6</th><th>8</th><th>10</th><th>12</th>'
	maintable += '<th>14</th><th>16</th><th>18</th><th>20</th><th>22</th></tr>'
#	maintable += '<tr><td><center>Today<br>C<br>RH%</center></td>'
	
	if os.path.exists( weatherLog ) :

		maintable += '<td><center>Today</center></td><td><center>&deg;%s<br>RH</center></td>' % ( deg )

		FILE2 = open( weatherLog, "r" )
		loglines = FILE2.readlines()
		FILE2.close()
		
#			loglines.sort( reverse = True )
		
		logseq = 0
		logseq2 = 0
		loghour = '00'
		

		avgHour = '00'
		avgHourStart = '00'
		avgTemp = []
		avgRH = []
		avgTempRound = 0
		avgRHRound = 0
		
		avgHour0 = { '00':'00', '01':'00', '02':'02', '03':'02',\
		'04':'04', '05':'04', '06':'06', '07':'06',\
		'08':'08', '09':'08', '10':'10', '11':'10',\
		'12':'12', '13':'12', '14':'14', '15':'14',\
		'16':'16', '17':'16', '18':'18', '19':'18',\
		'20':'20', '21':'20', '22':'22', '23':'22' }

		countlines = len ( loglines )

		for line in loglines:
		
			logseq += 1
			logseq2 += 1

			lineSplit = line.split(' ')
	
#			if logseq2 == 1:
			
			avgHour = line[11:13]
			aHour = int(avgHour)
#			if aHour <= 2  :
				

			currTemp = lineSplit[2]
			currRH = lineSplit[3]

			currTemp2 = float ( currTemp )
			currRH2 = float ( currRH )
			

							
			avgTemp.append ( currTemp2 )
			avgRH.append ( currRH2 )

			avgHour2 = avgHour0[ avgHour ]
			if avgHourStart != avgHour2 or logseq >= countlines :
#			if logseq2 > 120 or logseq == countlines :
			
				logseq2 = 0
				avgHourStart = avgHour2
				if len( avgTemp ) > 0 and len( avgRH ) > 0 :
			
					avgTemp2 = sum ( avgTemp ) / len ( avgTemp )
					avgTempRound = round( avgTemp2, 1)


					avgF = ( avgTempRound * 1.8 ) + 32
					avgFRound = round( avgF, 1 )
					avgFRound2 = str( avgFRound )
					avgFRound2 = avgFRound2[:-2]

					avgRH2 = sum ( avgRH ) / len ( avgRH ) 
					avgRHRound = round( avgRH2, 1)

					bgcolor='white'
					if avgTempRound < 1 or avgRHRound > 80 :
						bgcolor='lemonchiffon'
					if avgTempRound < 0  or avgRHRound > 90:
						bgcolor='pink'
					

#						maintable += '<td>%s %s %s</td><td>%s</td><td>%s</td>' % ( logseq, logseq2, avgHour, avgTempRound, avgRHRound )
#					maintable += '<td bgcolor=%s><center>%s<br><b>%s</b><br><FONT SIZE=-1>%s</font></center></td>' % ( bgcolor, avgHour, avgTempRound, avgRHRound )
					if deg == 'C' :
					 
#						maintable += '<td bgcolor=%s><center><b>%s</b><br><FONT SIZE=-1>%s %s</font></center></td>' % ( bgcolor, avgTempRound, avgRHRound, avgHour2 )
						maintable += '<td bgcolor=%s><center><b>%s</b><br><FONT SIZE=-1>%s</font></center></td>' % ( bgcolor, avgTempRound, avgRHRound )

					else :
					
						maintable += '<td bgcolor=%s><center><b>%s</b><br><FONT SIZE=-1>%s</font></center></td>' % ( bgcolor, avgFRound2, avgRHRound )

#					avgHour = '00'
					avgTemp = []
					avgRH = []
					avgTempRound = 0
					avgRHRound = 0
				
				else:
				
					maintable += '<td bgcolor=%s><center>No Arrays</td>'
			
#			else:
			
#				maintable += '<td><120 Details %s</td>' % ( line )

	else:
	
		maintable += '<td>No Weather Log %s</td>' % ( weatherLog )


	weatherLog2 = '/var/www/html/sumlogs/weather/' + yesterday2 + '.txt'
#	weatherLog2 = '/var/www/html/sumlogs/weather/tom.txt'

	hourin = '01'
#		maintable += 'Yesterday<br><table cellpadding=2 cellspacing=2 border=2 rules=all>'

	maintable += '<tr><td><center>Yesterday</center></td><td><center>&deg;%s<br>RH</center></td>' % ( deg )
	
	if os.path.exists( weatherLog2 ) :

		FILE2 = open( weatherLog2, "r" )
		loglines = FILE2.readlines()
		FILE2.close()
		
#			loglines.sort( reverse = True )
		
		logseq = 0
		logseq2 = 0
		loghour = '00'
		

		avgHour = '00'
		avgTemp = []
		avgRH = []
		avgTempRound = 0
		avgRHRound = 0

		countlines = len ( loglines )

		for line in loglines :
		
			logseq += 1
			logseq2 += 1

			lineSplit = line.split(' ')
			
			if logseq == 1:
			
				avgHour = line[11:13]
		
			currTemp = lineSplit[2]
			currRH = lineSplit[3]
		
			currTemp2 = float ( currTemp )
			currRH2 = float ( currRH )
										
			avgTemp.append ( currTemp2 )
			avgRH.append ( currRH2 )

			if logseq2 > 120 or logseq >= countlines :
			
				logseq2 = 0
				
				if len( avgTemp ) > 0 and len( avgRH ) > 0 :
			
					avgTemp2 = sum ( avgTemp ) / len ( avgTemp )
					avgTempRound = round( avgTemp2, 1)


					avgF = ( avgTempRound * 1.8 ) + 32
					avgFRound = round( avgF, 1 )
					avgFRound2 = str( avgFRound )
					avgFRound2 = avgFRound2[:-2]

					avgRH2 = sum ( avgRH ) / len ( avgRH ) 
					avgRHRound = round( avgRH2, 1 )
					


					bgcolor='white'
					if avgTempRound < 1 or avgRHRound > 80 :
						bgcolor='lemonchiffon'
					if avgTempRound < 0  or avgRHRound > 90:
						bgcolor='pink'

					if deg == 'C' :
					
						maintable += '<td bgcolor=%s><center><b>%s</b><br><FONT SIZE=-1>%s</font></center></td>' % ( bgcolor, avgTempRound, avgRHRound )

					else :
					
						maintable += '<td bgcolor=%s><center><b>%s</b><br><FONT SIZE=-1>%s</font></center></td>' % ( bgcolor, avgFRound2, avgRHRound )
#						currhours += 1

					avgHour = '00'
					avgTemp = []
					avgRH = []
					avgTempRound = 0
					avgRHRound = 0
				
#		maintable += '</tr></table>'
		maintable += '</tr>'
	
		
	maintable += '</tr>'
		
#		maintable += '</tr>'
				
#		maintable += '</td></table>'
#		maintable += '</td></table>'


	maintable += '</table>'
	maintable += '</td></table>'

	return ( maintable )

	
#now = datetime.datetime.now()
#today = now.strftime('%Y-%m-%d')
#dt = now.strftime('%Y-%m-%d %H:%M:%S')

#oneday = datetime.timedelta ( days = 1 )
#tmrw = now - oneday

#today2 = now.strftime('%y%m%d')
#yday2 = tmrw.strftime('%y%m%d')


if 'date' in field :

	date = field['date'].value
	
else:
	
	date = today
	

if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

idno2 = int( idno )	

if 'type' in field :

	type = field['type'].value
	
else:
	
	type = 'UpdateA'
	
type = type.strip()

if 'driver' in field :

	driver = field['driver'].value
	
else:
	
	driver = ''

if 'rdriver' in field :

	rdriver = field['rdriver'].value

else:

	rdriver = ''
	
if 'pass2' in field :

	pass2 = field['pass2'].value

else:

	pass2 = ''

if 'rpass2' in field :

	rpass2 = field['rpass2'].value

else:

	rpass2 = ''

if 'monitor' in field :

	monitor = field['monitor'].value

else:

	monitor = ''

if 'deg' in field :

	deg = field['deg'].value

else:

	deg = 'C'
	
driver = driver.strip()
rdriver = rdriver.strip()
pass2 = pass2.strip()
rpass2 = rpass2.strip()
monitor = monitor.strip()

date = date[0:10]
	
oneday = datetime.timedelta( days = 1 )

today1 = datetime.date ( int( date[0:4] ), int( date[5:7] ), int( date[8:10] ) )
today1Day = today1.strftime( '%a' )

yday = today1 - oneday
yday2 = yday.strftime( '%Y-%m-%d' )
yday2Day = yday.strftime( '%a' )

tday = today1 + oneday
tday2 = tday.strftime( '%Y-%m-%d' )
tday2Day = tday.strftime( '%a' )


today2 = now.strftime('%y%m%d')

yesterday2 = yday.strftime('%y%m%d')

yesterday3 = yday - oneday
yesterday4 = yesterday3.strftime('%y%m%d')


if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
	
	updateComment = "no update"
	
#	weatherFile = '/var/www/html/sumlogs/access_module:x
	weatherData = getWeather( today2, yesterday2, yesterday4, deg )
#	weatherData = 'Weather Data is not reporting'
	
	if method == 'POST' and int( idno ) > 0 : 

# Edit Passenger Updates
	
		if field['action'].value == 'Save' and type == 'SavePass' :

			if len( driver ) > 0 :
				
				updateComment = "Update Save<br>" + str( dt ) + ' idno: ' + idno + ' date: ' + date 
				
				cursor3.execute("update res set driver = '%s' where idno = '%s'" % ( driver, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
				updateComment += "post Driver dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date + ' driver: ' + driver + "<br>"

			if len( rdriver ) > 0 :
						
				cursor3.execute("update res set rdriver = '%s' where idno = '%s'" % ( rdriver, idno2 ) )
				updateComment += "post RetDriver dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date + ' rdriver: ' + rdriver + "<br>"


			if len( pass2 ) > -1 :
				
				cursor3.execute("update res set pass = '%s' where idno = '%s'" % ( pass2, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
				updateComment += "post Pass dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date + ' pass: ' + pass2 + "<br>"

			if len( rpass2 ) > -1 :
				
				cursor3.execute("update res set rpass = '%s' where idno = '%s'" % ( rpass2, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
				updateComment += "post RPass dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date + ' rpass: ' + rpass2 + "<br>"

			if len( monitor ) > -1 :
			
				cursor3.execute("update res set monitor = '%s' where idno = '%s'" % ( monitor, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
				updateComment += "post Monitor dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date + ' monitor: ' + monitor + "<br>"

		
#		if field['action'].value == 'UpdateA' :
		if type == 'UpdateA' :
				
			cursor3.execute("update res set datea = '%s' where idno = '%s'" % ( dt, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post updateA dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Update-A %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )


		if type == 'UpdateB' :
				
			cursor3.execute("update res set dateb = '%s' where idno = '%s'" % ( dt, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post updateB dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Update-B %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'UpdateC' :
				
			cursor3.execute("update res set datec = '%s' where idno = '%s'" % ( dt, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post updateB dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Update-C %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'UpdateD' :
				
			cursor3.execute("update res set dated = '%s' where idno = '%s'" % ( dt, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post updateD dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Update-D %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'UpdateE' :
				
			cursor3.execute("update res set datee = '%s' where idno = '%s'" % ( dt, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post updateE dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Update-E %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'UpdateF' :
				
			cursor3.execute("update res set datef = '%s' where idno = '%s'" % ( dt, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post updateF dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Update-F %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

# Zero INputs for Clear Posting

		ts = '0000-00-00 00:00:00'

		if type == 'ClearA' :
		
			cursor3.execute("update res set datea = '%s' where idno = '%s'" % ( ts, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post clearA dt: " + str( ts ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Clear-A %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'ClearB' :
		
			cursor3.execute("update res set dateb = '%s' where idno = '%s'" % ( ts, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post clearB dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Clear-B %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'ClearC' :
		
			cursor3.execute("update res set datec = '%s' where idno = '%s'" % ( ts, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post clearC dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Clear-C %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'ClearD' :
		
			cursor3.execute("update res set dated = '%s' where idno = '%s'" % ( ts, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post clearD dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Clear-D %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'ClearE' :
		
			cursor3.execute("update res set datee = '%s' where idno = '%s'" % ( ts, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post clearE dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Clear-E %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

		if type == 'ClearF' :
		
			cursor3.execute("update res set datef = '%s' where idno = '%s'" % ( ts, idno2 ) )
#			cursor4.execute("update res set datea = '2020-06-02 09:00' where idno = '47'") % ( dt, idno2 )
			updateComment = "post clearF dt: " + str( dt ) + ' idno: ' + idno + ' date: ' + date 

			new_history = today + ' - ' + username + " - Clear-F %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno2 ) )

#	termlimit = str( now + term )
	
	pagename = '<center><b>Cars Travel Login</b> | ' + username + " [" + end + '] | ' 
	pagename += '<FONT SIZE=-1><i>refresh ~5min:</i> [%s] HST</FONT><br><br>' % ( dt )
#	weatherData ='None'
#	pagename += '<b>Weather: </b> ' + weatherData + '<br>' 
	pagename +=  weatherData + '<br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

	cursor.execute("select car, loc, phone, pass, type, seq, status, wheels, idno from cars where status='Active' order by seq")
	numrows=cursor.rowcount
	
	
	maintext = pagename 
#	maintext += 'rows: ' + str( numrows ) + ' date: ' + date + '<br>' + updateComment + "<br>"
	if username == 'twin' or username == 'winegar' :
	
		maintext += updateComment + "<br>"
	
	maintext += "<FONT SIZE=-1><a href=restimes.py?date=%s>%s %s</a></font> | <b>%s %s</b> | <FONT SIZE=-1><a href=restimes.py?date=%s>%s %s ></a></font><br>" % ( yday2, yday2, yday2Day, date, today1Day, tday2, tday2, tday2Day )
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>Car</th><th>#</th><th>Reservations</th></tr>'

# Cars Page Loop

	for row in cursor.fetchall() :

		car = row[0]
		loc = row[1]
		phone = row[2]
		pass2 = str( row[3] )
		type = row[4]
		seq = row[5]
		status = row[6]
		wheels = row[7]
		car_idno = row[8]
		
				
#		cursor2.execute("select idno, car, date, datein, dateout, driver, rdriver, overnight, datea, dateb, datec, dated, datee, datef, destiny, pass, rpass \
#		from res where date = '%s' and car = '%s' and status='Active' and overnight = 'Daytime' order by datein " % ( date, car ) )
# Todays are both Daytime and Overnight
		cursor2.execute("select idno, car, date, datein, dateout, driver, rdriver, overnight, datea, dateb, datec, dated, datee, datef, destiny, pass, rpass, car2, monitor, \
		year( datea ), year( dateb ), year( datec ), year( dated ), year( datee ), year( datef ), blocking \
		from res where date = '%s' and ( car = '%s' or car2 = '%s' ) and status='Active' order by datein " % ( date, car, car ) )
		numrows2 = cursor2.rowcount
		numrowsTwo = str( numrows2 )

		cursor3.execute("select idno, car, date, datein, dateout, driver, rdriver, overnight, datea, dateb, datec, dated, datee, datef, destiny, pass, rpass, car2, monitor, \
		year( datea ), year( dateb ), year( datec ), year( dated ), year( datee ), year( datef ), blocking \
		from res where date = '%s' and ( car = '%s' or car2 = '%s' ) and status='Active' and overnight = 'Overnight' order by datein " % ( yday2, car, car ) )

		numrows3 = cursor3.rowcount
		numrowsThree = numrows3

		
#		maintext += "<tr><td>%s</td><td><a href=carone.py?idno=%s>%s</a></td><td>" % ( seq, car_idno, car ) 
		maintext += "<tr><td>%s</td><td><center><FONT SIZE=+1><b>%s</b></font> (%s)<br>%s<br>%s | Seats: %sp</center></td><td>%s-%s</td><td>" % ( seq, car, wheels, type, phone, pass2, numrows2, numrows3  )
		innertext = '<table rules=all border=2 cellspacing=3 cellpadding=3><tr><th>Car</th><th>Depart</th><th>Arrive</th><th>Depart</th><th>Arrive</th><th>Depart</th><th>Arrive</th></tr>'

# The Single Overnight Reservatuin for One Car
# The Yesterday's Overnight Reaervation is first				

#		if False :
		if numrows3 == 1 :

			raw = cursor3.fetchone()
			res_idno = str( raw[0] )		
			res_car = raw[1]
			res_date = str( raw[2] )
	
			res_datein = str( raw[3] )		
			res_hourin = res_datein[11:13]
			res_dateout = str( raw[4] )
			res_hourout = res_dateout[11:13]
			res_driver = raw[5]
			res_rdriver = raw[6]
			res_overnight = raw[7]
		
			res_atime = str( raw[8] )
			res_btime = str( raw[9] )
			res_ctime = str( raw[10] )
			res_dtime = str( raw[11] )
			res_etime = str( raw[12] )
			res_ftime = str( raw[13] )
			
			res_atime = res_atime.strip()
			res_btime = res_btime.strip()
			res_ctime = res_ctime.strip()
			res_dtime = res_dtime.strip()
			res_etime = res_etime.strip()
			res_ftime = res_ftime.strip()
			
			res_destiny = raw[14]
			res_destiny=res_destiny[0:4]

			res_pass = raw[15]
			res_pass = res_pass.strip()
			res_rpass = raw[16]
			res_rpass = res_rpass.strip()
			res_car2 = raw[17]
			res_monitor = raw[18]
			res_monitor = res_monitor.strip()
			
			res_yearA = raw[19]
			res_yearB = raw[20]
			res_yearC = raw[21]
			res_yearD = raw[22]
			res_yearE = raw[23]
			res_yearF = raw[24]

			res_blocking = raw[25]
			
			
			dcodes = { 'B':'Base', 'H':'HP', 'S':'Sum', 'O':'Hilo', 'X':'None', 'K':'Kona', 'W':'Waimea' }

#				ds = res_destiny.split()

			aDepart = dcodes [ res_destiny[0] ]
			bArrive = dcodes [ res_destiny[1] ]
			dArrive = dcodes [ res_destiny[2] ]
			fArrive = dcodes [ res_destiny[3] ]

			destinyString = aDepart + '-' 
			
			if bArrive != 'None' :
				
				destinyString += bArrive + '-' 
#					destinyString += cArrive + '-' 
				
			if dArrive != 'None' :
				
				destinyString += dArrive + '-' 
#					destinyString += eArrive + '-' 
				
			destinyString += fArrive 

#			destinyString= aDepart + '-' + bArrive + '-' + dArrive + '-'+ fArrive 
		
#			innertext += "<tr>"
		
# Last Night OVernight Reservation Box				

#			innertext += "<td bgcolor=lemonchiffon><b>->Overnight Last Night</b><br><a href=resone.py?idno=%s>(%s) -> %s %s</a><br>P: %s<br>M: %s<br>%s</td>" \
#			% ( res_idno, res_hourin, res_hourout, res_driver, res_pass, res_monitor, destinyString )
			innertext += "<td bgcolor=lavender><b>->Overnight Last Night</b><br><a href=resone.py?idno=%s>%s)~%s %s</a><br>" % ( res_idno, res_hourin, res_hourout, res_driver )

# Edit Fields for Edit Pass

			if res_idno != idno or method == 'POST':
			
				if len( res_pass ) > 0 and res_pass != 'None' and res_pass != '.none' :

					innertext += "P: %s<br>" % ( res_pass )

				if len( res_rpass ) > 0 and res_rpass != 'None' and res_rpass != '.none' :

					innertext += "RP: %s<br>" % ( res_rpass )
					
				if len( res_monitor ) > 0 and res_monitor != 'None' and res_monitor != '.none':

					innertext += "M: %s<br>" % ( res_monitor )

			else:
	 
				if  method == 'GET' :
		# Driver Spinner
					cursor3.execute( "select user, train from users order by user" )

					numrows3 = cursor3.rowcount

					driver2 = '<select name=driver>'

					for result3 in cursor3.fetchall() :

						driver3 = result3[0]
						train3 = result3[1]
						driver3 = driver3.strip()

						driver3txt = driver3

						if train3 == 'P' :
	
							driver3txt = driver3 + ' (NoSum)'

						if driver3 == res_driver :
	
							driver2 += "<option value='%s' selected>%s" % ( driver3, driver3txt )
	
						else :
	
							driver2 += "<option value='%s'>%s" % ( driver3, driver3txt )

					driver2 += '</select>'


					cursor3.execute( "select user, train from users order by user" )
	
					numrows3 = cursor3.rowcount

					rdriver2 = '<select name=rdriver>'
	
					for result3 in cursor3.fetchall() :
	
						driver3 = result3[0]
						train3 = result3[1]
						driver3 = driver3.strip()
		
						driver3txt = driver3
		
						if train3 == 'P' :
			
							driver3txt = driver3 + ' (NoSum)'
	
						if driver3 == res_rdriver :
			
							rdriver2 += "<option value='%s' selected>%s" % ( driver3, driver3txt )
			
						else :
			
							rdriver2 += "<option value='%s'>%s" % ( driver3, driver3txt )
	
					rdriver2 += '</select>'
#					rdriver2=''
	
#				if  method == 'GET' and type == 'Edit'  :
		
#				innertext += 'tom<br>'
	
					innertext += "<form method=post action=./restimes.py?>"
#					innertext += "<input name=date type=hidden size=30 value='%s'><br>" % ( today )
					innertext += "<input name=date type=hidden size=30 value='%s'><br>" % ( date )
					innertext += "<input name=idno type=hidden size=30 value='%s'><br>" % ( res_idno )
					innertext += "<input type=hidden name=type value='%s'>" % ( 'SavePass' )									
#					innertext += " D: <input name=driver type=text size=30 value='%s'><br>" % ( res_driver )
					innertext += " D ] %s<br>RD ] %s<br>" % ( driver2, rdriver2 )
					innertext += " P ] <input name=pass2 type=text size=40 maxsize=100 value='%s'><br>" % ( res_pass )
					innertext += "RP ] <input name=rpass2 type=text size=40 maxsize=100 value='%s'><br>" % ( res_rpass )
					innertext += " M ] <input name=monitor type=text size=20 value='%s'><br>" % ( res_monitor )
					innertext += "<input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>"
					innertext += "</form>"


					
				
			innertext += "%s<br>" % ( destinyString )

			innertext += "<a href=./restimes.py?idno=%s&date=%s>[ Edit Pass ]</a>" % ( res_idno, date ) 

			if res_blocking == 'Block-24' :

				innertext += " - <b>Block-24</b>"
			
			
			innertext += "</td>"

# A-Time
			buttontxt = "<form method=post action=./restimes.py?>"
#				buttontxt += "<input name=action type=submit value='UpdateA'>" % ( 'UpdateA' )
			buttontxt += "<input name=action type=submit value='%s'>" % ( 'Depart ' + aDepart ) 
			buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
#			buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
			buttontxt += "<input type=hidden name=date value='%s'>" % ( date )
			buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateA' )
			buttontxt += "</form>"				

			bgcolorA = 'palegreen'
			bgcolorB = 'palegreen'
			bgcolorC = 'palegreen'
			bgcolorD = 'palegreen'
			bgcolorE = 'palegreen'
			bgcolorF = 'palegreen'
			
			bgcolorW = 'whitesmoke'
			bgcolorG = 'gainsboro'
					
#				if len( res_atime ) > 0 :
#			if res_atime[0:4] == '0000' :
#			if not res_atime == '0000-00-00 00:00:00' :		
					
#				bgcolorA ='pink'

#			if res_btime[0:4] == '0000' :
#			if not res_btime == '0000-00-00 00:00:00' :		
			
#				bgcolorB ='pink'
			
#			if res_ctime[0:4] == '0000' :
#			if not res_ctime == '0000-00-00 00:00:00' :		
		
#				bgcolorC ='pink'

#			if res_dtime[0:4] == '0000' :
#			if not res_dtime == '0000-00-00 00:00:00' :		
		
#				bgcolorD ='pink'
			
#			if res_etime[0:4] == '0000':
#			if not res_etime == '0000-00-00 00:00:00' :		
		
#				bgcolorE ='pink'

#			if res_ftime[0:4] == '0000' :
#			if not res_ftime == '0000-00-00 00:00:00' :		
		
#				bgcolorF ='pink'					
			
			
			
#				if len ( res_atime ) > 0 :

#			if not res_atime[0:4] == '0000' :
#			if aDepart == 'None'
#			if not res_atime == '0000-00-00 00:00:00' :

			if res_yearA > 0 or res_yearB > 0 or res_yearC > 0 or res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :

				if res_yearF > 0 :

					bgcolorW = bgcolorG
		
#				innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorA, aDepart, res_atime[11:16], buttontxt)
#				innertext += "<td bgcolor=%s><center><i>departed-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, aDepart, res_atime[11:16], buttontxt )
				innertext += "<td bgcolor=%s><center><i>departed-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, aDepart, res_atime[11:16], buttontxt )				
		
			else :

				innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorA, aDepart, ':' , buttontxt )
#				innertext += "<td bgcolor=%s><center>Depart-%s<br>%s</center></td>" % ( bgcolorA, aDepart, buttontxt )
			
# B-Time	
			buttontxt = "<form method=post action=./restimes.py>"
			buttontxt += "<input name=action type=submit value='%s'>" % (  'Arrive ' + bArrive )
			buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
#			buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
			buttontxt += "<input type=hidden name=date value='%s'>" % ( date )
			buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateB' )
			buttontxt += "</form>"				


#				if len ( res_btime ) > 0 :
#			if not res_btime[0:4] == '0000' :
			bArriveTxt = bArrive
			
			if bArrive == 'None' :

				buttontxt = ''
				bArriveTxt = ''

#			if not res_btime == '0000-00-00 00:00:00' :

			if res_yearB > 0 or res_yearC > 0 or res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :
		
				if res_yearF > 0 :

					bgcolorW = bgcolorG

				innertext += "<td bgcolor=%s><center><i>arrived-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, bArriveTxt, res_btime[11:16], buttontxt )


			else :
			
				innertext += "<td bgcolor=%s><center>Arrive-%s<br>%s<br>%s</center></td>" % ( bgcolorB, bArriveTxt, ':', buttontxt )

# C-Time
			buttontxt = "<form method=post action=./restimes.py>"
			buttontxt += "<input name=action type=submit value='%s'>" % ( 'Depart ' + bArrive )
			buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
#			buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
			buttontxt += "<input type=hidden name=date value='%s'>" % ( date )
			buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateC' )
			buttontxt += "</form>"				

#			if not res_ctime[0:4] == '0000' :
			if bArrive == 'None' :

				buttontxt = ''
				bArriveTxt = ''
				
#			if not res_ctime == '0000-00-00 00:00:00' :
			if res_yearC > 0 or res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :
		
				if res_yearF > 0 :

					bgcolorW = bgcolorG

				innertext += "<td bgcolor=%s><center><i>departed-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, bArriveTxt, res_ctime[11:16], buttontxt )


			else :
			
				innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorC, bArriveTxt, ':', buttontxt )

# D-Time
			buttontxt = "<form method=post action=./restimes.py>"
			buttontxt += "<input name=action type=submit value='%s'>" % ( 'Arrive ' + dArrive )
			buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
#			buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
			buttontxt += "<input type=hidden name=date value='%s'>" % ( date )
			buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateD' )
			buttontxt += "</form>"				

#			if not res_dtime[0:4] == '0000' :
			dArriveTxt = dArrive
			
			if dArrive == 'None' :

				buttontxt = ''
				dArriveTxt = ''
				
#			if not res_dtime == '0000-00-00 00:00:00' :
			if res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :
		
				if res_yearF > 0 :

					bgcolorW = bgcolorG
					
				innertext += "<td bgcolor=%s><center><i>arrived-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, dArriveTxt, res_dtime[11:16], buttontxt )

			else :
			
				innertext += "<td bgcolor=%s><center>Arrive-%s<br>%s<br>%s</center></td>" % ( bgcolorD, dArriveTxt, ':', buttontxt )
			
# E-Time

			buttontxt = "<form method=post action=./restimes.py>"
			buttontxt += "<input name=action type=submit value='%s'>" % ( 'Depart ' + dArrive )
			buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
#			buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
			buttontxt += "<input type=hidden name=date value='%s'>" % ( date )
			buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateE' )
			buttontxt += "</form>"				

#			if not res_etime[0:4] == '0000' :
			dArriveTxt = dArrive
			
			if dArrive == 'None' :

				buttontxt = ''
				dArriveTxt = ''

#			if not res_etime == '0000-00-00 00:00:00' :
			if res_yearE > 0 or res_yearF > 0 :
			
				if res_yearF > 0 :

					bgcolorW = bgcolorG
		
				innertext += "<td bgcolor=%s><center><i>depart-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, dArriveTxt, res_etime[11:16], buttontxt )

			else :
			
				innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorE, dArriveTxt, ':', buttontxt )
# F-Time

			buttontxt = "<form method=post action=./restimes.py>"
			buttontxt += "<input name=action type=submit value='%s'>" % ( 'Arrive ' + fArrive )
			buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
#			buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
			buttontxt += "<input type=hidden name=date value='%s'>" % ( date )
			buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateF' )
			buttontxt += "</form>"				

#			if not res_ftime[0:4] == '0000' :
#			if not res_ftime == '0000-00-00 00:00:00' :
			if res_yearF > 0 :
		
				innertext += "<td bgcolor=%s><center><i>arrived-%s</i><br>%s<br>%s</center></td>" % ( bgcolorG, fArrive, res_ftime[11:16], buttontxt )

			else :
			
#					innertext += "</td></tr>"
				innertext += "<td bgcolor=%s><center>Arrive-%s<br>%s<br>%s</center></td>" % ( bgcolorF, fArrive, ':', buttontxt )

	
			innertext += "</tr>"

# ToDays Reservations
#		if False :
		if numrows2 > 0 :
			
			seq = 0
			
			for raw in cursor2.fetchall() :
				
				seq += 1
				res_idno = str( raw[0] )

				res_car = raw[1]
				res_car = res_car.strip()

				res_date = raw[2]
				res_datein = str( raw[3] )
				res_dateout = str( raw[4] )
				res_driver = raw[5]
				res_rdriver = raw[6]
				res_overnight = raw[7]
				res_overnight = res_overnight.strip()
#				res_rdriver = raw[6]
#				res_rdriver = raw[7]
				res_hourin = res_datein[11:13]
				res_hourout = res_dateout[11:13]
				
				res_atime = str( raw[8] )
				res_btime = str( raw[9] )
				res_ctime = str( raw[10] )
				res_dtime = str( raw[11] )
				res_etime = str( raw[12] )
				res_ftime = str( raw[13] )

				res_atime = res_atime.strip()
				res_btime = res_btime.strip()
				res_ctime = res_ctime.strip()
				res_dtime = res_dtime.strip()
				res_etime = res_etime.strip()
				res_ftime = res_ftime.strip()

				res_destiny = raw[14]
				res_destiny=res_destiny[0:4]

				res_pass = raw[15]
				res_pass = res_pass.strip()
				res_rpass = raw[16]
				res_rpass = res_rpass.strip()
				res_car2 = raw[17]
				res_monitor = raw[18]

				res_yearA = raw[19]
				res_yearB = raw[20]
				res_yearC = raw[21]
				res_yearD = raw[22]
				res_yearE = raw[23]
				res_yearF = raw[24]

				res_blocking = raw[25]

				
				dcodes = { 'B':'Base', 'H':'HP', 'S':'Sum', 'O':'Hilo', 'X':'None', 'K':'Kona', 'W':'Waimea' }
				
#				ds = res_destiny.split()
				
				aDepart = dcodes [ res_destiny[0] ]
				bArrive = dcodes [ res_destiny[1] ]
				dArrive = dcodes [ res_destiny[2] ]
				fArrive = dcodes [ res_destiny[3] ]

				destinyString = aDepart + '-' 
				
				if bArrive != 'None' :
					
					destinyString += bArrive + '-' 
#					destinyString += cArrive + '-' 
					
				if dArrive != 'None' :
					
					destinyString += dArrive + '-' 
#					destinyString += eArrive + '-' 
					
				destinyString += fArrive 
				
#				destinyString= aDepart + '-' + bArrive + '-' + dArrive + '-'+ fArrive 
								
				innertext += "<tr>"

# Reservation Box				
				bgcolor = 'whitesmoke'
				
				if res_overnight == 'Overnight' :					
					
					bgcolor = 'lightblue'
					
					innertext += "<td bgcolor=%s><b>Overnight Tonight-></b><br><a href=resone.py?idno=%s>%s~(%s %s</a><br>" % ( bgcolor, res_idno, res_hourin, res_hourout, res_driver )
					
#					P: %s<br>M: %s<br>%s</td>" % ( bgcolor, res_idno, res_hourin, res_hourout, res_driver, res_pass, res_monitor, destinyString )
					
				else:
					
					bgcolor = 'blanchedalmond'
					
					innertext += "<td bgcolor=%s><a href=resone.py?idno=%s>%s-%s %s</a><br>" % ( bgcolor, res_idno, res_hourin, res_hourout, res_driver )

				if res_idno != idno or method == 'POST':


					if len( res_pass ) > 0 and res_pass != 'None' and res_pass != '.none' :

						innertext += "P: %s<br>" % ( res_pass )

					if len( res_rpass ) > 0 and res_rpass != 'None' and res_rpass != '.none' :

						innertext += "RP: %s<br>" % ( res_rpass )
					
					if len( res_monitor ) > 0 and res_monitor != 'None' and res_monitor != '.none':

						innertext += "M: %s<br>" % ( res_monitor )

				else:

					if  method == 'GET' :
			# Driver Spinner
						cursor3.execute( "select user, train from users order by user" )

						numrows3 = cursor3.rowcount

						driver2 = '<select name=driver>'

						for result3 in cursor3.fetchall() :

							driver3 = result3[0]
							train3 = result3[1]
							driver3 = driver3.strip()

							driver3txt = driver3

							if train3 == 'P' :

								driver3txt = driver3 + ' (NoSum)'

							if driver3 == res_driver :

								driver2 += "<option value='%s' selected>%s" % ( driver3, driver3txt )

							else :

								driver2 += "<option value='%s'>%s" % ( driver3, driver3txt )

						driver2 += '</select>'


						cursor3.execute( "select user, train from users order by user" )

						numrows3 = cursor3.rowcount

						rdriver2 = '<select name=rdriver>'

						for result3 in cursor3.fetchall() :

							driver3 = result3[0]
							train3 = result3[1]
							driver3 = driver3.strip()

							driver3txt = driver3

							if train3 == 'P' :
	
								driver3txt = driver3 + ' (NoSum)'

							if driver3 == res_rdriver :
	
								rdriver2 += "<option value='%s' selected>%s" % ( driver3, driver3txt )
	
							else :
	
								rdriver2 += "<option value='%s'>%s" % ( driver3, driver3txt )

						rdriver2 += '</select>'

	#				if  method == 'GET' and type == 'Edit'  :

	#				innertext += 'tom<br>'

						innertext += "<form method=post action=./restimes.py?>"
#						innertext += "<input name=date type=hidden size=30 value='%s'><br>" % ( today )
						innertext += "<input name=date type=hidden size=30 value='%s'><br>" % ( date )
						innertext += "<input name=idno type=hidden size=30 value='%s'><br>" % ( res_idno )
#						innertext += "<input name=date type=hidden size=30 value='%s'><br>" % ( date )
						innertext += "<input type=hidden name=type value='%s'>" % ( 'SavePass' )									
	#					innertext += " D: <input name=driver type=text size=30 value='%s'><br>" % ( res_driver )
						innertext += " D ] %s<br>RD ] %s<br>" % ( driver2, rdriver2 )
						innertext += " P ] <input name=pass2 type=text size=40 maxsize=100 value='%s'><br>" % ( res_pass )
						innertext += "RP ] <input name=rpass2 type=text size=40 maxsize=100 value='%s'><br>" % ( res_rpass )
						innertext += " M ] <input name=monitor type=text size=20 value='%s'><br>" % ( res_monitor )
						innertext += "<input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>"
						innertext += "</form>"


				
				innertext += "%s<br>" % ( destinyString )
				
				innertext += "<a href=./restimes.py?idno=%s&date=%s>[ Edit Pass ]</a>" % ( res_idno, date ) 
				
				if res_blocking == 'Block-24' :
	
					innertext += " - <b>Block-24</b>"
				
				innertext += "</td>"

				
# A-Time
				buttontxt = "<form method=post action=./restimes.py?>"
#				buttontxt += "<input name=action type=submit value='UpdateA'>" % ( 'UpdateA' )
				buttontxt += "<input name=action type=submit value='%s'>" % ( 'Depart ' + aDepart ) 
				buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
				buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
				buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateA' )
				buttontxt += "</form>"				

				bgcolorA = 'palegreen'
				bgcolorB = 'palegreen'
				bgcolorC = 'palegreen'
				bgcolorD = 'palegreen'
				bgcolorE = 'palegreen'
				bgcolorF = 'palegreen'

				bgcolorW = 'whitesmoke'
				bgcolorG = 'gainsboro'
							
#				if len( res_atime ) > 0 :
#				if not res_atime == '0000-00-00 00:00:00' :		
					
#					bgcolorA ='pink'

	#			if res_btime[0:4] == '0000' :
#				if not res_btime == '0000-00-00 00:00:00' :		
			
#					bgcolorB ='pink'
			
	#			if res_ctime[0:4] == '0000' :
#				if not res_ctime == '0000-00-00 00:00:00' :		
		
#					bgcolorC ='pink'

	#			if res_dtime[0:4] == '0000' :
#				if not res_dtime == '0000-00-00 00:00:00' :		
		
#					bgcolorD ='pink'
			
	#			if res_etime[0:4] == '0000':
#				if not res_etime == '0000-00-00 00:00:00' :		
		
#					bgcolorE ='pink'

	#			if res_ftime[0:4] == '0000' :
#				if not res_ftime == '0000-00-00 00:00:00' :		
		
#					bgcolorF ='pink'					
					
					
					
#				if len ( res_atime ) > 0 :

#				if not res_atime[0:4] == '0000' :

#				ayear = res_atime[0:4] 
#				if int( ayear ) > 0 :
#				if not res_atime == '0000-00-00 00:00:00' :
				if res_yearA > 0 or res_yearB > 0 or res_yearC > 0 or res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :

					if res_yearF > 0 :

						bgcolorW = bgcolorG
					
#					innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorA, aDepart, res_atime[11:16], buttontxt)
					innertext += "<td bgcolor=%s><center><i>departed-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, aDepart, res_atime[11:16], buttontxt )
				
				else :
					
					innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorA, aDepart, ':' , buttontxt )
					
# B-Time	
				buttontxt = "<form method=post action=./restimes.py>"
				buttontxt += "<input name=action type=submit value='%s'>" % (  'Arrive ' + bArrive )
				buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
				buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
				buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateB' )
				buttontxt += "</form>"


#				if len ( res_btime ) > 0 :
#				if not res_btime[0:4] == '0000' :
				bArriveTxt = bArrive

				if bArrive == 'None' :

					buttontxt = ''
					bArriveTxt = ''
					

#				byear = res_btime[0:4] 
				
#				if int( byear ) > 0 :

#				if not res_btime == '0000-00-00 00:00:00' :
				if res_yearB > 0 or res_yearC > 0 or res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :
					
					if res_yearF > 0 :

						bgcolorW = bgcolorG
				
					innertext += "<td bgcolor=%s><center><i>arrived-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW , bArriveTxt, res_btime[11:16], buttontxt )

				else :
					
					innertext += "<td bgcolor=%s><center>Arrive-%s<br>%s<br>%s</center></td>" % ( bgcolorB, bArriveTxt, ':', buttontxt )

# C-Time
				buttontxt = "<form method=post action=./restimes.py>"
				buttontxt += "<input name=action type=submit value='%s'>" % ( 'Depart ' + bArrive )
				buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
				buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
				buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateC' )
				buttontxt += "</form>"				
	
#				if not res_ctime[0:4] == '0000' :
				bArriveTxt = bArrive

				if bArrive == 'None' :

					buttontxt = ''
					bArriveTxt = ''

#				if not res_ctime == '0000-00-00 00:00:00' :
				if res_yearC > 0 or res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :
				

					if res_yearF > 0 :

						bgcolorW = bgcolorG
						
					innertext += "<td bgcolor=%s><center><i>departed-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, bArriveTxt, res_ctime[11:16], buttontxt )

				else :
					
					innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorC, bArriveTxt, ':', buttontxt )

# D-Time
				buttontxt = "<form method=post action=./restimes.py>"
				buttontxt += "<input name=action type=submit value='%s'>" % ( 'Arrive ' + dArrive )
				buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
				buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
				buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateD' )
				buttontxt += "</form>"				
	
#				if not res_dtime[0:4] == '0000' :
				dArriveTxt = dArrive
				
				if dArrive == 'None' :

					buttontxt = ''
					dArriveTxt = ''

#				if not res_dtime == '0000-00-00 00:00:00' :
				if res_yearD > 0 or res_yearE > 0 or res_yearF > 0 :

					if res_yearF > 0 :

						bgcolorW = bgcolorG
				
					innertext += "<td bgcolor=%s><center><i>arrived-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, dArriveTxt, res_dtime[11:16], buttontxt )

				else :
					
					innertext += "<td bgcolor=%s><center>Arrive-%s<br>%s<br>%s</center></td>" % ( bgcolorD, dArriveTxt, ':', buttontxt )
					
# E-Time

				buttontxt = "<form method=post action=./restimes.py>"
				buttontxt += "<input name=action type=submit value='%s'>" % ( 'Depart ' + dArrive )
				buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
				buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
				buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateE' )
				buttontxt += "</form>"				
	
#				if not res_etime[0:4] == '0000' :
				dArriveTxt = dArrive

				if dArrive == 'None' :

					buttontxt = ''
					dArriveTxt = ''
					
#				if not res_etime == '0000-00-00 00:00:00' :
				if res_yearE > 0 or res_yearF > 0 :

					if res_yearF > 0 :

						bgcolorW = bgcolorG
					
					innertext += "<td bgcolor=%s><center><i>departed-%s</i><br>%s<br>%s</center></td>" % ( bgcolorW, dArriveTxt, res_etime[11:16], buttontxt )
				

				else :
					
					innertext += "<td bgcolor=%s><center>Depart-%s<br>%s<br>%s</center></td>" % ( bgcolorE, dArriveTxt, ':', buttontxt )
# F-Time

				buttontxt = "<form method=post action=./restimes.py>"
				buttontxt += "<input name=action type=submit value='%s'>" % ( 'Arrive ' + fArrive )
				buttontxt += "<input type=hidden name=idno value='%s'>" % ( res_idno )
				buttontxt += "<input type=hidden name=date value='%s'>" % ( res_date )
				buttontxt += "<input type=hidden name=type value='%s'>" % ( 'UpdateF' )
				buttontxt += "</form>"				
	
#				if not res_ftime[0:4] == '0000' :

#				if not res_ftime == '0000-00-00 00:00:00' :
				if res_yearF > 0 :
				
					innertext += "<td bgcolor=%s><center><i>arrived-%s</i><br>%s<br>%s</center></td>" % ( bgcolorG, fArrive, res_ftime[11:16], buttontxt )

				else :
					
#					innertext += "</td></tr>"
					innertext += "<td bgcolor=%s><center>Arrive-%s<br>%s<br>%s</center></td>" % ( bgcolorF, fArrive, ':', buttontxt )
				
			innertext += "</tr>"
			
#				maintext += innertext


		
			
			
			
			innertext += "</table>"

#			maintext += innertext
					
#					hourTable += "<td><a href=resone.py?idno=%s>%s 00-23</a></td>" % ( res_idno, car, '00', '23' , car  )
								#		else:
#			maintext += "<a href=resone.py?idno=%s>%s-%s %s</a> - " % ( res_idno, res_datein[11:13], res_dateout[11:13], res_driver  )
					
		else:
			
			innertext += "</tr></table>"
				
		if numrows2 == 0 and numrows3 == 0 :
			
			noRes = True
#				innertext = "No Reservat"
			innertext = "<center><b>No Reserves for %s</b>" % ( car  )
#				innertext += "<a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>Reserve %s 00-23</a><br>" % ( date, car, '00', '23', car  )
			calc_width4 = 12
			disp_width4 = str( 12 * calc_width4 )
		
#			innertext += "<table><tr><td>No Reserves for %s</td></tr></table>" % ( car )
##			boxtext += "<table><th width=%s>No Res for %s</th></tr>" % ( disp_width4, car  )
#			innertext += "<td width=%s bgcolor=palegreen class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>Reserve 00-23</a></td></tr></table>" \
#			% ( disp_width4, date, car, '00', '23' )

#				maintext += "<tr><td colspan=4 bgcolor=palegreen><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>00-23 [ free ] </a></td></tr></table>" % ( date, car, '00', '23'  )				
# innertext removed 210710
		maintext += innertext
		maintext += "</td></tr>"
		
#	else:

#		maintext += "</td></tr>"
		
#		maintext += "</td></tr>"
	
	maintext += "</td></tr></table>"
	maintext += "bott inntertext table<br>"
			
			
		
#		maintext += "<tr><td>%s</td><td><a href=carone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car_idno, car, loc, phone, pass2, type, status, wheels  )

#	maintext += "</td></tr></table>all bottom table"

else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
