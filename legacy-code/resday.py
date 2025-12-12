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
import logproc3 as logproc

field = cgi.FieldStorage()

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

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "th.center { background-color: lemonchiffon; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 10px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold }"
	css_text += "</style>"


	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
#	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
# Cars pages refresh every hour 3600, 15 hour session.
	printpg += "<META HTTP-EQUIV='refresh' CONTENT='3600'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

#def main() :

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')

if 'date' in field :

	date = field['date'].value
	
else:
	
	date = today
	
date = date[0:10]
dateYear = date[0:4]
dateYear2 = int( date[0:4] ) + 1

dateYear3 = str( dateYear2 )


oneday = datetime.timedelta( days = 1 )

today1 = datetime.date ( int( date[0:4] ), int( date[5:7] ), int( date[8:10] ) )

today1Day = today1.strftime( '%a' )

yday = today1 - oneday
yday2 = yday.strftime( '%Y-%m-%d' )
yday2Day = yday.strftime( '%a' )

tday = today1 + oneday
tday2 = tday.strftime( '%Y-%m-%d' )
tday2Day = tday.strftime( '%a' )
  
locs = { 'B':'Base', 'H':'HP', 'S':'Sum', 'O':'Hilo', 'X':'None' }

if 'block' in field :

	block = field['block'].value
	
else:
	
	block = 'yes'
	
if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
	
	cursor6.execute( "select user from users where stnuser='%s'" % ( username ) ) 
	numrows6 = cursor6.rowcount

	driver = username
	if numrows6 == 1 :

		 fromUsers = cursor6.fetchone()
		 driver = fromUsers[0]

	checkDriver = '' + driver + ','
	checkCrew = '+' + logcrew2 + ','
		 
#	termlimit = str( now + term )

#	admin2_users = ( 'winegar', 'letawsky',  'noriko' )
	admin2_users = ( 'letawsky',  'noriko' )
	admin_users = ( 'letawsky', 'noriko', 'roth', 'vmpas', 'kaoki', 'takagi', 'ichi', 'harakawa', 'tak', 'terai', 'arai', 'koshida', 'lozi', 'kudotm', 'winegar' )
#	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar' )
#	admin_users = ( 'noriko', 'roth', 'winegar', 'jpr' )
	
	reserveAdmin = False 
	reserveAdmin2 = False 
		
	if username in admin_users :
	
		reserveAdmin = True 

	if username in admin2_users :
	
		reserveAdmin2 = True 
	
	pagename = '<center><b>Cars Today!</b> | ' + username + ' ' + logcrew2 + '<FONT SIZE=-1> | session ends: [' + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

	cursor.execute("select car, loc, phone, pass, type, seq, status, wheels, idno, comment, pass, \
	drivers from cars where status='Active' order by seq")
#	cursor.execute("select car, loc, phone, pass, type, seq, status, wheels, idno from cars where status='Active' order by seq")
	numrows=cursor.rowcount
	
	
	maintext = pagename 

#	maintext += 'rows: ' + str( numrows ) + ' date: ' + date + '<br>'
	maintext += "<FONT SIZE=-1><a href=resday.py?date=%s>< %s %s</a></font> | <FONT SIZE=+1><b>%s %s</b></font> | <FONT SIZE=-1><a href=resday.py?date=%s>%s %s ></a></font><br>" % ( yday2, yday2, yday2Day, date, today1Day, tday2, tday2, tday2Day )

	car_seq = 0
	
	if reserveAdmin2 == True :
	
		maintext += 'admin2 Display: <a href=resday.py?date=%s&block=yes>Hide-Blocks<a> | <a href=resday.py?date=%s&block=no>Show-Blocks</a> | checks: %s %s<br>' \
		 % ( date, date, checkDriver, checkCrew )
	
	maintext += '<table cellpadding=3 cellspacing=3><tr><td></td><td>'

	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>Car</th><th>Shift</th><th>Last Arrive Loc</th><th>24-hr Timeline</th></tr>'
	
	
	for row in cursor.fetchall() :

		car_seq += 1

		car = row[0]
		loc = row[1]
		phone = row[2]
		pass2 = str( row[3] )
		type = row[4]
		seq = row[5]
		status = row[6]
		wheels = row[7]
		car_idno = row[8]
		car_comment = row[9]
		car_comment = car_comment.strip()
		car_seats = row[10]
		car_drivers = row[11]
		car_drivers = car_drivers.strip()
		
		approvedDriver = False

		if car_drivers[0:4] == '+All' or car_drivers[0:3] == 'All' :

			approvedDriver = True
		
		else :
	
			if checkDriver in car_drivers or checkCrew in car_drivers :
			
				approvedDriver = True

		car = car.strip()
		
		cursor4.execute("select idno, car, start, end, recur, type, warning from blackres where car = '%s' and status='Active' order by start" % ( car ) )
		numrows4 = cursor4.rowcount
		
		wheel_type = wheels
		wheel_warning = ''

		wheel_type2 = 'Not-Shift'
		wheel_warning2 = 'No-Wheel-Warning'

		blackres_start2 = date
		blackres_end2 = date

