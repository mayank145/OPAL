#! /usr/local/python

import os
import sys
import cgi
import datetime
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import dbconnect
import logproc3 as logproc
import textwrap

#from datetime import date

import http.cookies as Cookie
import shelve

field = cgi.FieldStorage()
method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()
cursor4.execute("set autocommit = 1")
cursor5=db.cursor()

def isDuped( date, car, datein, dateout, idno2, repcount, reps, repcount2 ) :

	datein2 = datein.split('-')
	dayin2=datein2[2]
	dayin2=dayin2[0:2]
	hourin2 = datein[11:13]
	minin2 = datein[14:16]
	datein3 = datetime.datetime ( int( datein2[0] ), int( datein2[1] ), int( dayin2 ), int( hourin2 ), int( minin2 ), 0 )
	datein4=datein3.strftime('%y-%m-%d %H:%M')
	datein5=datein3.strftime('%m-%d %H:%M')

	dateout2 = dateout.split('-')
	dayout2=dateout2[2]
	dayout2=dayout2[0:2]
	hourout2 = dateout[11:13]
	minout2 = dateout[14:16]
	dateout3 = datetime.datetime ( int( dateout2[0] ), int( dateout2[1] ), int( dayout2 ), int( hourout2 ), int( minout2 ), 0 )
	dateout4=dateout3.strftime('%y-%m-%d %H:%M')
	dateout5=dateout3.strftime('%m-%d %H:%M')

	date1 = date.split('-')

	today = datetime.date( int( date1[0] ) , int( date1[1] ), int( date1[2] ) )
	yday = datetime.timedelta ( days = 1 )
	yesterday = today - yday
	yday2 = yesterday.strftime( '%Y-%m-%d' )

	cursor2.execute("select idno, car, date, datein, dateout, overnight, driver from res where ( date='%s' or date = '%s' ) \
	and car='%s' and status='Active' order by datein" % ( date, yday2, car ) )
	numrows2=cursor2.rowcount

	mfail = False
	mfailComment = ''
	failidno = 0

	if numrows2 > 0 :
		
		
		seq = 0

		mfailTable = ''
		# 220826 Debug line
		mfailComment+='Confirming ' + datein + ' ' + dateout + ' repcount: ' + str( repcount ) + ' reps: ' + str( reps ) + ' repcount2: ' + str( repcount2 ) + '<br>'
		
		for rew in cursor2.fetchall() :

			res_idno = rew[0]
			res_car = rew[1]
			res_date = rew[2]
			res_datein = rew[3]
			res_dateout = rew[4]
			res_overnight = rew[5]
			res_driver = rew[6]
		
			res_datein2 =  str( res_datein )
		
			res_hourin2 = res_datein2[11:13]
			res_minin2 = res_datein2[14:16]
		
			res_dateout2 =  str( res_dateout )

			res_hourout2 = res_dateout2[11:13]
			res_minout2 = res_dateout2[14:16]	
			
			
#			datein2 = datein.strftime( '%m-%d %H:%M' )
#			dateout2 = dateout.strftime( '%m-%d %H:%M' )

			mfailComment += "check exist res: " + res_car + ' ' + str( res_idno ) + ' ' + str( res_date ) + ' ' + res_overnight + ' in: ' + str( res_datein ) + " out: " + str( res_dateout )+'<br>'
			
#			if not res_idno == idno2 :

# completely outside other ress
				
			if datein3 < res_datein and dateout3 > res_dateout :

				mfail = True
				mfailComment += '<i>Confirming ' + car + ' ' + datein[5:13] + ' ' + dateout[5:13] + ' reps: ' + str( reps ) + ' repcount: ' + str(repcount) + ' repcount2: ' + str( repcount2 ) + '</i><br>NewRes Start-End Outside:' + res_car  + ' ' + res_datein2[5:16] +  ' - ' + res_dateout2[5:16] + ' - ' + res_driver + ' ' + res_overnight + '<br>'
				mfailTable += '<tr><td>NewRes Start-End Outside</td><td>(' + str( res_idno ) + ')</td><td>'  + res_car  + '</td><td>' + res_datein2[5:16] + ' - ' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
				 + res_driver + '</td</tr>'
				failidno = res_idno

# completely same Times or Times within other res
				
			if datein3 >= res_datein and dateout3 <= res_dateout :
				
				mfail = True
				mfailComment += '<i>Confirming ' + car + ' ' + datein[5:13] + ' ' + dateout[5:13] + ' reps: ' + str( reps ) + ' repcount: ' + str(repcount) + ' repcount2: ' + str( repcount2 ) + '</i><br>NewRes All-Inside:  ' + res_car  + ' ' + res_datein2[5:16] + ' - ' + res_dateout2[5:16] + ' - ' + res_driver + ' ' + res_overnight  + '<br>'
				mfailTable += '<tr><td>All-Inside Existing Res</td><td>(' + str( res_idno)  + ')</td><td>' + res_car  + '</td><td>' + res_datein2[5:16] + ' - ' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
				 + res_driver + '</td</tr>'
				failidno = res_idno

# dateout within other res
#				if datein3 < res_datein and dateout3 >= res_datein and dateout3 <= res_dateout  :
# if dateout3 == datein, its OK = New Res Ends When Old Res Starts
			if datein3 < res_datein and dateout3 > res_datein and dateout3 <= res_dateout  :
				
				mfail = True
				mfailComment += '<i>Confirming ' + car + ' ' + datein[5:13] + ' ' + dateout[5:13] + ' reps: ' + str( reps ) + ' repcount: ' + str(repcount) + ' repcount2: ' + str( repcount2 ) + '</i><br>NewRes Ends-Inside: ' + res_car  + res_datein2[5:13]  + '-' + res_dateout2[11:13] + ' - ' + res_driver + ' ' + res_overnight + '<br>'
				mfailTable += '<tr><td>NewRes Ends-Inside</td><td>(' + str( res_idno )  + ')</td><td>'  + res_car  + '</td><td>' + res_datein2[5:16] + ' - ' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
				+ res_driver + '</td</tr>' 
				failidno = res_idno
# datein within other res
#				if dateout3 > res_dateout and datein3 >= res_datein and datein3 <= res_dateout  :
# if datein3 == dateout, its OK. New Res Starts When Old Res Ends
			if dateout3 > res_dateout and datein3 >= res_datein and datein3 < res_dateout  :
				
				mfail = True
				mfailComment += '<i>Confirming ' + car + ' ' + datein[5:13] + ' ' + dateout[5:13] + ' reps: ' + str( reps ) + ' repcount: ' + str(repcount) + ' repcount2: ' + str( repcount2 ) + '</i><br>NewRes Starts-Inside: '+ res_car + ' ' + res_datein2[5:13] + '-' + res_dateout2[11:13] + ' - ' + res_driver + ' ' + res_overnight + '<br>'
				mfailTable += '<tr><td>NewRes Starts-Inside</td><td>(' + str( res_idno ) + '</td><td>'  + res_car  + '</td><td> in ' + res_datein2[5:16] + ' - ' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
				+ res_driver + '</td</tr>'
				failidno = res_idno
	
#		mfailTable +='</table>'

		
#		if mfail == True :
			
#			mfailTable2 = '<table><tr><th colspan=7 bgcolor=pink><FONT SIZE=+1><b>Your Reservation Conflicts with</FONT></th></tr>'
#			mfailTable2 += '<tr><th>Failure Reason</th><th>IDNo</th><th>Car</th><th>DateIn</th><th>DateOut</th><th>Overnight</th><th>Driver</th></tr>'
#			mfailTable2 += mfailTable
		
#			mfailComment = mfailTable
			
	else:

		mfail = False
		mfailComment = 'No conflict reservations<br>'
		failidno = 0
				
