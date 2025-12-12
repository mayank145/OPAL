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

method=os.environ.get("REQUEST_METHOD","")

field = cgi.FieldStorage()

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()
cursor5=db.cursor()
cursor6=db.cursor()
cursor7=db.cursor()
cursor4.execute("set autocommit = 1")

#MariaDB [sumlogs]> desc res;
#+-----------+-------------+------+-----+---------+----------------+
# Field     | Type        | Null | Key | Default | Extra          |
#+-----------+-------------+------+-----+---------+----------------+
#| idno      | int(11)     | NO   | PRI | NULL    | auto_increment |
#| car       | char(10)    | YES  |     | NULL    |                |
#| date      | date        | YES  |     | NULL    |                |
#| datein    | datetime    | YES  |     | NULL    |                |
#| dateout   | datetime    | YES  |     | NULL    |                |
#| overnight | char(1)     | YES  |     | NULL    |                |
#| dateb     | datetime    | YES  |     | NULL    |                |
#| datec     | datetime    | YES  |     | NULL    |                |
#| dated     | datetime    | YES  |     | NULL    |                |
#| datee     | datetime    | YES  |     | NULL    |                |
#| destiny   | char(4)     | YES  |     | NULL    |                |
#| comment   | char(100)   | YES  |     | NULL    |                |
#| history   | mediumtext  | YES  |     | NULL    |                |
#| driver    | char(20)    | YES  |     | NULL    |                |
#| rdriver   | char(20)    | YES  |     | NULL    |                |
#| datea     | datetime    | YES  |     | NULL    |                |
#| datef     | datetime    | YES  |     | NULL    |                |
#| pass      | varchar(80) | YES  |     | NULL    |                |
#| rpass     | varchar(80) | YES  |     | NULL    |                |
#| masterid  | int(11)     | YES  |     | NULL    |                |
#| status    | char(10)    | YES  |     | NULL    |                |
#| car2      | char(10)    | YES  |     | NULL    |                |
#+-----------+-------------+------+-----+---------+----------------+
#22 rows in set (0.01 sec)

def isDuped( date, car, datein, dateout, idno2 ) :

	datein2 = datein.split('-')
	dayin2=datein2[2]
	dayin2=dayin2[0:2]
	hourin2 = datein[11:13]
	minin2 = datein[14:16]
	datein3 = datetime.datetime ( int( datein2[0] ), int( datein2[1] ), int( dayin2 ), int( hourin2 ), int( minin2 ), 0 )
	datein4 = str( datein3 )
	datein4 = datein4[5:16]
	
	dateout2 = dateout.split('-')
	dayout2=dateout2[2]
	dayout2=dayout2[0:2]
	hourout2 = dateout[11:13]
	minout2 = dateout[14:16]
	dateout3 = datetime.datetime ( int( dateout2[0] ), int( dateout2[1] ), int( dayout2 ), int( hourout2 ), int( minout2 ), 0 )
	dateout4 = str( dateout3 )
	dateout4 = dateout4[5:16]

	date1 = date.split('-')

	today2 = datetime.date( int( date1[0] ) , int( date1[1] ), int( date1[2] ) )
	yday = datetime.timedelta ( days = 1 )
	yesterday = today2 - yday
	yday2 = yesterday.strftime( '%Y-%m-%d' )

	cursor2.execute("select idno, car, date, datein, dateout, overnight, driver, blocking, car2 from res where ( date='%s' or date = '%s' ) \
	and ( car = '%s' or car2 = '%s' ) and status = 'Active' order by datein" % ( date, yday2, car, car ) )
	numrows2=cursor2.rowcount

	mfail = False
	mfailComment = ''
	failidno = 0

#	mfailTable = '<table><tr><th colspan=7 bgcolor=pink><FONT SIZE=+1><b>Your Reservation Conflicts with ' + str(numrows2) + '</FONT></th></tr>'
	if numrows2 > 0 :
		
		mfailTable = '<table>' 

		if datein4[0:5] == dateout4[0:5] :
		
			mfailTable += '<tr><th colspan=7 bgcolor=pink><FONT SIZE=+1>Your update: ' + datein4 + ' to ' + dateout4 +'</FONT></th></tr>'

		else :

			mfailTable += '<tr><th colspan=7 bgcolor=pink><FONT SIZE=+1>Your update: Overnight ' + datein4 + ' to ' + dateout4 +'</FONT></th></tr>'

		mfailTable += '<tr><th colspan=7 bgcolor=pink><FONT SIZE=+1><b>Conflicts with others !</FONT></th></tr>'


		mfailTable += '<tr><th>Failure Reason</th><th>IDNo</th><th>Car</th><th>DateIn</th><th>DateOut</th><th>Overnight</th><th>Driver</th></tr>'
	
		for rew in cursor2.fetchall() :

			res_idno = rew[0]
			res_car = rew[1]
			res_date = rew[2]
			res_datein = rew[3]
			res_dateout = rew[4]
			res_overnight = rew[5]
			res_driver = rew[6]
			res_blocking = rew[7]
			res_blocking = res_blocking.strip()

			res_car2 = rew[8]
		
			res_datein2 =  str( res_datein )
		
			res_hourin2 = res_datein2[11:13]
			res_minin2 = res_datein2[14:16]
			
			res_datein3 = res_datein2[0:10]
		
			res_dateout2 =  str( res_dateout )

			res_hourout2 = res_dateout2[11:13]
			res_minout2 = res_dateout2[14:16]
			
			res_dateout3 = res_dateout2[0:10]
						
#			print("test res: " + res_car  ) 
#			print("test res: " + res_car + ' ' + str( res_idno ) + ' ' + str( res_date ) + ' ' + res_overnight + ' dtein: ' + str( res_datein ) + " dtout: " + str( res_dateout ) ) 
# debug
#			mfailTable += '<tr><td>check  - idno: </td><td>(' + str( res_idno ) + '</td><td>'+res_car+'</td><td> intime: ' + res_datein2 +  '</td><td>outtime: ' + res_dateout2 + '</td><td>' + res_overnight + '</td></tr>'
			if not res_idno == idno2 :

# debug
#				mfailTable += '<tr><td>NOT IDNo: </td><td>(' + str( res_idno ) + '</td><td>'+res_car+'</td><td> intime: ' + res_datein2 + '/'+ str(datein3)+ '</td><td>outtime: ' + res_dateout2 + '/'+str(dateout3)+'</td><td>' + res_overnight + '</td></tr>'

# completely outside other ress
				
				if datein3 < res_datein and dateout3 > res_dateout :
	
					mfail = True
					mfailComment += 'Start-End Outside - idno: (' + str( res_idno ) + ') intime: ' + res_datein2[5:16] +  ' outtime: ' + res_dateout2[5:16] + '<br>'
					mfailTable += '<tr><td>Start-End Outside</td><td>(' + str( res_idno ) + ')</td><td>'  + res_car + ' | ' + res_car2  + '</td><td>' + res_datein2[5:16] + '</td><td>' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
					 + res_driver + '</td</tr>'
					failidno = res_idno


# completely same or completely within other res
				
				if datein3 >= res_datein and dateout3 <= res_dateout :
					
					mfail = True
					mfailComment += 'all inside - idno: (' + str( res_idno ) + ') intime: ' + res_datein2[5:16] +  ' outtime: ' + res_dateout2[5:16] + '<br>'
					mfailTable += '<tr><td>Start-End Inside</td><td>(' + str( res_idno ) + ')</td><td>'  + res_car + ' | ' + res_car2  + '</td><td>' + res_datein2[5:16] + '</td><td>' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
					 + res_driver + '</td</tr>'
					failidno = res_idno
# dateout within
#				if datein3 < res_datein and dateout3 >= res_datein and dateout3 <= res_dateout  :
# if dateout3 == datein, its OK = New Res Ends When Old Res Starts
				if datein3 < res_datein and dateout3 > res_datein and dateout3 <= res_dateout  :
					
					mfail = True
					mfailComment += 'starts inside - idno: (' + str( res_idno ) + ') intime: ' + res_datein2[5:16]  + ' outtime: ' + res_dateout2[5:16] + '<br>'
					mfailTable += '<tr><td>Starts Inside</td><td>(' + str( res_idno ) + ')</td><td>'  + res_car  + ' | ' + res_car2 + '</td><td>' + res_datein2[5:16] + '</td><td>' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
					+ res_driver + '</td</tr>'
					failidno = res_idno
# datein within
#				if dateout3 > res_dateout and datein3 >= res_datein and datein3 <= res_dateout  :
# if datein3 == dateout, its OK. New Res Starts When Old Res Ends
				if dateout3 > res_dateout and datein3 >= res_datein and datein3 < res_dateout  :
					
					mfail = True
					mfailComment += 'ends inside - idno: ('+ str( res_idno ) + ') intime: ' + res_datein2[5:16] + ' outtime: ' + res_dateout2[5:16] + '<br>'
					mfailTable += '<tr><td>Ends Inside</td><td>(' + str( res_idno ) + ')</td><td>'  + res_car  + ' | ' + res_car2 + '</td><td>' + res_datein2[5:16] + '</td><td>' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
					 + res_driver + '</td</tr>'
					failidno = res_idno

# if same datein and Block-24
				
#				if datein3 == res_datein3 and res_blocking == 'Black-24' :
				if datein3 == res_datein3 and res_blocking == 'Block-24' :

					mfail = True
					mfailComment += 'Block-24 - idno: (' + str( res_idno ) + ') intime: ' + res_datein2[5:16] +  ' outtime: ' + res_dateout2[5:16] + '<br>'
					mfailTable += '<tr><td>Block-24</td><td>(' + str( res_idno ) + ')</td><td>'  + res_car + ' | ' + res_car2  + '</td><td>' + res_datein2[5:16] + '</td><td>' + res_dateout2[5:16] + '</td><td>' + res_overnight + '</td><td>' \
					 + res_driver + '</td</tr>'
					failidno = res_idno

	
		mfailTable +='</table>'

		mfailComment = mfailTable
			
	else:

		mfail = False
		mfailComment = 'No conflicts'
		failidno = 0
				
	return ( mfail, mfailComment, failidno )


#def isBlacked( date, car, datein, dateout, idno2, destiny, car2 ) :
def isBlacked( date, car, datein, dateout, idno2, destiny ) :

	datein2 = datein.split('-')
	dayin2 = datein2[2]
	dayin2 = dayin2[0:2]
	hourin2 = datein[11:13]
	minin2 = datein[14:16]
	datein3 = datetime.datetime ( int( datein2[0] ), int( datein2[1] ), int( dayin2 ), int( hourin2 ), int( minin2 ), 0 )

	dateout2 = dateout.split('-')
	dayout2=dateout2[2]
	dayout2=dayout2[0:2]
	hourout2 = dateout[11:13]
	minout2 = dateout[14:16]
	dateout3 = datetime.datetime ( int( dateout2[0] ), int( dateout2[1] ), int( dayout2 ), int( hourout2 ), int( minout2 ), 0 )

	date1 = date.split('-')

	today2 = datetime.date( int( date1[0] ) , int( date1[1] ), int( date1[2] ) )
	yday = datetime.timedelta ( days = 1 )
	yesterday = today2 - yday
	yday2 = yesterday.strftime( '%Y-%m-%d' )
	
	dateYear = date1[0]
	
	dateYear2 = int ( dateYear ) + 1
	dateYear3 = str( dateYear2 )

