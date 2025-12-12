#! /usr/local/python

import os
import sys
import datetime
import dbconnect
import cgi
import cgitb; cgitb.enable();
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
#import logproc
import logproc3 as logproc
import html

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3] )
db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()
cursor5=db.cursor()
cursor6=db.cursor()
cursor7=db.cursor()
cursor8=db.cursor()
cursor9=db.cursor()
cursor10=db.cursor()
cursor11=db.cursor()
cursor12=db.cursor()
cursor13=db.cursor()

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:14px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
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
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	



#Database changed
#MariaDB [sumlogs]> desc items;
#+------------+------------+------+-----+---------+----------------+
#| Field      | Type       | Null | Key | Default | Extra          |
#+------------+------------+------+-----+---------+----------------+
#| idno       | int(11)    | NO   | PRI | NULL    | auto_increment |
#| dayidno    | int(11)    | YES  |     | NULL    |                |
#| date       | date       | YES  |     | NULL    |                |
#| day        | char(10)   | YES  |     | NULL    |                |
#| logcrew    | char(2)    | YES  |     | NULL    |                |
#| itemtime   | datetime   | YES  |     | NULL    |                |
#| itemtitle  | char(200)  | YES  |     | NULL    |                |
#| itemtext   | mediumtext | YES  |     | NULL    |                |
#| user       | char(20)   | YES  |     | NULL    |                |
#| type       | char(10)   | YES  |     | NULL    |                |
#| downtime   | char(3)    | YES  |     | NULL    |                |
#| subsystem  | char(10)   | YES  |     | NULL    |                |
#| status     | char(15)   | YES  |     | NULL    |                |
#| timestamp  | datetime   | YES  |     | NULL    |                |
#| history    | mediumtext | YES  |     | NULL    |                |
#| oldidno    | int(11)    | YES  | MUL | NULL    |                |
#| comment    | mediumtext | YES  |     | NULL    |                |
#| endtime    | datetime   | YES  |     | NULL    |                |
#| realstart  | datetime   | YES  |     | NULL    |                |
#| realend    | datetime   | YES  |     | NULL    |                |
#| niteeffect | char(100)  | YES  |     | NULL    |                |
#| dayeffect  | char(100)  | YES  |     | NULL    |                |
#| location   | char(20)   | YES  |     | NULL    |                |
#| assigned1  | char(30)   | YES  |     | NULL    |                |
#| dcassist   | char(3)    | YES  |     | NULL    |                |
#| location2  | char(20)   | YES  |     | NULL    |                |
#| location3  | char(20)   | YES  |     | NULL    |                |
#| completion | char(200)  | YES  |     | NULL    |                |
#| contact2   | char(50)   | YES  |     | NULL    |                |
#| others     | char(50)   | YES  |     | NULL    |                |
#| master     | int(11)    | YES  |     | NULL    |                |
#+------------+------------+------+-----+---------+----------------+
#31 rows in set (0.00 sec)



now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')

today2 = datetime.date.today()
tmrw = today2 + datetime.timedelta( days = 1 )
tmrw_txt = tmrw.strftime('%Y-%m-%d')

#referpage=cgi.os.environ['HTTP_REFERER']
#clientip=cgi.os.environ['REMOTE_ADDR']


#if field.has_key('idno'):
if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

#if field.has_key('date'):
if 'date' in field :

	date = field['date'].value
	
else:
	
	date = today
	
#if field.has_key('logcrew'):
if 'logcrew' in field :

	logcrew = field['logcrew'].value
	
else:
	
	logcrew = 'WP'

#if field.has_key('itemtitle'):
if 'itemtitle' in field :

	itemtitle = field['itemtitle'].value
	
else:
	
	itemtitle = ''

#if field.has_key('itemtext'):
if 'itemtext' in field :

	itemtext = field['itemtext'].value
	
else:
	
	itemtext = ''


#if field.has_key('type'):
if 'type' in field :

	type = field['type'].value
	
else:
	
	type = 'Comment'

#if field.has_key('downtime'):
if 'downtime' in field :

	downtime = field['downtime'].value
	
else:
	
	downtime = '0'

#if field.has_key('subsystem'):
if 'subsystem' in field :

	subsystem = field['subsystem'].value
	
else:
	
	subsystem = 'None'

#if field.has_key('itemtime'):
if 'itemtime' in field :

	itemtime = field['itemtime'].value
	
else:
	
	itemtime = '00:00'

#if field.has_key('status'):
if 'status' in field :

	status = field['status'].value
	
else:
	
	status = 'Completed'

#if field.has_key('history'):
if 'history' in field :

	history = field['history'].value
	
else:
	
	history = ''

#if field.has_key('user'):
if 'user' in field :

	user = field['user'].value
	
else:
	
	user = ''

#if field.has_key('todo'):
if 'todo' in field :

	todo = field['todo'].value
	
else:
	
	todo = 'query'
	
if 'endtime' in field :

	endtime = field['endtime'].value
	
else:
	
	endtime = '0000-00-00 00:00'

if 'realstart' in field :

	realstart = field['realstart'].value
	
else:
	
	realstart = '0000-00-00 00:00'

if 'realend' in field :

	realend = field['realend'].value
	
else:
	
	realend = '0000-00-00 00:00'

if 'niteeffect' in field :

	niteeffect = field['niteeffect'].value
	
else:
	
	niteeffect = ''
	
if 'dayeffect' in field :

	dayeffect = field['dayeffect'].value
	
else:
	
	dayeffect = ''
	
if 'location' in field :

	location = field['location'].value
	
else:
	
	location = '.none'

if 'location2' in field :

	location2 = field['location2'].value
	
else:
	
	location2 = '.none'

if 'location3' in field :

	location3 = field['location3'].value
	
else:
	
	location3 = '.none'		

if 'assigned1' in field :

	assigned1 = field['assigned1'].value
	
else:
	
	assigned1 = ''

if 'dcassist' in field :

	dcassist = field['dcassist'].value
	
else:
	
	dcassist = '.none'

if 'completion' in field :

	completion = field['completion'].value
	
else:
	
	completion = ''	

if 'contact2' in field :

	contact2 = field['contact2'].value
	
else:
	
	contact2 = ''
	
if 'others' in field :

	others = field['others'].value
	
else:
	
	others = ''

if 'master' in field :

	master = field['master'].value
	
else:
	
	master = ''

if 'hr' in field :

	hr = field['hr'].value
	
else:
	
	hr = '10'
	
if 'assigned2' in field :

	assigned2 = field['assigned2'].value
	
else:
	
	assigned2 = '.none'

assigned2=assigned2.strip()

if 'notify' in field :

	notify = field['notify'].value
	
else:
	
	notify = '.none'

if 'comptext' in field :

	comptext = field['comptext'].value
	
else:
	
	comptext = ''

if 'stamp' in field :

	stamp = field['stamp'].value
	
else:
	
	stamp = 'none'

if 'copyid' in field :

	copyid = field['copyid'].value
	
else:
	
	copyid = '0'
	

if 'copyx' in field :

	copyx = field['copyx'].value
	
else:
	
	copyx = '0'


if 'start2' in field :

	start2 = field['start2'].value
	
else:
	
	start2 = '00:00'


if 'end2' in field :

	end2 = field['end2'].value
	
else:
	
	end2 = '00:00'	

if 'hrout' in field :

	hrout = field['hrout'].value
	
else:
	
	hrout = '16:00'	

if 'otherreq' in field:

	otherreq = field['otherreq'].value
	
else:
	
	otherreq = ''
	
#if 'residno' in field:

#	residno = field['residno'].value
	
#else:
	
#	residno = '0'


# RID = Edit Res IDNO from Get to Open Edit Fields for One Res
	
if 'rid' in field:

	rid = field['rid'].value

else:

	rid = '0'

rid = rid.strip()

if 'driver' in field:

	driver = field['driver'].value

else:

	driver = ''

driver=driver.strip()

if 'rdriver' in field:

	rdriver = field['rdriver'].value

else:

	rdriver = ''

rdriver=rdriver.strip()


if 'pass1' in field:

	pass1 = field['pass1'].value

else:

	pass1 = ''

pass1 = pass1.strip()

if 'rpass1' in field:

	rpass1 = field['rpass1'].value

else:

	rpass1 = ''

rpass1 = rpass1.strip()

if 'monitor' in field:

	monitor = field['monitor'].value

else:

	monitor = ''

monitor = monitor.strip()

#wg_users = ( 'winegar', 'rikilee', 'letawsky', 'kiaina', 'kambe', 'hiwas51', 'noriko', 'pyo', 'wung', 'hattori' )
wg_users = ( 'winegar' )

#if True :
				
if logproc.validCookie() :

	username, end, term, logcrew2 = logproc.getUsername()
	
	username = username.strip()
	
	cursor2.execute("select user from users where stnuser = '%s' " % ( username ) )
	numrows2 = cursor2.rowcount

	if numrows2 == 1 :

		row = cursor2.fetchone()
		user_contact1 = row[0]
		
	else :

		user_contact1 = '.none'
		
	user_contact1 = user_contact1.strip()

#	if method == 'POST' and field['action'].value == 'Cancel' and int( idno ) > 0 :
#	
#		cursor2.execute("update items set status='Cancelled' where idno = '%s'" % ( idno ) )
			
	updateComment = ''

	if method == 'POST' and field['action'].value == 'SaveRes' and int( rid ) > 0 :
	
		cursor.execute("update res set driver = '%s', rdriver = '%s', pass = '%s', rpass = '%s', monitor = '%s' where idno = '%s'" % (  driver, rdriver, pass1, rpass1, monitor, rid ) )
		updateComment += 'Post SaveRes: ' + rid + "<br>"

		seats = 1
		
		driver2 = driver.upper()
		
		pass2 = pass1.strip()
		
		pass2 = pass2.upper()
		
#		if len( pass2 ) > 0 and pass2 != 'None' and pass2 != '.none' :
		if len( pass2 ) > 0 and pass2 != 'NONE' and pass2 != '.NONE' :
			
			countpass = pass2.split(',')
			
			countpass2 = []

			countpass2.append( driver2 )
			
			if len( countpass ) > 0 :

				for pass3 in countpass :
				
					pass3 = pass3.strip()
					
					if len ( pass3 ) > 0 :
										
#					if pass3 not in countpass2 :
											
						countpass2.append( pass3 )
#									if len( countpass ) > 0  :

			if len( countpass2 ) > 0  :
					
				seats = len ( countpass2 )


		
		rpass2 = rpass1.strip()
		
		rpass2 = rpass2.upper()
		
		rdriver2 = rdriver.upper()

		rseats = 1

#		if len( rpass2 ) > 0 and rpass2 != 'NONE' and rpass2 != '.NONE' :

#			countpass = rpass2.split(',')

#			countpass = countpass.upper()

#			countpass2 = []

#			countpass2.append( rdriver2 )

#			if len( countpass ) > 0 :

#				for pass3 in countpass :

#					pass3 = pass3.strip()
				
#					if len ( pass3 ) > 0 :
							
#					if pass3 not in countpass2 :
								
#						countpass2.append( pass3 )
#									if len( countpass ) > 0  :
#
#			if len( countpass2 ) > 0  :
		
#				rseats = len ( countpass2 )

		cursor.execute("update res set seats = '%s', rseats='%s' where idno = '%s'" % (  seats, rseats, rid ) )
					
	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :
	
		cursor2.execute("select date, itemtime, endtime, realstart, realend from items where idno = '%s'" % ( idno ) )
		numrows2 = cursor2.rowcount
		
		if numrows2 == 1 :
		
			row = cursor2.fetchone()

			date4 = row[0]
			start4 = row[1]
			end4 = row[2]
			realstart4 = row[3]
			realend4 = row[4]

			date = str( date4 )
		
		now = datetime.datetime.now()
		dt = now.strftime('%Y-%m-%d %H:%M:%S')

		clean_itemtitle = html.escape( itemtitle, quote=True )
		clean_itemtext = html.escape( itemtext, quote=True )
		
		history_text = ''
		history_text += '<br>**********<br>timestamp: ' + dt + ' ( ' + username + ' ) <br>' 

		history_text += 'title: ' + clean_itemtitle + '<br>' 
		history_text += 'text: ' + clean_itemtext + '<br>' 
		
		starttime3 = date + ' ' + start2
		endtime3 = date + ' ' + end2

		seats = 1
		pseats = 0
		
		assigned1 = assigned1.strip()
		assigned2 = assigned2.strip()
		teampass1 = pass1.upper()
		
		driver2 = assigned1.upper()
		pass2 = assigned2.upper()
		teampass1 = teampass1.upper()
		
#		pass2 = pass2.strip()
		
		if len( pass2 ) > 0 and pass2 != 'NONE' and pass2 != '.NONE' :
			
			countpass = pass2.split(',')
			
#			countpass = countpass.upper()
			
			countpass2 = []

			countpass2.append( driver2 )
			
#			if len( countpass ) > 0  and countpass[0] != 'None' and countpass[0] != '.none' :
			if len( countpass ) > 0 :

				for pass3 in countpass :
				
					pass3 = pass3.strip()
					
					if len( pass3 ) > 0:
#					if pass3 not in countpass2 :
											
						countpass2.append( pass3 )
#									if len( countpass ) > 0  :

			if len( countpass2 ) > 1  :
					
				seats = len ( countpass2 )

		
		if len( teampass1 ) > 0 and teampass1 != 'NONE' and teampass1 != '.NONE' :
	
			countpass = teampass1.split(',')
	
#			countpass = countpass.upper()
	
			countpass2 = []
	
#			if len( countpass ) > 0  and countpass[0] != 'None' and countpass[0] != '.none' :
			if len( countpass ) > 0 :

				for pass3 in countpass :
		
					pass3 = pass3.strip()
			
					if len( pass3 ) > 0:
#					if pass3 not in countpass2 :
									
						countpass2.append( pass3 )
#									if len( countpass ) > 0  :

			if len( countpass2 ) > 1  :
					
				pseats = len ( countpass2 )



#		cursor.execute("update items set itemtime = '%s', itemtitle = '%s', itemtext = '%s', type = '%s', downtime = '%s', \
#		subsystem = '%s', status = '%s', user = '%s', logcrew = '%s', history = concat( '%s', history ) where idno = '%s'" % ( itemtime, clean_itemtitle, clean_itemtext, \
#		type, downtime, subsystem, status, user, logcrew, history_text, idno ) )