#	return ( mfail, mfailComment, failidno )
	return ( mfail, mfailComment, failidno )

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:14px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold }"
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

if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

if 'car' in field :

	car = field['car'].value
	
else:
	
	car = 'J-01'

if 'car2' in field :

	car2 = field['car2'].value
	
else:
	
	car2 = 'J-01'

if 'date' in field :

	date = field['date'].value
	
else:
	
	date= ''

if 'datein' in field :

	datein = field['datein'].value
	
else:
	
	datein = '0000-00-00 00:00'

if 'dateout' in field :

	dateout = field['dateout'].value
	
else:
	
	dateout = '0000-00-00 00:00'

if 'overnight' in field :

	overnight = field['overnight'].value

else:
	
	overnight = 'Daytime'
	
if 'destiny' in field :

	destiny = field['destiny'].value
	
else:
	
	destiny = 'BHSB'
    

if 'driver' in field :

	driver = field['driver'].value
	
else:
	
	driver = 'None'

if 'blocking' in field :

	blocking = field['blocking'].value
	
else:
	
	blocking = 'In-Out'	

if 'pass1' in field :

	pass1 = field['pass1'].value

else:

	pass1 = ''
	
if 'realin' in field :

	realin = field['realin'].value

else:

	realin = '08'

if 'realout' in field :

	realout = field['realout'].value

else:

	realout = '16'	

realin = realin.strip()

realout = realout.strip()

if len ( realin ) == 0 :

	realin = '08'

if len ( realout ) == 0 :

	realout = '16'


	
	
if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()

#	admin_users = ( 'letawsky', 'noriko', 'roth' )
	admin_users = ( 'letawsky', 'noriko', 'roth', 'winegar' )

	night_users = ( 'letawsky' )
	
	reserveAdmin = False 
		
	if username in admin_users :
	
		reserveAdmin = True 

	
	updateComment = 'No Update<br>'
	
	cursor3.execute("select user, privy, hourin, hourout from users where stnuser = '%s'" % ( username ) )
	
	numrows3 = cursor3.rowcount
	
	if numrows3 == 1:
		
		users = cursor3.fetchone()
		
		real_username = users[0]
		users_privy = users[1]
		user_hourin = users[2]
		user_hourout = users[3]
		
		real_username = real_username.strip()
		users_privy = users_privy.strip()
	

	if method == 'POST' :
	
		if  field['action'].value == 'Save' and int( idno ) > 0 :
#			mpass = True
			date1 = date[0:10]
		
			idno2 = int( idno )
		
			datein = datein.strip()
			dateout = dateout.strip()
			
			datein2 = datein[0:10]
			dateout2 = dateout[0:10]
				
			hourin = datein[11:13]
			hourout = dateout[11:13]
		
#			starttime = start2.strip()
#			endtime = end2.strip()
		
			overnight = overnight.strip()
					
			car = car.strip()
			car2 = car2.strip()
		
			driver = driver.strip()

			pass1 = pass1.strip()
			
			if date1 != datein2 :
			
				date1 = datein2
						
			cursor2.execute("select driver from shifts where idno = '%s'" % ( idno2 ) )
			numrows2=cursor2.rowcount
			ruw = cursor2.fetchone()
			old_driver = ruw[0]
			
			if not driver == old_driver :

				cursor2.execute("select hourin, hourout from users where user = '%s'" % ( driver ) )

				numrows2=cursor2.rowcount
				
				if numrows2 == 1 :
					
					raw = cursor2.fetchone()
					hourin = raw[0] + ':00'
					hourout = raw[1] + ':00'
#					users_privy = raw[1] + ':00'
					
				if driver == '.DayCrew1' :
					
					destiny = 'BaseSum_Days-MonTh'
					overnight = 'Daytime'

				if driver == '.DayCrew2' :
					
					destiny = 'BaseSum_Days-MonFr'
					overnight = 'Daytime'

				if driver == '.Garage' :
					
					destiny = 'BaseSum_Days-All'
					overnight = 'Daytime'
			
			datein = datein[0:10] + ' ' + hourin

			mfailComment = 'No Failure<br>'
			
			if logcrew2 == 'WP' and reserveAdmin == False :
			
				dateinArray = datein2.split('-')
				dateoutArray = dateout2.split('-')
				datein3 = datetime.datetime( int( dateinArray[0] ) , int( dateinArray[1] ), int( dateinArray[2] ) )
				dateout3 = datetime.datetime( int( dateoutArray[0] ) , int( dateoutArray[1] ), int( dateoutArray[2] ) )
				shiftMax = datetime.timedelta ( days = 10 )
				maxShift = datein3 + shiftMax
				maxShiftDate = maxShift.strftime('%Y-%m-%d')
				
				if dateout3 > maxShift :
				
					mfailComment += '<b>You can only reserve 10 days maximum = '+ maxShiftDate + '</b><br>'
				
					dateout=maxShiftDate
				
				
#					dateout = maxShift[0:10]
				
			
			dateout = dateout[0:10] + ' ' + hourout	
			
#			mfailComment = 'No Failure<br>'
			
			#cursor4.execute("update res set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', rdriver = '%s',  pass = '%s', pass2 = '%s', status = '%s', masterid = '%s', comment = '%s' where idno = '%s'" % (car, date, datein, dateout, overnight, destiny, driver,rdriver, pass1, pass2, status, idno, comment,  idno ) )
			cursor4.execute("update shifts set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', username='%s', \
			timestamp='%s', car2='%s', blocking='%s', pass='%s' where idno = '%s'" % (car, date1, datein, dateout, overnight, destiny, driver, username, today, car2, blocking, pass1, idno ) )

				
			updateComment += 'Update Shifts OK - Date: ' + str( date1 ) + ' DateIn: ' + str( datein ) + ' DateOut: ' + str( dateout ) + ' Destiny: ' + destiny + "<br>" 
			updateComment += 'mfailComment: ' + mfailComment
			
		if  field['action'].value == 'Delete Res' and int( idno ) > 0 :
#			mpass = True
			
			mfailComment = 'No Failure<br>'
			
			#cursor4.execute("update res set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', rdriver = '%s',  pass = '%s', pass2 = '%s', status = '%s', masterid = '%s', comment = '%s' where idno = '%s'" % (car, date, datein, dateout, overnight, destiny, driver,rdriver, pass1, pass2, status, idno, comment,  idno ) )
			cursor4.execute("delete from res where masterid = '%s'" % ( idno ) )
			cursor4.execute("update shifts set status='UnBooked' where idno = '%s'" % ( idno ) )
				
			updateComment += '<table><td bgcolor=pink>Deleted Reserves OK ( ShiftNo: ' + str( idno ) + " ) </td></table><br>" 
			updateComment += 'mfailComment: ' + mfailComment
#		else :
				