#		bstatus = 'above blackres'
		bstatus = ''
	
		if numrows4 > 0 :
			
			for ruw in cursor4.fetchall() :
				
				blackres_car = ruw[1]
				blackres_start = str( ruw[2] )
				blackres_end = str( ruw[3] )
				blackres_recur = ruw[4]
				blackres_type = ruw[5]
				blackres_warning = ruw[6]

				blackres_recur = blackres_recur.strip()

				blackres_start2 = dateYear + '-' + blackres_start[5:10]
				blackres_end2 = dateYear3 + '-' + blackres_end[5:10]

				if blackres_recur == 'Yearly' :					
					
					if date >= blackres_start and date <= blackres_end :
						
#						bstatus='inside dates'
						
						wheel_type = blackres_type
						wheel_warning = blackres_warning
		

				if blackres_recur == 'Daily' and blackres_type == 'Shift-Car':			

					wheel_type2 = blackres_type
					wheel_warning2 = blackres_warning
		
# column for car info		
#		maintext +='<td>%s</td><td>%s<br>%s<br>%s (%S) %s</td>' % ( car_seq, car, wheel_type, wheel_warning, str( numrows4 ), bstatus )


# One Car Box
		car_comment2 = car_comment
		
		if len( car_comment ) > 0 :
		
			car_comment2 = '<br>' + car_comment

		if wheel_type == '4WD-Studs' or wheel_type2 == 'Shift-Car':
		
			maintext +='<td>%s</td><td bgcolor=lemonchiffon width=60><center><FONT SIZE=+1><b>%s</b></font> <FONT SIZE=-1>( %s - %sp )<br>%s %s<b>%s</b>' \
			% ( car_seq, car, wheel_type, car_seats, type, phone, car_comment2  )
			if len( wheel_warning ) > 0 :
				maintext += '<br>%s' % ( wheel_warning )
			maintext += '<br>%s</center></td>' % ( car_drivers )
			

		else :

			maintext +='<td>%s</td><td width=60><center><FONT SIZE=+1><b>%s</b></font> <FONT SIZE=-1>( %s - %sp )<br>%s %s<b>%s</b>' \
			% ( car_seq, car, wheel_type, car_seats, type, phone, car_comment2  )
			if len( wheel_warning ) > 0 :
				maintext += '<br>%s' % ( wheel_warning )
			maintext += '<br>%s</center></td>' % ( car_drivers )
			
# column for res info		

		add5 = datetime.timedelta( days = 5 )
		weeklook = today1 + add5
		date2 = weeklook.strftime("%Y-%m-%d")
		cursor4.execute("select idno, car from res where date > '%s' and date <= '%s' and car='%s' and status='Active'  \
		order by datein " % ( date, date2, car ) )
		numrows4 = cursor4.rowcount
		reserves5 = numrows4

		add30 = datetime.timedelta( days = 30 )
		monlook = today1 + add30
		date2 = monlook.strftime("%Y-%m-%d")
		cursor4.execute("select idno, car from res where date > '%s' and date <= '%s' and car='%s' and status='Active'  \
		order by datein " % ( date, date2, car ) )
		numrows4 = cursor4.rowcount
		reserves30 = numrows4

		if reserveAdmin == True :