#		cursor.execute("update items set itemtime = '%s', itemtitle = '%s', itemtext = '%s', type = '%s', downtime = '%s', \
#		subsystem = '%s', status = '%s', history = concat( '%s', history ) where idno = '%s'" % ( itemtime, clean_itemtitle, clean_itemtext, \
#		type, downtime, subsystem, status, history_text, idno ) )

#		cursor.execute("update items set itemtime = '%s', itemtitle = '%s', itemtext = '%s', type = '%s', downtime = '%s', \
#		subsystem = '%s', status = '%s', history = concat( '%s', history ) where idno = '%s'" % ( starttime3, clean_itemtitle, clean_itemtext, \
#		type, downtime, subsystem, status, history_text, idno ) )
		updateComment += 'Post Save: 2 updates' + idno + "<br>"

		cursor.execute("update items set itemtime = '%s', itemtitle = '%s', itemtext = '%s', type = '%s',  \
		subsystem = '%s', status = '%s', history = concat( '%s', history ) where idno = '%s'"
		% ( starttime3, clean_itemtitle, clean_itemtext, type, subsystem, status, history_text, idno ) )

		
		cursor.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', \
		location = '%s', assigned1 = '%s', dcassist = '%s', location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', \
		others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' where idno = '%s'" \
		% ( endtime3, realstart, realend, niteeffect, dayeffect, location, assigned1, dcassist, location2, location3, completion, contact2, others, master, \
		assigned2, notify, comptext, otherreq, idno ) )

# set driver+assigned to seats, seats2, default residno, residno2, residno3

#		cursor.execute("update items set seats = %s, seats2 = %s, residno=0, residno2=0, residno3=0 where idno = '%s'" % ( seats, seats, idno ) )
		cursor.execute("update items set seats = %s, seats2 = %s, pass = '%s', pseats= %s where idno = '%s'" % ( seats, seats, pass1, pseats, idno ) )


#		cursor.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', \
#		location = '%s', assigned1 = '%s', dcassist = '%s', location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', \
#		comptext = '%s' where idno = '%s'" % ( endtime, realstart, realend, niteeffect, dayeffect, location, assigned1, dcassist, location2, location3, completion, contact2, others, master, \
#		assigned2, notify, comptext, idno ) )
		

# delete all itemreqs

		if int( idno ) > 0 :

			cursor4.execute("delete from itemreqs where planidno = %s" % ( idno ) )

# find checked values and write itemreqs


			cursor3.execute("select text from refer where code='%s' or code='%s' order by seq" % ( 'PLANREQ', 'PLANLOCK' ) )

			numrows3 = cursor3.rowcount

			for result3 in cursor3.fetchall() :

				refer_lock = result3[0]

				if refer_lock in field :

					check_lock = field[ refer_lock ].value

					if refer_lock == check_lock :

						cursor4.execute("insert into itemreqs ( code, planidno ) values ( '%s', %s ) " \
						% ( refer_lock, idno ) )

# New PLans GET + idno=0

	if method == 'GET' and int( idno ) == 0 and date > '0000-00-00' :
	

		now = datetime.datetime.now()
		dt = now.strftime('%Y-%m-%d %H:%M:%S')

		new_date = date
		
		cursor2.execute("select user from users where stnuser = '%s' " % ( username ) )
		numrows2 = cursor2.rowcount

		if numrows2 == 1 :
		
			row = cursor2.fetchone()
			contact1 = row[0]
		else :
		
			contact1 = '.none'

		cursor2.execute("select idno, day from days where date='%s' " % ( new_date ) )
		numrows2 = cursor2.rowcount

		if numrows2 == 1 :
		
			row = cursor2.fetchone()
			days_idno = row[0]
			days_day = row[1]
		else :
		
			days_idno = 0
			days_day = 'None'
				
		itemtime3 = date + ' ' + hr + ':00'
		new_endtime3 = date + ' ' + hrout + ':00'
		clean_itemtitle = ''
		clean_itemtitle += username + " New WorkPlan" 
		clean_itemtext = ''
		new_type = 'Comment'
		new_downtime = '0'
		new_subsystem = '-none-'
		new_status = 'Planned'
		new_history_text = ''

		new_endtime = '0000-00-00 00:00'
		new_realstart = '0000-00-00 00:00'
		new_realend = '0000-00-00 00:00'
		new_niteeffect = ''
		new_dayeffect = ''
		new_location = ''
		new_assigned1 = contact1
		new_dcassist = ''
		new_location2 = ''
		new_location3 = ''
		new_completion = ''
		new_contact2 = ''
		new_others = ''
		new_master = '0'
		new_assigned2 = ''
		new_notify = '.none'
		new_comptext = ''
		new_otherreq = ''

		new_seats = 1
		new_seats2 = 1
		
		itemreqs = []
		
		if int( copyid ) > 0 :
			
			cursor7.execute("select itemtime, itemtitle, itemtext, type, contact1, endtime, assigned1, assigned2, contact2, location, location2, location3, dcassist, seats, seats2 \
			from items where idno='%s'" % ( copyid ) )
			numrows7 = cursor7.rowcount
			
			if numrows7 == 1 :
			
				ruw = cursor7.fetchone()
				new_itemtime = str( ruw[0] )
				clean_itemtitle = ruw[1]
				clean_itemtext = ruw[2]
				new_type = ruw[3]
				contact1 = ruw[4]
				new_endtime = str( ruw[5] )
				new_assigned1 = ruw[6]
				new_assigned2 = ruw[7]
				new_contact2 = ruw[8]
				
				itemtime3 = date + ' ' + new_itemtime[11:16]
				new_endtime3 = date + ' ' + new_endtime[11:16]
				
				new_location = ruw[9]
				new_location2 = ruw[10]
				new_location3 = ruw[11]
				new_dcassist = ruw[12]
				new_seats = ruw[13]
				new_seats2 = ruw[14]
				
				cursor8.execute("select code, planidno from itemreqs where planidno = %s" % ( int( copyid ) ) )
				
				numrows8 = cursor8.rowcount
				
				if numrows8 > 0 :
					
					for result8 in cursor8.fetchall() :
					
						itemreq_code = result8[0]
						itemreqs.append ( itemreq_code )
				

		
#		cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
#		( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( new_date, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
#		new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1 ) )

#		updateComment += 'Get IDNO = 0: ' + rid + "<br>"
		updateComment += 'Get IDNO = 0: ' + idno + "<br>"

		cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1, \
		seats, seats2, residno, residno2, residno3, residno4, residno5, residno6, pass, rpass, pseats ) values \
		( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, 0, 0, 0, '', '', 0  ) " \
		% ( new_date, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
		new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1, new_seats, new_seats2 ) )

		itemsidno = int( cursor3.lastrowid )

		updateComment += 'Get IDNO = 0: ' + str( itemsidno ) + "<br>"

		if itemsidno > 0 :

			cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
			location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' \
			where idno='%s'" % ( new_endtime3, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
			new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, new_otherreq, itemsidno ) )

#			cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
#			location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' where idno='%s'" % ( new_endtime3, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
#			new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, copyx, itemsidno ) )

		
			if len( itemreqs ) > 0 :

				for reqcode in itemreqs :
					
					cursor8.execute( "insert into itemreqs ( code, planidno ) values ( '%s', %s )" % ( reqcode, itemsidno ) )		
		
		
		
		idno = str( itemsidno )