#			updateComment = 'Update-FAIL - [' + str( mfail ) + ' ' + str( failidno ) + '] ' + mfailComment + ' ' + '<br>'

		if  field['action'].value == 'Make Res' and int( idno ) > 0 :

			cursor2.execute("select idno, car, date, datein, dateout, overnight, driver, destiny, username, timestamp, car2, status, blocking, pass from shifts where idno = '%s'" % ( idno ) )

			numrows2=cursor2.rowcount

		#	maintext += ('Subaru SciOps Car Shifts - %s<br><br>' % ( username )  )

			boxtext = '<table>'
			boxtext += '<tr><th>DayIn</th><th>DayOut</th><th>Car</th><th>Driver</th><th>Overnight</th></tr>'

			if numrows2 == 1:
	
				row = cursor2.fetchone()
	
				shift_idno = row[0]		
				shift_car = row[1]		
				shift_date = str( row[2] )	
				shift_datein = str( row[3] )
				shift_hourin = shift_datein[5:16]

				shift_dateout = str( row[4] )
				shift_hourout = shift_dateout[5:16]
				shift_overnight = row[5]
				shift_driver = row[6]
				shift_destiny = row[7]	
				shift_username = row[8]	
				shift_timestamp = str( row[9] )	
				shift_car2 = row[10]	
				shift_status = row[11]	
				shift_status = shift_status.strip()
				shift_blocking = row[12]
				shift_blocking = shift_blocking.strip()
				shift_pass = row[13]
				shift_pass = shift_pass.strip()
				shift_pass = shift_pass.upper()
				
				countpass4 = 1
				countpass3 = 0

				if len( shift_pass ) > 0 and shift_pass != '.NONE' and shift_pass != 'NONE' :

					countpass = shift_pass.split(',')

					countpass2 = []
	
					if len( countpass ) > 0 :

						for pass3 in countpass :

							pass3 = pass3.strip()

							if len ( pass3 ) > 0 :
				
								countpass2.append( pass3 )

					if len( countpass2 ) > 0  :

						countpass3 = len ( countpass2 )
				
				
				if ( shift_driver == '.DayCrew1' or shift_driver == 'DayCrew1' or shift_driver == '.DayCrew2' ) and countpass3 > 0 :

					countpass4 = countpass3

				else :
				
					countpass4 += countpass3
			
#				countpass=6
					
#			mpass = True
				date1 = shift_date[0:10]
		
				idno2 = shift_idno
		
				datein = shift_datein.strip()
				dateout = shift_dateout.strip()
		
#				hourin = datein[11:13]
#				hourout = dateout[11:13]
				hourin = datein[11:16]
				hourout = dateout[11:16]


				real_hourin = realin
				real_hourout = realout
		
	#			starttime = start2.strip()
	#			endtime = end2.strip()
		
				overnight = shift_overnight.strip()
				
				pass1 = shift_pass
				
				car = shift_car.strip()
				car2 = shift_car2.strip()
		
				driver = shift_driver.strip()
				
				cursor2.execute("select hourin, hourout, privy from users where user = '%s'" % ( driver ) )

				numrows2=cursor2.rowcount
				
				if numrows2 == 1 :
					
					raw = cursor2.fetchone()
					users2_hourin = raw[0] 
					users2_hourout = raw[1]
					users2_privy = raw[2]
		
				date2 = date1.split('-')
			
				date3 = dateout[0:10]
				date4 = date3.split('-')
						
				start1 = datetime.datetime( int( date2[0] ), int( date2[1] ), int( date2[2] ), 0, 0, 0, 0 )			
				end1 = datetime.datetime( int( date4[0] ), int( date4[1] ), int( date4[2] ), 0, 0, 0, 0 )
				
				start1Date = start1.strftime('%Y-%m-%d')
				end1Date = end1.strftime('%Y-%m-%d')
						
				days1 = end1 - start1
				
				oneday = datetime.timedelta( days = 1 )
				
				if overnight == 'Overnight' :
					
					reps = days1.days
	#				oneday = datetime.timedelta( days = 1 )
#					end1 = end1 - oneday
					
				else :
					
					reps = days1.days + 1
					
# 220609 Trouble HPNights

#				if shift_destiny == 'BaseSum_HP-Nights' :
				
#					reps += 1
							
#				seats = 1
#				rseats = 1

				seats = countpass4
				rseats = countpass4

				carseats = 4
						
# Operator Night Shift with 1st Bight Acclimitization

				BaseSumHP = ( 'XXXX','BXXH', 'HXSH', 'HSHB' )
#				BaseSumHP = ( 'XXXX','BXXH', 'HXSH', 'HXXB' )

# Daytime Shift to Summit				
				
				BaseSumNoHP = ( 'XXXX','BHSB', 'BHSB', 'BHSB' )
				
# Daytime Base-Hilo SHift
	
				BaseHiloBase = ( 'XXXX','BXOB', 'BXOB', 'BXOB' )

# SA Night Shift No Acclimitization
				
				BaseSumHPSA = ( 'XXXX','BHSH', 'HXSH', 'HSHB' )

# Operator Night Shift to SUmmit - 4WD

				HPSumHP = ( 'XXXX','HXSH', 'HXSH', 'HXSH' )
			
				repcount = 0
				repcount2 = 1		
			
				
#				mfail, mfailComment, failidno = isDuped( date1, car, datein, dateout, idno2 )
#				mfail2, mfailComment2, failidno2 = isDuped( date1, car2, datein, dateout, idno2 )
				
				daycrews = False
				
				if driver == '.DayCrew1' or driver == 'DayCrew1' or driver == '.DayCrew2' :
					
					daycrews = True


				hourin2 = hourin
				hourout2 = hourout
				 
				if int( real_hourin ) > 0  :
					
					hourin2 = real_hourin + ':00'

				else: 
				
					if int( users2_hourin ) > 0  :

						hourin2 = users2_hourin + ':00'
					
				if int( real_hourout ) > 0  :
			
					hourout2 = real_hourout + ':00'

				else: 
		
					if int( users2_hourout ) > 0  :

						hourout2 = users2_hourout + ':00'	
						
				DateInDisplay = datein[2:13]				
				DateOutDisplay = dateout[2:13]				

				mfail = False
				failidno = 0

				mfail2 = False
				failidno2 = 0
			
				updateComment = '<table><tr><th>Status</th><th>Date</th><th>Destiny/Comment</th><th>InOut</th><th>Destiny</th></tr>'
				mfailComment = ''
				mfailComment2 = ''
				

#				tday = datetime.timedelta ( days = 1 )
				
				mfail3 = False
				rundate = start1

				if shift_overnight == 'Overnight' :

					rundate2 = start1 + oneday

				else:

					rundate2 = start1
					
				residnos=[]
								
#				while rundate2 <= end1 and reps > repcount :
				while reps > repcount :
				
					repcount += 1
					repcount2 = 1
									
					checkdate = rundate.strftime('%Y-%m-%d')
					checkdate2 = rundate2.strftime('%Y-%m-%d')
							
					datein2 = checkdate + ' ' + hourin2
					dateout2 = checkdate + ' ' + hourout2
											
#					if repcount > 1 and reps - repcount  > 0 :
					if repcount > 1 and reps != repcount :

						repcount2 = 2
							
						if overnight == 'Overnight' :
					
							datein2 = checkdate + ' 16:00'
							dateout2 = checkdate2 + ' 08:00'
				
						else :
					
							datein2 = checkdate + ' ' + hourin2
							dateout2 = checkdate + ' ' + hourout2

#					else :
					if reps == repcount :
					
						repcount2 = 3

						hourin2Check = hourin2

#						if shift_destiny == 'BaseSum_HP-Nights' :

#							overnight = 'Daytime'
#							hourin2Check = '08:00'
#							checkdate = checkdate2

						if overnight == 'Overnight' :
					
							datein2 = checkdate + ' 16:00'
							dateout2 = checkdate2 + ' ' + hourout2
					
						else: 
						
							datein2 = checkdate + ' ' + hourin2Check
							dateout2 = checkdate2 + ' ' + hourout2
										
				
					mfail, mfailComment3, failidno = isDuped( checkdate, car, datein2, dateout2, idno2, repcount, reps, repcount2 )
					
					mfail2, mfailComment2, failidno2 = isDuped( checkdate, car2, datein2, dateout2, idno2, repcount, reps, repcount2 )

					if mfail == True or mfail2 == True :

# any date conflict for dubug 200826å

#						mfail3 = True
											
						if failidno not in residnos :
						
							residnos.append( failidno )
							mfailComment += mfailComment3