#		if False :
		
#		if wheel_type2 == 'Not-Shift' or reserveAdmin == True :
			
			maintext +='<td><a href=shiftone.py?idno=0&date=%s&car=%s&overnight=%s>+Day-Shift</a><br>' % ( date, car, 'Daytime' )
			maintext +='<a href=shiftone.py?idno=0&date=%s&car=%s&overnight=%s>+Night-Shift</a><br>' % ( date, car, 'Overnight' )
		
		else:
		
			maintext +='<td><b>Shift-Car</b></a><br>'
			
#		if numrows4 > 0 :
		maintext += '5d=' + str( reserves5 ) + ', '
		maintext += '30d=' + str( reserves30 ) + '<br>'
#		maintext += 'black start' + blackres_start2 + '<br>'
#		maintext += 'black_end' + blackres_end2 + '<br>'
		maintext +='</td>'
# Last Arrive Column
		maintext +='<td class=center>'
		sub30 = datetime.timedelta( days = 30 )
		weeklooksub = today1 - sub30
		searchDate = weeklooksub.strftime("%Y-%m-%d")
		cursor5.execute("select idno, car, date, datein, dateout, driver, overnight, car2, blocking, destiny from res where date >= '%s' and date <= '%s' and ( car = '%s' or car2 = '%s' ) and status='Active'  \
		order by dateout desc " % (searchDate, yday2, car, car ) )
		numrows5 = cursor5.rowcount

#		maintext += str ( numrows5 )
		if numrows5 > 0 :
			seq = 0
			for rzw in cursor5.fetchall() :

				seq += 1
				lastdatein = rzw[3]	
				lastdatein=str(lastdatein)
				lasthourin = lastdatein[11:13]
				lastovernight = rzw[6]	
				lastdestiny = rzw[9]	
				finalArrive = lastdestiny[3:]
				arriveLoc = locs[finalArrive]
				lastdateout = rzw[4]
				if lastovernight == 'Overnight' :
	
#					lastdateout1 = lastdateout.strftime('%m-%d )-%H %a')	
					lastdateout1 = lastdateout.strftime('%m-%d )-%H')	
				else:
					lastdateout1 = lastdateout.strftime('%m-%d -%H')	
				if seq < 2:	
					if seq == 1 :
						maintext += '<b><FONT SIZE=+1>'			
#					maintext+= 'Last Arrived: ' + arriveLoc + ' ' + lastdestiny + ' ' + lastdateout1 + '<br>'
					maintext+= '' + arriveLoc + '</font></b><br> ' + lastdateout1 + '<br>'
#					if seq == 1 :
#						maintext += '</b>'			
		 
		maintext +='</td>'

# Res Box
		maintext +='<td>'
		
		cursor2.execute("select idno, car, date, datein, dateout, driver, overnight, car2, blocking, destiny from res where date = '%s' and ( car = '%s' or car2 = '%s' ) and status='Active'  \
		order by datein " % ( date, car, car ) )

		numrows2 = cursor2.rowcount
		numrowsTwo = numrows2


		cursor3.execute("select idno, car, date, datein, dateout, driver, overnight, car2, blocking, destiny from res where date = '%s' and overnight = 'Overnight' and ( car = '%s' or car2 = '%s' ) and status='Active'  \
		order by datein " % ( yday2, car, car ) )
		
		numrows3 = cursor3.rowcount
		numrowsThree = numrows3

		if numrows3 == 1 :
			
			raw = cursor3.fetchone()
			raws_idno = str( raw[0] )		
			raws_car = raw[1]
			raws_date = str( raw[2] )
				
			raws_datein = str( raw[3] )		
			raws_hourin = raws_datein[11:13]
			raws_dateout = str( raw[4] )
			raws_hourout = raws_dateout[11:13]

			raws_minout = raws_dateout[ 14:16 ]

			if raws_minout == '30' :
			
				new_hourout = int( raws_hourout ) + 1
				
				raws_hourout = str( new_hourout )

				if len( raws_hourout ) == 1 :
					
					raws_hourout = '0' + raws_hourout



			raws_driver = raw[5]
			raws_overnight = raw[6]
			raws_car2 = raw[7]
			raws_blocking = raw[8]
			raws_destiny = raw[9]
			raws_blocking = raws_blocking.strip()
	
			raws_calc_width = int( raws_hourout )
			raws_disp_width = str( 16 * raws_calc_width )



