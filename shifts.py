#! /usr/local/python

import os
import sys
import cgi
import datetime
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import dbconnect
#import logproc
import logproc3 as logproc
import textwrap

field = cgi.FieldStorage()
method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()
cursor5=db.cursor()


def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:14px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:14px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:14px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px; font-weight: bold }"
	css_text += "</style>"
#	css_text += "<script src='https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js'></script>"
#	css_text += "<script src='https://cdn.tiny.cloud/1/wew3bls4o7rcb9bz5e5fbsims2qe8k35v6ydly22743hjexy/tinymce/5/tinymce.min.js'></script>"
#	css_text += "<script>tinymce.init({selector:'textarea', forced_root_block: '' });</script>"

	css_text += "<script src='https://code.jquery.com/jquery-1.12.4.js'></script>"
	css_text += "<script src='https://code.jquery.com/ui/1.12.1/jquery-ui.js'></script>"
	css_text += "<script src='js/jquery-clockpicker.js'></script>"
	css_text += '<link rel="stylesheet" href="js/jquery-clockpicker.css">'


	css_text += "<script>"
#	css_text += "$('.clockpicker').clockpicker();"
	css_text += "$('#single-input').clockpicker({"
	css_text += "placement: 'top', "
	css_text += "align: 'left', "
	css_text += "default: '12:30', "
	css_text += "});"
	css_text += "</script>"

	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<!DOCTYPE html>"
	printpg += "<HTML><HEAD>"
#	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += "<META HTTP-EQUIV='refresh' CONTENT='3600'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	


now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d %H:%M')


if 'driver' in field :

	driver = field['driver'].value
	
else:
	
	driver = 'all'
	
driver=driver.strip()

if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )
	pagename = '<center><b>Car-Shifts Listing</b> | %s [%s]<br><br>' % ( username, end )
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

	cursor3.execute("select user, privy, hourin, hourout, shiftin, shiftcar, shifttype, shiftdest  from users where stnuser = '%s'" % ( username ) )
	
	numrows3 = cursor3.rowcount
	
	if numrows3 == 1:
		
		users = cursor3.fetchone()
		
		real_username = users[0]
		users_privy = users[1]
		user_hourin = users[2]
		user_hourout = users[3]

		user_shiftin = users[4]
		user_shiftcar = users[5]
		user_shifttype = users[6]
		user_shiftdest = users[7]


		user_hourin = user_hourin.strip()
		user_hourout = user_hourout.strip()

		
		real_username = real_username.strip()
		user_privy = users_privy.strip()




	maintext = pagename 
	
	

	maintext += '<table cellpadding=3 cellspacing=3><td>'
	
	maintext += '<table cellpadding=3 cellspacing=3>'
	maintext += '<tr><th bgcolor=yellow>'
	maintext += 'Shifts reserves 1 car for <i> > 1 Day/Night</i>, in consecutive days/nights using a destination pattern.<br>For <i>only 1 day/night</i>, use Cars Today / Calendar and pick a green button</th></tr>'
	maintext += '<tr><td><center>One Shift can reserve from 2-11 days/nights.<br>DC, TO/IO, TED make months of reserves for the same car.</center></td></tr>'
	maintext += '<tr><td><center>You are <b>%s</b> and your shifts are <FONT SIZE=+1>%s - %s</center></td></tr>' % ( real_username, user_hourin, user_hourout )
#	maintext += '<tr><td><center>Your Shift Training is DateIn: <b>%s</b> Car: <b>%s</b> Type: <b>%s</b> Destiny: <b>%s</b></center></td></tr>' \
#	% ( user_shiftin, user_shiftcar, user_shifttype, user_shiftdest )
	maintext += '<tr><td><center><FONT SIZE=+1><a href=shiftone.py?idno=0&date=2020-01-01&car=%s>Start Training</a> <b>%s</b> <b>%s</b> <b>%s</b> <b>%s</b></center></td></tr>' \
	% ( user_shiftcar, user_shiftin, user_shiftcar, user_shifttype, user_shiftdest )

	maintext += '</table>'

	trainText = '<table><td>Train Car</td>'
	cursor4.execute("select car, traindate, trainuser from cars where status='Active' and car != 'J-04' and car != 'J-05' order by seq")
	numrows4 = cursor4.rowcount
#	numrows4=0
	
	if numrows4 > 0 :
	
		for carsTrain in cursor4.fetchall() :

			cars_car = carsTrain[0]
			cars_traindate = carsTrain[1]
			cars_trainuser = carsTrain[2]
						
			cursor5.execute("select car, date from res where substring( date, 1, 7 ) = '2020-01' and car = '%s' and status='Active'" % ( cars_car ) )
			numrows5 = cursor5.rowcount
			
#			if cars_traindate == today  or numrows5 > 0 :	
			if cars_traindate == today or numrows5 > 0  :	
				
#				if cars_trainuser == real_username :