# advance the dates
						
					tmrw = rundate + oneday
					rundate = tmrw
					
					if shift_overnight == 'Overnight' :
					
						rundate2 = tmrw	+ oneday
					
					else :
						
						rundate2 = tmrw
					
#				mfail = mfail3

				repcount = 0
				repcount2 = 0		

				if  mfail3 == False and reps > 0 :

#				if  mfail == False and mfail2 == False and reps > 0 :
					
					while reps > repcount :
					
						repcount += 1
# the First rep
						if repcount == 1:
						
							repcount2 = 1		
						
							writedate = start1
							
							if overnight == 'Daytime' :
							
								hourin = hourin2							
								hourout = hourout2

							else :
							
								hourin = hourin2							
								hourout = '08:00'
							
#							if shift_destiny == 'BaseSum_HP-Nights' :
 
							car2 = shift_car.strip()

					
						else:
						
							nextdate = datetime.timedelta( days = 1 )
							writedate = writedate + nextdate
					
						writedate2 = writedate.strftime('%Y-%m-%d')

						writedate4 = writedate.strftime('%Y-%m-%d')

#						if overnight == 'Overnight' and repcount > 1 :
						if overnight == 'Overnight' :

							nextdate = datetime.timedelta( days = 1 )
							writedate3 = writedate + nextdate
							writedate4 = writedate3.strftime('%Y-%m-%d')
					
						nextDateIn = writedate2 + ' ' + hourin
#						nextDateOut = writedate2 + ' ' + hourout
						nextDateOut = writedate4 + ' ' + hourout
											
#						if overnight == 'Overnight' and repcount == 1 :
#							
#							nextDateOut = writedate4 + ' 20:00'
# the Middle reps rep
					
						if repcount > 1 and reps != repcount :
						
							repcount2 = 2
							
							if overnight == 'Overnight' :
								
								nextDateIn = writedate2 + ' 16:00'
								nextDateOut = writedate4 + ' 08:00'
							
							else :
								
								nextDateIn = writedate2 + ' ' + hourin2
								nextDateOut = writedate4 + ' ' + hourout2
								
							if shift_car != shift_car2 :
							
								car = shift_car2.strip()
								car2 = shift_car2.strip()
							
							else :

								car = shift_car.strip()
								car2 = shift_car.strip()
								

					
						if reps == repcount :
							
							repcount2 = 3

#							if shift_destiny == 'BaseSum_HP-Nights' :

#								overnight = 'Daytime'
#								hourin2 = '08:00'
#								writedate4 = writedate2

							if overnight == 'Overnight' :
							
								nextDateIn = writedate2 + ' 16:00'
								nextDateOut = writedate4 + ' ' + hourout2
							
							else: 
								
								nextDateIn = writedate2 + ' ' + hourin2
								nextDateOut = writedate4 + ' ' + hourout2
					
						
							if shift_destiny == 'BaseSum_HP-Nights' and shift_car != shift_car2  :
								
								car = shift_car2.strip()
								car2 = shift_car2.strip()								

							else :

								car = shift_car.strip()
								car2 = shift_car.strip()
							
												
							
							

#				destinys = ( 'Base-Sum_With-HP-Nights', 'Base-Sum_No-HP-Nights', 'Base-Sum_Days-All', 'Base-Sum_Days-MonTh', 'Base-Sum_Days-MonFr' )
							
							
						if shift_destiny == 'BaseSum_HP-Nights' :
						
							if reps == repcount and shift_car != shift_car2 : 
							
								nextDestiny = BaseSumHP[ 2 ]
						
							else:
								
								nextDestiny = BaseSumHP[ repcount2 ]
							

						else:

							if shift_destiny == 'BaseSum_HP-Nights_SA' :
						
								nextDestiny = BaseSumHPSA[ repcount2 ]
							
							else :

								if shift_destiny == 'HPSum_HP-Nights' :
						
									nextDestiny = HPSumHP[ repcount2 ]
							
								else :

# BHSB all days								
									nextDestiny = BaseSumNoHP[ repcount2 ]			

						
						status = 'Active'
						
						blocking = shift_blocking
						
						dow = writedate.strftime('%a')
						
						mgo = False
						
# Night/Day Shifts - 7 Day shift
											
						if shift_destiny == 'BaseSum_HP-Nights' or shift_destiny == 'BaseSum_No-HP-Nights' or \
						shift_destiny == 'BaseSum_Days-All' or shift_destiny == 'BaseSum_HP-Nights_SA' or \
						shift_destiny == 'HPSum_HP-Nights' :

							mgo = True
				#cursor4.execute("update res set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', rdriver = '%s',  pass = '%s', pass2 = '%s', status = '%s', masterid = '%s', comment = '%s' where idno = '%s'" % (car, date, datein, dateout, overnight, destiny, driver,rdriver, pass1, pass2, status, idno, comment,  idno ) )
#							cursor4.execute("insert into res ( car, date, datein, dateout, overnight, destiny, driver, rdriver, username, timestamp, car2, status, masterid, pass, rpass,\
#							comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, monitor  ) values \
#							( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '', '', '', '0000-00-00 00:00', '0000-00-00 00:00', \
#							'0000-00-00 00:00', '0000-00-00 00:00', '0000-00-00 00:00', '0000-00-00 00:00', '%s', '%s', '%s', '', '0000-00-00 00:00', '%s', '' )" \
#							% ( car, writedate2, nextDateIn, nextDateOut, overnight, nextDestiny, driver, driver, username, today, car2, status, idno, seats, rseats, carseats, blocking ) )   		
						else:
							
# 5 Days Shifts Mon-Fri DC2
							
							baddays = ( 'Sat', 'Sun' )
# 4 Days Shifts- Mon-Th DC1		
							if shift_destiny == 'BaseSum_Days-MonTh' : 
								
								baddays = ( 'Fri', 'Sat', 'Sun' )
													
							if dow not in baddays :
								
								mgo = True
								
						DateInDisplay = str( nextDateIn )
						DateInDisplay = DateInDisplay[5:13]				
						DateOutDisplay = str( nextDateOut )					
						DateOutDisplay = DateOutDisplay[5:13]				
							
						if mgo == True :
							
							cursor4.execute("insert into res ( car, date, datein, dateout, overnight, destiny, driver, rdriver, username, timestamp, car2, status, masterid, pass, rpass,\
							comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, monitor  ) values \
							( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', \
							'0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '%s', '%s', '%s', '', '0000-00-00 00:00:00', '%s', '' )" \
							% ( car, writedate2, nextDateIn, nextDateOut, overnight, nextDestiny, driver, driver, username, today, car2, status, idno, pass1, pass1, seats, rseats, carseats, blocking ) )   				

							if repcount > 1 and reps - repcount  > -1 and shift_car != shift_car2 and shift_destiny ==  'BaseSum_HP-Nights' :
							
								car3 = shift_car.strip()

								blocking='Block-24'
							
								cursor4.execute("insert into res ( car, date, datein, dateout, overnight, destiny, driver, rdriver, username, timestamp, car2, status, masterid, pass, rpass,\
								comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, monitor  ) values \
								( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', \
								'0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '%s', '%s', '%s', '', '0000-00-00 00:00:00', '%s', '' )" \
								% ( car3, writedate2, nextDateIn, nextDateOut, overnight, nextDestiny, driver, driver, username, today, car3, status, idno, pass1, pass1, seats, rseats, carseats, blocking ) )   				



							if reps == repcount and shift_car != shift_car2 and shift_destiny == 'BaseSum_HP-Nights'  :


								car = shift_car.strip()

								overnight = 'Daytime'
								blocking = 'In-Out'

								hourin2 = '08:00'
								writedate2 = writedate4
								
								nextDateIn = writedate2 + ' ' + hourin2
								nextDateOut = writedate4 + ' ' + hourout2
								nextDestiny = 'HXXB'
								
						
								cursor4.execute("insert into res ( car, date, datein, dateout, overnight, destiny, driver, rdriver, username, timestamp, car2, status, masterid, pass, rpass,\
								comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, monitor  ) values \
								( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', \
								'0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '%s', '%s', '%s', '', '0000-00-00 00:00:00', '%s', '' )" \
								% ( car, writedate2, nextDateIn, nextDateOut, overnight, nextDestiny, driver, driver, username, today, car, status, idno, pass1, pass1, seats, rseats, carseats, blocking ) )   				


							newres_idno = cursor4.lastrowid
							newres_idno = str( newres_idno )
							
							cursor4.execute("update shifts set status='Booked' where idno = '%s'" % ( idno ) )

							new_history = today + ' - ' + username + " - Shift-Insert-Res *****\n"
							new_history += driver + ' in ' + car + '/' + car2 + ' on ' + writedate2 + ' from ' + nextDateIn + ' - ' + nextDateOut + ' ' + nextDestiny + ' ' + overnight + "\n"
							
							cursor4.execute("update res set history = '%s' where idno='%s'" % ( new_history, newres_idno ) )
				