# Res Box

		boxtext = ''				

		seq = 0

		running_end = 0
		

		boxtext += '<table cellpadding=2 cellspacing=2>'
		boxtext += '<tr>'

		if numrows2 > 0 :

# Last Nights Overnight
			
			if numrows3 > 0 :

				calc_width4 = int( raws_hourout )
				disp_width4 = str( 16 * calc_width4 )
	
				boxtext += "<table>"
	#			boxtext += "<table><th width=%s>No Res for %s</th></tr>" % ( disp_width4, car  )
				boxtext += "<td width=%s bgcolor=lavender class=center valign=center><a href=resone.py?idno=%s>%s)~%s %s [%s]</a></td>" \
				% ( disp_width4, raws_idno, raws_hourin, raws_hourout,raws_driver,  raws_destiny[0]+raws_destiny[2:4]  )
				
				running_end = int( raws_hourout )
				
# Todays Reservations

			for row in cursor2.fetchall() :

				seq += 1
		
				res_idno = row[0]		
				res_car = row[1]
				res_date = str( row[2] )
					
				res_datein = str( row[3] )		
				res_hourin = res_datein[11:13]
				res_dateout = str( row[4] )
				res_hourout = res_dateout[11:13]

				res_minout = res_dateout[14:16]

				if res_minout == '30' :
			
					new_hourout = int( res_hourout ) + 1
				
					res_hourout = str( new_hourout )

					if len( res_hourout ) == 1 :
					
						res_hourout = '0' + res_hourout

				res_driver = row[5]
				res_overnight = row[6]
				res_overnight = res_overnight.strip()
				res_car2 = row[7]
				res_blocking = row[8]
				res_destiny = row[9]

#				if res_overnight == 'Overnight' :
				
#						res_hourout == '24'
#						running_end = 24
						
				calc_width = int( res_hourout ) - int( res_hourin )
				disp_width = str( 16 * calc_width )

# Add Res Green button before Res
 		
				if int( res_hourin ) > running_end :
					
#					if numrows3 == 0 :
			
					calc_width2 = int( res_hourin ) - running_end
					if calc_width2 < 3 :
						calc_width2 = 3
					disp_width2 = str( 16 * calc_width2 )
					
					running_endS = str( running_end )
					running_endS = running_endS.strip()
					
					if len( running_endS ) == 1 :
						
						running_endS = '0' + running_endS 
						
#					if ( res_blocking != 'Block-24' and wheel_type2 != 'Shift-Car' ) or ( reserveAdmin == True and block == 'yes' ) :
					if ( res_blocking != 'Block-24' and wheel_type2 != 'Shift-Car' and approvedDriver == True ) or ( reserveAdmin == True and block == 'yes' ) :
		
#						boxtext += "<td width=%s bgcolor=lime class=center valign=center>" % (  disp_width2  )
						boxtext += "<td width=%s bgcolor=palegreen class=center valign=center>" % (  disp_width2  )
						boxtext += "<a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>%s-%s</a></td>" % ( date, car, running_endS, res_hourin, running_end, res_hourin  )

					else :
					
						if res_blocking == 'Block-24' :
											
							boxtext += "<td width=%s bgcolor=pink class=center valign=center>" % (  disp_width2  )
							boxtext += "Block-24 %s</td>" % ( res_date  )
						
						if wheel_type2 == 'Shift-Car' :
#						
							boxtext += "<td width=%s bgcolor=pink class=center valign=center>" % (  disp_width2  )
							boxtext += "Shift-Car %s</td>" % ( res_date  )

						if approvedDriver == False :