# 2nd copy	
				
		if int( copyid ) > 0 and int( copyx ) > 1 :
		
			startYear = int( date[0:4] )
			startMonth = int( date[5:7] )
			startDay = int( date[8:10] )
		
			datex2 = datetime.date( startYear, startMonth, startDay )
			datexTwo = datex2 + datetime.timedelta( days = 1 )
			nextdate = datexTwo.strftime( '%Y-%m-%d' )
			
			cursor2.execute("select idno, day from days where date='%s'" % ( nextdate ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				raw = cursor2.fetchone()
				days_idno = raw[0]
				days_day = raw[1]

			else :
		
				days_idno = 0
				days_day = 'None'

			itemtime3 = nextdate + ' ' + new_itemtime[11:16]
			new_endtime3 = nextdate + ' ' + new_endtime[11:16]

#			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
#			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
#			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1 ) )

			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1, \
			seats, seats2, residno, residno2, residno3, residno4, residno5, residno6, pass, rpass, pseats ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, 0, 0, 0, '', '', 0  ) " \
			% ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1, new_seats, new_seats2 ) )

			itemsidno = int( cursor3.lastrowid )

			updateComment += 'Copy 1: ' + str( itemsidno ) + "<br>"

			if itemsidno > 0 :

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' where idno='%s'" \
				% ( new_endtime3, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, new_otherreq, itemsidno ) )

				if len( itemreqs ) > 0 :

					for reqcode in itemreqs :

						cursor8.execute( "insert into itemreqs ( code, planidno ) values ( '%s', %s )" % ( reqcode, itemsidno ) )		

# 3rd copy	

		if int( copyid ) > 0 and int( copyx ) > 2 :
		
			startYear = int( date[0:4] )
			startMonth = int( date[5:7] )
			startDay = int( date[8:10] )
		
			datex2 = datetime.date( startYear, startMonth, startDay )
			datexTwo = datex2 + datetime.timedelta( days = 2 )
			nextdate = datexTwo.strftime( '%Y-%m-%d' )
			
			cursor2.execute("select idno, day from days where date='%s'" % ( nextdate ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				raw = cursor2.fetchone()
				days_idno = raw[0]
				days_day = raw[1]

			else :
		
				days_idno = 0
				days_day = 'None'

			itemtime3 = nextdate + ' ' + new_itemtime[11:16]
			new_endtime3 = nextdate + ' ' + new_endtime[11:16]

#			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
#			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
#			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1 ) )

			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1, \
			seats, seats2, residno, residno2, residno3, residno4, residno5, residno6, pass, rpass, pseats ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, 0, 0, 0, '', '', 0  ) " \
			% ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1, new_seats, new_seats2 ) )


			itemsidno = int( cursor3.lastrowid )

			updateComment += 'Copy 2: ' + str( itemsidno ) + "<br>"

			if itemsidno > 0 :

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' where idno='%s'" \
				% ( new_endtime3, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, \
				new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, new_otherreq, itemsidno ) )

				if len( itemreqs ) > 0 :

					for reqcode in itemreqs :

						cursor8.execute( "insert into itemreqs ( code, planidno ) values ( '%s', %s )" % ( reqcode, itemsidno ) )		

# 4th copy	

		if int( copyid ) > 0 and int( copyx ) > 3 :
		
			startYear = int( date[0:4] )
			startMonth = int( date[5:7] )
			startDay = int( date[8:10] )
		
			datex2 = datetime.date( startYear, startMonth, startDay )
			datexTwo = datex2 + datetime.timedelta( days = 3 )
			nextdate = datexTwo.strftime( '%Y-%m-%d' )
			
			cursor2.execute("select idno, day from days where date='%s'" % ( nextdate ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				raw = cursor2.fetchone()
				days_idno = raw[0]
				days_day = raw[1]

			else :
		
				days_idno = 0
				days_day = 'None'

			itemtime3 = nextdate + ' ' + new_itemtime[11:16]
			new_endtime3 = nextdate + ' ' + new_endtime[11:16]

#			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
#			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
#			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1 ) )


			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1, \
			seats, seats2, residno, residno2, residno3, residno4, residno5, residno6, pass, rpass, pseats ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, 0, 0, 0, '', '', 0  ) " \
			% ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1, new_seats, new_seats2 ) )

			itemsidno = int( cursor3.lastrowid )
			
			updateComment += 'Copy 3: ' + str( itemsidno ) + "<br>"

			if itemsidno > 0 :

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' where idno='%s'" \
				% ( new_endtime3, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, new_otherreq, itemsidno ) )

				if len( itemreqs ) > 0 :

					for reqcode in itemreqs :

						cursor8.execute( "insert into itemreqs ( code, planidno ) values ( '%s', %s )" % ( reqcode, itemsidno ) )		

# 5th copy	

		if int( copyid ) > 0 and int( copyx ) > 4 :
		
			startYear = int( date[0:4] )
			startMonth = int( date[5:7] )
			startDay = int( date[8:10] )
		
			datex2 = datetime.date( startYear, startMonth, startDay )
			datexTwo = datex2 + datetime.timedelta( days = 4 )
			nextdate = datexTwo.strftime( '%Y-%m-%d' )
			
			cursor2.execute("select idno, day from days where date='%s'" % ( nextdate ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				raw = cursor2.fetchone()
				days_idno = raw[0]
				days_day = raw[1]

			else :
		
				days_idno = 0
				days_day = 'None'

			itemtime3 = nextdate + ' ' + new_itemtime[11:16]
			new_endtime3 = nextdate + ' ' + new_endtime[11:16]

#			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) \
#			values ( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " \
#			% ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
#			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1 ) )

			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1, \
			seats, seats2, residno, residno2, residno3, residno4, residno5, residno6, pass, rpass, pseats ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, 0, 0, 0, '', '', 0  ) " \
			% ( nextdate, days_idno, days_day, 'WP', itemtime3, clean_itemtitle, clean_itemtext, \
			new_type, new_downtime, new_subsystem, new_status, dt, username, new_history_text, contact1, new_seats, new_seats2 ) )


			itemsidno = int( cursor3.lastrowid )

			updateComment += 'Copy 4: ' + str( itemsidno ) + "<br>"

			if itemsidno > 0 :

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s' where idno='%s'" \
				% ( new_endtime3, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, new_otherreq, itemsidno ) )

				if len( itemreqs ) > 0 :

					for reqcode in itemreqs :

						cursor8.execute( "insert into itemreqs ( code, planidno ) values ( '%s', %s )" % ( reqcode, itemsidno ) )		
						
					
# residno2 & residno3 for WP Passengers
# GET Stanps
# 
	if method == 'GET' and int( idno ) > 0 and stamp != 'none':

		nowstamp = datetime.datetime.now()
		tstamp = nowstamp.strftime('%Y-%m-%d %H:%M:%S')

#		if not trip == 'none'  :

#		if ( int( residno ) > 0 or int( residno4 ) > 0 or int( residno5 ) > 0 or int( residno6 ) > 0 ) and ( stamp == 'up' or stamp == 'return' or stamp == 'both' ) :
		if int( rid ) > 0 and ( stamp == 'up' or stamp == 'return' or stamp == 'both' ) :
	
			if int( rid ) > 0 and stamp == 'up'  :

				cursor4.execute("update items set residno2 = '%s' where idno = '%s'" % ( int( rid ), idno ) )
				updateComment += 'STAMP UP: ' + idno + "<br>"
			
			if int( rid ) > 0 and stamp == 'both'  :
	
				cursor4.execute("update items set residno2 = '%s', residno3 = '%s' where idno = '%s'" % ( int( rid ), int( rid ), idno ) )
				updateComment += 'STAMP BOTH: ' + idno + "<br>"

			if int( rid ) > 0 and stamp == 'return'  :

				cursor4.execute("update items set residno3 = '%s' where idno = '%s'" % ( int( rid ), idno ) )
				updateComment += 'STAMP UP: ' + idno + "<br>"

			items_assigned1 = username.strip()
			items_assigned2 = ''
			items_itemtitle = ''
			
			cursor4.execute("select seats, assigned1, assigned2, itemtitle from items where idno = '%s'" % ( idno ) )
			numrows4 = cursor4.rowcount

			items_seats = '0'

			if numrows4 == 1 :

					ruws = cursor4.fetchone()
					items_seats = str( ruws[0] )
					items_assigned1 = ruws[1]
					items_assigned2 = ruws[2]
					items_assigned1 = items_assigned1.strip()
					items_assigned2 = items_assigned2.strip()

					items_itemtitle = ruws[3]
					items_itemtitle = items_itemtitle.strip()
						
			cursor4.execute("select driver, date, datein, dateout, car, rdriver, pass, rpass, destiny from res where idno = '%s'" % (  int( rid )  ) )	

			numrows4 = cursor4.rowcount

			if numrows4 == 1 :

				raws = cursor4.fetchone()
				item_driver = raws[0]
				item_date = str( raws[1] )
				item_datein = str( raws[2] )
				item_dateout = str( raws[3] )
				item_car = raws[4]
				item_rdriver = raws[5]
				item_pass = raws[6]
				item_rpass = raws[7]
				item_destiny = raws[8]
				
				item_driver = item_driver.strip()
				item_rdriver = item_rdriver.strip()

				item_pass = item_pass.strip()
				item_rpass = item_rpass.strip()
				

#					username=username.strip()
				
				emailsubject = "Add (" + items_seats + ") WP Passengers for " + item_date[5:10] + ' in ' + item_car 
				emailtext = "Date: " + item_date + " " + item_datein[11:13] + "-" + item_dateout[11:13] + " | Car: " + item_car + " | Destiny: " + item_destiny+ "\n\n"
#					emailtext += "Added ( " + items_seats + " ) Passengers for " + item_date + ' in ' + item_car  + "\n"
				emailtext += "New WorkPlan ***\n"

				if stamp == 'up' or stamp == 'both' :

					emailtext += "WP Passengers:  " + items_assigned1  + ", " + items_assigned2 + "\n"
					
				else:

					emailtext += "WP Return Passengers:  " + items_assigned1  + ", " + items_assigned2 + "\n"
					
				emailtext += "WP Task:  " + items_itemtitle + "\n\n"
				
				emailtext += "Current ********\n"
				emailtext += "Driver:  " + item_driver  + " / " + item_rdriver + "\n"
				emailtext += "Passengers:  " + item_pass  + " / " + item_rpass + "\n"
				
				logproc.sendemail ( 'Winegar', emailsubject, emailtext )
#					logproc.sendemail ( item_assigned1, emailsubject, emailtext )

		if stamp == 'unup'  :
	
			cursor4.execute("update items set residno2 = '%s' where idno = '%s'" % ( 0, idno ) )
			updateComment += 'STAMP UNUP: ' + idno + "<br>"

		if stamp == 'unboth'  :
	
			cursor4.execute("update items set residno2 = '%s', residno3 = '%s' where idno = '%s'" % ( 0, 0, idno ) )
			updateComment += 'STAMP UNBOTH: ' + idno + "<br>"
		
		if stamp == 'unreturn'  :
	
			cursor4.execute("update items set residno3 = '%s' where idno = '%s'" % ( 0, idno ) )
			updateComment += 'STAMP UNRETURN: ' + idno + "<br>"
			
		if stamp == 'start' :
		
			cursor4.execute("update items set realstart = '%s', status = 'Started' where idno = '%s'" % ( tstamp, idno ) )
			updateComment += 'STAMP START: ' + idno + "<br>"

		if stamp == 'end' :

			cursor4.execute("update items set realend = '%s', status = 'Completed' where idno = '%s'" % ( tstamp, idno ) )
			updateComment += 'STAMP END: ' + idno + "<br>"

		if stamp == 'move' :
		
			new_date = date
			
			cursor2.execute("select idno, day from days where date='%s' " % ( new_date ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				row = cursor2.fetchone()
				days_idno = row[0]
				days_day = row[1]
			
			else :

				days_idno = 0
				days_day = 'None'


			cursor7.execute("select itemtime, itemtitle, itemtext, type, contact1, endtime, assigned1, assigned2, contact2, location, location2, location3 from items where idno='%s'" % ( idno ) )
			numrows7 = cursor7.rowcount

			updateComment += 'STAMP MOVE: ' + idno + "<br>"
			
			if numrows7 == 1 :
			
				result7 = cursor7.fetchone()
				
				oldstart = str( result7[0] )
				oldstart = oldstart[11:16]
				
				oldend= str( result7[5] )
				oldend = oldend[11:16]

				itemtime3 = new_date + ' ' + oldstart
				new_endtime3 = new_date + ' ' + oldend
						
				cursor4.execute("update items set date = '%s', dayidno = %s, day = '%s', itemtime = '%s', endtime = '%s' where idno = '%s'" \
				% ( new_date, days_idno, days_day, itemtime3, new_endtime3, idno ) )

	#maintext = ''


#	endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', \
#	location = '%s', assigned1 = '%s', dcassist = '%s', location2 = '%s', location3 = '%s', completion = '%s', contact2 = '%s', others = '%s', master

# Main Read of Items

	cmd = "select idno, dayidno, date, day, itemtime, itemtitle, itemtext, user, type, downtime, subsystem, status, timestamp, history, logcrew, \
	endtime, realstart, realend, niteeffect, dayeffect, location, assigned1, dcassist, location2, location3, comptitle, contact2, others, master, \
	assigned2, notify, comptext, contact1, otherreq, seats, seats2, residno, residno2, residno3, residno4, residno5, residno6, pass, rpass, pseats \
	from items where idno = '%s'" % ( idno )
	
#	maintext += 'query: '+ cmd + ' <br> ' + method

	cursor.execute( cmd  )

#	cursor.execute("select idno, dayidno, date, day, itemtime, itemtitle, itemtext, \
#	user, type, downtime, subsystem, status, timestamp, history, logcrew from items where idno = '%s'" % ( idno ) )

	numrows = cursor.rowcount
	
#	numrows = 0

	pagename = '<center><b>Summit WorkPlan</b><br><FONT SIZE=2>[ ' + username  + ' expires: ' + end + ' ]<FONT SIZE=3><br><br>'

#	pagename = ''
	
	maintext = pagename

#	maintext += 'rows: ' + str( numrows ) + '<br>'
	
	#maintext += "<form method=post action='./logone.py?'>"

	# outside frame
#	maintext += '<table><tr><th>Reports<hr></th><th>Status<hr></th></tr></table>'

	# left column
	#maintext += '<tr><td valign=top>'

#	if numrows == 0 :


	if numrows == 1 :

		row = cursor.fetchone()

		item_idno = row[0]
		item_dayidno = row[1]


		item_date = row[2]
		item_day = row[3]

		item_time = row[4]


		item_time2 = str( item_time )
		item_time2 = item_time2[0:16]
		item_hourin = item_time2[11:13]
		
		startdate = item_time2[0:10]
		starttime = item_time2[11:16]
		start_display = item_time2[5:16]

		item_title = row[5]
		item_text = row[6]

		item_user = row[7]
		item_user = item_user.strip()

		item_type = row[8]

		item_downtime = row[9]
		
		item_subsystem = row[10]

		item_status = row[11]

		item_timestamp = row[12]

		item_history = row[13]

		item_logcrew = row[14]

		item_endtime = row[15]
		item_endtime2 = str( item_endtime )
		item_endtime2 = item_endtime2[0:16]
		
		item_hourout = item_endtime2[11:13]
		
		enddate = item_endtime2[0:10]
		endtime = item_endtime2[11:16]
		end_display = item_endtime2[5:16]
		
		item_realstart = row[16]
		item_realstart2 = str( item_realstart )
		item_realstart2 = item_realstart2[0:16]

		item_realend = row[17]
		item_realend2 = str( item_realend )
		item_realend2 = item_realend2[0:16]

		item_niteeffect = row[18]

		item_dayeffect = row[19]

		item_location = row[20]

		item_assigned1 = row[21]
		item_assigned1 = item_assigned1.strip()

		item_dcassist = row[22]

		item_location2 = row[23]

		item_location3 = row[24]

		item_completion = row[25]
		
		item_contact2 = row[26]

		item_others = row[27]

		item_master = row[28]
		
		item_assigned2 = row[29]
		
		item_assigned2 = item_assigned2.strip()
		
		if item_assigned2 == '.none' or item_assigned2 == 'None' :

			item_assigned2 = ''

		item_notify = row[30]

		item_comptext = row[31]
		
		item_contact1 = row[32]
		
		item_otherreq = row[33]

#		item_seats = str( row[34] )

#		item_seats2 = str( row[35] )

# keep seats and setas2 as numerics

		item_seats = row[34]

		item_seats2 = row[35]
		
		item_residno = row[36]
		
		item_residno2 = row[37]
		
		item_residno3 = row[38]

		item_residno4 = row[39]
		
		item_residno5 = row[40]
		
		item_residno6 = row[41]

		item_pass = row[42]
		
		item_rpass = row[43]
		
		item_pseats = row[44]
		

#		residno_car = 'None'
#		residno2_car = 'None'
#		residno3_car = 'None'

		residno_car = ''
		residno_driver = ''
		residno_rdriver = ''
		residno_pass = ''
		residno_rpass = ''
		residno_monitor = ''
		
		residno2_car = ''
		residno2_driver = ''
		residno2_rdriver = ''
		residno2_pass = ''
		residno2_rpass = ''
		residno2_monitor = ''

		residno3_car = ''
		residno3_driver = ''
		residno3_rdriver = ''
		residno3_pass = ''
		residno3_rpass = ''
		residno3_monitor = ''

		residno4_car = ''
		residno4_driver = ''
		residno4_rdriver = ''
		residno4_pass = ''
		residno4_rpass = ''
		residno4_monitor = ''

		residno5_car = ''
		residno5_driver = ''
		residno5_rdriver = ''
		residno5_pass = ''
		residno5_rpass = ''
		residno5_monitor = ''

		residno6_car = ''
		residno6_driver = ''
		residno6_rdriver = ''
		residno6_pass = ''
		residno6_rpass = ''
		residno6_monitor = ''
		
		residno7_car = ''
		residno7_driver = ''
		residno7_rdriver = ''
		residno7_pass = ''
		residno7_rpass = ''
		residno7_monitor = ''


		
		rescars=[]
		passcars=[]
		
		qseq = 0
		
		if item_residno > 0 :
			
			qseq += 1
		
	
			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( item_residno ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno_car = raw[0]
				residno_driver = raw[1]
				residno_rdriver = raw[2]
				residno_pass = raw[3]
				residno_rpass = raw[4]
				residno_monitor = raw[5]

				residno_date = str( raw[6] )
				residno_datein = str( raw[7] )
				residno_dateout = str( raw[8] )
			
				rescars.append ( residno_car )

		if item_residno2 > 0 :

			qseq += 1
			
			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( item_residno2 ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno2_car = raw[0]
				residno2_driver = raw[1]
				residno2_rdriver = raw[2]
			
				residno2_pass = raw[3]
				residno2_rpass = raw[4]
				residno2_monitor = raw[5]

				residno2_date = str( raw[6] )
				residno2_datein = str( raw[7] )
				residno2_dateout = str( raw[8] )

#				rescars.append ( residno2_car )
				passcars.append ( residno2_car )
			
		if item_residno3 > 0 :

			qseq += 1
		
			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( item_residno3 ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno3_car = raw[0]
				residno3_driver = raw[1]
				residno3_rdriver = raw[2]
				residno3_pass = raw[3]
				residno3_rpass = raw[4]
				residno3_monitor = raw[5]

				residno3_date = str( raw[6] )
				residno3_datein = str( raw[7] )
				residno3_dateout = str( raw[8] )

#				rescars.append ( residno3_car )
				passcars.append ( residno3_car )


		if item_residno4 > 0 :
			
			qseq += 1


			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( item_residno4 ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno4_car = raw[0]
				residno4_driver = raw[1]
				residno4_rdriver = raw[2]
				residno4_pass = raw[3]
				residno4_rpass = raw[4]
				residno4_monitor = raw[5]

				residno4_date = str( raw[6] )
				residno4_datein = str( raw[7] )
				residno4_dateout = str( raw[8] )

				rescars.append ( residno4_car )

		if item_residno5 > 0 :

			qseq += 1

			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( item_residno5 ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno5_car = raw[0]
				residno5_driver = raw[1]
				residno5_rdriver = raw[2]
				residno5_pass = raw[3]
				residno5_rpass = raw[4]
				residno5_monitor = raw[5]

				residno5_date = str( raw[6] )
				residno5_datein = str( raw[7] )
				residno5_dateout = str( raw[8] )

				rescars.append ( residno5_car )

		if item_residno6 > 0 :

			qseq += 1

			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( item_residno6 ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno6_car = raw[0]
				residno6_driver = raw[1]
				residno6_rdriver = raw[2]
				residno6_pass = raw[3]
				residno6_rpass = raw[4]
				residno6_monitor = raw[5]

				residno6_date = str( raw[6] )
				residno6_datein = str( raw[7] )
				residno6_dateout = str( raw[8] )

				rescars.append ( residno6_car )

		if qseq == 0  and int( rid ) > 0 :

			cursor4.execute("select car, driver, rdriver, pass, rpass, monitor, date, datein, dateout from res where idno='%s' " % ( rid ) )
			numrows4=cursor4.rowcount
			if numrows4 == 1 :

				raw=cursor4.fetchone()

				residno7_car = raw[0]
				residno7_driver = raw[1]
				residno7_rdriver = raw[2]
				residno7_pass = raw[3]
				residno7_rpass = raw[4]
				residno7_monitor = raw[5]

				residno7_date = str( raw[6] )
				residno7_datein = str( raw[7] )
				residno7_dateout = str( raw[8] )
	
				rescars.append ( residno_car )


		residno_car = residno_car.strip()
		residno_driver = residno_driver.strip()
		residno_rdriver = residno_rdriver.strip()
		residno_pass = residno_pass.strip()
		residno_rpass = residno_rpass.strip()
		residno_monitor = residno_monitor.strip()

		if residno_pass == 'None':
			residno_pass = ''
		if residno_rpass == 'None':
			residno_rpass = ''
		if residno_monitor == 'None':
			residno_monitor = ''

		residno2_car = residno2_car.strip()
		residno2_driver = residno2_driver.strip()
		residno2_rdriver = residno2_rdriver.strip()
		residno2_pass = residno2_pass.strip()
		residno2_rpass = residno2_rpass.strip()
		residno2_monitor = residno2_monitor.strip()

		if residno2_pass == 'None':
			residno2_pass = ''
		if residno2_rpass == 'None':
			residno2_rpass = ''
		if residno2_monitor == 'None':
			residno2_monitor = ''

		residno3_car = residno3_car.strip()
		residno3_driver = residno3_driver.strip()
		residno3_rdriver = residno3_rdriver.strip()
		residno3_pass = residno3_pass.strip()
		residno3_rpass = residno3_rpass.strip()
		residno3_monitor = residno3_monitor.strip()


		if residno3_pass == 'None':
			residno3_pass = ''
		if residno3_rpass == 'None':
			residno3_rpass = ''
		if residno3_monitor == 'None':
			residno3_monitor = ''

		residno4_car = residno4_car.strip()
		residno4_driver = residno4_driver.strip()
		residno4_rdriver = residno4_rdriver.strip()
		residno4_pass = residno4_pass.strip()
		residno4_rpass = residno4_rpass.strip()
		residno4_monitor = residno4_monitor.strip()

		if residno4_pass == 'None':
			residno4_pass = ''
		if residno4_rpass == 'None':
			residno4_rpass = ''
		if residno4_monitor == 'None':
			residno4_monitor = ''

		residno5_car = residno5_car.strip()
		residno5_driver = residno5_driver.strip()
		residno5_rdriver = residno5_rdriver.strip()
		residno5_pass = residno5_pass.strip()
		residno5_rpass = residno5_rpass.strip()
		residno5_monitor = residno5_monitor.strip()

		if residno5_pass == 'None':
			residno5_pass = ''
		if residno5_rpass == 'None':
			residno5_rpass = ''
		if residno5_monitor == 'None':
			residno5_monitor = ''

		residno6_car = residno6_car.strip()
		residno6_driver = residno6_driver.strip()
		residno6_rdriver = residno6_rdriver.strip()
		residno6_pass = residno6_pass.strip()
		residno6_rpass = residno6_rpass.strip()
		residno6_monitor = residno6_monitor.strip()

		if residno6_pass == 'None':
			residno6_pass = ''
		if residno6_rpass == 'None':
			residno6_rpass = ''
		if residno6_monitor == 'None':
			residno6_monitor = ''

		residno7_car = residno7_car.strip()
		residno7_driver = residno7_driver.strip()
		residno7_rdriver = residno7_rdriver.strip()
		residno7_pass = residno7_pass.strip()
		residno7_rpass = residno7_rpass.strip()
		residno7_monitor = residno7_monitor.strip()

		if residno7_pass == 'None':
			residno7_pass = ''
			
		if residno7_rpass == 'None':
			residno7_rpass = ''
			
		if residno7_monitor == 'None':
			residno7_monitor = ''
		
		rescount = 0
		passcount = 0
		
		if item_residno2 > 0 :
		
			passcount += 1
		
		if item_residno3 > 0 :
			
			passcount += 1
			
	
		if item_residno > 0 :
		
			rescount += 1
		
		if item_residno4 > 0 :
			
			rescount += 1
		
		if item_residno5 > 0 :
			
			rescount += 1
		
		if item_residno6 > 0 :
			
			rescount += 1
			
		balcount = 4 - rescount 

	# items query

	# crew section

	#	if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter' ) ) : 
	#	if  method == 'POST' and field['action'].value == 'Save'  : 
	
# show display
		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' or field['action'].value == 'SaveRes' ) ) :
		
		
# plan requirements

			cursor4.execute("select code from itemreqs where planidno='%s'" % ( idno ) )

			numrows4 = cursor4.rowcount

			planreqs = []

			for result4 in cursor4.fetchall() :

				planreqs.append ( result4[0] )


			cursor3.execute("select text from refer where code='%s' order by seq" % ( 'PLANREQ' ) )

			numrows3 = cursor3.rowcount

			planreqs2 = '<table>'

			for result3 in cursor3.fetchall() :

				refer_lock=result3[0]

				if refer_lock in planreqs :

					planreqs2 += "<tr><td bgcolor=lime><input type=checkbox name=%s value=%s checked> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )
				else:

					planreqs2 += "<tr><td><input type=checkbox name=%s value=%s> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )

			planreqs2 += '</table>'



# plan lockouts
			cursor5.execute("select code from itemreqs where planidno='%s'" % ( idno ) )

			numrows5 = cursor5.rowcount

			planlocks = []

			for result5 in cursor5.fetchall() :

				planlocks.append ( result5[0] )

			cursor3.execute("select text from refer where code='%s' order by seq" % ( 'PLANLOCK' ) )

			numrows3 = cursor3.rowcount

			planlocks2 = '<table>'

			for result3 in cursor3.fetchall() :

				refer_lock=result3[0]

				if refer_lock in planlocks :

					planlocks2 += "<tr><td bgcolor=pink><input type=checkbox name='%s' value='%s' checked> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )
				else :

					planlocks2 += "<tr><td><input type=checkbox name='%s' value='%s'> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )

			planlocks2 += '</table>'


			formtxt = "<center><a href=logone.py?date=%s&logcrew=WP>return to WPs<br>%s</a></center>" % ( startdate, startdate )
			formtxt += "<br><form method=post action=./planone.py?idno=%s><input type=submit name=action value='Edit'></form>"  % ( idno )
			formtxt += "<br>Update Comment:<br>"
			formtxt += updateComment
			formtxt += "<br>"

			if username == 'winegar': 
			
#			if item_user == username or item_user == user_contact1 or item_assigned1 == username or item_assigned1 == user_contact1 or username == 'winegar' :			 
		
				formtxt += "<form method=post action=./planmove.py?idno=%s><input type=submit name=action value='Move'></form>" % ( idno )			
			
			formtxt += "<br>"
# <input type=submit name=action value='Move'>

			itemtable = '<table><td valign=top>'

			itemtable += '<center><b>Requested</b></center><hr><table>'
			itemtable += "<tr><td class=right><b>Requestor:</b></td><td><FONT SIZE=4>%s [ %s ]</td></tr>" % ( item_user, item_contact1 )
			itemtable += "<tr><td class=right>Contact2:</td><td><FONT SIZE=4>%s | Others: %s</td></tr>" % ( item_contact2, item_others )
#				itemtable += "<tr><td class=right>Others:</td><td><input type=text size=30 value='%s' name='others'></td></tr>" % ( item_others )

#				itemtable += "<tr><td class=right>Status:</td><td><input type=text size=20 value='%s' name='status'> | Type: <input type=text size=20 value='%s' name='type'></td></tr>" % ( item_status, item_type )
			itemtable += "<tr><td class=right>Status:</td><td><FONT SIZE=4><b>%s</b> | <FONT SIZE=2>Type: <FONT SIZE=4>%s | <FONT SIZE=2>Subsystem: <FONT SIZE=4>%s</td></tr>" % ( item_status, item_type, item_subsystem )

#			itemtable += "<tr><td class=right>StartTime:</a></td><td>%s End:</a> %s</td></tr>" % ( item_time, item_endtime )
			itemtable += "<tr><td class=right>StartTime:</a></td><td><FONT SIZE=4><b>%s</b> <FONT SIZE=2>End:</a> <FONT SIZE=4><b>%s</b></td></tr>" % ( start_display, end_display )
#				itemtable += "<tr><td class=right>EndTime</td><td><input type=text size=20 value='%s' name='endtime'></td></tr>" % ( str( item_endtime ) )

			itemtable += '<tr><td class=right colspan=2><hr></td></tr>'
			itemtable += "<tr><td class=right>Plan Title:</td><td><FONT SIZE=4><b>%s</b></td></tr>" % ( item_title )
			itemtable += "<tr><td class=right valign=top>Plan Text:</td><td>%s</td></tr>" % ( item_text )
#				itemtable += "<tr><td class=right>Text</td><td><input type=text size=50 value='%s' name='itemtext'></td></tr>" % ( item_text )
#				itemtable += "<tr><td class=right>Type</td><td><input type=text size=20 value='%s' name='type'></td></tr>" % ( item_type )
#				itemtable += "<tr><td class=right>Location1:</td><td>%s | 2: %s | 3: %s</td></tr>" % ( locations1, locations2, locations3 )
#				itemtable += "<tr><td class=right>Location1</td><td><input type=text size=20 value='%s' name='location'></td></tr>" % ( item_location )
#				itemtable += "<tr><td class=right>Location2</td><td><input type=text size=20 value='%s' name='location2'></td></tr>" % ( item_location2 )
#				itemtable += "<tr><td class=right>Location3</td><td><input type=text size=20 value='%s' name='location3'></td></tr>" % ( item_location3 )
			itemtable += '<tr><td class=right colspan=2><hr></td></tr>'
#			itemtable += "<tr><td class=right>Downtime:</td><td>%s</td></tr>" % ( item_downtime ) 
#			itemtable += "<tr><td class=right>Subsystem:</td><td>%s</td></tr>" % ( item_subsystem )
			itemtable += "<tr><td class=right>Locations:</td><td>%s | 2: %s | 3: %s</td></tr>" % ( item_location, item_location2, item_location3 )
			itemtable += "<tr><td class=right>Day Warning:</td><td>%s</td></tr>" % ( item_dayeffect )
			itemtable += "<tr><td class=right>Nite Warning:</td><td>%s</td></tr>" % ( item_niteeffect )
#			itemtable += "<tr><td colspan=2>ResIDNo 1-6: %s %s %s %s %s %s</td></tr>" % ( item_residno, item_residno2, item_residno3, item_residno4, item_residno5, item_residno6  )
#			itemtable += "<tr><td class=center colspan=2 valign=top>Cars Reserves for %s</td></tr>" % ( item_date )
			itemtable += "<tr><td class=right colspan=2><hr></td></tr>"
			
			if username in wg_users :
				
				itemtable += "<tr><td class=center colspan=2 valign=top><b>Drivers:</b> | %s | %s | %s | %s | <b>Pass:</b> | %s | %s | Reserves: %s</td></tr>" % (  item_residno, item_residno4, item_residno5, item_residno6, item_residno2, item_residno3, rescount )

				itemtable += "<tr><td class=center colspan=2 valign=top><FONT SIZE=+1>Cars Schedule for %s</FONT><br>" % ( item_date )
			
# Car Summary Start

			carsum = '<center><table cellpadding=3 cellspacing=3><tr><th bgcolor=lime>#</th><th bgcolor=lime>Cars</th><th bgcolor=lime>InOut</th>' 
			carsum += '<th bgcolor=lime>Driver</th><th bgcolor=lime>Passengers</th><th bgcolor=lime>Ret-Passengers</th><th bgcolor=lime>Monitor</th></tr>'

			seq = 0
			
			if item_residno > 0 :

				inout = residno_datein[5:13] + '-' + residno_dateout[11:13]
			
				seq += 1
#				itemtable += "<b>Driver: %s</b> #%s " % ( residno_car, item_residno )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, residno_car,  residno_driver, residno_pass, residno_rpass, residno_monitor )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, '',  '', '', '', '' )
				if int( rid ) == item_residno and method == 'GET':
				
#					carsum += "<form method='POST' action=./planone2.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
#					carsum += "<input type=hidden name=residno size=10 value=%s></td></tr>" % ( item_residno )
					
#					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='%s'></td></tr>" \
#					% ( seq, residno_car, residno_driver )
					
					cursor3.execute("select user, train from users where status='Active' order by user")
	
					numrows3 = cursor3.rowcount

					residnoSpin = '<select name=driver size=1>'
					residnoRSpin = '<select name=rdriver size=1>'
	
					for result3 in cursor3.fetchall() :
		
						user_text = result3[0]
						user_train = result3[1]
						
						user_text2 = user_text
						
						if user_train != 'D' :
												
							user_text2 += ' (NoSum)'
	
						if residno_driver == user_text :
													
							residnoSpin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
							
						else:
									
							residnoSpin += "<option value='%s'>%s" % ( user_text, user_text2 )
							
#							residno4Spin += "<option value='%s'>%s" % ( user_text, user_text )
						if residno_rdriver == user_text :

	
							residnoRSpin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
	
						else:


							residnoRSpin += "<option value='%s'>%s" % ( user_text, user_text2 )
							

					residnoSpin += '</select>'

					residnoRSpin += '</select>'
				
				
					carsum += "<form method='POST' action=./planone.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
					carsum += "<input type=hidden name=rid size=10 value=%s></td></tr>" % ( item_residno )
					
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Driver: </td>" % ( seq, residno_car )
					
#					carsum += "<td colspan=4><input type=text name=driver size=20 value='%s'></td>" % ( residno4_driver )

					carsum += "<td colspan=4>%s | %s</td>" % ( residnoSpin, residnoRSpin )

					carsum += "</tr>"


#					carsum += "<tr><td>1</td><td>1</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='TOM'></td></tr>" 

					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Passenger: </td><td colspan=3><input type=text name=pass1 size=40 maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno_car, residno_pass )
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Ret-Passenger: </td><td colspan=3><input type=text name=rpass1 size=40  maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno_car, residno_rpass )
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Monitor: </td><td colspan=3><input type=text name=monitor size=20  maxsize=80 value='%s'></td></tr> " \
					% ( seq, residno_car, residno_monitor )
					carsum += "<td colspan=7><input type=submit name=action value='SaveRes'> <input type=submit name=action value='Cancel'></td></tr>" 

					carsum += "</form>"

				else:
				
					carsum += "<tr><td>%s</td><td><a href=planone.py?idno=%s&rid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
					% ( seq, item_idno, item_residno, residno_car, inout, residno_driver, residno_pass, residno_rpass, residno_monitor  )
#					carsum += "<tr><td colspan=7>TOM</td></tr>"

#			else:
#				itemtable += "Driver: %s #%s " % ( residno_car, item_residno )
#				carsum += "<tr><td bgcolor=pink><b>1:</b> %s #%s</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>" % ( residno_car, item_residno )


			if item_residno4 > 0 :

				inout = residno4_datein[5:13] + '-' + residno4_dateout[11:13]
			
				seq += 1
#				itemtable += "<b>Driver: %s</b> #%s " % ( residno_car, item_residno )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, residno_car,  residno_driver, residno_pass, residno_rpass, residno_monitor )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, '',  '', '', '', '' )
				if int( rid ) == item_residno4 and method == 'GET':
				# Assigned1				
					cursor3.execute("select user, train from users where status='Active' order by user")
	
					numrows3 = cursor3.rowcount

					residno4Spin = '<select name=driver size=1>'
					residno4RSpin = '<select name=rdriver size=1>'
	
					for result3 in cursor3.fetchall() :
		
						user_text = result3[0]
						user_train = result3[1]
						user_text2 = user_text
						
						if user_train != 'D' :
												
							user_text2 += ' (NoSum)'
	
						if residno4_driver == user_text :
						
							residno4Spin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
							
						else:
						
							residno4Spin += "<option value='%s'>%s" % ( user_text, user_text2 )
							

						if residno4_rdriver == user_text :


							residno4RSpin += "<option value='%s' selected>%s" % ( user_text, user_text2 )

						else:


							residno4RSpin += "<option value='%s'>%s" % ( user_text, user_text2 )
							

#							residno4Spin += "<option value='%s'>%s" % ( user_text, user_text )
							

					residno4Spin += '</select>'
					residno4RSpin += '</select>'
				
				
					carsum += "<form method='POST' action=./planone.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
					carsum += "<input type=hidden name=rid size=10 value=%s></td></tr>" % ( item_residno4 )
					
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Driver: </td>" % ( seq, residno4_car )
					
#					carsum += "<td colspan=4><input type=text name=driver size=20 value='%s'></td>" % ( residno4_driver )

					carsum += "<td colspan=4>%s | %s</td>" % ( residno4Spin, residno4RSpin )
					
					carsum += "</tr>"
					

#					carsum += "<tr><td>1</td><td>1</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='TOM'></td></tr>" 

					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Passenger: </td><td colspan=3><input type=text name=pass1 size=40 maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno4_car, residno4_pass )
					
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Ret-Passenger: </td><td colspan=3><input type=text name=rpass1 size=40 maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno4_car, residno4_rpass )
					
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Monitor: </td><td colspan=3><input type=text name=monitor size=20  maxsize=80 value='%s'></td></tr> " \
					% ( seq, residno4_car, residno4_monitor )
					
					carsum += "<td colspan=7><input type=submit name=action value='SaveRes'> <input type=submit name=action value='Cancel'></td></tr>" 

					carsum += "</form>"

				else:
				
					carsum += "<tr><td>%s</td><td><a href=planone.py?idno=%s&rid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
					% ( seq, item_idno, item_residno4, residno4_car, inout, residno4_driver, residno4_pass, residno4_rpass, residno4_monitor  )
#
			if item_residno5 > 0 :

				inout = residno5_datein[5:13] + '-' + residno5_dateout[11:13]
			
				seq += 1
#				itemtable += "<b>Driver: %s</b> #%s " % ( residno_car, item_residno )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, residno_car,  residno_driver, residno_pass, residno_rpass, residno_monitor )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, '',  '', '', '', '' )
				if int( rid ) == item_residno5 and method == 'GET':
				
#					carsum += "<form method='POST' action=./planone2.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
#					carsum += "<input type=hidden name=residno size=10 value=%s></td></tr>" % ( item_residno5 )
					
#					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='%s'></td></tr>" \
#					% ( seq, residno5_car, residno5_driver )


					cursor3.execute("select user, train from users where status='Active' order by user")
	
					numrows3 = cursor3.rowcount

					residno5Spin = '<select name=driver size=1>'
					residno5RSpin = '<select name=rdriver size=1>'
	
					for result3 in cursor3.fetchall() :
		
						user_text = result3[0]
						user_train = result3[1]
						user_text2 = user_text
						
						if user_train != 'D' :
												
							user_text2 += ' (NoSum)'
	
						if residno5_driver == user_text :
													
							residno5Spin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
							
						else:
			
						
							residno5Spin += "<option value='%s'>%s" % ( user_text, user_text2 )

						if residno5_rdriver == user_text :
												
							residno5RSpin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
						
						else:
		
					
							residno5RSpin += "<option value='%s'>%s" % ( user_text, user_text2 )
							
#							residno4Spin += "<option value='%s'>%s" % ( user_text, user_text )
							

					residno5Spin += '</select>'
					residno5RSpin += '</select>'
				
				
					carsum += "<form method='POST' action=./planone.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
					carsum += "<input type=hidden name=rid size=10 value=%s></td></tr>" % ( item_residno5 )
					
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Driver: </td>" % ( seq, residno5_car )
					
#					carsum += "<td colspan=4><input type=text name=driver size=20 value='%s'></td>" % ( residno4_driver )

					carsum += "<td colspan=4>%s | %s</td>" % ( residno5Spin, residno5RSpin )
					
					carsum += "</tr>"

#					carsum += "<tr><td>1</td><td>1</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='TOM'></td></tr>" 

					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Passenger: </td><td colspan=3><input type=text name=pass1 size=40 maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno5_car, residno5_pass )
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Ret-Passenger: </td><td colspan=3><input type=text name=rpass1 size=40  maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno5_car, residno5_rpass )
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Monitor: </td><td colspan=3><input type=text name=monitor size=20  maxsize=80 value='%s'></td></tr> " \
					% ( seq, residno5_car, residno5_monitor )
					carsum += "<td colspan=7><input type=submit name=action value='SaveRes'> <input type=submit name=action value='Cancel'></td></tr>" 

					carsum += "</form>"

				else:
				
					carsum += "<tr><td>%s</td><td><a href=planone.py?idno=%s&rid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
					% ( seq, item_idno, item_residno5, residno5_car, inout, residno5_driver, residno5_pass, residno5_rpass, residno5_monitor  )

			if item_residno6 > 0 :

				inout = residno6_datein[5:13] + '-' + residno6_dateout[11:13]
	
				seq += 1
#				itemtable += "<b>Driver: %s</b> #%s " % ( residno_car, item_residno )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, residno_car,  residno_driver, residno_pass, residno_rpass, residno_monitor )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, '',  '', '', '', '' )
				if int( rid ) == item_residno6 and method == 'GET':
		
#					carsum += "<form method='POST' action=./planone2.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
#W					carsum += "<input type=hidden name=residno size=10 value=%s></td></tr>" % ( item_residno6 )
			
#					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='%s'></td></tr>" \
#					% ( seq, residno6_car, residno6_driver )
					
					cursor3.execute("select user, train from users where status='Active' order by user")
	
					numrows3 = cursor3.rowcount

					residno6Spin = '<select name=driver size=1>'
					residno6RSpin = '<select name=rdriver size=1>'
	
					for result3 in cursor3.fetchall() :
		
						user_text = result3[0]
						user_train = result3[1]
#						user_train = result3[1]
						user_text2 = user_text
						
						if user_train != 'D' :
												
							user_text2 += ' (NoSum)'
	
						if residno6_driver == user_text :
						
							residno6Spin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
							
						else:
			
							residno6Spin += "<option value='%s'>%s" % ( user_text, user_text2 )
							

						if residno6_rdriver == user_text :
					
							residno6RSpin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
						
						else:
		
							residno6RSpin += "<option value='%s'>%s" % ( user_text, user_text2 )
#							residno4Spin += "<option value='%s'>%s" % ( user_text, user_text )
							
					residno6Spin += '</select>'
					residno6RSpin += '</select>'
				
				
					carsum += "<form method='POST' action=./planone.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
					carsum += "<input type=hidden name=rid size=10 value=%s></td></tr>" % ( item_residno6 )
					
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Driver: </td>" % ( seq, residno6_car )
					
#					carsum += "<td colspan=4><input type=text name=driver size=20 value='%s'></td>" % ( residno4_driver )


					carsum += "<td colspan=4>%s | %s</td>" % ( residno6Spin, residno6RSpin )

					carsum += "</tr>"
					
#					carsum += "<tr><td>1</td><td>1</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='TOM'></td></tr>" 

					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Passenger: </td><td colspan=3><input type=text name=pass1 size=40 maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno6_car, residno6_pass )
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Ret-Passenger: </td><td colspan=3><input type=text name=rpass1 size=40  maxsize=80 value='%s'></td></tr>" \
					% ( seq, residno6_car, residno6_rpass )
					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Monitor: </td><td colspan=3><input type=text name=monitor size=20  maxsize=80 value='%s'></td></tr> " \
					% ( seq, residno6_car, residno6_monitor )
					carsum += "<td colspan=7><input type=submit name=action value='SaveRes'> <input type=submit name=action value='Cancel'></td></tr>" 

					carsum += "</form>"

				else:
		
					carsum += "<tr><td>%s</td><td><a href=planone.py?idno=%s&rid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
					% ( seq, item_idno, item_residno6, residno6_car, inout, residno6_driver, residno6_pass, residno6_rpass, residno6_monitor  )



			if item_residno2 > 0 :
#				itemtable += "<b>PassUp: %s</b> #%s " % ( residno2_car, item_residno2 ) 

				inout2 = residno2_datein[5:13] + '-' + residno2_dateout[11:13]

				seq += 1

				carsum += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
				% ( seq, residno2_car, inout2, residno2_driver, residno2_pass, residno2_rpass, residno2_monitor  )

#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno2_idno, residno2_car,  residno2_driver, residno2_pass, residno2_rpass, residno2_monitor )
		
#			else :
#				itemtable += "PassUp: %s #%s " % ( residno2_car, item_residno2 ) 
#				carsum += "<tr><td><b>2</b> %s #%s</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>" % ( residno2_car, item_residno2 )

			if item_residno3 > 0 :
#				itemtable += "<b>PassReturn: %s</b> #%s<br>"  % ( residno3_car, item_residno3 )
#				carsum += "<tr><td bgcolor=lime><b>Passengers Return:</b> <b>%s</b> #%s</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>" % ( residno3_car, item_residno3 )
				inout3 = residno3_datein[5:13] + '-' + residno3_dateout[11:13]

				seq += 1

				carsum += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
				% ( seq, residno3_car, inout3, residno3_driver, residno3_pass, residno3_rpass, residno3_monitor  )

#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno3_idno, residno3_car,  residno3_driver, residno3_pass, residno3_rpass, residno3_monitor )
			if seq == 0 and int( rid ) > 0 and method == 'GET':
						
			
				inout = residno7_datein[5:13] + '-' + residno7_dateout[11:13]
			
				seq += 1
#				itemtable += "<b>Driver: %s</b> #%s " % ( residno_car, item_residno )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, residno_car,  residno_driver, residno_pass, residno_rpass, residno_monitor )
#				carsum += "<tr><td>%s</td><td bgcolor=lime><a href=planone2.py?idno=%s&residno=%s><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#				% ( seq, item_idno, residno_idno, '',  '', '', '', '' )
#				if int( rid ) == item_residno7 and method == 'GET':
				
#					carsum += "<form method='POST' action=./planone2.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
#					carsum += "<input type=hidden name=residno size=10 value=%s></td></tr>" % ( item_residno5 )
					
#					carsum += "<tr><td>%s</td><td>%s</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='%s'></td></tr>" \
#					% ( seq, residno5_car, residno5_driver )


				cursor3.execute("select user, train from users where status='Active' order by user")

				numrows3 = cursor3.rowcount

				residno7Spin = '<select name=driver size=1>'
				residno7RSpin = '<select name=rdriver size=1>'

				for result3 in cursor3.fetchall() :
	
					user_text = result3[0]
					user_train = result3[1]
					user_text2 = user_text
					
					if user_train != 'D' :
											
						user_text2 += ' (NoSum)'

					if residno7_driver == user_text :
												
						residno7Spin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
						
					else:
		
					
						residno7Spin += "<option value='%s'>%s" % ( user_text, user_text2 )

					if residno7_rdriver == user_text :
											
						residno7RSpin += "<option value='%s' selected>%s" % ( user_text, user_text2 )
					
					else:
	
				
						residno7RSpin += "<option value='%s'>%s" % ( user_text, user_text2 )
						
#							residno4Spin += "<option value='%s'>%s" % ( user_text, user_text )
						

				residno7Spin += '</select>'
				residno7RSpin += '</select>'
			
			
				carsum += "<form method='POST' action=./planone.py?idno=%s>" % ( item_idno )
#					carsum += "<input type=hidden name=idno size=10 value=%s></td></tr>" % ( item_idno )
				carsum += "<input type=hidden name=rid size=10 value=%s></td></tr>" % ( rid )
				
				carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Driver: </td>" % ( seq, residno7_car )
				
#					carsum += "<td colspan=4><input type=text name=driver size=20 value='%s'></td>" % ( residno4_driver )

				carsum += "<td colspan=4>%s | %s</td>" % ( residno7Spin, residno7RSpin )
				
				carsum += "</tr>"

#					carsum += "<tr><td>1</td><td>1</td><td colspan=2>Driver: </td><td colspan=4><input type=text name=driver size=20 value='TOM'></td></tr>" 

				carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Passenger: </td><td colspan=3><input type=text name=pass1 size=40 maxsize=80 value='%s'></td></tr>" \
				% ( seq, residno7_car, residno7_pass )
				carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Ret-Passenger: </td><td colspan=3><input type=text name=rpass1 size=40  maxsize=80 value='%s'></td></tr>" \
				% ( seq, residno7_car, residno7_rpass )
				carsum += "<tr><td>%s</td><td>%s</td><td colspan=2 bgcolor=lime>Monitor: </td><td colspan=3><input type=text name=monitor size=20  maxsize=80 value='%s'></td></tr> " \
				% ( seq, residno7_car, residno7_monitor )
				carsum += "<td colspan=7><input type=submit name=action value='SaveRes'> <input type=submit name=action value='Cancel'></td></tr>" 

				carsum += "</form>"

# Remove for Residno7 - Hidden inside Table
#				else:
				
#					carsum += "<tr><td>%s</td><td><a href=planone2.py?idno=%s&rid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#					% ( seq, item_idno, item_residno5, residno5_car, inout, residno5_driver, residno5_pass, residno5_rpass, residno5_monitor  )
			
#			else :
#				itemtable += "PassReturn: %s #%s<br>"  % ( residno3_car, item_residno3 )
#				carsum += "<tr><td><b>3:</b> %s #%s</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>" % ( residno3_car, item_residno3 )
			
			carsum += "</table></center>"

# Car Summary Ending

#			itemtable += carsum
			itemtable_display = False
#			itemtable_display = True

			carstable = ""
#			carstable += "<tr><td class=center colspan=2 valign=top>Cars Daily Schedule for %s<br>" % ( item_date )
			
			if itemtable_display == True :
				
				carstable += "<table rules=2 border=all cellpadding=2 cellspacing=2>"

				carstable += "<tr>"

				carslist = ( 'J-01', 'J-02', 'J-03', 'J-04', 'J-05', 'J-06', 'J-07', 'J-08', 'J-09', 'J-10', 'J-11', 'J-12', 'J-13', 'J-14', 'J-15', 'BSIT', )
#				carslist = ( 'J-01', 'J-02', 'J-03', 'J-06', 'J-07', 'J-08', 'J-09', 'J-10', 'J-11', 'J-12', 'J-13', 'J-14', 'J-15', 'BSIT', )
				badcarslist = ( 'J-04', 'J-05' )
				
				for car in carslist :

					totalseats = 4
					
					cursor9.execute("select pass from cars where car='%s'" % ( car ) )
					numrows9 = cursor9.rowcount
					if numrows9 == 1 :
						
						carseats = cursor9.fetchone()
						totalseats = carseats[0]
						
				
					cursor9.execute("select idno, date, car, datein, dateout, destiny, driver, seats, rseats, carseats, pass, rpass from res where \
					date='%s' and car='%s' and status='Active' order by datein" % ( item_date, car ) )
					
					numrows9 = cursor9.rowcount

# Open 1-Car Options Table to Users
					
#					carstable += "<td valign=top class=center><FONT SIZE=+1><b>" + car + "</b></font> (" + str( numrows9 ) + " res)<br>"
					carstable += "<td valign=top class=center><FONT SIZE=+1><b>%s</b></font> (%s res)<br>" % ( car, numrows9 )

					cartext1 = ''


# If Existing Reservations for this Car
#					if False :
#					if numrows9 > 0 and car not in badcarslist :
					if numrows9 > 0 :

						for rows9 in cursor9.fetchall() :
				
							idno9 = rows9[0]
							date9 = rows9[1]
							car9 = rows9[2]
							datein9 = str( rows9[3] )
							dateout9 = str( rows9[4] )
					
							destiny9 = rows9[5]
							destiny9 = destiny9.strip()
					
							driver9 = rows9[6]
							seats9 = rows9[7]
							rseats9 = rows9[8]
							carseats9 = rows9[9]

							pass9 = rows9[10]
							pass9 = pass9.strip()
							
							if pass9 =='.none' or pass9 == 'None' :
							
								pass9 = ''
								
							rpass9 = rows9[11]
							rpass9 = rpass9.strip()
					
							hourin9 = datein9[11:13]
							hourout9 = dateout9[11:13]
					
							cursor10.execute("select name from destiny where code = '%s'" % ( destiny9 ) )
							raws10 = cursor10.fetchone()
							destinyName = raws10[0]
	#						allpass = 0
							cursor10.execute("select coalesce ( sum( seats ), 0 ) from items where residno2 = '%s'" % ( idno9 ) )
	#						numrows10 = cursor10.rowcount
	#						if numrows10 > 0 :
							raws10 = cursor10.fetchone()
							allpass = raws10[0]

							cursor11.execute("select coalesce ( sum( seats2 ), 0 ) from items where residno3 = '%s'" % ( idno9 ) )
							raws11 = cursor11.fetchone()
							allrpass = raws11[0]
# numrows12 is this Plan Driver
							cursor12.execute("select idno from items where residno = %s " % ( idno9 ) )
							numrows12 = cursor12.rowcount
# numrows13 is this Plan WP Pass Up
							cursor12.execute("select idno from items where residno2 = %s " % ( idno9 ) )
							numrows13 = cursor12.rowcount
# numrows14 is this Plan WP Pass Down
							cursor12.execute("select idno from items where residno3 = %s " % ( idno9 ) )
							numrows14 = cursor12.rowcount

# numrows15 is Driver2 residno4
							cursor12.execute("select idno from items where residno4 = %s " % ( idno9 ) )
							numrows15 = cursor12.rowcount
# numrows16 is Driver3 residno5
							cursor12.execute("select idno from items where residno5 = %s " % ( idno9 ) )
							numrows16 = cursor12.rowcount
# numrows17 is Driver4 residno6 
							cursor12.execute("select idno from items where residno6 = %s " % ( idno9 ) )
							numrows17 = cursor12.rowcount

	#						allrpass = 0
	#						cursor11.execute("select sum( seats2 ) from items where residno3 = '%s'" % ( idno9 ) )
	#						numrows11 = cursor11.rowcount
	#						if numrows11 > 0 :
	#							raws11 = cursor11.fetchone()
	#							allrpass = raws11[0]
					
	#						openseats = carseats9 - seats9 - allpass
	#						openrseats = carseats9 - rseats9  - allrpass

#								openseats = carseats9 - seats9 - allpass - item_seats
#							openrseats = carseats9 - rseats9 - allrpass - item_seats2
# must include current WP seats seats2 

#							openseats = carseats9 - seats9 - allpass - int( item_seats )
#							openrseats = carseats9 - rseats9 - allrpass - int( item_seats2 )
# keep item_seats and item_seats2 as numerics

							openseats = carseats9 - seats9 - allpass - item_seats
							openrseats = carseats9 - rseats9 - allrpass - item_seats2

							openseatsPre = carseats9 - seats9 - allpass
							openrseatsPre = carseats9 - rseats9 - allrpass


#								openseats = 0
#								openrseats = 0

							cartext1 += "<table border=2 rules=all cellpadding=3 cellspacing=3>"

#							if rescount > 0 :

							if rescount > 0 and car9 in rescars :

								cartext1 += "<tr><th colspan=3 bgcolor=aqua><a href=resone.py?idno=%s>%s-%s YOU WP Driver: %s<br>P: %s</a> \
								<a href=planone.py?idno=%s&rid=%s>(Edit)</a></td></tr>" % ( idno9, hourin9, hourout9, driver9[0:12], pass9[0:20], item_idno, idno9  )

							else :

								
								if item_residno2 == idno9 or item_residno3 == idno9 :
						
									cartext1 += "<tr><th colspan=3 bgcolor=lime><a href=resone.py?idno=%s>%s-%s YOU WP Pass<br>with Driver: %s<br>P: %s</a> \
									<a href=planone.py?idno=%s&rid=%s>(Edit)</a></td></tr>" % ( idno9, hourin9, hourout9, driver9[0:12], pass9[0:20], item_idno, idno9  )

								else :
								
									cartext1 += "<tr><th colspan=3 bgcolor=yellow><a href=resone.py?idno=%s>%s-%s Driver: %s</a><br>P: %s  \
									<a href=planone.py?idno=%s&rid=%s>(Edit)</a></td></tr>" % ( idno9, hourin9, hourout9, driver9[0:12], pass9[0:20], item_idno, idno9 )

							
#							cartext1 += "<td colspan=3 bgcolor=white class=center>" + destinyName + '<br>' + str( openseatsPre ) + '/' + str( openrseatsPre ) + ' Open of ' + str( carseats9 ) + '</td></tr>'
							cartext1 += "<td colspan=3 bgcolor=white class=center>%s<br>OpenSeats: %s/%s of %s</td></tr>" % ( destinyName, openseatsPre, openrseatsPre, carseats9 )

#							cartext1 += "<tr><td colspan=2>D: %s P: %s</td><td><a href=planone2.py?idno=%s&rid=%s>(Edit)</a></td></tr>" \
#							% ( driver9, pass9, item_idno, idno9  )


							seatsImage = "seats4.jpg"

							if openseatsPre <= 0 :

								seatsImage = "seats0.jpg"

							else :
								
								if openseatsPre < 4 :
								
									seatsImage = "seats%s.jpg" % ( openseatsPre )
										

							seatsImage2 = "seats4.jpg"

							if openrseatsPre <= 0 :

								seatsImage2 = "seats0.jpg"

							else :
								
								if openrseatsPre < 4 :
								
									seatsImage2 = "seats%s.jpg" % ( openrseatsPre )
										
						
#								cartext1 += "<td colspan=3 bgcolor=white class=center valign=center>" + str( openseats ) + "<img src='../pix/" + seatsImage + \
#								"'> | <img src='../pix/" + seatsImage2 + "'>" + str( openrseats ) + "<br>(" + str( openseats ) + '/' + str( openrseats ) + \
#								' Open of ' + str( carseats9 ) + ' seats)</td></tr>'

#								cartext1 += "<td colspan=3 bgcolor=white class=center valign=center>" + str( openseatsPre ) + "<img src='../pix/" + seatsImage
#								cartext1 += "'> | <img src='../pix/" + seatsImage2 + "'>" + str( openrseatsPre ) + "</td></tr>"

#							cartext1 += "<td colspan=3 bgcolor=white class=center valign=center><img src='../pix/" + seatsImage + "'> | <img src='../pix/" + seatsImage2 + "'></td></tr>"
							cartext1 += "<td colspan=3 bgcolor=white class=center valign=center><img src='../pix/%s'> | <img src='../pix/%s'></td></tr>" % ( seatsImage, seatsImage2 )

	#						cartext1 += '<tr><th colspan=3 bgcolor=lime>Driver: %s</th></tr>' % ( driver9 )

# this res is not the current WP and No WP Driver, and Not Up or Return for thie Res

#								if (idno9 != item_residno and idno9 != item_residno4 or idno9 != item_residno5 or idno9 != item_residno ) \
#								and ( numrows13 == 0 and numrows14 == 0 ) :

# Passengers Heading: if No WP Drivers and residno2 or residno3 > 0

#							if rescount == 0 and ( numrows13 == 0 or numrows14 == 0 ) :
#							if numrows13 == 0 or numrows14 == 0 :
#							if True :
							if not car in rescars :
							
								if openseats >= 0 or openrseats >= 0 :

									cartext1 += "<tr><th colspan=3 bgcolor=lime>+%s Carpool Pass</th></tr>" % ( item_seats )
#									cartext1 += "<tr><th>Up/Return</th><th>Up</th><th>Return</th></tr>"

#										cartext1 += '<tr>'									
								else:

									cartext1 += "<tr><th colspan=3 class=center bgcolor=yellow>No Carpool Pass (%s)</th></tr>" % ( car9 )
									
									if openseatsPre > 0 or openrseatsPre > 0 :
									
										cartext1 += "<tr><th colspan=3 class=center bgcolor=yellow>Not Enough Seats! (%s/%s)</td></tr>" % ( openseats, openrseats )
#										cartext1 += '<tr><th>Up/Return</th><th>Up</th><th>Return</th></tr>'
									else:
										
#										cartext1 += "<tr><th colspan=3 class=center bgcolor=pink>No Carpool Pass (%s)</th></tr>" % ( car9 )
										cartext1 += "<tr><th colspan=3 class=center bgcolor=pink>All Seats Booked! (%s/%s)</td></tr>" % ( openseats, openrseats )
										
# Both Trips residno2 and residno3: - 1st Column

								if item_residno2 == idno9 and item_residno3 == idno9 :

# colspan = 3						
									cartext1 += "<tr><td colspan=3 class=center bgcolor=lime><b>You WP-Pass BOTH</b> (+%s/%s)</td></tr>" % ( item_seats, item_seats2 )
						
								else:
								
									if item_residno2 == idno9 or item_residno3 == idno9 :
						
										cartext1 += "<td colspan=3 class=center bgcolor=lime>You WP-Pass 1-Way (+%s/+%s)</td></tr>" % ( item_seats, item_seats2  )
								
									else :
						
										cartext1 += "<td colspan=3 class=center bgcolor=yellow>Not WP-Pass (+%s/+%s)</td></tr>" % ( item_seats, item_seats2 )
														
# Plus Seats Boxes
# Both
								cartext1 += "<tr><th>Up/Return</th><th>Up</th><th>Return</th></tr>"
						
								if openseats >= 0 and openrseats >= 0 and item_residno2 != idno9 and item_residno3 != idno9 :

									cartext1 += "<tr><td class=center><a href=planone.py?idno=%s&rid=%s&stamp=both>+%s</a></td>" % ( item_idno, idno9, item_seats  )
									
								else: 
								
									cartext1 += "<tr><td class=center>No Both</td>"

# Up													
								if openseats >= 0 and item_residno2 != idno9 :
								
									cartext1 += "<td class=center><a href=planone.py?idno=%s&rid=%s&stamp=up>+%s</a></td>" % ( item_idno, idno9, item_seats  )
									
								else :
									
									cartext1 += "<td class=center>No Up</td>"

# Return								
								if openrseats >= 0 and item_residno3 != idno9:
								
									cartext1 += "<td class=center><a href=planone.py?idno=%s&rid=%s&stamp=return>+%s</a></td></tr>" % ( item_idno, idno9, item_seats2  )
								
								else :
								
									cartext1 += "<td class=center>No Ret</td></tr>"
								
								
									


# What is this? removed 201016
#								cartext1 += "</td>"

# If No Car Reservations for this Car

							else:
								 
								if rescount > 0 :
																													
#									cartext1 += "<td colspan=3 class=center bgcolor=pink><b>WP Driver:<br>%s, %s</b></td></tr>" % ( item_assigned1, item_assigned2  )
									cartext1 += "<td colspan=3 class=center bgcolor=pink><b>WP Driver:<br>%s, %s</b></td></tr>" % ( driver9, pass9  )
								
								if item_residno2 == idno9 or item_residno3 == idno9 :
								
									cartext1 += "<td colspan=3 class=center bgcolor=pink><b>WP Passenger:<br>%s, %s</b></td></tr>" % ( item_assigned1, item_assigned2 )

# UnDo buttons for WP Passengers residno2 & residdno3

						
							if item_residno2 == idno9 or item_residno3 == idno9  :
							
								mtext= True

#								cartext1 += "</tr><td class=center>test</td><td class=center>test</td><td class=center>test</td></tr>" 
#								cartext1 += "</tr><td class=center>test</td>" 
							
# What is this? rmeoved 201016
#								cartext1 += "</tr>"
								cartext1 += "<tr><th colspan=3 bgcolor=pink>Undo Buttons</th></tr>"

#								cartext1 += "<tr><th>Up/Return</th><th>Up</th><th>Return</th></tr>"

								if item_residno2 == idno9 and item_residno3 == idno9 :

									cartext1 += "<tr><td class=center><a href=planone.py?idno=%s&rid=%s&stamp=unboth>(-%s)</a></td>"  % ( item_idno, idno9, item_seats )

								else:

									cartext1 += "<tr><td class=center></td>"

								if item_residno2 == idno9 :

									cartext1 += "<td class=center><a href=planone.py?idno=%s&rid=%s&stamp=unup>(-%s)</a></td>" % ( item_idno, idno9, item_seats  )

								else:

									cartext1 += "<td class=center>No Up</td>"

								if item_residno3 == idno9 :

									cartext1 += "<td class=center><a href=planone.py?idno=%s&rid=%s&stamp=unreturn>(-%s)</a></td></tr>"  % ( item_idno, idno9, item_seats2 )

								else:

									cartext1 += "<td class=center>No Ret</td></tr>"

								

#								cartext1 += "<td class=center><a href=planone2.py?idno=%s&residno=%s&stamp=unboth>(unbook -%s)</a></td>"  % ( item_idno, idno9, item_seats  )

#							cartext1 += "</tr></table>"
							cartext1 += "</table>"				

		
					else:

# If No Existing Reservations for Car

# If Not Booked Residno REsidno2 Residno3
						if rescount < 4  :  
				
							cartext1 += "<table rules=all border=1 cellpadding=2 cellspacing=2>"
							cartext1 += "<th colspan=3><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s&wpid=%s>00-23 Driver: free</a><br>(%s Res remain)<br>" \
							% ( item_date, car, item_hourin, item_hourout, item_idno, balcount )
							cartext1 += str( totalseats ) + "<img src=../pix/seats4.jpg></th></tr></table>"
						
						else :

#						if item_residno > 0 or item_residno4 > 0 or item_residno5 > 0 or item_residno6 > 0:

							cartext1 += "<br><center><table rules=all border=1 cellpadding=2 cellspacing=2>"
#							cartext1 += "<tr><th colspan=3 bgcolor=pink>Booked (4) WP Drivers:<br>%s, %s (+%s)</th>" % ( item_assigned1, item_assigned2, item_seats )
#							cartext1 += "<tr><th colspan=3 bgcolor=pink>Booked (4) WP Drivers: %s, %s (%s)</th>" % ( driver9, pass9, seats9 )
							cartext1 += "<tr><th colspan=3 bgcolor=pink>Booked 4 WP Drivers</th>"
							cartext1 += "</tr></table></center><br>" 
							
							
						

# If Residno2 or Residno3 = Booked
						
						if item_residno2 > 0 or item_residno3 > 0 :

							cartext1 += "<br><center><table rules=all border=1 cellpadding=2 cellspacing=2>"
							cartext1 += "<tr><th colspan=3 bgcolor=pink>Booked WP Pass:<br>%s, %s (+%s)</th>" % ( item_assigned1, item_assigned2, item_seats )
							cartext1 += "</tr></table></center><br>" 
					
#						else:
#						
# If Not Booked Residno REsidno2 Residno3
#			
#							cartext1 += "<table rules=all border=1 cellpadding=2 cellspacing=2>"
#							cartext1 += "<th colspan=3><a href=resone.py?idno=0&date=%s&car=%s&in=%s&out=%s&wpid=%s>00-23 Driver: free</a><br>" \
#							% ( item_date, car, item_hourin, item_hourout, item_idno )
#							cartext1 += str( totalseats ) + "<img src=../pix/seats4.jpg></th></tr></table>"
 
					 
				
					carstable += cartext1 + '</FONT>'
			
					carstable += "</td>"
				
					if car == 'J-04' or car == 'J-08' or car == 'J-12' :
				
						carstable += "</tr><tr>"
				
				carstable += "</tr><tr>"

	#			itemtable += "<td>none</td>" 
	#			itemtable += "<td>none</td>" 
				carstable += "</tr>"
				carstable += "</table>" 
				
			carstable += "Cars End Column:</td></tr>" 
			
#			wg_users = ( 'winegar', 'rikilee', 'letawsky', 'kiaina', 'kambe', 'iwashita', 'noriko', 'pyo', 'wung', 'hattori' )
#			wg_users = ( 'winegar', )
			
			if username in wg_users :
				
#				itemtable += carstable
				itemtable += "<tr><td class=right valign=top bgcolor=yellow><a href=./planone.py?idno=%s>PlanOne2 Demo: ( %s )</a></td><td bgcolor=yellow>Cars WG User Only</td></tr>" % ( idno, idno )
#				test=True
				
			else:

				
				itemtable += '<tr><td class=right valign=top bgcolor=yellow>Not WG User</td><td></td></tr>'		
			
			
			itemtable += "<tr><td class=right valign=top>History:</td><td>%s</td></tr>" % ( item_history )

# end left table				
			itemtable += '</table>'
# col split
			itemtable += '</td><td valign=top>'



#		cursor.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', \
#		location = '%s', assigned1 = '%s', dcassist = '%s', location2 = '%s', location3 = '%s', completion = '%s', contact2 = '%s', others = '%s', master = '%s' \
#		where idno = '%s'" % ( endtime, realstart, realend, niteeffect, dayeffect, location, assigned1, dcassist, location2, location3, completion, contact2, others, master, idno ) )

			itemtable += '<center><b>Assigned</b></center><hr><table>'
			itemtable += "<tr><td class=right><b>Assigned1:</b></td><td><FONT SIZE=4>%s</td></tr>" % ( item_assigned1 )
			itemtable += "<tr><td class=right><b>Assigned2:</b></td><td><FONT SIZE=4>%s</td></tr>" % ( item_assigned2 )
			
			if item_residno > 0 :
			
				itemtable += "<tr><td class=right><b>Team Pass:</b></td><td><FONT SIZE=4>%s</font> / PSeats: %s</td></tr>" % ( item_pass, item_pseats )
			
			itemtable += "<tr><td class=right><b>DC Assist:</b></td><td><FONT SIZE=4>%s | <FONT SIZE=2>Notify: <FONT SIZE=4>%s | <FONT SIZE=2>Seats: %s / %s</td></tr>" % ( item_dcassist, item_notify, item_seats, item_seats2 )
#				itemtable += "<tr><td class=right>DC Assist</td><td>%s</td></tr>" % ( dcassist2 )
#			itemtable += "<tr><td class=right>RealStart:</td><td>%s End: %s</td></tr>" % ( item_realstart, item_realend )
			itemtable += "<tr><td class=right><a href=./planone.py?idno=%s&stamp=start>RealStart:</a></td><td>%s <a href=./planone.py?idno=%s&stamp=end>RealEnd:</a> %s</td></tr>" % ( idno, item_realstart2, idno, item_realend2 )
			itemtable += '<tr><td class=right colspan=2><hr></td></tr>'
			itemtable += "<tr><td class=right>Completion Title:</td><td>%s</td></tr>" % ( item_completion )
			itemtable += "<tr><td class=right>Completion Text:</td><td>%s</td></tr>" % ( item_comptext )
# 				itemtable += "<tr><td class=right>RealEnd</td><td><input type=text size=20 value='%s' name='realend'></td></tr>" % ( str( item_realend ) )
#				itemtable += "<tr><td class=right>Master:</td><td><input type=text size=10 value='%s' name='master'></td></tr>" % ( item_master )
#				itemtable += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( str( item_idno ) )
#				itemtable += "<tr><td class=right>Created:</td><td>%s</td></tr>" % ( str( item_timestamp ) )
#				itemtable += "<tr><td class=right>LogCrew:</td><td>%s</td></tr>" % ( item_logcrew )
			itemtable += "</table>"
# start 3rd column
#				itemtable += '</td><td valign=top>'

			itemtable += '<hr><center><table><td valign=top><b>Required:</b><br>' + str( planreqs2 ) 
			
			itemtable += "Others Req: %s<br>" % ( item_otherreq ) 

			itemtable += '</td><td valign=top>'

			itemtable += '<b>LockOuts:</b><br>'+ str( planlocks2 ) + '</td></table></center><br>'


#			itemtable += '<hr><b>planreqs:</b><br>' + str( planreqs )

#			itemtable += '<hr><b>planlocks:</b><br>'+ str( planlocks ) + '<br>'
# details table

			itemtable += '<table>'

			itemtable += "<tr><td class=right>Master:</td><td>%s</td></tr>" % ( item_master )
			itemtable += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( str( item_idno ) )
			itemtable += "<tr><td class=right>Created:</td><td>%s</td></tr>" % ( str( item_timestamp ) )
			itemtable += "<tr><td class=right>LogCrew:</td><td>%s</td></tr>" % ( item_logcrew )
			itemtable += "</table><br>"

			itemtable += '</td></table>'

			itemtable += '</center>'


#			itemtable = '<hr><table>'
#			itemtable += "<tr><td>Requested by</td><td>%s</td></tr>" % ( item_user )
#			itemtable += "<tr><td>Contact 2</td><td>%s</td></tr>" % ( item_contact2 )
#			itemtable += "<tr><td>Others</td><td>%s</td></tr>" % ( item_others )
#			itemtable += "<tr><td>Created</td><td>%s</td></tr>" % ( str( item_timestamp ) )
#
#			itemtable += "<tr><td>Time</td><td>%s</td></tr>" % ( item_time )
#			itemtable += "<tr><td>Title</td><td>%s</td></tr>" % ( item_title )
#			itemtable += "<tr><td>Text</td><td>%s</td></tr>" % ( item_text )
#			itemtable += "<tr><td>Type</td><td>%s</td></tr>" % ( item_type )
#			itemtable += "<tr><td>Downtime</td><td>%s</td></tr>" % ( item_downtime ) 
#			itemtable += "<tr><td>Subsystem</td><td>%s</td></tr>" % ( item_subsystem )
#			itemtable += "<tr><td>Status</td><td>%s</td></tr>" % ( item_status )
#			itemtable += "<tr><td>History</td><td>%s</td></tr>" % ( item_history )
#			itemtable += "<tr><td>LogCrew</td><td>%s</td></tr>" % ( item_logcrew )

##		cursor.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', \
##		location = '%s', assigned1 = '%s', dcassist = '%s', location2 = '%s', location3 = '%s', completion = '%s', contact2 = '%s', others = '%s', master = '%s' \
##		where idno = '%s'" % ( endtime, realstart, realend, niteeffect, dayeffect, location, assigned1, dcassist, location2, location3, completion, contact2, others, master, idno ) )

#			itemtable += "<tr><td>EndTime</td><td>%s</td></tr>" % ( str( item_endtime ) )
#			itemtable += "<tr><td>RealStart</td><td>%s</td></tr>" % ( str( item_realstart ) )
#			itemtable += "<tr><td>RealEnd</td><td>%s</td></tr>" % ( str( item_realend ) )
#			itemtable += "<tr><td>NiteEffect</td><td>%s</td></tr>" % ( item_niteeffect )
#			itemtable += "<tr><td>DayEffect</td><td>%s</td></tr>" % ( item_dayeffect )
#			itemtable += "<tr><td>Location</td><td>%s</td></tr>" % ( item_location )
#			itemtable += "<tr><td>Assigned1</td><td>%s</td></tr>" % ( item_assigned1 )
#			itemtable += "<tr><td>Assigned2</td><td>%s</td></tr>" % ( item_assigned2 )
#			itemtable += "<tr><td>Notify</td><td>%s</td></tr>" % ( item_notify )
#			itemtable += "<tr><td>DC Assist</td><td>%s</td></tr>" % ( item_dcassist )
#			itemtable += "<tr><td>Location2</td><td>%s</td></tr>" % ( item_location2 )
#			itemtable += "<tr><td>Location3</td><td>%s</td></tr>" % ( item_location3 )
#			itemtable += "<tr><td>Completion</td><td>%s</td></tr>" % ( item_completion )
##			itemtable += "<tr><td>Completion Text</td><td>%s</td></tr>" % ( item_comptext )
#			itemtable += "<tr><td>IDNo</td><td>%s</td></tr>" % ( str( item_idno ) )
#			itemtable += "<tr><td>Master</td><td>%s</td></tr>" % ( item_master )
#			itemtable += "</table>"

			maintext = maintext + formtxt + itemtable


# Edit Display
			
		else:
		
			if method == 'POST' and field['action'].value == 'Edit' :


# DC Assist
				cursor3.execute("select text from refer where code='%s' order by seq" % ( 'DCASSIST' ) )
				
				numrows3 = cursor3.rowcount
				
				dcassist2 = "<select name=dcassist size=1>"
				
				for result3 in cursor3.fetchall() :
				
					dcassist3 = result3[0]
					
					dcassist3 = dcassist3.strip()
				
					if dcassist3 == item_dcassist :
						
						dcassist2 += "<option value='%s' selected>%s" % ( dcassist3, dcassist3 )
					else :
						
						dcassist2 += "<option value='%s'>%s" % ( dcassist3, dcassist3 )
				
				dcassist2 += "</select>"

# plan requirements

				cursor4.execute("select code from itemreqs where planidno='%s'" % ( idno ) )
				
				numrows4 = cursor4.rowcount

				planreqs = []
				
				for result4 in cursor4.fetchall() :
				
					planreqs.append ( result4[0] )


				cursor3.execute("select text from refer where code='%s' order by seq" % ( 'PLANREQ' ) )
				
				numrows3 = cursor3.rowcount

				planreqs2 = '<table>'
				
				for result3 in cursor3.fetchall() :
				
					refer_lock=result3[0]
				
					if refer_lock in planreqs :
						
						planreqs2 += "<tr><td bgcolor=lightgreen><input type=checkbox name=%s value=%s checked> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )
					else :
						
						planreqs2 += "<tr><td><input type=checkbox name=%s value=%s> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )
				
				planreqs2 += '</table>'



# plan lockouts
				cursor5.execute("select code from itemreqs where planidno='%s'" % ( idno ) )
				
				numrows5 = cursor5.rowcount

				planlocks = []
				
				for result5 in cursor5.fetchall() :
				
					planlocks.append ( result5[0] )

				cursor3.execute("select text from refer where code='%s' order by seq" % ( 'PLANLOCK' ) )
				
				numrows3 = cursor3.rowcount

				planlocks2 = '<table>'
				
				for result3 in cursor3.fetchall() :
					
					refer_lock=result3[0]
				
					if refer_lock in planlocks :
						
						planlocks2 += "<tr><td bgcolor=pink><input type=checkbox name='%s' value='%s' checked> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )
					else :
						
						planlocks2 += "<tr><td><input type=checkbox name='%s' value='%s'> %s</td></tr>" % ( refer_lock, refer_lock, refer_lock )

				planlocks2 += '</table>'

# Locations
				cursor3.execute("select text from refer where code='%s' order by seq" % ( 'LOCATIONS' ) )

				locations1 = '<select name=location size=1>'
				locations2 = '<select name=location2 size=1>'
				locations3 = '<select name=location3 size=1>'
				
				
				location = location.strip()
				location2 = location2.strip()
				location3 = location3.strip()
				
				for result3 in cursor3.fetchall() :
				
					refer_location = result3[0]
					refer_location = refer_location.strip()
				
					if item_location == refer_location  :
						
						locations1 += "<option value='%s' selected>%s" % ( refer_location, refer_location )
					else :
						
						locations1 += "<option value='%s'>%s" % ( refer_location, refer_location )

					if item_location2 == refer_location :
						
						locations2 += "<option value='%s' selected>%s" % ( refer_location, refer_location )
					else :
						
						locations2 += "<option value='%s'>%s" % ( refer_location, refer_location )

					if item_location3 == refer_location :
						
						locations3 += "<option value='%s' selected>%s" % ( refer_location, refer_location )
					else :
						
						locations3 += "<option value='%s'>%s" % ( refer_location, refer_location )

				locations1 += "</select>"
				locations2 += "</select>"
				locations3 += "</select>"
						
# status
				statii = ( 'Planned', 'Started', 'Completed', 'NotComplete', 'Cancelled' )
				status2 = '<select name=status size=1>'
				
				for stat in statii:
				
					if stat == item_status :
					
						status2 += "<option value=%s selected>%s" % ( stat, stat )
					else:
						
				
						status2 += "<option value=%s>%s" % ( stat, stat )
					 
				status2 += "</select>"

# Types
				types = ( 'Comment', 'Trouble', 'Summary', 'Warning', 'Observation', 'Important' )

				logtypes1 = "<select name=type size=1>"

				for typ in types:
				
					if typ == item_type :

						logtypes1 += "<option value='%s' selected>%s" % ( typ, typ )
					else:
						
						logtypes1 += "<option value='%s'>%s" % ( typ, typ )

				logtypes1 += "</select>"

# Assigned1				
				cursor3.execute("select user from users order by user")
				
				numrows3 = cursor3.rowcount

				assigned1_2 = '<select name=assigned1 size=1>'
				
				for result3 in cursor3.fetchall() :
					
					user_text = result3[0]
				
					if user_text == item_assigned1 :
						
						assigned1_2 += "<option value='%s' selected>%s" % ( user_text, user_text )
					else:
						
						assigned1_2 += "<option value='%s'>%s" % ( user_text, user_text )

				assigned1_2 += '</select>'
								

# Notify

				cursor3.execute("select user from users order by user")

				notify2 = '<select name=notify size=1>'
				
				for result3 in cursor3.fetchall() :
					
					user_text = result3[0]
					user_text = user_text.strip()
				
					if user_text == item_notify :
						
						notify2 += "<option value='%s' selected>%s" % ( user_text, user_text )
					else:
						
						notify2 += "<option value='%s'>%s" % ( user_text, user_text )

				notify2 += '</select>'
# StartTime Spinner


				cursor3.execute("select text from refer where code='%s' order by seq" % ( 'TIME' ) )
				
				numrows3 = cursor3.rowcount

				start2 = '<select name=start2>'
				
				for result3 in cursor3.fetchall() :
				
					refer_start=result3[0]
				
					if refer_start == starttime :
						
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
				
					if refer_start == endtime :
						
						end2 += "<option value='%s' selected>%s" % ( refer_start, refer_start )
					else :
						
						end2 += "<option value='%s'>%s" % ( refer_start, refer_start )
				
				end2 += '</select>'


# Subsystem
				subsystem2 = "<select name=subsystem size=1>"

				subsystems = ( '-none-', 'Tel', 'Inst', 'SOSS', 'Weather', 'Operations', 'Others' )

				for subsys in subsystems :

					if subsys == item_subsystem :

						subsystem2 += "<option value=%s selected>%s" % ( subsys, subsys )

					else:

						subsystem2 += "<option value=%s>%s" % ( subsys, subsys )

				subsystem2 += "</select>"


# Edit Page
				formtxt = "<center><form method=post action=./planone.py?idno=%s><input type=submit name=action value='Save'>  <input type=submit name=action value='Cancel'></center>" % ( idno )
				
				itemtable = '<center>'
				
				
#				itemtable += '<div class="input-group clockpicker" data-autoclose="true">'
				
#				itemtable += "<input type='text' class='form-control' id='single-input' value='%s' name='start5'>" % ( starttime )
#				itemtable += "<input type='text' class='form-control' id='single-input' name='start5'>" 
#				itemtable += '<span class="input-group-addon"><span class="glyphicon glyphicon-time"></span></span>'
#				itemtable += "</div>"
				
				itemtable += "<table><td valign=top>"

				itemtable += '<center><b>Requested</b></center><hr><table>'
				itemtable += "<tr><td class=right><b>Requestor:</b></td><td>%s</td></tr>" % ( item_user )
				itemtable += "<tr><td class=right>Contact2:</td><td><input type=text size=30 value='%s' name='contact2'> | Others: <input type=text size=30 value='%s' name='others'></td></tr>" % ( item_contact2, item_others )
#				itemtable += "<tr><td class=right>Others:</td><td><input type=text size=30 value='%s' name='others'></td></tr>" % ( item_others )

#				itemtable += "<tr><td class=right>Status:</td><td><input type=text size=20 value='%s' name='status'> | Type: <input type=text size=20 value='%s' name='type'></td></tr>" % ( item_status, item_type )
				itemtable += "<tr><td class=right>Status:</td><td> %s | Type: %s | Subsystem: %s</td></tr>" % ( status2, logtypes1, subsystem2 )

#				itemtable += "<tr><td class=right>StartTime:</td><td><input type=text size=15 value='%s' name='itemtime'> End: <input type=text size=15 value='%s' name='endtime'></td></tr>" % ( item_time2, item_endtime2 )
				itemtable += "<tr><td class=right>Start2:</td><td>%s %s | End2: %s %s</td></tr>" % ( startdate, start2, enddate, end2 )
#				itemtable += "<tr><td class=right>Start3</td><td>"
#				itemtable += "<div class='input-group clockpicker' data-autoclose='true'>"
#				itemtable += "<input type=text class='form-control' id='single-input' value='%s' name='start5'>" % ( starttime )
#				itemtable += '<span class="input-group-addon"><span class="glyphicon glyphicon-time"></span></span>'
#				itemtable += "</div>"
				itemtable += "</td></tr>"
				itemtable += '<tr><td class=right colspan=2><hr></td></tr>'
				itemtable += "<tr><td class=right>Plan Title:</td><td><input type=text size=80 maxsize=200 value='%s' name='itemtitle'></td></tr>" % ( item_title )
				itemtable += "<tr><td class=right valign=top>Plan Text:</td><td><textarea name=itemtext rows=5 cols=80>%s</textarea></td></tr>" % ( item_text )
#				itemtable += "<tr><td class=right>Text</td><td><input type=text size=50 value='%s' name='itemtext'></td></tr>" % ( item_text )
#				itemtable += "<tr><td class=right>Type</td><td><input type=text size=20 value='%s' name='type'></td></tr>" % ( item_type )
#				itemtable += "<tr><td class=right>Location1:</td><td>%s | 2: %s | 3: %s</td></tr>" % ( locations1, locations2, locations3 )
#				itemtable += "<tr><td class=right>Location1</td><td><input type=text size=20 value='%s' name='location'></td></tr>" % ( item_location )
#				itemtable += "<tr><td class=right>Location2</td><td><input type=text size=20 value='%s' name='location2'></td></tr>" % ( item_location2 )
#				itemtable += "<tr><td class=right>Location3</td><td><input type=text size=20 value='%s' name='location3'></td></tr>" % ( item_location3 )
				itemtable += '<tr><td class=right colspan=2><hr></td></tr>'
				itemtable += "<tr><td class=right>Locations:</td><td>%s | 2: %s | 3: %s</td></tr>" % ( locations1, locations2, locations3 )
#				itemtable += "<tr><td class=right>Downtime:</td><td><input type=text size=2 value='%s' name='downtime'></td></tr>" % ( item_downtime ) 
#				itemtable += "<tr><td class=right>Subsystem:</td><td><input type=text size=50 value='%s' name='subsystem'></td></tr>" % ( item_subsystem )
				itemtable += "<tr><td class=right>Day Warning:</td><td><input type=text size=50 value='%s' name='dayeffect'></td></tr>" % ( item_dayeffect )
				itemtable += "<tr><td class=right>Nite Warning:</td><td><input type=text size=50 value='%s' name='niteeffect'></td></tr>" % ( item_niteeffect )
				itemtable += "<tr><td class=right valign=top>History:</td><td>%s</td></tr>" % ( item_history )

# end left table				
				itemtable += '</table>'
# col split
				itemtable += '</td><td valign=top>'
				
				

	#		cursor.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', \
	#		location = '%s', assigned1 = '%s', dcassist = '%s', location2 = '%s', location3 = '%s', completion = '%s', contact2 = '%s', others = '%s', master = '%s' \
	#		where idno = '%s'" % ( endtime, realstart, realend, niteeffect, dayeffect, location, assigned1, dcassist, location2, location3, completion, contact2, others, master, idno ) )

				itemtable += '<center><b>Assigned</b></center><hr><table>'
#				itemtable += "<tr><td class=right><b>Assigned1:</b></td><td><input type=text size=20 value='%s' name='assigned1'> DC Assist: %s</td></tr>" % ( item_assigned1, dcassist2 )
				itemtable += "<tr><td class=right><b>Assigned1:</b></td><td>%s</td></tr>" % ( assigned1_2 )
				itemtable += "<tr><td class=right><b>Assigned2:</b></td><td><input type=text size=50 value='%s' name='assigned2'></td></tr>" % ( item_assigned2 )
				itemtable += "<tr><td class=right><b>Team Pass:</b></td><td><input type=text size=50 value='%s' name='pass1'></td></tr>" % ( item_pass )
				itemtable += "<tr><td class=right><b>DC Assist:</b></td><td>%s | Notify: %s</td></tr>" % ( dcassist2, notify2  )
#				itemtable += "<tr><td class=right>DC Assist</td><td>%s</td></tr>" % ( dcassist2 )
				itemtable += "<tr><td class=right>RealStart:</td><td><input type=text size=15 value='%s' name='realstart'> End: <input type=text size=15 value='%s' name='realend'></td></tr>" % ( item_realstart2, item_realend2 )
				itemtable += '<tr><td class=right colspan=2><hr></td></tr>'
				itemtable += "<tr><td class=right valign=top>Completion Title:</td><td><input type=text size=50 value='%s' name='completion'></td></tr>" % ( item_completion )
				itemtable += "<tr><td class=right valign=top>Completion Text:</td><td><textarea cols=80 rows=5 name='comptext'>%s</textarea></td></tr>" % ( item_comptext )
# 				itemtable += "<tr><td class=right>RealEnd</td><td><input type=text size=20 value='%s' name='realend'></td></tr>" % ( str( item_realend ) )
#				itemtable += "<tr><td class=right>Master:</td><td><input type=text size=10 value='%s' name='master'></td></tr>" % ( item_master )
#				itemtable += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( str( item_idno ) )
#				itemtable += "<tr><td class=right>Created:</td><td>%s</td></tr>" % ( str( item_timestamp ) )
#				itemtable += "<tr><td class=right>LogCrew:</td><td>%s</td></tr>" % ( item_logcrew )
				itemtable += "</table>"
# start 3rd column
#				itemtable += '</td><td valign=top>'

				itemtable += '<hr><center><table><td valign=top><b>Required:</b><br>' + str( planreqs2 ) 
				
				itemtable += "Others Req: <INPUT type=text name='otherreq' size=50 value='%s'><br>" % ( item_otherreq )
				
				itemtable += '</td><td valign=top>'

				itemtable += '<b>LockOuts:</b><br>'+ str( planlocks2 ) + '</td></table></center><br>'


#				itemtable += '<hr><b>planreqs:</b><br>' + str( planreqs )

#				itemtable += '<hr><b>planlocks:</b><br>'+ str( planlocks ) + '<br>'
# details table
				
				itemtable += '<table>'

				itemtable += "<tr><td class=right>Master:</td><td><input type=text size=10 value='%s' name='master'></td></tr>" % ( item_master )
				itemtable += "<tr><td class=right>IDNo:</td><td>%s</td></tr>" % ( str( item_idno ) )
				itemtable += "<tr><td class=right>Created:</td><td>%s</td></tr>" % ( str( item_timestamp ) )
				itemtable += "<tr><td class=right>LogCrew:</td><td>%s</td></tr>" % ( item_logcrew )
				itemtable += "</table><br>"
				
				itemtable += '</td></table></center>'
				
				

				itemtable += "</form>"
				
				
				
				
				
				maintext = maintext + formtxt + itemtable

	else :

		maintext += '<tr><td colspan=8>No Summit Item Available ' + str( idno ) + '</td></tr>'

	
#	maintext += itemtable
else:

#	maintext = "OPAL Login Required <a href = '../login.php'>Here</a><br>"
        maintext = logproc.returnLogin()		

#maintext += '</table></form>'

#maintext = 'Thomas'	
printHTML( maintext )
	