#							updateComment += '<tr><td>Make-Res OK</td><td>' + str( writedate2 ) + ' (' + dow + ')</td><td>' + shift_destiny 
#							updateComment += ' In|Out: ' + str( nextDateIn ) + ' - ' + str( nextDateOut ) + ' Destiny: ' + nextDestiny + "<br>" 
#							updateComment += ' </td><td>' + DateInDisplay + ' - ' + DateOutDisplay + '</td><td>' + nextDestiny + "</td></tr>
							updateComment += 'mfailcomment: ' + mfailComment3
							updateComment += '<tr><td bgcolor=lime>Make-Res OK</td><td>' + str( writedate2 ) + ' (' + dow + ')</td><td>' + shift_destiny + '</td>' 
#							updateComment += ' In|Out: ' + str( nextDateIn ) + ' - ' + str( nextDateOut ) + ' Destiny: ' + nextDestiny + "<br>" 
							updateComment += '<td>' + DateInDisplay + ' - ' + DateOutDisplay + '</td><td>' + nextDestiny + "</td></tr>" 

						
						else :
							
#							updateComment += 'Shift is Not In Days:</td><td>' + str( writedate2 ) + ' (' + dow + ')</td><td>' + shift_destiny + "</td>"
#							updateComment += ' DateIn: ' + str( nextDateIn ) + ' DateOut: ' + str( nextDateOut ) + ' Destiny: ' + nextDestiny + "<br>" 
#							updateComment += '<td>' + DateInDisplay + ' - ' + DateOutDisplay + ' Destiny: ' + nextDestiny + "<br>" 

							updateComment += '<tr><td bgcolor=pink>Day NOT in Shift:</td><td>' + str( writedate2 ) + ' (' + dow + ')</td><td>' + shift_destiny + "</td>"
#							updateComment += ' DateIn: ' + str( nextDateIn ) + ' DateOut: ' + str( nextDateOut ) + ' Destiny: ' + nextDestiny + "<br>" 
							updateComment += '<td>' + DateInDisplay + ' - ' + DateOutDisplay + '</td><td>' + nextDestiny + "</td></tr>" 

							updateComment += 'mfailcomment: ' + mfailComment
							
			
				else :


				
					if mfail == True :
				
#						updateComment += '<tr><td bgcolor=pink>Make-Res FAIL Car1: ' + car + '</td><td>' + DateInDisplay + ' ' + '</td><td><b>' + mfailComment + '</b></td><td></td></tr>' 

						updateComment += '<tr><td bgcolor=pink>Make-Res FAIL Car1: ' + car + '</td><td>' + mfailComment + \
						'</td><td>This Shift: ' + DateInDisplay + ' - ' + DateOutDisplay +'</td></tr>' 
#						'</td><td>' + DateInDisplay + ' - ' + DateOutDisplay + ' reps: ' + str( reps ) + '/' + str( repcount ) +  '/' + str( repcount2 ) + '-'+str( rundate )+ '-'+str( rundate2 )+'</td></tr>' 

#						updateComment += '<br>residnos: '+str( residnos ) + '<br>'

					if mfail2 == True :
				
#						updateComment += '<tr><td bgcolor=pink>Make Res FAIL Car2: '+ car2 + ' [' + str( mfail2 ) + ' ' + str( failidno2 ) + '] ' + mfailComment2 + '<br>reps:str(reps ) + \
#						'<br>shift_date: ' + date1 + '<br>shift_datein: ' + datein + '<br>shift_dateout: ' + dateout + ' ' + '<br>' \
#						+ '<br>start1: ' + start1Date + '<br>end1: ' + end1Date + ' ' + '<br>'

#						updateComment += '<tr><td bgcolor=pink>Make-Res FAIL Car2: '+ car2 + '</td><td>' + DateInDisplay + ' ' + '</td><td><b>' + mfailComment + '</b></td><td></td></tr>' 

						updateComment += '<tr><td bgcolor=pink>Make-Res FAIL Car2: '+ car2 + '</td><td>' + mfailComment2 + \
						'</td><td>This Shift: ' + DateInDisplay + ' - ' + DateOutDisplay + '</td></tr>' 

				updateComment += '</table>'
	
	else :
		
			if method == 'GET' and int( idno ) == 0 and not date == '0000-00-00' and len( car ) > 0 :
#			
#			if not date == '0000-00-00' and len ( car ) > 0 : 

#				date1 = '2020-05-28'
				idno2 = 0
				date1 = date[0:10]
#				datein1 = date[0:10] + ' 00:00'
#				dateout1 = date[0:10] + ' 23:00'
#				datein1 = datein.strip()
#				dateout1 = dateout.strip()


				date2 = date1.split('-')

				dateOne = datetime.date( int( date2[0] ) , int( date2[1] ), int( date2[2] ) )
				tday = datetime.timedelta ( days = 1 )
				tmrw = dateOne + tday
				tmrw2 = tmrw.strftime( '%Y-%m-%d' )

				car = car.strip()
				car2 = car.strip()


				
				carseats = 4
				cursor5.execute("select pass from cars where car='%s' " % ( car ) )
				numrows5 = cursor5.rowcount
				if numrows5 > 0 :
					ruw=cursor5.fetchone()
					carseats = ruw[0]

#				if not hourin2 == 'none' and int ( hourin2 ) >= 0 and int( hourin2 ) < 24 :
#				car = 'J-02'

				pass1 = ''
				pass2 = ''
				
#				overnight = 'Overnight'
				overnight2 = overnight
				
				destiny = 'BaseSum_HP-Nights'

#				blocking = 'Block-24'
				blocking = 'In-Out'
				
				driver = driver
				rdriver = driver
				
				cursor3.execute("select user from users where stnuser = '%s'" % ( username ) )
				
				numrows3 = cursor3.rowcount
				
				if numrows3 == 1:
					
					users = cursor3.fetchone()
					real_username = users[0]
					driver = real_username.strip()
#					rdriver = real_username.strip()

				
				cursor2.execute("select hourin, hourout from users where user = '%s'" % ( driver ) )

				numrows2=cursor2.rowcount
				
				if numrows2 == 1 :
					
					raw = cursor2.fetchone()
					hourin2 = raw[0] 
					hourout2 = raw[1]
					
				
				
				if overnight2 == 'Overnight' :
				
					hourin2 = '16'
					hourout2 = '08'
				
					datein1 = date1 + ' ' + hourin2 + ':00'

#				if not hourout2 == 'none' and int ( hourout2 ) > 0 and int( hourout2 ) < 24:
					dateout1 = tmrw2 + ' ' + hourout2 + ':00'
				
				else :
				
					hourin2 = '08'
					hourout2 = '16'

					datein1 = date1 + ' ' + hourin2 + ':00'