#	cursor2.execute("select idno, car, date, datein, dateout, overnight, driver, blocking, car2 from res where ( date='%s' or date = '%s' ) \
#	and ( car = '%s' or car2 = '%s' ) and status = 'Active' order by datein" % ( date, yday2, car, car ) )
#	numrows2=cursor2.rowcount

	cursor2.execute("select idno, car, start, end, recur, type, warning from blackres where car = '%s' and status='Active' order by start" % ( car ) )
	numrows2 = cursor2.rowcount

	mfail = False
	mfailComment = ''
	failidno = 0

	if numrows2 > 0 :
		
		mfailTable = '<table><tr><th colspan=4 bgcolor=pink><FONT SIZE=+1><b>Your Reservation Blacked-Out !</FONT></th></tr>'
		mfailTable += '<tr><th>Failure Reason</th><th>Warning</th><th>DateIn</th><th>DateOut</th></tr>'
	
		for rew in cursor2.fetchall() :

			blackres_car = ruw[1]
			blackres_start = str( ruw[2] )
			blackres_end = str( ruw[3] )
			blackres_recur = ruw[4]
			blackres_type = ruw[5]
			blackres_warning = ruw[6]

			blackres_recur = blackres_recur.strip()

			blackres_start2 = dateYear + '-' + blackres_start[5:10]
			blackres_end2 = dateYear3 + '-' + blackres_end[5:10]

			if blackres_recur == 'Yearly':
				
				if date >= blackres_start2 and date <= blackres_end2 :		
					
					mfail = True
					mfailComment += 'BlackOut Yearly: (' + blackres_type + ') Begins: ' + blackres_start2 +  ' Ends: ' + blackres_end2 + '<br>'
					mfailTable += '<tr><td>' + blackres_type + '</td><td>(' + blackres_warning + ')</td><td>' + blackres_start2 + '</td><td>' + blackres_end2 + '</td</tr>'
					failidno = 0
				
			else : 
				
				if date >= blackres_start and date <= blackres_end :		

					mfail = True
					mfailComment += 'BlackOut InOut: (' + blackres_type + ') Begins: ' + blackres_start +  ' Ends: ' + blackres_end + '<br>'
					mfailTable += '<tr><td>' + blackres_type + '</td><td>(' + blackres_warning + ')</td><td>' + blackres_start + '</td><td>' + blackres_end + '</td</tr>'
					failidno = 0
				
		mfailTable +='</table>'

		mfailComment = mfailTable
			
	else:

		mfail = False
		mfailComment = 'No conflicts'
		failidno = 0
				
	return ( mfail, mfailComment, failidno )
	