#					cars_trainuser = '<b>' + cars_trainuser + '</b>'
	
			
				trainText += '<td><center><FONT SIZE=+1>%s<br>%s</center></td>' % ( cars_car, cars_trainuser )
	
			
			else :

				trainText += '<td><center><a href=shiftone.py?idno=0&date=2020-01-01&car=%s><b>%s</b></a></center></td>' % ( cars_car, cars_car  )

	trainText += '</tr></table>'
	
	maintext += trainText
	


	maintext += '</td><td>'
	
	maintext += '<table>'
	maintext += '<tr><th>Destiny Key</th><th>Description</th></tr>'
	maintext += '<tr><td>BaseSum_HP-Nights</td><td>Operator Nights - HP with acclimitization</td></tr>'
	maintext += '<tr><td>BaseSum_HP-Nights_SA</td><td>SA Nights - HP No acclimitization</td></tr>'
	maintext += '<tr><td>BaseSum_NoHP-Nights</td><td>Night staff stay at Base</td></tr>'
	maintext += '<tr><td>BaseSum_Days-All</td><td>All 7 days reserved, days and weekends</td></tr>'
	maintext += '<tr><td>BaseSum_Days-MonFri</td><td>only Mon-Fri are reserved</td></tr>'
#	maintext += '<tr><td>BaseSum_Days-MonTh</td><td>only Mon-Th are reserved</td></tr>'
	maintext += '<tr><td>BaseSum_Days-MonTh</td><td>only Mon-Th are reserved</td></tr>'
	maintext += '<tr><td>HPSum_HP-Nights</td><td>HP-Sum-HP NightShifts</td></tr>'
	maintext += '</table>'
	
	maintext += '</td></table><br>'
	
	
#	date = '2020-06-26'

	if driver == 'all' :
		
		cursor.execute("select idno, car, date, datein, dateout, overnight, driver, car2, destiny, status from shifts order by idno desc ")

	else :

		cursor.execute("select idno, car, date, datein, dateout, overnight, driver, car2, destiny, status from shifts where driver = '%s' \
		order by idno desc " % ( driver ) )
#		order by datein desc " % ( driver ) )
		
		
	numrows = cursor.rowcount

#	maintext += ('Subaru SciOps Car Shifts - %s<br><br>' % ( username )  )

#	boxtext = '<form method=post action='shiftone.py?idno=0'><input name=action type=submit value='Add Shift'></form>'
	boxtext = ''
	boxtext += '<table>'
	boxtext += '<tr><th>Seq</th><th>IDNo</th><th>DayIn</th><th>DayOut</th><th>Car</th><th>Driver</th><th>Overnight</th><th>Destiny</th>\
	<th>Status</th><th>Reserves</th></tr>'

	if numrows > 0:
	
		seq = 0
	
		running_end = 0

		for row in cursor.fetchall() :
		
			seq += 1
		
			shift_idno = row[0]		
			shift_car = row[1]		
			shift_date = str( row[2] )	
			shift_datein = str( row[3] )
			shift_hourin = shift_datein[5:16]

			shift_dateout = str( row[4] )
			shift_hourout = shift_dateout[5:16]
			shift_overnight = row[5]
			shift_driver = row[6]
			shift_car2 = row[7]		
			shift_destiny = row[8]		
			shift_status = row[9]		
		
#			maintext += "date: %s hourin: %s hourout %s car: %s driver: %s overnight: %s<br>" % ( shift_date, shift_hourin, shift_hourout, shift_car, shift_driver, \
			shift_overnight.strip()
			
			

			boxtext += "<tr><td class=center>%s</td><td class=center>%s</td><td bgcolor=lime><a href=shiftone.py?idno=%s>%s</a></td><td>%s</td>\
			<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"  \
			% (  seq, shift_idno, shift_idno, shift_hourin, shift_hourout, shift_car, shift_driver, shift_overnight, shift_destiny, shift_status )

			cursor2.execute("select idno, car, date, datein, dateout, overnight, driver, car2, destiny from res where masterid = '%s' order by datein desc" % ( shift_idno ) )

			numrows2=cursor2.rowcount

			bgcolor='yellow'

			if numrows2 > 0 :

				bgcolor='pink'

			boxtext += "<td bgcolor=%s class=center>( %s )</td></tr>" % ( bgcolor, numrows2)
#			if numrows2 > 0 :
				
#				seq2 = 0
				
#				for raw in cursor2.fetchall() :
		
#					seq2 += 1
		
#					res_idno = raw[0]		
#					res_car = raw[1]		
#					res_date = str( raw[2] )	
#					res_datein = str( raw[3] )
#					res_hourin = res_datein[11:13]
#					res_dateout = str( raw[4] )
#					res_hourout = res_dateout[11:13]
#					res_overnight = raw[5]
#					res_driver = raw[6]
#					res_car2 = raw[7]		
#					res_destiny = raw[8]		
#
#					boxtext += "<tr><td>%s</td><td><a href=shiftone.py?idno=%s>%s&nbsp;-&nbsp;%s<br>%s<br>overnight: %s</td></tr>" % (  seq2, res_idno, res_hourin, res_hourout, res_driver, res_overnight )
#		else:
				
#			boxtext += "<td bgcolor=pink>( 0 ) Reservations for Shift-ID: %s</td></tr>" % (  shift_idno )
				
	else:
		
		boxtext += "<td bgcolor=pink colspan=5>No Shifts for username: %s</td><td></td></tr>" % (  username )

	boxtext += '</tr></table>'
	maintext += boxtext

else:

	maintext = logproc.returnLogin()
	
printHTML( maintext )

		