#				if not hourout2 == 'none' and int ( hourout2 ) > 0 and int( hourout2 ) < 24:
					dateout1 = date1 + ' ' + hourout2 + ':00'

					destiny = 'BaseSum_Days-All'
				
#				status = 'Active'
				status = 'UnBooked'
#				mfail = True
				mfail = False
			
				cursor4.execute("insert into shifts ( car, date, datein, dateout, overnight, destiny, driver, username, timestamp, car2, status, blocking, pass  ) values \
				( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
				% ( car, date[0:10], datein1, dateout1, overnight2, destiny, driver, username, today, car2, status, blocking, pass1 ) ) 
				
				if date[0:7] == '2020-01' and len( car ) > 0 :
					
					cursor5.execute("update cars set traindate='%s', trainuser = '%s' where car = '%s'" % ( today, real_username, car ) ) 
				  				
				
				idno = cursor4.lastrowid
				
	
#	termlimit = str( now + term )
	pagename = '<center><b>Car-Shifts Listing</b> | %s %s [%s]<br><br>' % ( username, logcrew2, end )
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

	maintext = pagename 
	
	maintext += '<table cellpadding=3 cellspacing=3><td>'
	
	maintext += '<table cellpadding=3 cellspacing=3>'
	maintext += '<tr><td bgcolor=yellow>'
	maintext += '[ Edit ] Car, DateIn & DateOut, Day/Overnight, Driver, <br>Passengers, Destiny, [ Save ], then [ Make Res ].<br><b>ANY</b> one time-conflict stops <b>ALL</b> reseerves and reports.</td></tr>'
	maintext += '<tr><td><center>Destiny describes: Days or Nights, HP or NoHP, weekdays or weekends.</center></td></tr>'
	maintext += '<tr><td><center>You are <b>%s</b> and your shifts are <FONT SIZE=+1>%s - %s</center></td></tr>' % ( real_username, user_hourin, user_hourout )

	maintext += '</table>'

	maintext += '</td><td>'
	
	maintext += '<table>'
	maintext += '<tr><th>Destiny Key</th><th>Description</th></tr>'
	maintext += '<tr><td>BaseSum_HP-Nights</td><td>Operator Nights - HP with Base-HP 1st nite</td></tr>'
	maintext += '<tr><td>BaseSum_HP-Nights_SA</td><td>SA Nights - HP with Base-Sum-HP 1st nite</td></tr>'
	maintext += '<tr><td>BaseSum_NoHP-Nights</td><td>Night staff stays at Base in daytime</td></tr>'
	maintext += '<tr><td>BaseSum_Days-All</td><td>All 7 days reserved, days and weekends</td></tr>'
	maintext += '<tr><td>BaseSum_Days-MonFri</td><td>only Mon-Fri are reserved</td></tr>'
	maintext += '<tr><td>BaseSum_Days-MonTh</td><td>only Mon-Th are reserved</td></tr>'
	maintext += '<tr><td>HPSum_HP-Nights</td><td>HP-Sum-HP only</td></tr>'
	maintext += '</table>'
	
	maintext += '</td></table><br>'
	
#	date = '2020-06-26'

	cursor.execute("select idno, car, date, datein, dateout, overnight, driver, destiny, username, timestamp, car2, status, blocking, pass from shifts where idno = '%s'" % ( idno ) )

	numrows=cursor.rowcount

#	maintext += ('Subaru SciOps Car Shifts - %s<br><br>' % ( username )  )

	boxtext = 'numrows ( ' + str( numrows ) + " )<br>Day Check:<br>"+ updateComment + "<br>"

	boxtext += '<table>'
	boxtext += '<tr><th>DayIn</th><th>DayOut</th><th>Car</th><th>Driver</th><th>Overnight</th></tr>'

	if numrows == 1 :
	
		seq = 0
	
		running_end = 0

		for row in cursor.fetchall() :
		
			seq += 1
		
			shift_idno = row[0]		
			shift_car = row[1]		
			shift_date = str( row[2] )	
			shift_datein = str( row[3] )
			shift_hourin = shift_datein[ 5:16 ]


			shift_overnight = row[5]
			
			shift_driver = row[6]
			shift_driver = shift_driver.strip()
			
			shift_destiny = row[7]	
			shift_username = row[8]	
			shift_timestamp = str( row[9] )	
			shift_car2 = row[10]	
			shift_status = row[11]	
			shift_status = shift_status.strip()
			shift_blocking = row[12]	
			shift_blocking = shift_blocking.strip()
			shift_pass = row[13]	
			shift_pass = shift_pass.strip()
			

			shiftin1 = shift_datein[ 0:10 ]

			shift_dateout = str( row[4] )
			
			shift_hourout = shift_dateout[ 5:16 ]
			
			shiftout1 = shift_dateout[ 0:10 ]

			shift_hourin2 = shift_datein[ 11:13 ]
			shift_hourout2 = shift_dateout[ 11:13 ]

# count the days

			## Difference between two date
			shiftin2 = shiftin1.split( '-' )
			shiftout2 = shiftout1.split( '-' )
			# date objects
			yearin = int( shiftin2[0] )
			monthin = int( shiftin2[1] )
			dayin = int( shiftin2[2] )

			yearout = int( shiftout2[0] )
			monthout = int( shiftout2[1] )
			dayout = int( shiftout2[2] )
			
			date_1 = datetime.date( year = yearin, month = monthin, day = dayin )
			date_2 = datetime.date( year = yearout, month = monthout, day = dayout )
 
			# difference between days
			date_delta = date_2 - date_1        # date difference in timedelta data type

			number_of_days = date_delta.days  # days in integer
	
			daystring = " ( %s Nights )" % ( number_of_days )

			if shift_overnight == 'Daytime' :
			
				number_of_days += 1
				daystring = " ( %s Days )"  % ( number_of_days )
			
			cursor2.execute("select hourin, hourout from users where user = '%s'" % ( shift_driver ) )

			numrows2=cursor2.rowcount
			
			if numrows2 == 1 :
				
				raw = cursor2.fetchone()
				driver_hourin2 = raw[0] 
				driver_hourout2 = raw[1]


			postValuesShow = ( 'Save', 'Cancel', 'Delete', 'Make Res', 'Delete Res' )

			if method == 'GET' or ( method == 'POST' and field['action'].value in postValuesShow ) :

				cursor2.execute("select idno, car, date, datein, dateout, overnight, driver from res where masterid = '%s' order by datein desc" % ( shift_idno ) )

				numrows2=cursor2.rowcount

				if shift_status == 'Booked' :
					
					maintext += "[ <b>To Edit,</b> first Delete Res for <b>( " + str( numrows2 ) + " )</b> Reserves</b>  - (#%s)  ]<br><br>" % ( shift_idno )
				
				else : 
					
					maintext += "<form method=post action='shiftone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( shift_idno )

# ShiftBox Table
				maintext += '<table><td valign=top>'