def getCSS( hourin, hourout, username ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "th.big { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px; font-weight: bold }"
	css_text += "td.label2 { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 12px; font-weight: bold }"
	css_text += "</style>"
	css_text += "<script src='https://code.jquery.com/jquery-1.12.4.js'></script>"
	css_text += "<script src='https://code.jquery.com/ui/1.12.1/jquery-ui.js'></script>"
	css_text += "<script>"
#	css_text += '$( function() { $( "#slider-range" ).slider({range: true, min: 0,max: 24, values: [ 8, 16 ], step: .5, '
	css_text += '$( function() { $( "#slider-range" ).slider({ range: true, min: 0,max: 24, values: [ ' + hourin + ', ' + hourout +  '], step: .5, '
	css_text += 'slide: function( event, ui ) { $( "#amount" ).val( "[ " + ui.values[ 0 ] + " - " + ui.values[ 1 ] + " ]" );'
	css_text += '$( "#amountMin" ).val( ui.values[ 0 ] );'
	css_text += '$( "#amountMax" ).val( ui.values[ 1 ] );'
	css_text += '} });'
	css_text += '$( "#amount" ).val( "[ " + $( "#slider-range" ).slider( "values", 0 ) + ":00 - " + $( "#slider-range" ).slider( "values", 1 ) + ":00 ]" );'
	css_text += '$( "#amountMin" ).val( $( "#slider-range" ).slider( "values", 0 ) );'
	css_text += '$( "#amountMax" ).val( $( "#slider-range" ).slider( "values", 1 ) );'
	css_text += ' });'
	css_text += "</script>"

	css_text += "<script>"
	css_text += " $( function() { "
	css_text += "     var availableTags = ["
	
#	cursor3.execute("select distinct pass from res where username='%s' \
	cursor3.execute("select pass from res where username='%s' " % ( username ) )
#	cursor3.execute("select pass from res where username='winegar'" )

	numrows3=cursor3.rowcount
	oldPass = []

	if numrows3 > 0: 
		for ruw in cursor3.fetchall() :
			css_text += "'" + ruw[0] + "',"
			oldPass.append( ruw[0] )
	else:
		css_text += "'none,'" 
		oldPass.append( 'none' )

#	css_text += "<script>"
#	css_text += " $( function() { "
#	css_text += "     var availableTags = ["
#	css_text += "     var availableTags = "
#	css_text += oldPass
#	css_text += " 'ActionScript', "
#	css_text += " 'AppleScript', "
#	css_text += " 'Asp' "
	css_text += "];"
	css_text += '$( "#tags" ).autocomplete({'
	css_text += '  source: availableTags'
	css_text += '  });'
	css_text += "  });"
	css_text += "</script>"

	css_text += "<link rel='stylesheet' href='//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css'>"
	css_text += "<link rel='stylesheet' href='/resources/demos/style.css'></script>"
	return ( css_text )

def printHTML( maintext, hourin, hourout, username ) :

	css_text = getCSS( hourin, hourout, username )
#	css_text = ''
	
	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
#	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += "<META HTTP-EQUIV='refresh' CONTENT='3600'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

#def main() :

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d %H:%M:%S')
today2=now.strftime('%Y-%m-%d')
dt = today
#todayC = today[0:10]

if 'car' in field :

	car = field['car'].value
	
else:
	
	car = 'J-01'

if 'car2' in field :

	car2 = field['car2'].value
	
else:
	
	car2 = 'J-01'

if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

if 'date' in field :

	date = field['date'].value
	
else:
	
	date= ''

if 'datein' in field :

	datein = field['datein'].value
	
else:
	
	datein = '0000-00-00 00:00:00'

if 'dateout' in field :

	dateout = field['dateout'].value
	
else:
	
	dateout = '0000-00-00 00:00:00'

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

if 'rdriver' in field :

	rdriver = field['rdriver'].value
	
else:
	
	rdriver = 'None'

if 'pass1' in field :

	pass1 = field['pass1'].value
	
else:
	
	pass1 = 'None'

if 'pass2' in field :

	pass2 = field['pass2'].value
	
else:
	
	pass2 = 'None'


if 'status' in field :

	status = field['status'].value
	
else:
	
	status = 'Active'
	
if 'masterid' in field :

	masterid = field['masterid'].value
	
else:
	
	masterid = '0'

if 'comment' in field :

	comment = field['comment'].value
	
else:
	
	comment = ''
	
if 'datea' in field :

	datea = field['datea'].value
	
else:
	
	datea = '0000-00-00 00:00:00'
	
if 'dateb' in field :

	dateb = field['dateb'].value
	
else:
	
	dateb = '0000-00-00 00:00:00'
	
if 'datec' in field :

	datec = field['datec'].value
	
else:
	
	datec = '0000-00-00 00:00:00'
	
if 'dated' in field :

	dated = field['dated'].value
	
else:
	
	dated = '0000-00-00 00:00:00'

if 'datee' in field :

	datee = field['datee'].value
	
else:
	
	datee = '0000-00-00 00:00:00'
	
if 'datef' in field :

	datef = field['datef'].value
	
else:
	
	datef = '0000-00-00 00:00:00'

if 'in' in field :

	hourin2 = field['in'].value
	
else:
	
	hourin2 = 'none'
	
if 'out' in field :

	hourout2 = field['out'].value
	
else:
	
	hourout2 = 'none'

if 'wpid' in field :

	wpid = field['wpid'].value
	
else:
	
	wpid = '0'

if 'wpid2' in field :

	wpid2 = field['wpid2'].value
	
else:
	
	wpid2 = '0'
	
if 'start2' in field :

	start2 = field['start2'].value
	
else:
	
	start2 = '00:00'

if 'end2' in field :

	end2 = field['end2'].value
	
else:
	
	end2 = '00:00'

if 'blocking' in field:

	blocking = field['blocking'].value
	
else:
	
	blocking = 'In-Out'
	
if 'monitor' in field:

	monitor = field['monitor'].value
	
else:
	
	monitor = ''	
	
#if 'amountMin' in field :

#	amountMin = field['amountMin'].value
	
#else:
	
#	amountMin = '08'
	
#if 'amountMax' in field :

#	amountMax = field['amountMax'].value
	
#else:
	
#	amountMax = '17'

username = '.none'
updateComment = 'None'

	
if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
	username = username.strip()
#	termlimit = str( now + term )
	real_username = username
	
	cursor3.execute("select user, destiny from users where stnuser = '%s'" % ( username ) )

	numrows3 = cursor3.rowcount
	
	users_destiny='BHSB'

	if numrows3 == 1:
		
		users = cursor3.fetchone()
		real_username = users[0]
		real_username = real_username.strip()
#		driver = real_username.strip()
#		rdriver = real_username.strip()
		users_destiny = users[1]

	updateComment = ''

	idno2 = int( idno )

	if method == 'POST' :
		
		if  field['action'].value == 'Save' and int( idno ) > 0 :
#			mpass = True
			masterid2 = int( masterid )
			date1 = date[0:10]
						
			datein = datein.strip()
			dateout = dateout.strip()

			destiny = destiny.strip()
			
			hourin = datein[11:13]
			hourout = dateout[11:13]
			
			starttime = start2.strip()
			endtime = end2.strip()
			
			overnight = overnight.strip()
			
			if overnight == "Overnight" :
				
				dateNextA = date1.split('-')
#				dayNext = dateNextA[2]
				dateStart = datetime.date ( int( dateNextA[0] ), int( dateNextA[1] ), int( dateNextA[2] ) )
				dateInterval = datetime.timedelta ( days = 1 )
				tmrw = dateStart + dateInterval
				tmrw1 = tmrw.strftime( '%Y-%m-%d' )

#				dateout = tmrw1 + ' ' + hourout + ':00:00'
				datein = date1 + ' ' + starttime
				dateout = tmrw1 + ' ' + endtime
				
			else:
				
#				dateout = date1 + ' ' + hourout + ':00:00'
				datein = date1 + ' ' + starttime
				dateout = date1 + ' ' + endtime
				
				
			car = car.strip()
			car2 = car2.strip()
						
			seats = 1
			
			driver = driver.strip()
			driver2 = driver.upper()
			
			rdriver = rdriver.strip()
			rdriver2 = rdriver.upper()
			
			pass1 = pass1.strip()
			pass2 = pass2.strip()
			pass1b = pass1.upper()
			pass2b = pass2.upper()

			if len( pass1b ) > 0 and ( len( pass2b ) == 0 or pass2b == '.NONE' ) :
				
				pass2 = pass1
				
				pass2b = pass2.upper()
			
			
			countpass4 = 1			
			countpass3 = 0			
			
#			updateComment += 'date vars ' + str( datein ) + '/' + str( dateout ) + ' / ' + overnight + '<br>'
#			updateComment += 'cpass 4/3 In ' + str( countpass4 ) + '/' + str( countpass3 ) + '<br>'

			countpass2 = []
			
			if len( pass1b ) > 0 and pass1b != 'NONE' and pass1b != '.NONE':
				
				countpass = pass1b.split(',')

								
				countpass2.append( driver2 )

				if len( countpass ) > 0 :

					for pass3 in countpass :
						
						pass3 = pass3.strip()
										
						if len ( pass3 ) > 0 :
																	
							countpass2.append( pass3 )
#					
				if len( countpass2 ) > 0 :
				
					countpass3 = len ( countpass2 )

				if ( driver2 == 'DAYCREW1' or driver2 == '.DAYCREW1' or driver2 == 'DAYCREW2' ) and countpass3 > 0 :

					countpass4 = countpass3 - 1
					updateComment += 'DayCrew Seats ' + str( countpass4 ) + '/' + str( countpass3 ) + '/'+ str(countpass2 )+ '<br>'

				else :

					countpass4 = countpass3
					updateComment += 'NotDayCrew Seats ' + str( countpass4 ) + '/' + str( countpass3 ) + '/'+ str(countpass2 )+ '<br>'
				
# debug
#			updateComment += 'cpass 4/3 Out ' + str( countpass4 ) + '/' + str( countpass3 ) + '/'+ str(countpass2 )+ '<br>'
			
			seats = countpass4
			
				
			rseats = 1

			countrpass4 = 1			
			countrpass3 = 0			

			countpass2 = []

#			updateComment += 'crpass 4/3 In ' + str( countrpass4 ) + '/' + str( countrpass3 ) + '<br>'
			
			if len( pass2b ) > 0 and pass2b != 'NONE' and pass2b != '.NONE' :
				
				countpass = pass2b.split(',')

				
				countpass2.append( rdriver2 )

				if len( countpass ) > 0 :

					for pass3 in countpass :
						
						pass3 = pass3.strip()
										
						if len( pass3 ) > 0  :
																		
							countpass2.append( pass3 )
					
				if len ( countpass2 ) > 0 :
				
					countrpass3 = len ( countpass2 )
			
				if ( rdriver2 == 'DAYCREW1' or rdriver2 == '.DAYCREW1' or rdriver2 == '.DAYCREW2' ) and countrpass3 > 0 :

					countrpass4 = countrpass3 - 1
					updateComment += 'DayCrew Seats ' + str( countrpass4 ) + '/' + str( countrpass3 ) + '/'+ str(countpass2 )+ '<br>'

				else :

					countrpass4 = countrpass3
					updateComment += 'DayCrew Seats ' + str( countrpass4 ) + '/' + str( countrpass3 ) + '/'+ str(countpass2 )+ '<br>'
			
# debug
#			updateComment += 'crpass 4/3 Out ' + str( countrpass4 ) + '/' + str( countrpass3 ) + '/'+ str( countpass2 )+ '<br>'
	
			rseats = countrpass4
					

			blocking = blocking.strip()
			monitor = monitor.strip()
			destiny = destiny.strip()
			
			mfail = True
			mfail2 = True
			mfail3 = True
		
			wheels = '2WD'

			cursor5.execute("select car, loc, phone, pass, type, seq, status, wheels, idno from cars where car='%s'" % ( car ) )
			numrows5 = cursor5.rowcount
		
			if numrows5 == 1:
				
				raw = cursor5.fetchone()
				wheels = raw[7]

		
			wheel_type = wheels
			wheel_warning = ''

#			blackres_start2 = date1
#			blackres_end2 = date1
	#		bstatus = 'above blackres'
#			bstatus = ''
	
#			if numrows5 > 0 :
			
#				for ruw in cursor5.fetchall() :
				
#					blackres_car = ruw[1]
#					blackres_start = str( ruw[2] )
#					blackres_end = str( ruw[3] )
#					blackres_recur = ruw[4]
#					blackres_type = ruw[5]
#					blackres_warning = ruw[6]

#					blackres_recur = blackres_recur.strip()

#					if blackres_recur == 'Yearly' :					

#						blackres_start2 = dateYear + '-' + blackres_start[5:10]
#						blackres_end2 = dateYear3 + '-' + blackres_end[5:10]
					
#						if date >= blackres_start2 and date <= blackres_end2 :
						
#							bstatus='inside dates'
						
#							wheel_type = blackres_type
#							wheel_warning = blackres_warning
							
#			if wheel_type == '4WD-Studs' and ( destiny[0] == 'B' or destiny[3] == 'B' ) :
				
#				mfail3 == True
#				mfailComment3 = wheel_warning
#				failidno3 = 0 
			
#			amtMin = int( amountMin )
#			amtMax = int( amountMax )
			
#			hourin2 = datein[11:13]
#			hourout2 = dateout[11:13]
#			hourin3 = int( hourin )
#			hourout3 = int( hourout )
			
#			if amtMin > 0 and amtMax > 0 :
				
#				datein = date + ' ' + str( amtMin )  + ":00"
#				dateout = date + ' ' + str( amtMax ) + ":00"
#				updateComment = 'amtMin amtMax OK preelse'

#			else:
#				updateComment = 'amtMin amtMax TROUBLE else'

#			mfail, mfailComment, mfailidno = logproc.isDuped( date1, car, datein, dateout, idno2 )

			
			mfail, mfailComment, failidno = isDuped( date1, car, datein, dateout, idno2 )
			
			mfail2, mfailComment2, failidno2 = isDuped( date1, car2, datein, dateout, idno2 )
						
#			mfail3, mfailComment3, failidno3 = isBlacked( date1, car, datein, dateout, idno2, destiny )
			
#			mfail4, mfailComment4, failidno4 = isBlacked( date1, car2, datein, dateout, idno2 )

						
			if len( datea ) == 0 :
				
				datea = '0000-00-00 00:00:00'
			
			if len( dateb ) == 0 :
				
				dateb = '0000-00-00 00:00:00'
					
			if len( datec ) == 0 :
				
				datec = '0000-00-00 00:00:00'
					
			if len( dated ) == 0 :
			
				dated = '0000-00-00 00:00:00'
			
			if len( datee ) == 0 :
				
				datee = '0000-00-00 00:00:00'
			
			if len( datef ) == 0 :
				
				datef = '0000-00-00 00:00:00'

#			mfail = False

			if mfail == False and mfail2 == False  :
#			if mfail == False and mfail2 == False and mfail3 == False and mfail4 == False :
				
#			cursor4.execute("update res set car = '%s', date = '%s', datein = '%s', dateout = '%s', overnight='%s', destiny = '%s', driver = '%s', \
			#cursor4.execute("update res set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', rdriver = '%s',  pass = '%s', pass2 = '%s', status = '%s', masterid = '%s', comment = '%s' where idno = '%s'" % (car, date, datein, dateout, overnight, destiny, driver,rdriver, pass1, pass2, status, idno, comment,  idno ) )
				cursor4.execute("update res set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', rdriver = '%s',  \
				pass = '%s', rpass = '%s', status = '%s', masterid = '%s', comment = '%s', datea = '%s', dateb = '%s', datec = '%s', dated = '%s', datee = '%s', \
				datef = '%s', seats = '%s', rseats = '%s', blocking = '%s', monitor = '%s', car2 = '%s' where idno = '%s'" \
				% (car, date1, datein, dateout, overnight, destiny, driver, rdriver, pass1, pass2, status, masterid2, comment, datea, dateb, datec, dated, datee, datef, \
				seats, rseats, blocking, monitor, car2, idno ) )
				
				new_history = today + ' - ' + username + " - Save *****\n"
				new_history += car + '/' + car2 + ' ' + date1 + ' ' + datein + ' ' + dateout + ' ' + driver + ' ' + destiny + ' ' + overnight + ' P: ' + pass1 + ' RP: ' + pass2 \
				+ ' RD: ' + rdriver + ' M: ' + monitor + "\n"
				
				cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
				
				updateComment += '<b>Update-OK with No conflicts</b><br>'
#				updateComment += 'mfailcomment: ' + mfailComment
			
			else :
				
				if mfail == True :
					
					updateComment += '<b>Update-FAIL</b> Car1: ' + car +' [' + str( mfail ) + ' ' + str( failidno ) + '] ' + mfailComment + ' ' + '<br>'
				
				if mfail2 == True :
					
					updateComment += '<b>Update-FAIL</b> Car2: ' + car2 + ' [' + str( mfail2 ) + ' ' + str( failidno2 ) + '] ' + mfailComment2 + ' ' + '<br>'

#				if mfail3 == True :
					
#					updateComment += 'Update2-FAIL BlackOut Car1 ' + car + '- [' + str( mfail3 ) + ' ' + str( failidno3 ) + '] ' + mfailComment3 + ' ' + '<br>'

#				if mfail4 == True :
					
#					updateComment += 'Update2-FAIL BlackOut Car2 ' + car + '- [' + str( mfail3 ) + ' ' + str( failidno3 ) + '] ' + mfailComment3 + ' ' + '<br>'
					
#			cursor4.execute("update res set car='%s', date='%s', datein='%s', dateout='%s', overnight = '%s', destiny = '%s', driver='%s', rdriver = '%s',  \
#			pass = '%s', rpass = '%s', status = '%s', masterid = '%s', comment = '%s' where idno = '%s'" \
#			% (car, date, datein, dateout, overnight, destiny, driver,rdriver, pass1, pass2, status, masterid2, comment, idno ) )

		if field['action'].value == 'Update-A' and int( idno ) > 0 :
			
			cursor4.execute("update res set datea='%s' where idno = '%s'" % ( today, idno ) )

			new_history = today2 + ' - ' + username + " - Update-A %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
		
		if field['action'].value == 'Update-B' and int( idno ) > 0 :
			
			cursor4.execute("update res set dateb='%s' where idno = '%s'" % ( today, idno ) )

			new_history = today2 + ' - ' + username + " - Update-B %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			
		if field['action'].value == 'Update-C' and int( idno ) > 0 :
			
			cursor4.execute("update res set datec='%s' where idno = '%s'" % ( today, idno ) )

			new_history = today2 + ' - ' + username + " - Update-C %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			#
		if field['action'].value == 'Update-D' and int( idno ) > 0 :
			
			cursor4.execute("update res set dated='%s' where idno = '%s'" % ( today, idno ) )

			new_history = today2 + ' - ' + username + " - Update-D %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )

		if  field['action'].value == 'Update-E' and int( idno ) > 0 :
			
			cursor4.execute("update res set datee='%s' where idno = '%s'" % ( today, idno ) )

			new_history = today2 + ' - ' + username + " - Update-E %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			
		if  field['action'].value == 'Update-F' and int( idno ) > 0 :
			
			cursor4.execute("update res set datef='%s' where idno = '%s'" % ( today, idno ) )

			new_history = today2 + ' - ' + username + " - Update-F %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )

		if  field['action'].value == 'Clear-A' and int( idno ) > 0 :
			
			cursor4.execute("update res set datea='%s' where idno = '%s'" % ( '0000-00-00 00:00:00', idno ) )

			new_history = today2 + ' - ' + username + " - Clear-A %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			#
		if  field['action'].value == 'Clear-B' and int( idno ) > 0 :
			
			cursor4.execute("update res set dateb='%s' where idno = '%s'" % ( '0000-00-00 00:00:00', idno ) )

			new_history = today2 + ' - ' + username + " - Clear-B %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			
		if  field['action'].value == 'Clear-C' and int( idno ) > 0 :
			
			cursor4.execute("update res set datec='%s' where idno = '%s'" % ( '0000-00-00 00:00:00', idno ) )

			new_history = today2 + ' - ' + username + " - Clear-C %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			#
		if  field['action'].value == 'Clear-D' and int( idno ) > 0 :
			
			cursor4.execute("update res set dated='%s' where idno = '%s'" % ( '0000-00-00 00:00:00', idno ) )

			new_history = today2 + ' - ' + username + " - Clear-D %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )

		if  field['action'].value == 'Clear-E' and int( idno ) > 0 :
			
			cursor4.execute("update res set datee='%s' where idno = '%s'" % ( '0000-00-00 00:00:00', idno ) )

			new_history = today2 + ' - ' + username + " - Clear-E %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )
			#
		if  field['action'].value == 'Clear-F' and int( idno ) > 0 :
			
			cursor4.execute("update res set datef='%s' where idno = '%s'" % ( '0000-00-00 00:00:00', idno ) )

			new_history = today2 + ' - ' + username + " - Clear-F %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )

		if  field['action'].value == 'Delete' and int( idno ) > 0 :
			
			cursor4.execute("update res set status='%s', rmuser='%s', rmstamp='%s' where idno = '%s'" % ( 'Removed', real_username, today, idno ) )

			new_history = today2 + ' - ' + username + " - Res Removed %s *****\n" % ( dt )
			cursor4.execute("update res set history = concat( '%s', history ) where idno='%s'" % ( new_history, idno ) )

#			cursor3.execute("select residno, residno4, residno5, residno6 from items where residno = '%s' or residno4 = '%s' or residno5 = '%s' or \
#			residno6 = '%s'" % ( idno, idno, idno, idno ) )

# Deleted WP Passengers


			cursor4.execute("update items set residno2 = 0 where residno2 = '%s'" % ( idno ) )
	
			cursor4.execute("update items set residno3 = 0 where residno3 = '%s'" % ( idno ) )

			updateComment += 'residno2 & 3 OK ' + '<br>'

#			cursor4.execute("update items set residno = 0 where residno = '%s'" % ( idno ) )

# advance the residno  -> 1456

# Deleted WP Drivers

#			cursor3.execute("select residno, residno4, residno5, residno6 from items where residno = '%s'" % ( idno ) )

#			cursor3.execute("select idno, residno, residno4, residno5, residno6 from items where status = 'Active' and ( residno = '%s' or residno4 = '%s' or residno5 = '%s' or \
#			residno6 = '%s' ) " % ( idno, idno, idno, idno ) )

			cursor3.execute("select idno, residno, residno4, residno5, residno6 from items where residno = '%s' or residno4 = '%s' or residno5 = '%s' or \
			residno6 = '%s' " % ( idno, idno, idno, idno ) )

			numrows3 = cursor3.rowcount
			updateComment += 'num rows3 residnos: ' + str( numrows3 ) + '<br>'

			
			if numrows3 == 1 :
			
				riw = cursor3.fetchone()

				items2_idno = riw[0]
				items2_residno = riw[1]
				items2_residno4 = riw[2]
				items2_residno5 = riw[3]
				items2_residno6 = riw[4]
				
				if idno2 == items2_residno :
				
					updateComment += 'idno == residno2 0/4: ' + str( items2_residno ) + '/' + str( items2_residno4 ) + '<br>'
					updateComment += "<a href=planone2.py?idno=%s>Deleted from WP: %s</a><br>" % ( items2_idno, items2_idno )
#				
					cursor4.execute("update items set residno = %s where idno = '%s'" % ( items2_residno4, items2_idno ) )					
					cursor4.execute("update items set residno4 = %s where idno = '%s'" % ( items2_residno5, items2_idno ) )	
					cursor4.execute("update items set residno5 = %s where idno = '%s'" % ( items2_residno6, items2_idno ) )	
					cursor4.execute("update items set residno6 = %s where idno = '%s'" % ( 0, items2_idno ) )							

				else:

					updateComment += 'idno != residno2: 0/4 ' + str( items2_residno ) + '/' + str( items2_residno4 ) + '<br>'
				
				if idno2 == items2_residno4 :

					updateComment += 'idno2 == residno4 4/5: ' + str( items2_residno4 ) + '/' + str( items2_residno5 ) + '<br>'
					updateComment += "<a href=planone2.py?idno=%s>Deleted from WP: %s</a><br>" % ( items2_idno, items2_idno )
		
					cursor4.execute("update items set residno4 = %s where idno = '%s'" % ( items2_residno5, items2_idno ) )	
					cursor4.execute("update items set residno5 = %s where idno = '%s'" % ( items2_residno6, items2_idno ) )	
					cursor4.execute("update items set residno6 = %s where idno = '%s'" % ( 0, items2_idno ) )							
				
				else:

					updateComment += 'idno2 != residno4: 4/5' + str( items2_residno4 ) + '/' + str( items2_residno5 ) + '<br>'

#						
				if idno2 == items2_residno5 :

					updateComment += 'idno2 == residno5 5/6: ' + str( items2_residno5 ) + '/' + str( items2_residno6 ) + '<br>'
					updateComment += "<a href=planone2.py?idno=%s>Deleted from WP: %s</a><br>" % ( items2_idno, items2_idno )

					cursor4.execute("update items set residno5 = %s where idno = '%s'" % ( items2_residno6, items2_idno ) )	
					cursor4.execute("update items set residno6 = %s where idno = '%s'" % ( 0, items2_idno ) )							

				else:

					updateComment += 'idno2 != residno5: 5/6' + str( items2_residno5 ) + '/' + str( items2_residno6 ) + '<br>'
		
				if idno2 == items2_residno6 :

					updateComment += 'idno2 == residno6 6/6: ' + str( items2_residno6 ) + '/' + str( items2_residno6 ) + '<br>'
					updateComment += "<a href=planone2.py?idno=%s>Deleted from WP: %s</a><br>" % ( items2_idno, items2_idno )

					cursor4.execute("update items set residno6 = %s where idno = '%s'" % ( 0, items2_idno ) )

				else:

					updateComment += 'idno2 != residno6: 6/6' + str( items2_residno6 ) + '/' + str( items2_residno6 ) + '<br>'
					
				
#			cursor4.execute("update items set residno2=0 where residno2 = '%s'" % ( idno ) )
				
#			cursor4.execute("update items set residno3=0 where residno3 = '%s'" % ( idno ) )
					
			

#				cursor4.execute("update items set residno = residno4 where residno4 = '%s'" % ( idno ) )
#			cursor4.execute("update items set residno = 0 where residno = '%s'" % ( idno ) )
#			cursor4.execute("update items set residno = 0 where residno = '%s' and residno4 = 0 " % ( idno ) )
				
#				cursor4.execute("update items set residno = residno4 where residno = '%s' and residno4 > 0 " % ( idno ) )
				
#				cursor4.execute("update items set residno4 = residno5 where residno4 = '%s'  and residno5 > 0 " % ( idno ) )
				
#				cursor4.execute("update items set residno5 = residno6, residno6 = 0 where residno5 = '%s'  and residno6 > 0 " % ( idno ) )

#			cursor3.execute("select residno, residno4, residno5, residno6 from items where residno4 = '%s'" % ( idno ) )
#			numrows3 = numrows3.rowcount
#			if numrows3 == 1 :
#				
#				cursor4.execute("update items set residno4 = residno5 where residno4 = '%s' and residno5 > 0 " % ( idno ) )
#
#				cursor4.execute("update items set residno5 = residno6, residno6 = 0 where residno6 = '%s'" % ( idno ) )
#
#			cursor3.execute("select residno, residno4, residno5, residno6 from items where residno5 = '%s'" % ( idno ) )
#			numrows3 = numrows3.rowcount
#			if numrows3 == 1 :
#
#				cursor4.execute("update items set residno5 = residno6, residno6 = 0 where residno5 = '%s' and residno6 > 0" % ( idno ) )
#
#			cursor3.execute("select residno, residno4, residno5, residno6 from items where residno6 = '%s'" % ( idno ) )
#			numrows3 = numrows3.rowcount
#			if numrows3 == 1 :
#
#				cursor4.execute("update items set residno6 = 0 where residno6 = '%s'" % ( idno ) )
#		
#				
#			cursor4.execute("update items set residno4=0 where residno4 = '%s'" % ( idno ) )
#			cursor4.execute("update items set residno5=0 where residno5 = '%s'" % ( idno ) )
#			cursor4.execute("update items set residno6=0 where residno6 = '%s'" % ( idno ) )

	else:
		
		if method == 'GET' and int( idno ) == 0  and len( car ) > 0 and not date == '0000-00-00'  :
#			
#			if not date == '0000-00-00' and len ( car ) > 0 : 

#				date1 = '2020-05-28'
				idno2 = 0
				date1 = date[0:10]
				datein1 = date[0:10] + ' 00:00'
				dateout1 = date[0:10] + ' 23:00'
				car = car.strip()
				
				carseats = 4
				cursor5.execute("select pass from cars where car='%s' " % ( car ) )
				numrows5 = cursor5.rowcount
				if numrows5 > 0 :
					ruw=cursor5.fetchone()
					carseats = ruw[0]
				

				hourin2 = hourin2.strip()
				
				if len ( hourin2 ) == 1 :
					
					hourin2 = '0' + hourin2
				
				hourout2 = hourout2.strip()
				
				if len ( hourout2 ) == 1 :
					
					hourout2 = '0' + hourout2
							
				if hourin2 != 'none' and int ( hourin2 ) >= 0 and int( hourin2 ) < 24 :
				
					datein1 = date1 + ' ' + hourin2 + ':00'

				if hourout2 != 'none' and int ( hourout2 ) > 0 and int( hourout2 ) < 24 :
				
					dateout1 = date1 + ' ' + hourout2 + ':00'
#				car = 'J-02'

				pass1 = '.none'
				pass2 = '.none'
				overnight = 'Daytime'
				destiny = 'BHSB'
				
				if int( wpid ) == 0 and len( users_destiny ) > 0 :
				
					destiny = users_destiny
								
				driver = real_username
				rdriver = real_username
								
				status = 'Active'
				masterid = 0
				comment = ''

				datea = '0000-00-00 00:00:00'
				dateb = '0000-00-00 00:00:00'
				datec = '0000-00-00 00:00:00'
				dated = '0000-00-00 00:00:00'
				datee = '0000-00-00 00:00:00'
				datef = '0000-00-00 00:00:00'
				
				blocking = 'In-Out'
				monitor = ''
				
#				mfail = True
				mfail = False
			
				mfail, mfailComment, failidno = isDuped( date1, car, datein1, dateout1, idno2 )

#				mfail = True
				
#				cursor4.execute("insert into res ( car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, status, masterid, comment ) \
#				values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s' ) ")  % \
#				( car, date, datein, dateout, overnight, destiny, driver, rdriver, pass1, pass2, status, masterid, comment ) 

#				cursor4.execute("insert into res ( car, username, date, datein, dateout, overnight, driver, rdriver ) values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
#				% ( car, username, date[0:10], datein1, dateout1, overnight, driver, rdriver ) )   				

				if mfail == False :
					
					cursor4.execute("insert into res ( car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, \
					status, masterid, comment, username, datea, dateb, datec, dated, datee, datef, \
					timestamp, carseats, seats, rseats, blocking, monitor, car2  ) values \
					( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
					'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
					'%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
					% ( car, date[0:10], datein1, dateout1, overnight, destiny, driver, rdriver, pass1, pass2, status, masterid, comment, username, datea, \
					dateb, datec, dated, datee, datef, today, carseats, 1, 1, blocking, monitor, car ) )   				


					idno = cursor4.lastrowid
					idno = str( idno )

					new_history = today + ' - ' + username + " - Insert-Res *****\n"
					new_history += car + ' ' + date1 + ' ' + datein1 + ' ' + dateout1 + ' ' + driver + ' ' + destiny + ' ' + overnight + "\n"
					cursor4.execute("update res set history = '%s' where idno='%s'" % ( new_history, idno ) )

					if car == 'J-08' :
					
						shortDateIn2 = str( datein1 )
						shortDateOut2 = str( dateout1 )
						shortDate = shortDateIn2 [5:16] +  ' to ' + shortDateOut2 [5:16]
						emailsubject = car + ' Warning  - ' + driver + ' reserved: ' + car + ' / ' + date[5:10] + ' ' + overnight + ' from ' +  shortDate
#						emailtext = emailsubject
						emailtext = 'Reserve Warning for ' + date[0:10] + ' - ' + driver + ' reserved: ' + car + ' ' + overnight + ' from ' +  shortDate + "\n"
#						emailtext += "Please review the reservation. <a href=resone.py?idno=" + idno + ">" + car + '-' + date[0:10] + "</a>\n"
						logproc.sendemail( 'Yoshiyama', emailsubject, emailtext )
#						logproc.sendemail( 'Winegar', emailsubject, emailtext )

#					if False :
					
					if int( wpid ) > 0 and int( idno ) > 0 :

						cursor4.execute("select assigned1, assigned2, residno, residno4, residno5, residno6 from items where idno = '%s'" % ( int( wpid ) ) )	
						numrows4=cursor4.rowcount

						if numrows4 == 1 :
								
							ruws4 = cursor4.fetchone()
							
							wp_assigned1 = ruws4[0]
							wp_assigned2 = ruws4[1]

							wp_residno = ruws4[2]
							wp_residno4 = ruws4[3]
							wp_residno5 = ruws4[4]
							wp_residno6 = ruws4[5]
							
							wp_assigned1 = wp_assigned1.strip()
							wp_assigned2 = wp_assigned2.strip()
							
							wp_seats = 1
							wp_rseats = 1

#							countpass2String = 'None'

							
							if len( wp_assigned2 ) > 0 and wp_assigned2 != '.none':
			
# OpenSeats counts unique Driver + Pass names 

								wp_assigned3 = wp_assigned1.upper()
								wp_assigned4 = wp_assigned2.upper()
								
								countpass = wp_assigned4.split(',')
								
								countpass2 = []
								countdriver2 = []

# add Driver to Passenger.upper() Array
								
								countpass2.append( wp_assigned3 )
#								countdriver2.append( wp_assigned3 )
								
								for pass3 in countpass :

									pass3 =  pass3.strip()

#									if pass3 not in countpass2 :
									if len( pass3 ) > 0 :
									
										driverLower = pass3[1:]
										driverCheck = pass3[0] + driverLower.lower()									
										
										countpass2.append( pass3 )
										
#										cursor4.execute("select train from users where user = '%s'") % ( driverCheck )

#										numrows4 = cursor4.rowcount

#										if numrows4 == 1 :

#											raws = cursor4.fetchone()

#											if raws[0] == 'D' :
#											
#												countdriver2.append( driverCheck )
										
										
#									if len( countpass ) > 0  :


								if len( countpass2 ) > 1  :
				
									wp_seats = len ( countpass2 )
									wp_rseats = len ( countpass2 )

#									wp_seats += len ( countpass2 )
#									wp_rseats += len ( countpass2 )
									
#									countpass2String = str( countpass2 )

#								newDriver = wp_assigned1
								
#								passString = '' 
								
#								if wp_residno > 0 and len ( countpass2 ) > 0 :
								
#									if len ( countpass2 ) > 2 :
									
#										passString += countpass[2]
									
#									if len ( countpass2 ) > 3  :
									
#											passString += ', ' + countpass[3]
												

#								if wp_residno4 > 0 and len ( countpass2 ) > 0 :
					
#									if len ( countpass2 ) > 4 :
						
#										passString += countpass[4]
						
#									if len ( countpass2 ) > 5  :
						
#											passString += ', ' + countpass[5]

#								if wp_residno5 > 0 and len ( countpass2 ) > 0 :
		
#									if len ( countpass2 ) > 6 :
			
#										passString += countpass[6]
			
#									if len ( countpass2 ) > 7  :
			
#											passString += ', ' + countpass[7]

#									if item_residno4 == 0 :
									
#										if len ( countdriver2 ) > 0 :
								
#											newDriver = countdriver2[0]
										
#									else : 
								
#										if item_residno5 == 0 :
										
#											if len ( countdriver2 ) > 1 :
									
#												newDriver = countdriver2[1]
										
#											if len ( countpass2 ) > 4  :
										
#												passString += countpass2[4] 

#											if len ( countpass2 ) > 5  :
										
#												passString += ', ' + countpass2[5] 
										
												
#											passString = countpass2[2] + ', ' + countpass2[3]
											
#										else:
									
#											if item_residno6 == 0 :
											
#												if len ( countdriver2 ) > 2 :
									
#													newDriver = countdriver2[2]
									
#												if len( countpass2[6] ) > 6 :
									
#													passString += countpass2[6] 

#												if len( countpass2[7] ) > 7 :
									
#													passString += ', ' + countpass2[7] 
													
#												passString = countpass2[2] + ', ' + countpass2[3]
											
								
								
#								if len( newDriver ) > 0 and not newDriver == wp_assigned1 :
									
#									wp_assigned1 = newDriver
									
#								if len( passString ) > 0 and passString != wp_assigned2 :
	
#									wp_assigned2 = passString

#								cursor4.execute("update res set driver = '%s', rdriver = '%s', pass = '%s', rpass = '%s', seats = '%s', rseats = '%s' where idno = '%s'" \
#								% ( wp_assigned1, wp_assigned1, wp_assigned2, wp_assigned2, wp_seats, wp_rseats, idno ) )	

							cursor4.execute("update res set driver = '%s', rdriver = '%s', pass = '%s', rpass = '%s', seats = '%s', rseats = '%s' where idno = '%s'" \
							% ( wp_assigned1, wp_assigned1, wp_assigned2, wp_assigned2, wp_seats, wp_rseats, idno ) )	

#								cursor4.execute("update res set driver = '%s', rdriver = '%s', pass = '%s', rpass = '%s', seats = '%s', rseats = '%s' where idno = '%s'" \
#								% ( wp_assigned1, wp_assigned1, wp_assigned2, countpass2String, wp_seats, wp_rseats, idno ) )	
# update WorkPlans

#							cursor3.execute("select residno, residno2, residno3, residno4, residno5, residno6 from items where idno = '%s'" % ( int( wpid ) ) )
							
#							numrows3 = cursor3.rowcount
							
#							if numrows3 == 1:
							
#								ruw = cursor3.fetchone()
								
#								items3_residno = ruw[0]

#								items3_residno2 = ruw[1]
#								items3_residno3 = ruw[2]
								#
#								items3_residno4 = ruw[3]
#								items3_residno5 = ruw[4]
#								items3_residno6 = ruw[5]

							if wp_residno == 0 and int( idno ) > 0 :
							
								cursor4.execute("update items set residno = '%s' where idno = '%s'" % ( idno, int( wpid ) ) )
							
							else:
								
								if wp_residno4 == 0  and int( idno ) > 0 :
								
									cursor4.execute("update items set residno4 = '%s' where idno = '%s'" % ( idno, int( wpid ) ) )

								
								else:

									if wp_residno5 == 0 and int( idno ) > 0 :
									
										cursor4.execute("update items set residno5 = '%s' where idno = '%s'" % ( idno, int( wpid ) ) )

									else:
									
										if wp_residno6 == 0 and int( idno ) > 0 :
										
											cursor4.execute("update items set residno6 = '%s' where idno = '%s'" % ( idno, int( wpid ) ) )
											
										else:

											updateComment += '4 Reserves Max for 1 WorkPlan<br>'

				else:
					
					updateComment = '<CENTER>'
					updateComment += '<table cellpadding=3 cellspacing=3>'
					updateComment += '<tr><td colspan=2 bgcolor=pink><FONT SIZE=+1><b>FAILED - %s</b></FONT></td></tr>' % ( 'Your Res Conflicts with another' )
					updateComment += '<tr><td class=right>Your Date:</td><td>%s</td></tr>' % ( date1 )
					updateComment += '<tr><td class=right>Your Car:</td><td>%s</td></tr>' % ( car )
					updateComment += '<tr><td class=right>Your HourIn:</td><td>%s</td></tr>' % ( datein1 )
					updateComment += '<tr><td class=right>Your HourOut:</td><td>%s</td></tr>' % ( dateout1 )
					updateComment += '</table><br>'
					updateComment += 'failcomment:<br>' + mfailComment + '</center>'
					idno = '0'


	pagename = '<center><b>Car Reserves - One Reservation</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getCarMenu() + '<br>'

	cursor.execute("select idno, car, date, datein, dateout, overnight, destiny, driver, rdriver, pass, rpass, \
	status, masterid, comment, datea, dateb, datec, dated, datee, datef, seats, rseats, carseats, rmuser, rmstamp, blocking, \
	monitor, car2, history from res where idno = '%s'" % ( idno ) )
	numrows = cursor.rowcount
	maintext = pagename 
#	maintext += 'rows: ' + str( numrows ) + ' updateComment: ' + updateComment + '<br>'
	if username == 'twin' or username == 'winegar' :

		maintext += 'rows: ' + str( numrows ) + ' ' + updateComment +'<br>'
#	maintext += '<table cellpadding=3 cellspacing=3>'

	if numrows == 1 :
	
		row = cursor.fetchone()

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

		res_history = row[28]

		res_driver = res_driver.strip()
		res_rdriver = res_rdriver.strip()
		
#			driver = real_username.strip()
#			rdriver = real_username.strip()		

# Reminaing Seats		


		hourin = res_datein[11:13]
		hourout = res_dateout[11:13]


		hourminin = res_datein[11:16]
		hourminout = res_dateout[11:16]
		
		yr = res_date.split('-')
		dt = datetime.datetime( int(yr[0]) , int(yr[1]), int(yr[2]) )
#		dow = res_date.get_weekday()
		dow = dt.strftime('%a')
		dow2 = dt.strftime('%A')
#		timein = res_datein[11:16]
#		timein = res_datein[11:16]
#		timeout = res_datout[11:16]
#		hour2 = hourout
#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )


		cursor2.execute("select code, name from destiny where code='%s'" % ( res_destiny ) )
		numrows2 = cursor2.rowcount
		if numrows2 == 1 :

			riw = cursor2.fetchone()
			destinyName =  riw[1]

		else :

			destinyName =  'None'
			
		wpDriver = ''
		cursor7.execute("select idno, assigned1, assigned2 from items where residno='%s' or residno4='%s' or residno5='%s' or residno6='%s'" \
		% ( res_idno, res_idno, res_idno, res_idno ) )
		numrows7 = cursor7.rowcount
		if numrows7 > 0 :
			
			for rews in cursor7.fetchall() :
#				wpDriver += '' + rews[1] + ' (' + str( rews[0] ) + ')'
#				wpDriver += '| WP Driver: <a href=planone.py?idno=%s>%s</a>' % ( rews[0], rews[1], )
				wpDriver += '| WP Driver: <a href=planone2.py?idno=%s>%s</a>' % ( rews[0], rews[1], )

		else :

			wpDriver =  'None'
		
		wpNames2 = ''
		
		wp_pass2 = 0
		wp_residno2 = 0	
			
		cursor7.execute("select idno, assigned1, assigned2, pass, residno, pseats from items where residno2='%s'" % ( res_idno ) )
		numrows7 = cursor7.rowcount
		if numrows7 > 0 :
			
			for rews in cursor7.fetchall() :

				wp_residno2 = rews[0]
				wp_assigned1 = rews[1]
				wp_assigned1 = wp_assigned1.strip()
				
				wp_assigned2 = rews[2]
				wp_assigned2 = wp_assigned2.strip()
				wp_assigned2 = wp_assigned2.upper()

				wp_teamPass = rews[3]
				wp_teamPass = wp_teamPass.strip()

				wp_residno2_2 = rews[4]
				wp_pseats = rews[5]

				wp_pass2 = 1
				
				if len( wp_assigned2 ) > 0 and wp_assigned2 != '.NONE' and wp_assigned2 != 'NONE'  :

					countpass = wp_assigned2.split(',')

					countpass2 = []
					
					if len( countpass ) > 0 :

						for pass3 in countpass :

							pass3 = pass3.strip()
				
							if len ( pass3 ) > 0 :
								
								countpass2.append( pass3 )

					if len( countpass2 ) > 0  :
	
						wp_pass2 = len ( countpass2 )
						
# Team Pass does not include Driver

				wp_pass2_2 = 0

				if len( wp_teamPass ) > 0 and wp_teamPass != '.NONE' and wp_teamPass != 'NONE'  :

					countpass = wp_teamPass.split(',')

					countpass2 = []
			
					if len( countpass ) > 0 :

						for pass3 in countpass :

							pass3 = pass3.strip()
		
							if len ( pass3 ) > 0 :
						
								countpass2.append( pass3 )

					if len( countpass2 ) > 0  :

						wp_pass2_2 = len ( countpass2 )

						
				if wp_residno2_2 > 0 :
				
					wp_pass2 = wp_pass2_2
				
					wpNames2 += "<a href=planone2.py?idno=%s>%s</a> | " % ( rews[0], rews[3],  )
					
				else :
				
					wpNames2 += "<a href=planone2.py?idno=%s>%s %s</a> | " % ( rews[0], rews[1], rews[2],  )
				

		else :

			wpNames2 =  'None'

		wpNames3 = ''

#		wp_pass3 = 1
		
		wp_pass3 = 0
		wp_residno3 = 0

		cursor7.execute("select idno, assigned1, assigned2, pass, residno, pseats from items where residno3='%s'" % ( res_idno ) )
		numrows7 = cursor7.rowcount
		if numrows7 > 0 :
			
			for rews in cursor7.fetchall() :

				wp_residno3 = rews[0]

				wp_assigned1 = rews[1]
				wp_assigned1 = wp_assigned1.strip()
				
				wp_assigned2 = rews[2]
				wp_assigned2 = wp_assigned2.strip()

				wp_teamPass = rews[3]
				wp_teamPass = wp_teamPass.strip()

				wp_residno3_2 = rews[4]
				wp_pseats = rews[5]

#				wp_pass3 = 0

				wp_pass3 = 1

				if len( wp_assigned2 ) > 0 and wp_assigned2 != '.NONE' and wp_assigned2 != 'NONE' :

					countpass = wp_assigned2.split(',')

					countpass2 = []
	
					if len( countpass ) > 0 :

						for pass3 in countpass :

							pass3 = pass3.strip()

							if len ( pass3 ) > 0 :
				
								countpass2.append( pass3 )

					if len( countpass2 ) > 0  :

						wp_pass3 = len ( countpass2 )
						
						# Team Pass does not include Driver

				wp_pass3_2 = 0

				if len( wp_teamPass ) > 0 and wp_teamPass != '.NONE' and wp_teamPass != 'NONE'  :

					countpass = wp_teamPass.split(',')

					countpass2 = []

					if len( countpass ) > 0 :

						for pass3 in countpass :

							pass3 = pass3.strip()

							if len ( pass3 ) > 0 :

								countpass2.append( pass3 )

					if len( countpass2 ) > 0  :

						wp_pass3_2 = len ( countpass2 )

						
#						wp_rseats += len ( countpass )				
				if wp_residno3_2 > 0 :

					wp_pass3 = wp_pass3_2
				
					wpNames3 += "<a href=planone2.py?idno=%s>%s</a> | " % ( rews[0], rews[3], )

				else:
				
					wpNames3 += "<a href=planone2.py?idno=%s>%s, %s</a> | " % ( rews[0], rews[1], rews[2], )

					

		else :

			wpNames3 =  'None'		

# openseats = car seats - Reservation Seats - WP Seats
# openrseats = car seats - Reservation Return Seats - WP Return Seats

		res_openseats = res_carseats - res_seats - wp_pass2		
		res_openrseats = res_carseats - res_rseats - wp_pass3
		
		seattable = "<table><tr><th colspan=3>OpenSeats</th></tr>"
		seattable += "<th></th><th></th><th>Up</th><th>Return</th></tr>"
		seattable += "<tr><td>%s Seats#</td><td>%s</td><td>%s</td></tr>" % ( res_car, res_carseats, res_carseats )
		seattable += "<tr><td>Res Pass#</td><td>%s</td><td>%s</td></tr>" % ( res_seats, res_rseats )
		seattable += "<tr><td>WP Pass#</td><td>%s</td><td>%s</td></tr>" % ( wp_pass2, wp_pass3 )
		seattable += "<tr><td>Open Seats#</td><td>%s</td><td>%s</td></tr>" % ( res_openseats, res_openrseats )
		seattable += "</table>"


#		seattable2 = "<table><tr><th colspan=5 bgcolor=lime>OpenSeats</th></tr>"
		seattable2 = "<table>"
		seattable2 += "<tr><th></th><th bgcolor=lime>Seats#</th><th bgcolor=lime>Res#</th><th bgcolor=lime>WP#</th><th bgcolor=lime>Open#</th></tr>"	
		seattable2 += "<tr><td>%s Up</td><td class=center>%s</td><td class=center>%s</td><td class=center>%s</td><td class=center bgcolor=yellow><FONT SIZE=+1><b>%s</b></FONT></td></tr>" % ( res_car, res_carseats, res_seats, wp_pass2, res_openseats )
		seattable2 += "<tr><td>%s Return</td><td class=center>%s</td><td class=center>%s</td><td class=center>%s</td><td class=center bgcolor=yellow><FONT SIZE=+1><b>%s</b></FONT></td></tr>" % ( res_car, res_carseats, res_rseats, wp_pass3, res_openrseats )
		seattable2 += "</table>"	
			
		postValuesShow = ( 'Save', 'Cancel', 'Delete', 'Update-A', 'Clear-A', 'Update-B', 'Clear-B', 'Update-C', 'Clear-C', 'Update-D', 'Clear-D', 'Update-E', 'Clear-E', 'Update-F', 'Clear-F')
		
		if method == 'GET' or ( method == 'POST' and field['action'].value in postValuesShow ) :

#		if method == 'GET' : 

#			if field['action'].value == 'Delete' and int( idno ) > 0 :
			
#				cursor4.execute("delete from res where idno = '%s' ")  % ( idno )
#			
#				maintext += "Deleted Reservation - " + idno + "<br>"

#			else :

#				maintext += "<form method=post action='resone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( res_idno )

			if res_status == 'Active' :

				maintext += "<form method=post action='resone.py?idno=%s'><input name=action type=submit value='Edit'>" % ( res_idno )
#				maintext += "<form method=post action='resone2.py?idno=%s'><input name=action type=submit value='Edit'>" % ( res_idno )

#				if res_driver == real_username :
				
#				maintext += " <form method=post action='resone.py?idno=%s'><input name=action type=submit value='Delete'></form><br>" % ( res_idno )
				maintext += " | <input name=action type=submit value='Delete'></form><br>"

			else :

				maintext += "<br><table><tr><td bgcolor=pink>The reservation is <b>REMOVED</b> from Edit: %s</td></tr></table><br>" % ( res_idno )

				
#			maintext += "<form method=post action='resone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( res_idno )
#			maintext += '<br>car: <b>' + res_car + '</b> date: <b>'+ res_date + ' (' + dow + ')</b> <b>'+ hourin + ' - '+hourout + '</b><br><br>'
#			maintext += '<table><td bgcolor=lemonchiffon>CarsToday for <a href=resday.py?date=%s>%s <b>%s</b></a></b></td></table>' % ( res_date, dow2, res_date ) 
			maintext += '<table cellpadding=2 cellspacing=2><tr><th colspan=6>Your Car Reservation Summary</th></tr><tr><th bgcolor=lime>Car</th>\
			<th bgcolor=lime>Date</th>'
			
			if res_overnight == 'Daytime' :

				bgcolor='blanchedalmond'

			else :

				bgcolor='lightblue'

			maintext += '<th bgcolor=%s>%s</th>' % ( bgcolor, res_overnight )
			maintext += '<th bgcolor=lime>Destiny</th><th bgcolor=lime>Driver</th><th>Go Cars This Day</th></tr>'
			todayLink = '<a href=resday.py?date=%s>%s %s</a>' % ( res_date, res_date, dow )	
			if res_overnight == 'Overnight' :
				
				maintext += '<tr><td><FONT SIZE=+1>' + res_car + '</td><td><FONT size=+1>'+ res_date[2:10] + ' ' + dow + '</td><td><FONT size=+1>' \
				+  hourin + ' -> ('+ hourout + ')</td><td><FONT size=+1>'+ destinyName + '</td><td><FONT size=+1>' + res_driver + '</td><td>' + todayLink + '</td></tr></table>'
			
			else:
				
				maintext += '<tr><td><FONT SIZE=+1>' + res_car + '</td><td><FONT size=+1>'+ res_date[2:10] + ' ' + dow + '</td><td><FONT size=+1>' \
				+  hourin + ' - '+hourout + '</td><td><FONT size=+1>'+ destinyName + '</td><td><FONT size=+1>' + res_driver + '</td><td>' + todayLink + '</td></tr></table>'
				
			maintext += '<table>'
			maintext += '<tr><th class=thbig colspan=25 align=center>Hours of Day: ' +  res_date + '<th></tr>'

			maintext += '<tr><td>' + res_date + '<td>'
			th_seq = 0

# first days line
			
			while th_seq < 25 :
				
				if res_overnight == 'Daytime' :
				
	#				maintext += '<tr>'
					if th_seq >= int( hourin)  and th_seq <= int( hourout ) :

						maintext += '<td bgcolor=blanchedalmond><FONT SIZE=+1><b>' + str( th_seq ) + '</FONT></b></td>'

					else:

						maintext += '<td bgcolor=lime>' + str( th_seq ) + '</td>'
				
				else:
					
					if th_seq >= int( hourin ) :

						maintext += '<td bgcolor=lightblue><FONT SIZE=+1><b>' + str( th_seq ) + '</FONT></b></td>'

					else:

						maintext += '<td bgcolor=lime>' + str( th_seq ) + '</td>'
					
				th_seq += 1
				
			maintext += '</tr>'

# 2nd days line			

			if res_overnight == 'Overnight' :
				
				maintext += '<tr><td>' + res_date2 + '<td>'
				
				th_seq = 0
			
				while th_seq < 25 :

					if th_seq <= int( hourout ) :
						
						maintext += '<td bgcolor=lightblue><FONT SIZE=+1><b>' + str( th_seq ) + '</FONT></b></td>'

					else:

						maintext += '<td bgcolor=lime>' + str( th_seq ) + '</td>'
					
					th_seq += 1
				
				maintext += '</tr>'
				

#			maintext += '<tr><td class=label2>00</td><td class=label2>01</td><td class=label2>02</td><td class=label2>03</td><td class=label2>04</td><td class=label2>05</td><td class=label2>06</td><td class=label2>07</td><td class=label2>08</td><td class=label2>09</td><td class=label2>10</td><td class=label2>11</td><td class=label2>12</td><td class=label2>13</td><td class=label2>14</td><td class=label2>15</td><td class=label2>16</td><td class=label2>17</td><td class=label2>18</td><td class=label2>19</td><td class=label2>20</td><td class=label2>21</td><td class=label2>22</td><td class=label2>23</td><td class=label2>00</td></tr>'
#			maintext += '<td colspan=25><div id="slider-range"></div></td>'
			maintext += '</table><br>'


# outer table 	
			maintext += '<table cellpadding=2 cellspacing=2><tr><td valign=top>'
# right table			
			maintext += '<table cellpadding=2 cellspacing=2>'
			maintext += "<tr><td class=right>Cars:</td><td><FONT SIZE=+1>%s " % ( res_car )
		
			if not res_car == res_car2 :
				
				maintext += "& %s</FONT>" % ( res_car2 )
				 
			maintext += " | Date: <FONT SIZE=+1>%s</FONT> (<b>%s</b>)</td></tr>" % ( res_date, res_overnight ) 
#			maintext += "</table>"
#			maintext += "<table>"
#			maintext += '<tr><td class=label2>00</td><td class=label2>01</td><td class=label2>02</td><td class=label2>03</td><td class=label2>04</td><td class=label2>05</td><td class=label2>06</td><td class=label2>07</td><td class=label2>08</td><td class=label2>09</td><td class=label2>10</td><td class=label2>11</td><td class=label2>12</td><td class=label2>13</td><td class=label2>14</td><td class=label2>15</td><td class=label2>16</td><td class=label2>17</td><td class=label2>18</td><td class=label2>19</td><td class=label2>20</td><td class=label2>21</td><td class=label2>22</td><td class=label2>23</td><td class=label2>00</td></tr>'
#			maintext += "<tr><td colspan=24>"
#			maintext += "<div id='slider-range'></div></td></tr>" 
#			maintext += "<tr><td class=right>Date</td><td>%s</td></tr>" % ( res_date ) 
#			maintext += "</table>"
#			maintext += "<table>"
#			maintext += "<tr><td class=right>DateIn</td><td>%s</td></tr>" % ( res_datein ) 
			maintext += "<tr><td class=right>In|Out:</td><td><FONT SIZE=+2>%s " % ( res_datein[5:16]) 
#			maintext += "<tr><td class=right>HourIn</td><td>%s</td></tr>" % ( hourin ) 
			maintext += "%s</FONT></td></tr>" % ( res_dateout[5:16] ) 
#			maintext += "<tr><td class=right>HourOut</td><td>%s</td></tr>" % ( hourout ) 
			maintext += "<tr><td class=right>Destiny:</td><td><FONT SIZE=+1>%s - %s</FONT></td></tr>" % ( destinyName, res_destiny )

			maintext += "<tr><td colspan=2><hr></td></tr>"
			
			maintext += "<tr><td class=right>Driver:</td><td><FONT SIZE=+1>%s</FONT> %s</td></tr>" % ( res_driver, wpDriver ) 
			maintext += "<tr><td class=right>Passenger:</td><td><FONT SIZE=+1>%s</FONT></td></tr>" % ( res_pass ) 
			maintext += "<tr><td class=right>WP Passenger:</td><td bgcolor=yellow><FONT SIZE=+1>%s</FONT></td></tr>" % ( wpNames2 ) 
			maintext += "</table>"
			
# middle break
			maintext += '</td><td valign =top>' 			

# right table
			
			maintext += '<table cellpadding=2 cellspacing=2>'

			if res_overnight == 'Overnight' :
											
				maintext += "<tr><td class=right>Overnight:</td><td bgcolor=lightblue><b>%s</b></td></tr>" % ( res_overnight ) 
			
			else:

				maintext += "<tr><td class=right>Overnight:</td><td bgcolor=blanchedalmond><b>%s</b></td></tr>" % ( res_overnight ) 

			maintext += "<tr><td class=right>OpenSeats:</td><td>%s</td></tr>" % ( seattable2 )

			maintext += "<tr><td colspan=2><hr></td></tr>"

			maintext += "<tr><td class=right>Return Driver:</td><td><FONT SIZE=+1>%s</FONT></td></tr>" % ( res_rdriver ) 
			maintext += "<tr><td class=right>Return Passenger:</td><td><FONT SIZE=+1>%s</FONT></td></tr>" % ( res_pass2 ) 
			maintext += "<tr><td class=right>WP Return Passenger:</td><td bgcolor=yellow><FONT SIZE=+1>%s</FONT></td></tr>" % ( wpNames3 ) 
			maintext += "<tr><td class=right>Monitor:</td><td><FONT SIZE=+1>%s</FONT></td></tr>" % ( res_monitor ) 


#			maintext += "<tr><td class=right>IDNo</td><td>%s</td></tr>" % ( str( res_idno ) )
			maintext += "<tr><td colspan=2><hr></td></tr>"
			
			bgcolor = 'white'

			if res_status == "Removed" :

					bgcolor = 'pink'
					
			maintext += "<tr><td class=right bgcolor=%s>Status:</td><td bgcolor=%s>%s | IDNo: %s</td></tr>" % ( bgcolor, bgcolor, res_status, res_idno )
#			maintext += "<tr><td class=right>OpenSeats:</td><td><b>%s</b> ( %s - %s ) | OpenReturn: <b>%s</b> ( %s-%s )" \
#			% ( res_openseats, res_carseats, res_seats, res_openrseats, res_carseats, res_rseats )
			maintext += "<tr><td class=right>Shift IDNo:</td>"
			if res_masterid > 0 :
			
				maintext += "<td bgcolor=yellow><b><a href=shiftone.py?idno=%s>( %s )</a> Go Shift!</b></td></tr>" % ( res_masterid, res_masterid )
			
			else:
			
				maintext += "<td>( %s ) No Shift</td></tr>" % ( res_masterid )
				
			maintext += "<tr><td class=right bgcolor=%s>Blocking:</td><td>%s</td></tr>" % ( bgcolor, res_blocking )
			maintext += "<tr><td class=right>Comment:</td><td>%s</td></tr>" % ( res_comment )
			
			maintext += "</table>"
# close outer tabl;e
			maintext += '</td></table>' 
			
# times outer table
#			maintext += '<table cellpadding=2 cellspacing=2><td>'
			maintext += '<table cellpadding=2 cellspacing=2><th colspan=2>TimeStamps</th></tr>'
			maintext += '<tr><td>'

#right table
			maintext += '<table cellpadding=2 cellspacing=2 border=2 rules=all>'

#			maintext += "<tr><td valign=center><form method=POST action='resone.py?idno=%s'><input type=hidden name=idno size=20 value='%s'><input name=action type=submit value='Update-A'></form></td>" % ( res_idno, res_idno ) 
			maintext += "<tr><td valign=center><form method=POST action='resone.py?idno=%s'><input name=action type=submit value='Update-A'></form></td>" % ( res_idno ) 
			maintext += "<td valign=center><form method=POST action='resone.py?idno=%s'><input name=action type=submit value='Clear-A'></form></td>" % ( res_idno ) 

			maintext += "<td class=right>DateStamp-A:</td><td>%s</td></tr>" % ( res_datea ) 

			maintext += "<tr><td valign=center><form method=POST action='resone.py?idno=%s'><input name=action type=submit value='Update-B'></form></td>" % ( res_idno ) 
			maintext += "<td valign=center><form method=POST action='resone.py?idno=%s'><input name=action type=submit value='Clear-B'></form></td>" % ( res_idno ) 

			maintext += "<td class=right>DateStamp-B:</td><td>%s</td></tr>" % ( res_dateb ) 

			maintext += "<tr><td valign=center><form method=POST action='resone.py?idno=%s'><input name=action type=submit value='Update-C'></form></td>" % ( res_idno ) 
			maintext += "<td valign=center><form method=POST action='resone.py?idno=%s'><input name=action type=submit value='Clear-C'></form></td>" % ( res_idno ) 

			maintext += "<td class=right>DateStamp-C:</td><td>%s</td></tr>" % ( res_datec ) 
			maintext += "</table>"

# middle break 
			
			maintext += '</td><td valign =top>' 			
			
#right table
			maintext += '<table cellpadding=2 cellspacing=2 border=2 rules=all>'

			maintext += "<tr><td valign=center><form method=POST action=resone.py?idno=%s><input name=action type=submit value='Update-D'></form></td>" % ( res_idno ) 
			maintext += "<td valign=center><form method=POST action=resone.py?idno=%s><input name=action type=submit value='Clear-D'></form></td>" % ( res_idno ) 

			maintext += "<td class=right>DateStamp-D:</td><td>%s</td></tr>" % ( res_dated )

			maintext += "<tr><td valign=center><form method=POST action=resone.py?idno=%s><input name=action type=submit value='Update-E'></form></td>" % ( res_idno ) 
			maintext += "<td valign=center><form method=POST action=resone.py?idno=%s><input name=action type=submit value='Clear-E'></form></td>" % ( res_idno ) 


			maintext += "<td class=right>DateStamp-E:</td><td>%s</td></tr>" % ( res_datee )

			maintext += "<tr><td valign=center><form method=POST action=resone.py?idno=%s><input name=action type=submit value='Update-F'></form></td>" % ( res_idno ) 
			maintext += "<td valign=center><form method=POST action=resone.py?idno=%s><input name=action type=submit value='Clear-F'></form></td>" % ( res_idno ) 


			maintext += "<td class=right>DateStamp-F:</td><td>%s</td></tr>" % ( res_datef )
			
			maintext += "</table>"

			maintext += '</td><td valign =top>' 			

# seattable
#			maintext += seattable2

# close outer tabl;e
			
			maintext += '</td></table>' 
			
						
			
			maintext += '</center>'

			maintext += 'History Last ******<br><pre>%s</pre><br>****** History First<br>' % ( res_history )

#			maintext += '<table cellpadding=3 cellspacing=2 border=2 rules=all>'



# these 3 lines are slider results
#			maintext += 'amt: <input type="text" id="amount" readonly style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMin: <input type="text" id="amountMin" readonly style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMax: <input type="text" id="amountMax" readonly style="border:0; color:#f6931f; font-weight:bold;">'
			
#			maintext += '<table cellpadding=3 cellspacing=2 >'
#			maintext += '<tr><td class=label2>00</td><td class=label2>01</td><td class=label2>02</td><td class=label2>03</td><td class=label2>04</td><td class=label2>05</td><td class=label2>06</td><td class=label2>07</td><td class=label2>08</td><td class=label2>09</td><td class=label2>10</td><td class=label2>11</td><td class=label2>12</td><td class=label2>13</td><td class=label2>14</td><td class=label2>15</td><td class=label2>16</td><td class=label2>17</td><td class=label2>18</td><td class=label2>19</td><td class=label2>20</td><td class=label2>21</td><td class=label2>22</td><td class=label2>23</td><td class=label2>00</td></tr>'
#			maintext += '<tr><td colspan=25>'
#			maintext += '<div id="slider-range"></div>'
#			maintext += '</td></tr></table>'
#			maintext += 'amt: <input type="text" id="amount" readonly style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMin: <input type="text" id="amountMin" readonly style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMax: <input type="text" id="amountMax" readonly style="border:0; color:#f6931f; font-weight:bold;">'

		if method == 'POST' and field['action'].value == 'Edit' :

			cursor2.execute("select code, name from destiny order by code" )
			destinyCtrl = '<select size=1 name=destiny>'
		 	
			for raw in cursor2.fetchall() :

				code=raw[0]
				name=raw[1]

				if res_destiny == code:

					destinyCtrl += '<option value=%s selected>%s' % (  code, name )
				else:
					destinyCtrl += '<option value=%s>%s' % ( code, name )

			destinyCtrl += '</select>'

			status1 = ( 'Active', 'Removed', 'Garage' )
			statusCtrl = '<select size=1 name=status>'
			for status2 in status1 :
				if res_status == status2 :
					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
				else:
					statusCtrl += '<option value=%s>%s' % ( status2, status2 )

			statusCtrl += '</select>'
			
			overnight1 = ( 'Daytime', 'Overnight' )
			overnightCtrl = '<select size=1 name=overnight>'
			for overnight2 in overnight1 :
				if res_overnight == overnight2 :
					overnightCtrl += '<option value=%s selected>%s' % ( overnight2, overnight2 )
				else:
					overnightCtrl += '<option value=%s>%s' % ( overnight2, overnight2 )

			overnightCtrl += '</select>'

# Blocking - how does this res block new reserves. 
# In-Out = Duration of Datein->Dateout including Times, 
# Black-24 = Prevents New Reserves on the Date - all 24 hours, like Garage
# Out-24 = Prevents New Reserves on the OutDate - all 24 hours

#			blocking1 = ( 'In-Out', 'Black-24' )
			blocking1 = ( 'In-Out', 'Block-24' )
			blockCtrl = '<select size=1 name=blocking>'
			for block2 in blocking1 :
				if res_blocking == block2 :
					blockCtrl += '<option value=%s selected>%s' % ( block2, block2 )
				else:
					blockCtrl += '<option value=%s>%s' % ( block2, block2 )

			blockCtrl += '</select>'


			wPlans = "WorkPlans: "

			cursor6.execute("select idno, date, assigned1, assigned2 from items where residno='%s' and logcrew='WP' " )
			numrows6 = cursor6.rowcount
			if numrows6 > 0 :
				for ruw in cursor6.fetchall() :
						item_idno = ruw[0]
						item_assigned1 = ruw[2]
						item_assigned2 = ruw[3]
						wPlans += "WP +Driver: ( %s ) assigned1: %s assigned2: %s<br>" % ( str( item_idno ), item_assigned1, item_assigned2 )

			cursor6.execute("select idno, date, assigned1, assigned2 from items where residno2='%s' and logcrew='WP' " )
			numrows6 = cursor6.rowcount
			if numrows6 > 0 :
				for ruw in cursor6.fetchall() :
						item_idno = ruw[0]
						item_assigned1 = ruw[2]
						item_assigned2 = ruw[3]
						wPlans += "WP +Passengers: ( %s ) assigned1: %s assigned2: %s<br>" % ( str( item_idno ), item_assigned1, item_assigned2 )

			cursor6.execute("select idno, date, assigned1, assigned2 from items where residno3='%s' and logcrew='WP' " )
			numrows6 = cursor6.rowcount
			if numrows6 > 0 :
				for ruw in cursor6.fetchall() :
						item_idno = ruw[0]
						item_assigned1 = ruw[2]
						item_assigned2 = ruw[3]
						wPlans += "WP +Return Passengers: ( %s ) assigned1: %s assigned2: %s<br>" % ( str( item_idno ), item_assigned1, item_assigned2 )


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

# Return Driver Spinner


			cursor3.execute( "select user, train from users order by user" )
			
			numrows3 = cursor3.rowcount

			rdriver2 = '<select name=rdriver>'
			
			for result3 in cursor3.fetchall() :
			
				rdriver3 = result3[0]
				rdriver3 = rdriver3.strip()
				rtrain3 = result3[1]
				
				rdriver3txt = rdriver3

				if rtrain3 == 'P' :
					
					rdriver3txt = rdriver3 + ' (NoSum)'
			
				if rdriver3 == res_rdriver :
					
					rdriver2 += "<option value='%s' selected>%s" % ( rdriver3, rdriver3txt )
					
				else :
					
					rdriver2 += "<option value='%s'>%s" % ( rdriver3, rdriver3txt )
			
			rdriver2 += '</select>'
			
# StartTime Spinner


			cursor3.execute("select text from refer where code='%s' order by seq" % ( 'TIME' ) )
			
			numrows3 = cursor3.rowcount

			start2 = '<select name=start2>'
			
			for result3 in cursor3.fetchall() :
			
				refer_start=result3[0]
			
				if refer_start == hourminin :
					
					start2 += "<option value='%s' selected>%s" % ( refer_start, refer_start )
					
				else :
					
					start2 += "<option value='%s'>%s" % ( refer_start, refer_start )
			
			start2 += '</select>'

# EndTime Spinner

			cursor3.execute("select text from refer where code='%s' order by seq" % ( 'TIME' ) )
			
			numrows3 = cursor3.rowcount

			end2 = '<select name=end2>'
			
			for result3 in cursor3.fetchall() :
			
				refer_start=result3[0]
			
				if refer_start == hourminout :
					
					end2 += "<option value='%s' selected>%s" % ( refer_start, refer_start )
				else :
					
					end2 += "<option value='%s'>%s" % ( refer_start, refer_start )
			
			end2 += '</select>'


# Car Spinner


			cursor3.execute( "select car from cars where status = 'Active' order by seq" )
			
			numrows3 = cursor3.rowcount



			cars1 = '<select name=car>'
			
			for result3 in cursor3.fetchall() :
			
				car3 = result3[0]
				car3 = car3.strip()
				
				cursor5.execute("select idno, car, start, end, recur, type, warning from blackres where car = '%s' and recur='Daily' and status='Active' order by start" % ( car3 ) )
				numrows5 = cursor5.rowcount
				black_type = ''
				if numrows5 > 0 :
					raw = cursor5.fetchone()
					black_type = raw[5]

				car4 = car3 + ' ' + black_type
								
				if car3 == res_car :
							
					cars1 += "<option value='%s' selected>%s" % ( car3, car4 )
					
				else :
				
					cars1 += "<option value='%s'>%s" % ( car3, car4 )
			
			cars1 += '</select>'

			cursor3.execute( "select car from cars order by seq" )
			
			numrows3 = cursor3.rowcount

			cars2 = '<select name=car2>'
			
			for result3 in cursor3.fetchall() :
			
				car3 = result3[0]
				car3 = car3.strip()


				cursor5.execute("select idno, car, start, end, recur, type, warning from blackres where car = '%s' and recur='Daily' and status='Active' order by start" % ( car3 ) )
				numrows5 = cursor5.rowcount
				black_type = ''
				if numrows5 > 0 :
					raw = cursor5.fetchone()
					black_type = raw[5]

				car4 = car3 + ' ' + black_type
			
				if car3 == res_car2 :
					
					cars2 += "<option value='%s' selected>%s" % ( car3, car4 )
					
				else :
					
					cars2 += "<option value='%s'>%s" % ( car3, car4 )
			
			cars2 += '</select>'

			maintext += "<form method=post action='resone.py?idno=%s'><input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>" % ( res_idno )

			maintext += '<table>'
			maintext += '<tr><th class=thbig colspan=25 align=center>Hours of Day: ' +  res_date + '<th></tr>'

			maintext += '<tr><td>' + res_date + '<td>'
			
			th_seq = 0
			while th_seq < 25 :
#				maintext += '<tr>'
				if th_seq >= int( hourin)  and th_seq <= int( hourout ) :

					maintext += '<th bgcolor=blanchedalmond><FONT SIZE=+1><b>' + str( th_seq ) + '</FONT></b></th>'

				else:

					maintext += '<th bgcolor=lime>' + str( th_seq ) + '</th>'
					
				th_seq += 1

			maintext += '</tr>'
			
# 2nd days line			

			if res_overnight == 'Overnight' :
				
				maintext += '<tr><td>' + res_date2 + '<td>'
				
				th_seq = 0
			
				while th_seq < 25 :

					if th_seq <= int( hourout ) :
						
						maintext += '<td bgcolor=lightblue><FONT SIZE=+1><b>' + str( th_seq ) + '</FONT></b></td>'

					else:

						maintext += '<td bgcolor=lime>' + str( th_seq ) + '</td>'
					
					th_seq += 1
				
				maintext += '</tr>'


#			maintext += '<tr><td class=label2>00</td><td class=label2>01</td><td class=label2>02</td><td class=label2>03</td><td class=label2>04</td><td class=label2>05</td><td class=label2>06</td><td class=label2>07</td><td class=label2>08</td><td class=label2>09</td><td class=label2>10</td><td class=label2>11</td><td class=label2>12</td><td class=label2>13</td><td class=label2>14</td><td class=label2>15</td><td class=label2>16</td><td class=label2>17</td><td class=label2>18</td><td class=label2>19</td><td class=label2>20</td><td class=label2>21</td><td class=label2>22</td><td class=label2>23</td><td class=label2>00</td></tr>'
#			maintext += '<td colspan=25><div id="slider-range"></div></td>'
			maintext += '</table><br>'
			
			
# outer table 	
			maintext += '<table cellpadding=3 cellspacing=3><tr><td valign=top>'
			
# left column table
			
			maintext += '<table cellpadding=3 cellspacing=3>'
#			maintext += "<tr><td class=right>Cars:</td><td><input type=text name=car size=10 value='%s'> | "% ( res_car )
			maintext += "<tr><td class=right>Cars:</td><td>%s | "% ( cars1 )
#			maintext += "<input type=text name=car2 size=10 value='%s'></td></tr>" % ( res_car2 ) 
			maintext += "%s</td></tr>" % ( cars2 ) 
			maintext += "<tr><td class=right>Date:</td><td><input type=text name=date size=16 value='%s'></td></tr>" % ( res_date ) 
#			maintext += "<tr><td class=right>Date In</td><td><input type=text name=datein size=20 value='%s'></td></tr>" % ( res_datein ) 
#			maintext += "<tr><td class=right>Date Out</td><td><input type=text name=dateout size=20 value='%s'></td></tr>" % ( res_dateout ) 
#			maintext += "<tr><td class=right>Time In | Out:</td><td><input type=text name=datein size=20 value='%s'> | " % ( res_datein ) 
			maintext += "<tr><td class=right>In|Out:</td><td>%s | " % ( res_datein[5:16] ) 
			maintext += "%s | <b>Choose In|Out:</b> %s - %s</td></tr>" % ( res_dateout[5:16], start2, end2 ) 
#			maintext += "<tr><td class=right>OverNight</td><td><input type=text name=overnight size=20 value='%s'></td></tr>" % ( res_overnight ) 
#			maintext += "<tr><td class=right>OverNight</td><td><div class='ui-widget'><input name=overnight2 id='tags'></div></td></tr>" 
#			maintext += "<tr><td class=right>Destiny</td><td><input type=text name=destiny size=5 value='%s'></td></tr>" % ( res_destiny ) 
			maintext += "<tr><td class=right>Destiny:</td><td>%s</td></tr>" % ( destinyCtrl ) 
#			maintext += "<tr><td class=right>Driver:</td><td><input type=text name=driver size=20 value='%s'> | %s</td></tr>" % ( res_driver, driver2 ) 
			maintext += "<tr><td class=right>Driver:</td><td>%s</td></tr>" % ( driver2 ) 
			maintext += "<tr><td class=right>Passengers:</td><td><div class='ui-widget'><input name=pass1 id='tags' size=40 maxsize=80 value='%s'></div></td></tr>" % ( res_pass )
			maintext += "<tr><td class=right bgcolor=yellow>CSV List:</td><td bgcolor=yellow><FONT SIZE=-1><b>Passengers w/ COMMAs 'Takata, Takada, Takato', cargo in seats 'Takata, Box1, Box2' </td></tr>"
#			maintext += "<tr><td class=right bgcolor=yellow>Cargo Seats:</td><td>You may reserves Seats with cargo like 'Takata, Box1, Box2'</td></tr>"
			maintext += "<tr><td class=right bgcolor=yellow>Seats#:</td><td bgcolor=yellow><FONT SIZE=-1><b>Res# Seats counts COMMAs 'Takata, Takada, Takato' = 3 Pass. Seats = 4 includes Driver</td></tr>"

			maintext += "</table>"

#col break the two tables

			maintext += '</td><td valign =top>' 

# right column table			
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>OverNight:</td><td>%s</d></tr>" % ( overnightCtrl ) 
			maintext += "<tr><td class=right>Status:</td><td>%s | IDNo: %s</td></tr>" % ( statusCtrl, res_idno ) 
			maintext += "<tr><td class=right>Master IDNo:</td><td><input type=text name=masterid size=10 value='%s'></td></tr>" % ( res_masterid ) 
			maintext += "<tr><td class=right>Comment:</td><td><input type=text name=comment size=40  maxsize=80 value='%s'></td></tr>" % ( res_comment ) 
			
			
#			maintext += "<tr><td class=right>Return Driver:</td><td><input type=text name=rdriver size=20 value='%s'> | %s</td></tr>" % ( res_rdriver, rdriver2 ) 
			maintext += "<tr><td class=right>Return Driver:</td><td>%s</td></tr>" % ( rdriver2 ) 
#			maintext += "<tr><td class=right>Passengers</td><td><input type=text name=pass size=100 value='%s'></td></tr>" % ( res_pass ) 
			maintext += "<tr><td class=right>Return Passengers 2:</td><td><input type=text name=pass2 size=40 maxsize=80 value='%s'></td></tr>" % ( res_pass2 ) 
#			maintext += "<tr><td class=right>Status</td><td><input type=text name=status size=20 value='%s'></td></tr>" % ( res_status ) 
			maintext += "<tr><td class=right>Monitor:</td><td><input type=text name=monitor size=30  maxsize=80 value='%s'></td></tr>" % ( res_monitor ) 
			maintext += "<tr><td class=right>Blocking:</td><td>%s</td></tr>" % ( blockCtrl ) 

			maintext += "</table>"
			
			maintext += "</td></table>"

# bottom table times
			maintext += '<table cellpadding=3 cellspacing=3><th colspan=2>TimeStamps</th></tr>'

			maintext += '<tr><td>'

			maintext += '<table cellpadding=3 cellspacing=3>'
			

			maintext += "<tr><td class=right>DateStamp-A:</td><td><input type=text name=datea size=20 value='%s'></td></tr>" % ( res_datea ) 
			
			maintext += "<tr><td class=right>DateStamp-B:</td><td><input type=text name=dateb size=20 value='%s'></td></tr>" % ( res_dateb ) 

			maintext += "<tr><td class=right>DateStamp-C:</td><td><input type=text name=datec size=20 value='%s'></td></tr>" % ( res_datec ) 
			
			maintext += "</table>"

			maintext += "</td><td>"
			
			maintext += '<table cellpadding=3 cellspacing=3>'


			maintext += "<tr><td class=right>DateStamp-D:</td><td><input type=text name=dated size=20 value='%s'></td></tr>" % ( res_dated ) 
			maintext += "<tr><td class=right>DateStamp-E:</td><td><input type=text name=datee size=20 value='%s'></td></tr>" % ( res_datee ) 
			maintext += "<tr><td class=right>DateStamp-F:</td><td><input type=text name=datef size=20 value='%s'></td></tr>" % ( res_datef ) 

			maintext += "</table>"

			maintext += "</td></table>"
						
#			maintext += 'amt: <input type="text" id="amount" readonly style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMin: <input type="text" id="amountMin" name="amountMin" readonly style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMax: <input type="text" id="amountMax" name="amountMax" readonly style="border:0; color:#f6931f; font-weight:bold;">'

#			maintext += 'amtMin: <input type="text" id="amountMin" name="amountMin" style="border:0; color:#f6931f; font-weight:bold;">'
#			maintext += 'amtMax: <input type="text" id="amountMax" name="amountMax" style="border:0; color:#f6931f; font-weight:bold;">'

			maintext += "</form>"
	
#	maintext += '<div class="ui-widget"><input name=overnight2 id="tags"></div>' 
#	maintext += 'slider: <div id="slider"></div>'
	else :
			
		
		hourin = hourin2
		hourout = hourout2
		maintext += 'No Records<br>'

#		maintext += "Reservation IDNO: not exists ( " + str( numrows ) + " )"
#		maintext += "Reservation IDNO: " + idno + " not exists ( " + str( numrows ) + " )"
#		maintext += "If this is New-Res: " + idno + ", there is overlap with another Old-Res above ( " + str( numrows ) + " )<br>"

else :
	
	maintext = logproc.returnLogin()

#maintext='tom'
#hourin='8'
#hourout='10'
printHTML( maintext, hourin, hourout, username )