#						
							boxtext += "<td width=%s bgcolor=pink class=center valign=center>" % (  disp_width2  )
#							boxtext += "NotApproved %s</td>" % ( res_date  )
							boxtext += "NotApproved</td>"

#						if reserveAdmin == True and block == 'no' :
	#						
#							boxtext += "<td width=%s bgcolor=pink class=center valign=center>" % (  disp_width2  )
#							boxtext += "+admin Show-Blocks %s</td>" % ( res_date  )
								

#					else:
#
#						calc_width3 = raws_calc_width
#						if calc_width3 < 3 :
#							calc_width3 = 3
#						disp_width3 = str( 8 * calc_width3 )
			
#						boxtext += "<td width=%s bgcolor=pink class=center valign=center>" % (  disp_width3  )
#						boxtext += "<a href=resone.py?idno=%s>%s-%s (%s)</a></td>" % ( raws_idno, 'Overnite-', raws_hourout, raws_driver  )

					
			
				running_end = int( res_hourout )
		
#				maintext += "date: %s hourin: %s hourout %s overnight: %s<br>" % ( res_date, res_hourin, res_hourout, res_overnight )
# Todays Daytime Res

				if res_overnight == 'Daytime' :
					
					boxtext += "<td width=%s bgcolor=blanchedalmond class=center valign=center>" % (  disp_width )
#					boxtext += "<td width=%s bgcolor=aliceblue class=center valign=center>" % (  disp_width )
					boxtext += "<a href=resone.py?idno=%s>%s-%s %s [%s]</a></td>" % ( res_idno, res_hourin, res_hourout, res_driver, res_destiny[0]+res_destiny[2:4] )

# Todays Overnight Res				
				else:
					
					calc_width3 = 24 - int( res_hourin )
					if calc_width3 < 3 :
						calc_width3 = 3
					disp_width3 = str( 16 * calc_width3 )
		
					boxtext += "<td width=%s bgcolor=lightblue class=center valign=center>" % (  disp_width3  )
					boxtext += "<a href=resone.py?idno=%s>%s~(%s %s [%s]</a></td>" % ( res_idno, res_hourin, res_hourout, res_driver, res_destiny[0]+res_destiny[2:4]  )
					
					running_end = 24
					#					hourTable += "<td><a href=resone.py?idno=%s>%s 00-23</a></td>" % ( res_idno, car, '00', '23' , car  )
								#		else:
#			maintext += "<a href=resone.py?idno=%s>%s-%s %s</a> - " % ( res_idno, res_datein[11:13], res_dateout[11:13], res_driver  )

#			if running_end <= 23 :
# Last Res -> End of Day 23

			if running_end <= 22 :

				calc_width3 = 24 - running_end
				if calc_width3 < 3 :
					calc_width3 = 3
				disp_width3 = 16 * calc_width3
				
				running_endS = str( running_end )
				running_endS = running_endS.strip()
				
				if len( running_endS ) == 1 :
					
					running_endS = '0' + running_endS 
				

				if ( res_blocking != 'Block-24' and wheel_type2 != 'Shift-Car' and approvedDriver == True ) or ( reserveAdmin == True and block == 'yes'  ) :
#				if True :
				
#					boxtext += "<td width=%s bgcolor=lime class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>%s-%s</a></td>" % (  disp_width3, date, car, running_endS, 24,  running_end, 24 )
					boxtext += "<td width=%s bgcolor=palegreen class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>%s-%s</a></td>" % (  disp_width3, date, car, running_endS, 24,  running_end, 24 )

				else :
				
					if res_blocking == 'Block-24' : 
				
						boxtext += "<td width=%s bgcolor=pink class=center valign=center>Block-24 for %s</a></td>" % (  disp_width3, date )

					if wheel_type2 == 'Shift-Car' : 
					
						boxtext += "<td width=%s bgcolor=pink class=center valign=center><b>%s</b>Shift-Car for %s</a></td>" % ( disp_width3, wheel_type2, wheel_warning2 )

					if approvedDriver == False :
#						
						boxtext += "<td width=%s bgcolor=pink class=center valign=center>" % (  disp_width2  )