# ShiftTable left box
				
				maintext += '<table>'
				
				shift_month2 = shift_date[0:7]
				
				if shift_month2 == '2020-01' and shift_overnight == 'Daytime' :

					maintext += '<tr><td colspan=2 bgcolor=yellow><FONT SIZE=+1>Your 1st Training Goal is <b>5 Daytime reserves</b> from %s in %s.<br> \
					Try Edit, modify DateOut 01-05, Save, then [ Make Res ]</td></tr>' % ( shift_date, shift_car )

				if shift_month2 == '2020-01' and shift_overnight == 'Overnight' :

					maintext += '<tr><td colspan=2 bgcolor=yellow><FONT SIZE=+1>Your 2nd Training Goal is <b>6 Overnight reserves</b> from %s in %s.<br> \
					Try Edit, modify DateOut 01-07, Overnight, Destiny: BaseSum_HP-Nights, Save, then [ Make Res ]</td></tr>' % ( shift_date, shift_car )
				
				maintext += '<tr><td class=right>IDNo:</td><td>%s</td></tr>' % ( shift_idno )
				maintext += '<tr><td class=right>Car:</td><td>%s | Car2: %s</td></tr>' % ( shift_car, shift_car2 )
				maintext += '<tr><td class=right>Date:</td><td>%s</td></tr>' % ( shift_date )
				maintext += '<tr><td class=right>1st Depart:</td><td>%s</td></tr>' % ( shift_datein )
				maintext += '<tr><td class=right>Last Arrive:</td><td>%s %s</td></tr>'	 % ( shift_dateout, daystring )		
				maintext += '<tr><td class=right>Overnight:</td><td>%s</td></tr>' % ( shift_overnight )
				maintext += '<tr><td class=right>Driver:</td><td>%s ( %s - %s )</td></tr>' % ( shift_driver, driver_hourin2, driver_hourout2 )				
				maintext += '<tr><td class=right>Passengers:</td><td>%s</td></tr>' % ( shift_pass )				
				maintext += '<tr><td class=right>Destiny:</td><td>%s</td></tr>' % ( shift_destiny )				
				maintext += '<tr><td class=right>Status:</td><td>%s</td></tr>' % ( shift_status )				
				maintext += '<tr><td class=right>Blocking:</td><td>%s</td></tr>' % ( shift_blocking )				
##				maintext += '</table>'

				if int( driver_hourin2 ) > 0 and username in night_users :
				
					realin = driver_hourin2
				
				else :
				
					realin = shift_hourin2

				if int( driver_hourout2 ) > 0 and username in night_users :
			
					realout = driver_hourout2
				
				else:
				
					realout = shift_hourout2
				
				
				if numrows2 > 0 :
					
					maintext += "<tr><td class=right>Current Reserves: ( %s )</td><td><form method=post action=shiftone.py?idno=%s><input name=action type=submit value='Delete Res'>\
					</form></td></tr></td></tr>" % ( numrows2, shift_idno )	
					
					if shift_month2 == '2020-01' and shift_overnight == 'Daytime' and numrows2 == 5:

						maintext += '<tr><td colspan=2 bgcolor=yellow><FONT SIZE=+1>You PASSED 1st Goal of 5 Daytimes!<br>Your <b>2nd</b> Training Goal is <b>6 Overnights</b> from %s in %s.<br>\
						Try [Delete Res], Edit, Modify to Overnight, Save, then follow instructions at top.</td></tr>' % ( shift_date, shift_car )

					if shift_month2 == '2020-01' and shift_overnight == 'Overnight' and numrows2 == 6:

						maintext += '<tr><td colspan=2 bgcolor=yellow><FONT SIZE=+1>You PASSED 2nd Goal of 6 Overnights!<br> \
						email winegar@naoj.org with email subject: PASSED! Shift IDNo: %s</td></tr>' % ( shift_idno )
								
				
				else :

					maintext += "<tr><td class=right>Current Reserves ( 0 ) :</td>"
				
					if number_of_days == 1 :
					
						maintext += "<td bgcolor=yellow><b>Do not use Shifts for 1-Day/Night</b><br>Use Cars Today or Calendar!</td></tr>" 			

					else :

						maintext += "<td><form method=post action=shiftone.py?idno=%s>" % ( shift_idno )	
						maintext += "1st Depart | Last Arrive: <input type=text name=realin size=4 value='%s'> | <input type=text name=realout size=4 value='%s'> | " % ( realin, realout )
						maintext += "<input name=action type=submit value='Make Res'></form></td></tr>" 			
					
# Shift Out Table
				maintext += '</table>'
#Shift Open Cars Box Table
				maintext += '</td><td valign=top>'
				maintext += 'Quick-Date-Conflicts (time-conflicts display in Make Res)<br>'
				
				cursor3.execute("select car from cars where status='Active' order by seq")
				numrows3=cursor3.rowcount

				cars1 = '<table>'
#				'<tr><th>Car</th><th>Possible Conflicts</th></tr>'

				for result3 in cursor3.fetchall() :

					car3 = result3[0]
					car3 = car3.strip()

					cursor4.execute("select car, date, driver, datein, dateout  from res where date >= '%s' and date <= '%s' and car = '%s' and status='Active' order by date" % ( shiftin1, shiftout1, car3 ) )
					numrows4=cursor4.rowcount
					textFour=''

					if numrows4 > 0 :

						textFour += '(' + str( numrows4 ) + ') '
						seqFour = 0
						for result4 in cursor4.fetchall() :

							seqFour += 1
							carFour = result4[0]
							dateFour = str( result4[1] )
							driverFour = result4[2]
							hourinFour = str( result4[3] )
							hourinFour = hourinFour[ 11:13 ]
							houroutFour = str( result4[4] )
							houroutFour = houroutFour[ 11:13 ]
							if seqFour < 4 :
							
								textFour += dateFour[5:10] + ' (' + hourinFour + '-' + houroutFour + ') ' + driverFour + ', '

					else :

						textFour+= '(0)'

					if numrows4 > 0 :
					
						if numrows4 > 3 :
							
							remaining = str( numrows4 - 3 )
							
							cars1 += "<tr><td>%s</td><td>%s <b>(+%s)</b></td></tr>" % ( car3, textFour, remaining )
						
						else:
							
							cars1 += "<tr><td>%s</td><td>%s</td></tr>" % ( car3, textFour )
					
					else:
						
						cars1 += "<tr><td><b>%s</b></td><td><b>%s</b></td></tr>" % ( car3, textFour )

				cars1 += '</table>'
				maintext += cars1

			
#Shift Box Table				
				maintext += '</td></table>'
				
#
				maintext += '<table><tr><td colspan=9 bgcolor=lime><center><b>Reserves for this Shift</b></center></td></tr>'
				maintext += '<tr><th>Car</th><th>Car2</th><th>Date</th><th>In-Out</th><th>Overnight</th><th>Driver</th><th>Blocking</th><th>Destiny</th></tr>'
	
#				maintext += "date: %s hourin: %s hourout %s car: %s driver: %s overnight: %s<br>" % ( shift_date, shift_hourin, shift_hourout, shift_car, shift_driver, shift_overnight )
#				boxtext += "<td bgcolor=lime>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><tr>" % (  shift_hourin, shift_hourout, shift_car, shift_driver, shift_overnight )
#
				cursor2.execute("select idno, car, date, datein, dateout, overnight, driver, car2, blocking, destiny from res where masterid = '%s' order by datein" % ( shift_idno ) )

				numrows2=cursor.rowcount

				if numrows2 > 0 :
			
					for raw in cursor2.fetchall() :
	
						seq += 1
	
						res_idno = raw[0]		
						res_car = raw[1]		
						res_date = str( raw[2] )	
						res_date2 = raw[2]	
						res_datein = str( raw[3] )
						res_hourin = res_datein[11:13]
						res_dateout = str( raw[4] )
						res_hourout = res_dateout[11:13]
						res_overnight = raw[5]
						res_driver = raw[6]
						res_car2 = raw[7]		
						res_blocking = raw[8]		
						res_destiny = raw[9]
						
						cursor3.execute("select name from destiny where code = '%s'" % ( res_destiny ) )

						numrows3=cursor3.rowcount

						destinyName = 'None'

						if numrows3 == 1 :
			
							raw = cursor3.fetchone()
							destinyName = raw[0]
								
						dow2 = res_date2.strftime('%a')
						
						res_overnight = res_overnight.strip()
