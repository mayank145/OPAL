#! /usr/local/python

import datetime
import cgi
import os
import cgitb; cgitb.enable();
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
#import logproc
import logproc3 as logproc
import dbconnect
import calendar
#from dateutil.relativedelta import relativedelta

field=cgi.FieldStorage()

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')



#maxday = now + datetime.timedelta( days = 15 )


if 'year' in field:

	year=field[ 'year' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	year=today[0:4]


if 'month' in field:

	month=field[ 'month' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	month=today[5:7]

if 'type' in field:

	type=field[ 'type' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	type = 'All'


if 'logcrew' in field:

	logcrew=field[ 'logcrew' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	logcrew = 'Reserves'


if 'searchUser' in field:

	searchUser=field[ 'searchUser' ].value

else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())

	searchUser = '.none'

searchUser = searchUser.strip()
	
method=os.environ.get("REQUEST_METHOD","")


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
	
#/* Style the tab */
	css_text += ".tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1;}"

#/* Style the buttons that are used to open the tab content */
	css_text += ".tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s;}"

#/* Change background color of buttons on hover */
	css_text += ".tab button:hover { background-color: #ddd; }"

#/* Create an active/current tablink class */
	css_text += ".tab button.active { background-color: #ccc; }"

#/* Style the tab content */
	css_text += ".tabcontent { display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }"	
	
	css_text += "</style>"

	toppg = ''
	toppg += "Content-type: text/html;\n\n"
	toppg += "<!DOCTYPE html>"
	toppg += "<HTML><HEAD>"
#	toppg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
#	printpg += "<META HTTP-EQUIV='refresh' CONTENT='120'>"
	toppg += "<META HTTP-EQUIV='refresh' CONTENT='3600'>"
	toppg += css_text
	
	bottompg = "</HEAD><BODY>"
	bottompg += maintext
	bottompg += "</BODY></HTML>"
	
	print( toppg )
	
	print( bottompg )


dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])

cursor = db.cursor()
cursor2 = db.cursor()
cursor3 = db.cursor()
cursor4 = db.cursor()
cursor5 = db.cursor()
cursor6 = db.cursor()
cursor7 = db.cursor()


dbconn2=dbconnect.opalconn()
db2=MySQLdb.connect( host=dbconn2[0], user=dbconn2[1], passwd=dbconn2[2], db=dbconn2[3] )

cursorOPAL=db2.cursor()
#cursor2=db.cursor()
#cursor3=db.cursor()
#cursor4=db.cursor()

#logcrew = 'Reserves'

if method == "POST" : 

	logcrew = field['action'].value

if logproc.validCookie() :
#if True :


	username, end, term, logcrew2 = logproc.getUsername()

	day = '1'

	nyear = int( year )

	nmonth = int( month )	

	nday = int( day )

	daystext =  "Year: " + year
	daystext += "Month: " + month
	daystext += "Day: " + day 
	#	 	get the date offset correct

	#	print out the days of the week
	months = [ 'Zero', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec' ]

	weekdays = [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri',  'Sat' ]

	instr2 = { 'COMICS':'COM', 'FOCAS':'FCS', 'IRCS':'IRC', 'IRCS+AO':'IRC', 'CHARIS':'CRS', 'HSC':'HSC', 'MOIRCS':'MCS', 'HDS':'HDS', 'IRD':'IRD', 'SUKA':'SUK', 'PFS':'PFS' }


	cursor2.execute("select user, email, stnuser, idno, privy, train, status, hourin, hourout, destiny from users where stnuser='%s' order by user" % ( username ))
	numrows2 = cursor.rowcount
	if numrows2 == 1 :
	
		raw=cursor2.fetchone()
		username_user = raw[0]
		username_email = raw[1]
		username_stnuser = raw[2]
	
	else :
	
		username_user = username


	cursor2.execute("select user, email, stnuser, idno, privy, train, status, hourin, hourout, destiny from users order by user")
	numrows2 = cursor2.rowcount

	searchSpinner = "<select name=searchUser size=1>"

	if numrows2 > 0 :

		for raw in cursor2.fetchall() :

			username2_user = raw[0]
			username2_user = username2_user.strip()
			
			if searchUser == username2_user :
			
				searchSpinner += "<option value='%s' selected>%s" % ( username2_user, username2_user )
			
			else :
			
				searchSpinner += "<option value='%s'>%s" % ( username2_user, username2_user )
			 
	searchSpinner += "</select>"


	types = ( 'All', 'Comment', 'Trouble', 'Summary', 'Warning' )

	logtypes1 = "<select name=type size=1>"

	for typ in types:

		if typ == type :

			logtypes1 += "<option value='%s' selected>%s" % ( typ, typ )
		else:
			logtypes1 += "<option value='%s'>%s" % ( typ, typ )


	logtypes1 += "</select>"




	maintext = "<center><b>Subaru Cars Calendar</b> | " + username + " [" + end + "] " + "<br><br>" + logproc.getMenu() +  "<br>"
	#maintext += "<form method=post action='./sumcal.py?date=%s'>%s | " % ( today, logtypes1 )
	maintext += logproc.getCarMenu() + "<br>"

	maintext += "<form method=post action='./carcal.py?date=%s'>" % ( today )
	maintext += "<input type=hidden name=year value='%s'>" % ( year )
	maintext += "<input type=hidden name=month value='%s'>" % ( month )

	if logcrew == 'Reserves' :

		maintext += "<input type=submit name=action value='Reserves' style='background-color:lime'> "

	else:

		maintext += "<input type=submit name=action value='Reserves'> "

	if logcrew == 'Open' :

		maintext += "<input type=submit name=action value='Open' style='background-color:lime'> "
	
	else:
		
		maintext += "<input type=submit name=action value='Open'> "

	maintext += "Search: " + searchSpinner + "<br>"
	

#	if logcrew == 'TO' :
#
#		maintext += "<input type=submit name=action value='TO' style='background-color:lime'> "
#	else:
#		maintext += "<input type=submit name=action value='TO'> "
#
#	if logcrew == 'CA' :

#		maintext += "<input type=submit name=action value='CA' style='background-color:lime'> "
	
#	else:
		
#		maintext += "<input type=submit name=action value='CA'> "

	#if logcrew == 'MyPlans' :

	#	maintext += "<input type=submit name=action value='MyPlans'  style='background-color:lime'> "
	#else:
	#	maintext += "<input type=submit name=action value='MyPlans''> "

	#maintext += "<input type=submit name=action value='OPAL'> "
	maintext += "</form><br>"
	#maintext = "<input type=radio name=logcrew value='TO'> TO | <input name=logcrew type=radio value='DC'> DC | <input name=logcrew type=radio value='WP'> WP |"


	kmonth = nmonth - 2

	kyear = nyear

	if kmonth == 0 :

		kyear = str( int( kyear ) - 1 )
		kmonth = 12
		
	if kmonth == -1 :

		kyear = str( int( kyear ) - 1 )
		kmonth = 11

	if kmonth < 10 :
	#
		kmonthFull = '0' + str( kmonth )
	#
	else:
	#
		kmonthFull = str( kmonth )

	kmonthText = months[ kmonth ] + '-' + str( kyear )

	lmonth = nmonth - 1

	lyear = nyear

	if lmonth == 0 :

		lyear = str( int( lyear ) - 1 )
		lmonth = 12

	if lmonth < 10 :
	#
		lmonthFull = '0' + str( lmonth )
	#
	else:
	#
		lmonthFull = str( lmonth )

	lmonthText = months[ lmonth ] + '-' + str( lyear )



	omonth = nmonth + 1

	oyear = nyear

	if omonth == 13 :

		oyear = int( oyear ) + 1
		omonth = 1

	omonthText = months[ omonth ] + '-'+ str( oyear )

	if omonth < 10 :

		omonthFull = '0' + str( omonth )
	else:
		omonthFull = str( omonth )
		

	pmonth = nmonth + 2

	pyear = nyear

	if pmonth == 13 :

		pyear = int( pyear ) + 1
		pmonth = 1
		
	if pmonth == 14:

		pyear = str( int( pyear ) + 1 )
		pmonth = 2


	pmonthText = months[ pmonth ] + '-'+ str( pyear )

	if pmonth < 10 :

		pmonthFull = '0' + str( pmonth )
	
	else:
		pmonthFull = str( pmonth )

	#maintext += "<a href=./sumcal.py?year=" + lyear + "&month=" + lmonthFull + ">"
	#maintext += months[ lmonth ] + "-" + lyear + "</a> | "
	#maintext += months[ nmonth ] + "-" + year + " | "
	#maintext += "<a href=./sumcal.py?year=" + oyear + "&month=" + omonthFull + ">"
	#maintext += months[ omonth ] + " - " + oyear + "</a>"

	
	maintext += "<a href=./carcal.py?year=" + str( kyear ) + "&month=" + kmonthFull + "&logcrew=" + logcrew + "&searchUser=" + searchUser + '>' + kmonthText + '</a> | '
	
	maintext += "<a href=./carcal.py?year=" + str( lyear ) + "&month=" + lmonthFull + "&logcrew=" + logcrew + "&searchUser=" + searchUser + '>' + lmonthText + '</a> | ' 
	
	maintext += '<b><FONT SIZE=+1>' + months[ nmonth ] + " - " + year + '</b></FONT> | '

	maintext += "<a href=./carcal.py?year=" + str( oyear ) + "&month=" + omonthFull + "&logcrew=" + logcrew + "&searchUser=" + searchUser + '>' + omonthText + '</a> | '

	maintext += "<a href=./carcal.py?year=" + str( pyear ) + "&month=" + pmonthFull + "&logcrew=" + logcrew + "&searchUser=" + searchUser + '>' + pmonthText + '</a><br>'

	maintext += "<table cellpadding=3 cellspacing=3 rules=all border=2>"
	maintext += "<tr><td colspan=7 class=center bgcolor=lime><FONT FACE='Arial,Helvetica' SIZE=3>" + months[ nmonth ] + " - " + year + " - [" + logcrew + "]</td></tr>"
	#maintext += "<tr><td colspan=7 align=center bgcolor=lime><FONT FACE='Arial,Helvetica' SIZE=3>"+lmonth_link + " || " + nmonth_link+"</td></tr>"


	startdate = datetime.date( nyear, nmonth, nday )

	dayno = startdate.strftime("%w")

	offset, totaldays = calendar.monthrange( nyear, nmonth )

	#offset = int( dayno )

	#offset += 1

	#maintext += 'offset: ' + str( offset ) + ' totaldays: ' + str( totaldays )

	maintext += "<tr>"

	for dow in weekdays:

		maintext += "<td class=center><FONT FACE='Arial,Helvetica' SIZE=3><b>%s</b></td>" % ( dow )

	maintext += "</tr>"


	#startdate = datetime.date( nyear, nmonth, nday)


	#maintext += "<tr>" 

	i = -1

	#totaldays = totaldays + 15


	if offset <  6 : 

	#	maintext += "</tr>"

		while i < offset:

	#		maintext += "<td>start-offset</td>"
			maintext += "<td>&nbsp;</td>"
			i += 1


	#if offset ==  6 : 

	#	maintext += "</tr>"

	if offset == 6 :

		tempoffset = -1 
	else: 
		tempoffset = offset

	while nday <= totaldays:

		if nmonth < 10:

			montext = '0'+str( nmonth )

		else:

			montext = str( nmonth )

		if nday < 10:

			daytext = '0'+str( nday )

		else:
		
			daytext = str( nday )



		fulldate =  year + '-' + montext + '-' + daytext
		
#		fullDate1 = datetime.date( int( year ), nmonth, nday )

		fulldate2 = datetime.date( nyear, nmonth, nday )

		yday1 = datetime.timedelta( days = 1 )
		fullDate3 = fulldate2 - yday1
		tmrwDate = fullDate3.strftime('%Y-%m-%d')
		

	#	monthText = fulldate2.strftime('%b') + ' ' + fulldate2.strftime( '%m/%d' )
		monthText =  fulldate2.strftime( '%m/%d' )

		bgcolor = 'white'

		if today == fulldate :

			bgcolor='yellow'	

#		if logcrew == 'Reserves' or logcrew == 'Open'  :

		maintext += "<td valign=top bgcolor=%s><a href=resday.py?date=%s&logcrew=%s>[ %s  ] Cars Today</a>" \
		% ( bgcolor, fulldate, logcrew, monthText )

#		maintext += "<td valign=top bgcolor=%s><a href=resday.py?date=%s&logcrew=%s>[ %s ]</a>" \
#		% ( bgcolor, fulldate, logcrew, monthText )
			
#		maintext += " | <a href=./resday.py?date=%s>Cars</a>" % ( fulldate )

		maintext += "<br>"

		cursor3.execute("select car, wheels, drivers from cars where status='Active' order by seq")

		if logcrew == 'Reserves':
			
			cursor4.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, \
			status, masterid, comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, \
			monitor, car2 from res where date='%s' and status<>'Removed' order by car, datein" \
			% ( fulldate ) )

			cursor5.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, \
			status, masterid, comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, \
			monitor, car2 from res where date='%s' and overnight='Overnight' and status<>'Removed' order by car, datein" \
			% ( tmrwDate ) )

			numrows4=cursor4.rowcount
			numrows5=cursor5.rowcount


		else:
			
			cursor4.execute("select car from cars where status='Active' order by seq")
			
			numrows4=cursor4.rowcount

		
#		maintext += "fulldate All Todays: %s <br>" % ( fulldate  )
#		maintext += "tmrwDate YDay Overnights: %s<br>" % ( tmrwDate  )
#		maintext += "fulldate All Todays: %s <br>" % ( cnumrows4  )
#		maintext += "tmrwDate YDay Overnights: %s<br>" % ( cnumrows5  )


	#	maintext += 'numrows4: ' + str( numrows4 )

		daywarning = ''

		nitewarning = ''
		
		freeCars = '<hr>'
#		freeCars = 'Free Cars<br>'


#		if numrows4 > 0 ) :
		if logcrew == 'Reserves' :

			itemstext = '<table>'
			itemstext2 = ''
			
			
		
			for ruw in cursor3.fetchall() :
			
				car_car = ruw[0]
				car_car = car_car.strip()

				car_wheels = ruw[1]
				car_wheels = car_wheels.strip()
				car_drivers = ruw[2]
				car_drivers = car_drivers.strip()

				cursor7.execute( "select user from users where stnuser='%s'" % ( username ) ) 
				numrows7 = cursor7.rowcount

				driver = username
				if numrows7 == 1 :

					 fromUsers = cursor7.fetchone()
					 driver = fromUsers[0]

				checkDriver = '' + driver + ','
				checkCrew = '+' + logcrew2 + ','
				
				cursor4.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, \
				status, masterid, comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, \
				monitor, car2 from res where date='%s' and ( car = '%s' or car2 = '%s') and status<>'Removed' order by car, datein" \
				% ( fulldate, car_car, car_car ) )
				

				cursor5.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, \
				status, masterid, comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, \
				monitor, car2 from res where date='%s' and overnight='Overnight' and ( car = '%s' or car2 = '%s' ) and status<>'Removed' order by car, datein" \
				% ( tmrwDate, car_car, car_car ) )


				numrows4=cursor4.rowcount
				numrows5=cursor5.rowcount
		
				cnumrows4=str( numrows4 )
				cnumrows5=str( numrows5 )
				
				itemstext2 = ''

# yesterday Overnights				
#			numrows5 = cursor5.rowcount
				if numrows5 == 1 :


					rew = cursor5.fetchone()

					rew_idno = str( rew[0] )
					rew_car = rew[1]
					rew_date = str( rew[2] )
					rew_datein = str( rew[3] )
					rew_datein = rew_datein[0:16]

					rew_dateout = str( rew[4] )
					rew_dateout = rew_dateout[0:16]
					rew_date2 = rew_dateout[0:10]

					rew_overnight = rew[5]
					rew_destiny = rew[6]
					rew_driver = rew[7]
					rew_rdriver = rew[8]
					rew_status = rew[11]
					rew_status = rew_status.strip()


					rew_seats = rew[20]
					rew_rseats = rew[21]
					rew_carseats = rew[22]


					rew_car2 = rew[27]

					rew_driver = rew_driver.strip()
					rew_rdriver = rew_rdriver.strip()

					rew_hourin = rew_datein[11:13]
					rew_hourout = rew_dateout[11:13]
		#				itemstext += '<a href=planone.py?idno=%s><b>'+item_time + '</b></a>&nbsp;' +item_title + ' -' + item_downtime +' (' + item_type +')<br>' % ( item_idno )
#					itemstext += '<a href=resone.py?idno=' + rew_idno + '>'+rew_car + '</a> (' +rew_hourin + ')->' + rew_hourout + '&nbsp;' \
#					+ rew_driver+"<br>"
#					bgcolor = 'white'
					bgcolor = 'lavender'
#					bgcolor = 'honeydew'
#					bgcolor = 'lavenderblush'
##					bgcolor = 'azure'
											
					if searchUser == rew_driver :
					
						itemstext2 += "<tr><td bgcolor=%s><a href=resone.py?idno=%s>%s</td><td>%s)~%s</a></td><td bgcolor=lime><b>%s</b></td></tr>" % ( bgcolor, rew_idno, rew_car, rew_hourin, rew_hourout, rew_driver  )
					
					else :
					
						itemstext2 += "<tr><td bgcolor=%s><a href=resone.py?idno=%s>%s</td><td>%s)~%s</a></td><td>%s</td></tr>" % ( bgcolor, rew_idno, rew_car, rew_hourin, rew_hourout, rew_driver  )

#					if len( itemstext2 ) > 0 :
				
#						itemstext += itemstext2

# today Days and Overnights
					
				if numrows4 > 0 :
				
					if len ( itemstext2 ) > 0 :
					
						itemstext += itemstext2

					for row in cursor4.fetchall() :

						res_idno = str( row[0] )
						res_car = row[1]
						res_date = str( row[2] )
						res_datein = str( row[3] )
						res_datein = res_datein[0:16]
		
						res_dateout = str( row[4] )
						res_dateout = res_dateout[0:16]
						res_date2 = res_dateout[0:10]
		
						res_overnight = row[5]
						res_destiny = row[6]
						res_driver = row[7]
						res_rdriver = row[8]
						res_pass = row[9]
						res_pass2 = row[10]
						res_status = row[11]
						res_status = res_status.strip()

						res_masterid = row[12]
						res_comment = row[13]
						res_datea = str( row[14] )
						res_dateb = str( row[15] )
						res_datec = str( row[16] )
						res_dated = str( row[17] )
						res_datee = str( row[18] )
						res_datef = str( row[19] )		

						res_seats = row[20]
						res_rseats = row[21]
						res_carseats = row[22]
						res_rmuser = row[23]
						res_rmstamp = row[24]
						res_blocking = row[25]
						res_blocking = res_blocking.strip()

						res_monitor = row[26]
						res_monitor = res_monitor.strip()

						res_car2 = row[27]

						res_driver = res_driver.strip()
						res_rdriver = res_rdriver.strip()

						res_hourin = res_datein[11:13]
						res_hourout = res_dateout[11:13]
	#				itemstext += '<a href=planone.py?idno=%s><b>'+item_time + '</b></a>&nbsp;' +item_title + ' -' + item_downtime +' (' + item_type +')<br>' % ( item_idno )

						bgcolor = 'blanchedalmond'

						if res_overnight == 'Overnight' :

							bgcolor = 'lightblue'
						
	#						itemstext += '<a href=resone.py?idno=' + res_idno + '>'+res_car + '</a> ' +res_hourin + '->(' + res_hourout + ')&nbsp;' \
	#						+ res_driver+"<br>"

							if searchUser == res_driver :
						
								itemstext += "<tr><td bgcolor=%s><a href=resone.py?idno=%s>%s</td><td>%s~(%s</a></td><td bgcolor=lime><b>%s</b></td></tr>" % ( bgcolor, res_idno, res_car, res_hourin, res_hourout, res_driver  )

							else :

								itemstext += "<tr><td bgcolor=%s><a href=resone.py?idno=%s>%s</td><td>%s~(%s</a></td><td>%s</td></tr>" % ( bgcolor, res_idno, res_car, res_hourin, res_hourout, res_driver  )
					
						else :
						
	#						itemstext += '<a href=resone.py?idno=' + res_idno + '>'+res_car + '</a> ' +res_hourin + '-' + res_hourout + '&nbsp;' \
	#						+ res_driver+"<br>"
							if searchUser == res_driver :

								itemstext += "<tr><td bgcolor=%s><a href=resone.py?idno=%s>%s</td><td>%s-%s</a></td><td bgcolor=lime><b>%s</b></td></tr>" % ( bgcolor, res_idno, res_car, res_hourin, res_hourout, res_driver  )

							else :
						
								itemstext += "<tr><td bgcolor=%s><a href=resone.py?idno=%s>%s</td><td>%s-%s</a></td><td>%s</td></tr>" % ( bgcolor, res_idno, res_car, res_hourin, res_hourout, res_driver  )
					

#	no Today Daytime or Overnightss
						
				else:

					itemstext += itemstext2

					#	no yday Overnights


					if numrows5 == 0 :

						approvedDriver = False
					
						if car_drivers[0:4] == '+All' or car_drivers[0:3] == 'All' :

							approvedDriver = True
		
						else :
	
							if checkDriver in car_drivers or checkCrew in car_drivers :
			
								approvedDriver = True
					
					
						if approvedDriver == True :
					
							freeCars += "<a href=resone.py?idno=0&date=%s&car=%s&in=00&out=23>%s (%s) Free</a></br>" % ( fulldate, car_car, car_car, car_wheels )

						else :

							freeCars += "%s (%s) NA</br>" % ( car_car, car_wheels )
					
				
#			freeCars += '</table>'

			itemstext += "</table>"

			itemstext += '<center>' + freeCars + '</center>'
		
#			itemstext += freeCars
		
		else :
		
			itemstext = '<table>'
			itemstext2 = ''
#			itemstext += "not working"
#			itemstext += "numrows4: " + str(numrows4)

			if numrows4 > 0 :
			
				
#				itemstext += "<table><tr><td valign=top>"
				seq = 0
				bookedList = ''
				for ruw in cursor4.fetchall() :

					cars_car = ruw[0]
					cars_car = cars_car.strip()
#					itemstext += "<tr><td>" + cars_car 
					cursor5.execute("select idno, car, datein, dateout, driver from res where date='%s' and car='%s' and status='Active' " % ( fulldate, cars_car ) )
					numrows5 = cursor5.rowcount
					todayRes = numrows5
#					todayRes = 0
					
					cursor6.execute("select idno, car, datein, dateout, driver from res where date='%s' and overnight='Overnight' and car='%s' and status='Active' " % ( tmrwDate, cars_car ) )
					numrows6 = cursor6.rowcount
					ydayRes = numrows6
#					ydayRes = 0
#					if numrows5 > 0 :
#					itemstext += "%s  ( %s )<br>" % ( cars_car, numrows5 )
					if todayRes == 0 and ydayRes == 0 :					
						seq += 1
						itemstext += "<tr><td><a href=resone.py?idno=0&date=%s&car=%s&in=00&out=23>%s free</a></td></tr>" % ( fulldate, cars_car, cars_car )
					else :
						bookedList += "<tr><td>" + cars_car + "</td></tr>" 
#					else :
#						itemstext += "%s (%s)<br>" % ( cars_car, numrows5 )
#					if seq == 10 or seq == 20 :
#						itemstext += "</td><td valign=top>"
#					itemstext += "</td></tr>"
			
				itemstext += bookedList

#				itemstext += "</td></tr></table>"

			itemstext += "</table>"



		
		maintext += itemstext	

	#			maintext += '<tr><td colspan=3><hr></td></tr>'




#		maintext += '</table>'

		maintext += '</td>'


	#	breakday = ( 5, 12, 19, 26 )

	#	if nday in breakday :

	#		maintext += "</tr>"

		tempoffset += 1

		if tempoffset == 6:

			maintext += "</tr>"
			tempoffset = -1


		nday += 1

	if tempoffset > 0:

		tempoffset = 6 - tempoffset
		i = 0
		while i < tempoffset:

	#		maintext +="<td>endoffset: &nbsp;</td>"
			maintext +="<td>&nbsp;</td>"
			i += 1

	maintext += "</tr></table> offset / totaldays: " + str( tempoffset ) + ' / ' + str( totaldays ) + ' dayno: ' + str( dayno )

else :

#	maintext = "OPAL Login Required <a href='../login.php'>Here</a>"
	maintext = logproc.returnLogin()

printHTML( maintext )