#						boxtext += "NotApproved %s</td>" % ( res_date  )
						boxtext += "NotApproved</td>"

#					if reserveAdmin == True and block == 'no' : 
					
#						boxtext += "<td width=%s bgcolor=pink class=center valign=center><b>%s</b>+admin Show-Blocks for - %s</a></td>" % ( disp_width3, wheel_type2, wheel_warning2 )


					
			boxtext += '</tr></table>'
					
		else:

	
# If No Res Today - and None Yesterday
			
			if numrows3 == 0 :
				
				calc_width4 = 24
				disp_width4 = str( 16 * calc_width4 )
			
#				boxtext += "<table>"
				
				if ( wheel_type2 == 'Shift-Car' or approvedDriver == False ) and ( reserveAdmin == False or block == 'no' ) :
				
					if approvedDriver == False:
					
						wheel_type2 = '! Not-Approved-Driver !'
						wheel_warning2 = ''
						
	#			boxtext += "<table><th width=%s>No Res for %s</th></tr>" % ( disp_width4, car  )
					boxtext += "<td width=%s bgcolor=pink class=center valign=center><b>%s</b> - %s</a></td></tr></table>" % ( disp_width4, wheel_type2, wheel_warning2 )

				else:
#				
#					boxtext += "<td width=%s bgcolor=lime class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>Reserve 00-23</a></td></tr></table>" % ( disp_width4, date, car, '00', '23' )
					boxtext += "<td width=%s bgcolor=palegreen class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>Reserve 00-23</a></td></tr></table>" % ( disp_width4, date, car, '00', '23' )

# If No Res Today - but Res Exists from Yesterday

			else:
				
#				if running_end < 24  and 
#				''
				calc_width4 = int( raws_hourout )
				disp_width4 = str( 16 * calc_width4 )
				
				boxtext += "<table>"
#	#			boxtext += "<table><th width=%s>No Res for %s</th></tr>" % ( disp_width4, car  )
				boxtext += "<td width=%s bgcolor=lavender class=center valign=center><a href=resone.py?idno=%s>%s)~%s %s [%s]</a></td>" % ( disp_width4, raws_idno, raws_hourin, raws_hourout, raws_driver, raws_destiny[0]+raws_destiny[2:4]  )
##			boxtext += "<table cellpadding=2 cellspacing=2 border=2 rules=all><tr><th>0-6</th><th>6-12</th><th>12-18</th><th>18-24</th></tr>"
##				maintext += "<a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>Reserve %s 00-23</a></td></tr></table>" % ( date, car, '00', '23', car  )
##			boxtext += "<a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>00-23 [ free ] </a>" % ( date, car, '00', '23'  )
				calc_width4 = 24 - int( raws_hourout )
				disp_width4 = str( 16 * calc_width4 )

				if ( wheel_type2 == 'Shift-Car' or approvedDriver == False ) and ( reserveAdmin == False or block == 'no' ) :

#					boxtext += "<td width=%s bgcolor=pink class=center valign=center><b>%s</b> - %s</a></td></tr></table>" % ( disp_width4, wheel_type2, wheel_warning2 )
					boxtext += "<td width=%s bgcolor=pink class=center valign=center><b>%s</b>-%s</a></td></tr>" % ( disp_width4, wheel_type2, wheel_warning2 )

				else :
				
#					boxtext += "<td width=%s bgcolor=lime class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>%s-%s </a></td></tr>" % ( disp_width4, date, car, raws_hourout, 24, raws_hourout, 24 )
					boxtext += "<td width=%s bgcolor=palegreen class=center valign=center><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s>%s-%s </a></td></tr>" % ( disp_width4, date, car, raws_hourout, 24, raws_hourout, 24 )

				boxtext += "</table>"				
		

		maintext += boxtext

		maintext += "</td></tr>"
			
			
		
#		maintext += "<tr><td>%s</td><td><a href=carone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car_idno, car, loc, phone, pass2, type, status, wheels  )

	maintext += "</table>"

	maintext += "</td></tr></table>"

else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