#
						if res_overnight == 'Overnight' :
							
							maintext += "<td>%s</td><td>%s</td><td><a href=resone.py?idno=%s>%s %s</a></td><td bgcolor=lime>%s&nbsp;->&nbsp;%s</td><td bgcolor=lime>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
							% (  res_car, res_car2, res_idno, res_date, dow2, res_hourin, res_hourout, res_overnight, res_driver, res_blocking, res_destiny, destinyName  )
						
						else: 
							
							maintext += "<td>%s</td><td>%s</td><td><a href=resone.py?idno=%s>%s %s</a></td><td bgcolor=white>%s&nbsp;-&nbsp;%s</td><td bgcolor=white>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
							% (  res_car, res_car2, res_idno, res_date, dow2, res_hourin, res_hourout, res_overnight, res_driver, res_blocking, res_destiny, destinyName  )
			
				else :
					
					maintext += "<td bgcolor=pink colspan=5>No Car Reservations for Shift-ID: %s</td></tr>" % (  shift_idno )
				
				maintext += "</table>"
			
			if method == 'POST' and field['action'].value == 'Edit' :

				destinys = ( 'BaseSum_HP-Nights', 'BaseSum_HP-Nights_SA', 'BaseSum_No-HP-Nights', 'BaseSum_Days-All', 'BaseSum_Days-MonTh', \
				'BaseSum_Days-MonFr', 'HPSum_HP-Nights'  )

				destinyCtrl = '<select size=1 name=destiny>'
		 	
				for code in destinys :

					if shift_destiny == code:

						destinyCtrl += '<option value=%s selected>%s' % (  code, code )
						
					else:

						destinyCtrl += '<option value=%s>%s' % ( code, code )

				destinyCtrl += '</select>'

				status1 = ( 'Booked', 'UnBooked', 'Cancel' )
				statusCtrl = '<select size=1 name=status>'
				for status2 in status1 :
					if shift_status == status2 :
						statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
					else:
						statusCtrl += '<option value=%s>%s' % ( status2, status2 )
#
				statusCtrl += '</select>'
			
				overnight1 = ( 'Daytime', 'Overnight' )
				overnightCtrl = '<select size=1 name=overnight>'
				for overnight2 in overnight1 :
					if shift_overnight == overnight2 :
						overnightCtrl += '<option value=%s selected>%s' % ( overnight2, overnight2 )
					else:
						overnightCtrl += '<option value=%s>%s' % ( overnight2, overnight2 )

				overnightCtrl += '</select>'
				
				blocking1 = ( 'In-Out', 'Block-24' )
				blockCtrl = '<select size=1 name=blocking>'
				for block2 in blocking1 :
					if shift_blocking == block2 :
						blockCtrl += '<option value=%s selected>%s' % ( block2, block2 )
					else:
						blockCtrl += '<option value=%s>%s' % ( block2, block2 )

				blockCtrl += '</select>'
				

# Driver Spinner

				cursor3.execute( "select user from users where train='D' order by user" )

				numrows3 = cursor3.rowcount

				driver2 = '<select name=driver>'

				for result3 in cursor3.fetchall() :

					driver3 = result3[0]
					driver3 = driver3.strip()

					if driver3 == shift_driver :
		
						driver2 += "<option value='%s' selected>%s" % ( driver3, driver3 )
		
					else :
		
						driver2 += "<option value='%s'>%s" % ( driver3, driver3 )

				driver2 += '</select>'


				cursor3.execute("select car from cars order by seq")
				numrows3=cursor3.rowcount

				cars1 = '<select name=car>'

				for result3 in cursor3.fetchall() :

					car3 = result3[0]
					car3 = car3.strip()

					if car3 == shift_car :
		
						cars1 += "<option value='%s' selected>%s" % ( car3, car3 )
		
					else :
		
						cars1 += "<option value='%s'>%s" % ( car3, car3 )

				cars1 += '</select>'
				

				cursor3.execute("select car from cars order by seq")
				numrows3=cursor3.rowcount

				cars2 = '<select name=car2>'

				for result3 in cursor3.fetchall() :

					car3 = result3[0]
					car3 = car3.strip()

					if car3 == shift_car2 :
		
						cars2 += "<option value='%s' selected>%s" % ( car3, car3 )
		
					else :
		
						cars2 += "<option value='%s'>%s" % ( car3, car3 )

				cars2 += '</select>'
			
				maintext += "<form method=post action='shiftone.py?idno=%s'><input name=action type=submit value='Save'><input name=action type=submit value='Cancel'>" % ( shift_idno )
				maintext += '<table cellpadding=3 cellspacing=3>'
#				maintext += "<tr><td class=right>Car:</td><td><input type=text name=car size=10 value='%s'></td></tr>" % ( shift_car ) 
#				maintext += "<tr><td class=right>Car2:</td><td><input type=text name=car2 size=10 value='%s'></td></tr>" % ( shift_car2 ) 

				shift_month2 = shift_date[0:7]

				if shift_month2 == '2020-01' and shift_overnight == 'Daytime' :

					maintext += '<tr><td colspan=2 bgcolor=yellow><FONT SIZE=+1>Your 1st Goal is <b>5 Daytime reserves</b> from %s in %s.<br> \
					Try Edit, modify DateOut, Save, then [ Make Res ]</td></tr>' % ( shift_date, shift_car )

				if shift_month2 == '2020-01' and shift_overnight == 'Overnight' :

					maintext += '<tr><td colspan=2 bgcolor=yellow><FONT SIZE=+1>Your 2nd Goal is <b>6 Overnight reserves</b> from %s in %s.<br> \
					Try Edit, modify DateOut, Overnight, Destiny: BaseSum_HP-Nights, Save, then [ Make Res ]</td></tr>' % ( shift_date, shift_car )


				maintext += "<tr><td class=right>Cars:</td><td>%s | %s</td></tr>" % ( cars1, cars2 ) 
				maintext += "<tr><td class=right>Date:</td><td><input type=text name=date size=16 value='%s'></td></tr>" % ( shift_date ) 
				maintext += "<tr><td class=right>1st Depart | Last Arrive:</td><td><input type=text name=datein size=18 value='%s'> | " % ( shift_datein[0:16] ) 
				maintext += "<input type=text name=dateout size=18 value='%s'></td></tr>" % ( shift_dateout[0:16] ) 
#				maintext += "<tr><td class=right>Overnight:</td><td><input type=text name=overnight size=20 value='%s'></td></tr>" % ( shift_overnight ) 
				maintext += "<tr><td class=right>Overnight:</td><td>%s</td></tr>" % ( overnightCtrl ) 
#				maintext += "<tr><td class=right>Driver:</td><td><input type=text name=driver size=20 value='%s'></td></tr>" % ( shift_driver ) 
				maintext += "<tr><td class=right>Driver:</td><td>%s</td></tr>" % ( driver2 ) 
				maintext += "<tr><td class=right>Passengers:</td><td><input type=text name=pass1 size=30 value='%s'></td></tr>" % ( shift_pass ) 
				maintext += "<tr><td class=right>Destiny:</td><td>%s</td></tr>" % ( destinyCtrl ) 
				maintext += "<tr><td class=right>Status:</td><td>%s</td></tr>" % ( statusCtrl ) 
				maintext += "<tr><td class=right>Blocking:</td><td>%s</td></tr>" % ( blockCtrl ) 
				maintext += '</form>'
				maintext += '</table>'
	
	else:
	
		boxtext += "<td bgcolor=pink colspan=5>No Shifts for Shifts-IDNo: %s</td><td></td></tr>" % (  idno )

	boxtext += '</tr></table>'
	maintext += boxtext

else:

	maintext = logproc.returnLogin()
	
printHTML( maintext )
		
