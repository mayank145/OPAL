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
#import logproc
import logproc3 as logproc
import html
import re
#import ldap

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")
#method=os.environ["REQUEST_METHOD"]

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
cursor8=db.cursor()
cursor9=db.cursor()
cursor10=db.cursor()
cursor11=db.cursor()
cursor12=db.cursor()



def printHTML( maintext ) :


	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "table.t1 { background: url('./clockface_non.jpg') no-repeat; background-position: 52% 55% }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px; font-weight: bold }"
	css_text += "td.t1 { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px; font-weight: bold; width: 10px }"
	css_text += "td.t2 { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12Px; font-weight: bold; width: 10px }"
	
#/* Style the tab */
#	css_text += ".tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1;}"

#/* Style the buttons that are used to open the tab content */
#	css_text += ".tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s;}"

#/* Change background color of buttons on hover */
#	css_text += ".tab button:hover { background-color: #ddd; }"

#/* Create an active/current tablink class */
#	css_text += ".tab button.active { background-color: #ccc; }"

#/* Style the tab content */
#	css_text += ".tabcontent { display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }"	
	
	css_text += "</style>"

	css_text += '<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">'
	css_text += '<link rel="stylesheet" href="/resources/demos/style.css">'

#	css_text += "<script src='https://cdn.tiny.cloud/1/wew3bls4o7rcb9bz5e5fbsims2qe8k35v6ydly22743hjexy/tinymce/5/tinymce.min.js'></script>"
#	css_text += "<script>tinymce.init({selector:'textarea', forced_root_block: ''});</script>"
#	css_text += "<script src='./js/jquery-1.4.2.min.js'></script>"
#	css_text += "<script src='./js/jquery-ui-1.8.4.custom.min.js'></script>"

	css_text += "<script src='https://code.jquery.com/jquery-1.12.4.js'></script>"
	css_text += "<script src='https://code.jquery.com/ui/1.12.1/jquery-ui.js'></script>"


	css_text += "<script>$( function() {"
	css_text += '$( "#tabs" ).tabs();'
	css_text += "} );</script>"

	toppg = ''
	toppg += "Content-type: text/html; \n\n"
#	toppg += "Content-type: text/html; \n\n"
	toppg += "<!DOCTYPE html>"
	toppg += "<HTML><HEAD>"
	toppg += "<META  http-equiv='Content-Type' content='text/html; charset=UTF-8'>"
#	toppg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	toppg += css_text
	
	bottompg = "</HEAD><BODY>"
	bottompg += maintext
	bottompg += "</BODY></HTML>"
	
	print( toppg )
	
	print( bottompg )
		


def STNldapgroups( username ) :

	l=ldap.open('ldap.subaru.nao.ac.jp',389)
	
#	l=ldap.open('s03.subaru.nao.ac.jp',389)
#	loginline = "memberuid=" + username + ",ou=group,dc=subaru,dc=nao,dc=ac,dc=jp"
	
	l.simple_bind_s('','')
	base='ou=group,dc=subaru,dc=nao,dc=ac,dc=jp'
	scope=ldap.SCOPE_SUBTREE
#	scope=ldap.SCOPE_ONELEVEL
	
	filter = "memberuid=%s" % ( username )
	retrieve_attributes = None
	timeout = 0
	series = 0
	result_set = []
	result_id=l.search(base,scope,filter,retrieve_attributes)
	
	while 1:
		
		result_type,result_data = l.result(result_id,timeout)
		
		if (result_data==[]):
			
			break
		
		else:
			
			if result_type == ldap.RES_SEARCH_ENTRY:
				
				result_set.append(result_data)
			
	ldapgroups=[]
	
	for i in range(len(result_set)):
		
		for entry in result_set[i]:
			
			name=entry[1]['cn'][0]
			ldapgroups.append(name)
			
#	hscmaster='o14421'
#	
#	hscchildren=['o14406']
#	
#	for j in ldapgroups:
#		if j == hscmaster:
#			for k in hscchildren:
#				ldapgroups.append(k)

	ldapgroups.sort()
	
	return ldapgroups

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

#username = 'winegar'

#if field.has_key('date'):

if 'date' in field:

	date = field['date'].value
	
else:
	
	date = today
	
#if field.has_key('logcrew'):

if 'logcrew' in field:

	logcrew = field['logcrew'].value
	
else:
	
	logcrew = 'TO'

#if field.has_key('itemtitle'):

if 'itemtitle' in field:

	itemtitle = field['itemtitle'].value
	
else:
	
	itemtitle = ''

if 'itemtitle2' in field:

	itemtitle2 = field['itemtitle2'].value
	
else:
	
	itemtitle2 = ''

#if field.has_key('itemtext'):

if 'itemtext' in field:

	itemtext = field['itemtext'].value
	
else:
	
	itemtext = ''


if 'itemtext2' in field:

	itemtext2 = field['itemtext2'].value
	
else:
	
	itemtext2 = ''

#if field.has_key('dc1'):

if 'dc1' in field:

	dc1 = field['dc1'].value
	
else:
	
	dc1 = ''

#if field.has_key('dc2'):

if 'dc2' in field:

	dc2 = field['dc2'].value
	
else:
	
	dc2 = ''

#if field.has_key('to1'):

if 'to1' in field:

	to1 = field['to1'].value
	
else:
	
	to1 = ''


#if field.has_key('to2'):

if 'to2' in field:

	to2 = field['to2'].value
	
else:
	
	to2 = ''

if 'toin' in field:

	toin = field['toin'].value
	
else:
	
	toin = '0000-00-00 00:00'


#if field.has_key('to2'):

if 'toout' in field:

	toout = field['toout'].value
	
else:
	
	toout = '0000-00-00 00:00'

if 'ioin' in field:

	ioin = field['ioin'].value
	
else:
	
	ioin = '0000-00-00 00:00'


#if field.has_key('to2'):

if 'ioout' in field:

	ioout = field['ioout'].value
	
else:
	
	ioout = '0000-00-00 00:00'


#if field.has_key('io1'):

if 'io1' in field:

	io1 = field['io1'].value
	
else:
	
	io1 = ''

#if field.has_key('io2'):

if 'io2' in field:

	io2 = field['io2'].value
	
else:
	
	io2 = ''

#if field.has_key('to1loc'):

if 'to1loc' in field:

	to1loc = field['to1loc'].value
	
else:
	
	to1loc = 'Choose'

#if field.has_key('to2loc'):

if 'to2loc' in field:

	to2loc = field['to2loc'].value
	
else:
	
	to2loc = 'Choose'

#if field.has_key('io1loc'):

if 'io1loc' in field:

	io1loc = field['io1loc'].value
	
else:
	
	io1loc = 'Choose'

#if field.has_key('io2loc'):

if 'io2loc' in field:

	io2loc = field['io2loc'].value
	
else:
	
	io2loc = 'Choose'
	

#if field.has_key('sky'):

if 'sky' in field:

	sky = field['sky'].value
	
else:
	
	sky = ''

#if field.has_key('seeing'):

if 'seeing' in field:

	seeing = field['seeing'].value
	
else:
	
	seeing = ''
	
#if field.has_key('temp'):

if 'temp' in field:

	temp = field['temp'].value
	
else:
	
	temp = ''

#if field.has_key('wind'):

if 'wind' in field:

	wind = field['wind'].value
	
else:
	
	wind = ''

#if field.has_key('humid'):

if 'humid' in field:

	humid = field['humid'].value
	
else:
	
	humid = ''

#if field.has_key('comment'):

if 'comment' in field:

	comment = field['comment'].value
	
else:
	
	comment = ''

#if field.has_key('type'):

if 'type' in field:

	type = field['type'].value
	
else:
	
	type = 'Comment'

#if field.has_key('downtime'):

if 'downtime' in field:

	downtime = field['downtime'].value
	
else:
	
	downtime = '0'

#if field.has_key('subsystem'):

if 'subsystem' in field:

	subsystem = field['subsystem'].value
	
else:
	
	subsystem = 'None'

if 'type2' in field:

	type2 = field['type2'].value
	
else:
	
	type2 = 'Comment'

#if field.has_key('downtime'):

if 'downtime2' in field:

	downtime2 = field['downtime2'].value
	
else:
	
	downtime2 = '0'

#if field.has_key('subsystem'):

if 'subsystem2' in field:

	subsystem2 = field['subsystem2'].value
	
else:
	
	subsystem2 = 'None'

#if field.has_key('itemtime'):

if 'itemtime' in field:

	itemtime = field['itemtime'].value
	
else:
	
	itemtime = '00:00'

if 'itemtime2' in field:

	itemtime2 = field['itemtime2'].value
	
else:
	
	itemtime2 = '00:00'


#if field.has_key('status'):

if 'status' in field:

	status = field['status'].value
	
else:
	
	status = 'Completed'

#if field.has_key('todo'):

if 'todo' in field:

	todo = field['todo'].value
	
else:
	
	todo = 'query'

if 'intervene1' in field:

	intervene1 = field['intervene1'].value

else:

#	intervene1 = 'No'
	intervene1 = 'Choose'

if 'intervene2' in field:

	intervene2 = field['intervene2'].value

else:

#	intervene2 = 'No'
	intervene2 = 'Choose'
	
if logproc.validCookie() :
#if True :


	username, end, term, logcrew2 = logproc.getUsername()
	username = username.strip()

	toin_year='9999'


	cursor9.execute("select user from users where stnuser = '%s'" % ( username ) )
	numrows9 = cursor9.rowcount

	if numrows9 == 1 :

		ruw = cursor9.fetchone()
		newuser = ruw[0]

	else :

		newuser = username


	if method == 'POST' :

		if field['action'].value == 'DC In' :

			cursor.execute("update days set dc1 = '%s', dcin = '%s' where date = '%s'" % ( username, now, date ) )

		if field['action'].value == 'DC Out' :

			cursor.execute("update days set dcout = '%s' where date = '%s'" % ( now, date ) )

		if field['action'].value == 'TO In' :

			cursor9.execute("select user from users where stnuser = '%s'" % ( username ) )
			numrows9 = cursor9.rowcount

			if numrows9 == 1 :

				ruw = cursor9.fetchone()
				newuser = ruw[0]

			else :

				newuser = username

			cursor7.execute("select to1, to2 from days where date = '%s'" % ( date ) )
			numrows7 = cursor7.rowcount

			if numrows7 == 1:

				ruw = cursor7.fetchone()
				days_to1 = ruw[0]
				days_to1 = days_to1.strip()
				days_to2 = ruw[1]			
				days_to2 = days_to2.strip()

				to2s = days_to2.split(',')			
	#			
				if len( days_to1 ) == 0 :	 


	#				cursor.execute("update days set to1 = '%s', toin = '%s' where date = '%s'" % ( username, now, date ) )
					cursor.execute("update days set to1 = '%s', toin = '%s' where date = '%s'" % ( newuser, now, date ) )

				else :

					if not days_to1 == username :

						if len( days_to2 ) == 0  : 

							cursor.execute("update days set to2 = '%s' where date = '%s'" % ( newuser, date ) )
	#						cursor.execute("update days set to2 = '%s' where date = '%s'" % ( username, date ) )
						else:

							if newuser not in to2s :
	#						if username not in to2s :

								update_names = days_to2 + ', ' + newuser
	#							update_names = days_to2 + ', ' + username

								cursor.execute("update days set to2 = '%s' where date = '%s'" % ( update_names, date ) )


		if field['action'].value == 'TO Out' :

			cursor.execute("update days set toout = '%s' where date = '%s'" % ( now, date ) )

		if field['action'].value == 'IO In' :

			cursor9.execute("select user from users where stnuser = '%s'" % ( username ) )
			numrows9 = cursor9.rowcount

			if numrows9 == 1 :

				ruw = cursor9.fetchone()
				newuser = ruw[0]

			else :

				newuser = username

			cursor7.execute("select io1, io2 from days where date = '%s'" % ( date ) )
			numrows7 = cursor7.rowcount

			if numrows7 == 1:

				ruw = cursor7.fetchone()
				days_io1 = ruw[0]
				days_io1 = days_io1.strip()
				days_io2 = ruw[1]			
				days_io2 = days_io2.strip()

				io2s = days_io2.split(',')			
	#			
				if len( days_io1 ) == 0 : 

					cursor.execute("update days set io1 = '%s', ioin = '%s' where date = '%s'" % ( newuser, now, date ) )
	#				cursor.execute("update days set io1 = '%s', ioin = '%s' where date = '%s'" % ( username, now, date ) )

				else :

					if not days_io1 == username :

						if len( days_io2 ) == 0  : 

	#						cursor.execute("update days set io2 = '%s' where date = '%s'" % ( username, date ) )
							cursor.execute("update days set io2 = '%s' where date = '%s'" % ( newuser, date ) )
						else:

							if username not in io2s :

	#							update_names = days_io2 + ', ' + username
								update_names = days_io2 + ', ' + newuser

								cursor.execute("update days set io2 = '%s' where date = '%s'" % ( update_names, date ) )


		if field['action'].value == 'IO Out' :

			cursor.execute("update days set ioout = '%s' where date = '%s'" % ( now, date ) )


		if field['action'].value == 'Save' :

			clean_sky = html.escape( sky, quote=True )
			clean_seeing = html.escape( seeing, quote=True )
			clean_temp = html.escape( temp, quote=True )
			clean_wind = html.escape( wind, quote=True )
			clean_humid = html.escape( humid, quote=True )
			clean_comment = html.escape( comment, quote=True )

			cursor.execute("update days set dc1 = '%s', dc2 = '%s', to1 = '%s', to2 = '%s', io1 = '%s', io2 = '%s', \
			to1loc = '%s', to2loc = '%s', io1loc = '%s', io2loc = '%s', sky = '%s', seeing = '%s', temp = '%s', wind = '%s', humid = '%s', comment = '%s', \
			toin = '%s', toout = '%s', ioin = '%s', ioout = '%s' \
			where date = '%s'" % ( dc1, dc2, to1, to2, io1, io2, to1loc, to2loc, io1loc, io2loc, clean_sky, clean_seeing, clean_temp, clean_wind, clean_humid, clean_comment, \
			toin, toout, ioin, ioout, date ) )

		if field['action'].value == 'Enter TO' :

			now2 = datetime.datetime.now()
			dt = now2.strftime('%Y-%m-%d %H:%M:%S')

			itemtime=itemtime.strip()

			if len( itemtime ) == 4 and itemtime[1] == ':' :

				itemtime = '0' + itemtime

			timehours = itemtime[0:2]
			timemin = itemtime[3:5]

			itemtime3 = dt

			if int( timehours ) > 0 or int( timemin ) > 0 :

				if int( timehours ) > 14 :

					itemtime3 = date + ' ' + itemtime

				else:
					dateStart = date.split('-')
					y = int( dateStart[0] )
					m = int( dateStart[1] )
					D = int( dateStart[2] )
					startDate = datetime.date( y, m, D)
					date2 = startDate + datetime.timedelta( days = 1 ) 
					date3 = date2.strftime('%Y-%m-%d')
					itemtime3 = date3 + ' ' + itemtime

			cursor2.execute("select user from users where stnuser = '%s' " % ( username ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				row = cursor2.fetchone()
				contact1 = row[0]
			else :

				contact1 = '.none'


			cursor2.execute("select idno, day from days where date='%s' " % ( date ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				row = cursor2.fetchone()
				days_idno = row[0]
				days_day = row[1]
			else :

				days_idno = 0
				days_day = 'None'


	#		clean_itemtitle = logproc.html_escape( itemtitle )
	#		clean_itemtext = logproc.html_escape( itemtext )

			clean_itemtitle = html.escape( itemtitle, quote=True )
			clean_itemtext = html.escape( itemtext, quote=True )

			clean_itemtitle2 = html.escape( itemtitle2, quote=True )
			clean_itemtext2 = html.escape( itemtext2, quote=True )
#250408 unicode errors
#			clean_itemtitle = ascii( clean_itemtitle )
#			clean_itemtext = ascii( clean_itemtext )
#250408 unicode errors
#			clean_itemtitle2 = ascii( clean_itemtitle2 )
#			clean_itemtext2 = ascii( clean_itemtext2 )


			fail_Title = False
			fail_Text = False
			clean_Title = ''
			clean_Text = ''
			
			validOrd = range ( 32, 126 )
			
			for char1 in clean_itemtitle :
				if not ord( char1 ) in validOrd :
					fail_Title = True					
				else :
					clean_Title += char1
					
			if fail_Title == True:
			
				clean_itemtitle = clean_Title
				
			for char2 in clean_itemtext :
			
				if not ord( char2 ) in validOrd :
					fail_Text = True
				else :
					clean_Text += char2
			
			if fail_Text == True :
				
				clean_itemtext = clean_Text					

			history_text = ''
			history_text += 'timestamp: ' + dt + ' ( ' + username + ' ) <br>' 
			history_text += 'title: ' + clean_itemtitle + '<br>' 
			history_text += 'text: ' + clean_itemtext + '<br>' 

			new_endtime = '0000-00-00 00:00'
			new_realstart = '0000-00-00 00:00'
			new_realend = '0000-00-00 00:00'
			new_niteeffect = ''
			new_dayeffect = ''
			new_location = ''
			new_assigned1 = ''
			new_dcassist = ''
			new_location2 = ''
			new_location3 = ''
			new_completion = ''
			new_contact2 = ''
			new_others = ''
			new_master = '0'
			new_assigned2 = ''
			new_notify = ''
			new_comptext = ''
			new_otherreq = ''

	#		cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem ) \
	#		values ( '%s', %s, '%s', '%s', '%s', '%s', '%s', '', 0, '' ) " % ( date, days_idno, days_day, logcrew, dt, itemtitle, itemtext ) )

	#		cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history ) values \
	#		( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, logcrew, itemtime3, itemtitle, itemtext, type, downtime, subsystem, status, dt, username, history_text ) )

			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, 'TO', itemtime3, clean_itemtitle, clean_itemtext, \
			type, downtime, subsystem, status, dt, username, history_text, contact1 ) )

			itemsidno = int( cursor3.lastrowid )

			if itemsidno > 0  :

#				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
#				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify='%s', comptext = '%s', otherreq = '%s', \
#				updatestamp = '%s', intervene = '%s' where idno='%s'" % ( new_endtime, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
#				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, \
#				new_comptext, new_otherreq, dt, 'No', itemsidno ) )

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify='%s', comptext = '%s', otherreq = '%s', \
				updatestamp = '%s', intervene = '%s' where idno='%s'" % ( new_endtime, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, \
				new_comptext, new_otherreq, dt, intervene1, itemsidno ) )

	#		if len( clean_itemtitle2 ) > 0 :
	#			
	#			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history ) values \
	#			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, 'IO', itemtime3, clean_itemtitle2, clean_itemtext2, type2, downtime2, subsystem2, status, dt, username, history_text ) )


			itemtitle = ''
			itemtext = ''
	#		itemtitle2 = ''
	#		itemtext2 = ''



		if field['action'].value == 'Enter IO' :

			now2 = datetime.datetime.now()
			dt = now2.strftime('%Y-%m-%d %H:%M:%S')
	#		
			if len( itemtime2 ) == 4 and itemtime2[1] == ':' :

				itemtime2 = '0' + itemtime2

			timehours = itemtime2[0:2]
			timemin = itemtime2[3:5]
	#		
			itemtime3 = dt
	#		
			if int( timehours ) > 0 or int( timemin ) > 0 :
	#		
				if int( timehours ) > 14 :
	#			
					itemtime3 = date + ' ' + itemtime2
	#				
				else:
					dateStart = date.split('-')
					y = int( dateStart[0] )
					m = int( dateStart[1] )
					D = int( dateStart[2] )
					startDate = datetime.date( y, m, D)
					date2 = startDate + datetime.timedelta( days = 1 ) 
					date3 = date2.strftime('%Y-%m-%d')
					itemtime3 = date3 + ' ' + itemtime2
	#		
			cursor2.execute("select user from users where stnuser = '%s' " % ( username ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				row = cursor2.fetchone()
				contact1 = row[0]
			else :

				contact1 = '.none'


			cursor2.execute("select idno, day from days where date='%s' " % ( date ) )
			numrows2 = cursor2.rowcount
	#
			if numrows2 == 1 :
	#		
				row = cursor2.fetchone()
				days_idno = row[0]
				days_day = row[1]
			else :
	#		
				days_idno = 0
				days_day = 'None'
	#

			
			clean_itemtitle = html.escape( itemtitle, quote=True )
			clean_itemtext = html.escape( itemtext, quote=True )

			clean_itemtitle2 = html.escape( itemtitle2, quote=True )
			clean_itemtext2 = html.escape( itemtext2, quote=True )

#250408 unicode errors
#			clean_itemtitle = ascii( clean_itemtitle )
#			clean_itemtext = ascii( clean_itemtext )
#250408 unicode errors
#			clean_itemtitle2 = ascii( clean_itemtitle2 )
#			clean_itemtext2 = ascii( clean_itemtext2 )

			fail_Title = False
			fail_Text = False
			clean_Title = ''
			clean_Text = ''
			
			validOrd = range ( 32, 126 )
			
			for char1 in clean_itemtitle2 :
				if not ord( char1 ) in validOrd :
					fail_Title = True					
				else :
					clean_Title += char1
					
			if fail_Title == True:
			
				clean_itemtitle2 = clean_Title

				
			for char2 in clean_itemtext2 :
			
				if not ord( char2 ) in validOrd :
					fail_Text = True
				else :
					clean_Text += char2
			
			if fail_Text == True :
				
				clean_itemtext2 = clean_Text					


			history_text = ''
			history_text += 'timestamp: ' + dt + ' ( ' + username + ' ) <br>' 
			history_text += 'title: ' + clean_itemtitle2 + '<br>' 
			history_text += 'text: ' + clean_itemtext2 + '<br>' 

			new_endtime = '0000-00-00 00:00'
			new_realstart = '0000-00-00 00:00'
			new_realend = '0000-00-00 00:00'
			new_niteeffect = ''
			new_dayeffect = ''
			new_location = ''
			new_assigned1 = ''
			new_dcassist = ''
			new_location2 = ''
			new_location3 = ''
			new_completion = ''
			new_contact2 = ''
			new_others = ''
			new_master = '0'
			new_assigned2 = ''
			new_notify = ''
			new_comptext = ''
			new_otherreq = ''


			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, 'IO', itemtime3, clean_itemtitle2, clean_itemtext2, \
			type2, downtime2, subsystem2, status, dt, username, history_text, contact1 ) )

			itemsidno = int( cursor3.lastrowid )

			if itemsidno > 0 :

#				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
#				updatestamp = '%s', intervene = '%s' where idno='%s'" % ( new_endtime, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
#				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, \
#				new_comptext, new_otherreq, dt, 'No', itemsidno ) )

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify='%s', comptext = '%s', otherreq = '%s', \
				updatestamp = '%s', intervene = '%s' where idno='%s'" % ( new_endtime, new_realstart, new_realend, new_niteeffect, new_dayeffect, \
				new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, \
				new_comptext, new_otherreq, dt, intervene2, itemsidno ) )

	#		if len( clean_itemtitle ) > 0 :
	#			
	#			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history ) values \
	#			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, 'TO', itemtime3, clean_itemtitle, clean_itemtext, type, downtime, subsystem, status, dt, username, history_text ) )

	#		itemtitle = ''
	#		itemtext = ''
			itemtitle2 = ''
			itemtext2 = ''


		if field['action'].value == 'Enter DC' :

			now2 = datetime.datetime.now()
			dt = now2.strftime('%Y-%m-%d %H:%M:%S')

			timehours = itemtime[0:2]
			timemin = itemtime[3:5]

			itemtime3 = dt

			if int( timehours ) > 0 or int( timemin ) > 0 :

				if int( timehours ) > 14 :

					itemtime3 = date + ' ' + itemtime

				else:
					dateStart = date.split('-')
					y = int( dateStart[0] )
					m = int( dateStart[1] )
					D = int( dateStart[2] )
					startDate = datetime.date( y, m, D)
					date2 = startDate + datetime.timedelta( days = 1 ) 
					date3 = date2.strftime('%Y-%m-%d')
					itemtime3 = date3 + ' ' + itemtime

			cursor2.execute("select user from users where stnuser = '%s' " % ( username ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				row = cursor2.fetchone()
				contact1 = row[0]
			else :

				contact1 = '.none'

			cursor2.execute("select idno, day from days where date='%s' " % ( date ) )
			numrows2 = cursor2.rowcount

			if numrows2 == 1 :

				row = cursor2.fetchone()
				days_idno = row[0]
				days_day = row[1]
			else :

				days_idno = 0
				days_day = 'None'


	#		clean_itemtitle = logproc.html_escape( itemtitle )
	#		clean_itemtext = logproc.html_escape( itemtext )

			clean_itemtitle = html.escape( itemtitle, quote=True )
			clean_itemtext = html.escape( itemtext, quote=True )
#250408 unicode errors
#			clean_itemtitle = ascii( clean_itemtitle )
#			clean_itemtext = ascii( clean_itemtext )

			history_text = ''
			history_text += 'timestamp: ' + dt + ' ( ' + username + ' ) <br>' 
			history_text += 'title: ' + clean_itemtitle + '<br>' 
			history_text += 'text: ' + clean_itemtext + '<br>' 



			new_endtime = '0000-00-00 00:00'
			new_realstart = '0000-00-00 00:00'
			new_realend = '0000-00-00 00:00'
			new_niteeffect = ''
			new_dayeffect = ''
			new_location = ''
			new_assigned1 = ''
			new_dcassist = ''
			new_location2 = ''
			new_location3 = ''
			new_completion = ''
			new_contact2 = ''
			new_others = ''
			new_master = '0'
			new_assigned2 = ''
			new_notify = ''
			new_comptext = ''
			new_otherreq = ''

	#		cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem ) \
	#		values ( '%s', %s, '%s', '%s', '%s', '%s', '%s', '', 0, '' ) " % ( date, days_idno, days_day, logcrew, dt, itemtitle, itemtext ) )

	#		cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history ) values \
	#		( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, logcrew, itemtime3, itemtitle, itemtext, type, downtime, subsystem, status, dt, username, history_text ) )


			cursor3.execute("insert into items ( date, dayidno, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, timestamp, user, history, contact1 ) values \
			( '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " % ( date, days_idno, days_day, logcrew, itemtime3, clean_itemtitle, clean_itemtext, \
			type, downtime, subsystem, status, dt, username, history_text, contact1 ) )

			itemsidno = int( cursor3.lastrowid )

			if itemsidno > 0 :

				cursor4.execute("update items set endtime = '%s', realstart = '%s', realend = '%s', niteeffect = '%s', dayeffect = '%s', location = '%s', assigned1 = '%s', dcassist = '%s', \
				location2 = '%s', location3 = '%s', comptitle = '%s', contact2 = '%s', others = '%s', master = '%s', assigned2 = '%s', notify = '%s', comptext = '%s', otherreq = '%s', \
				updatestamp = '%s', intervene = '%s' where idno='%s'" \
				% ( new_endtime, new_realstart, new_realend, new_niteeffect, new_dayeffect, new_location, new_assigned1, new_dcassist, new_location2, new_location3, new_completion, new_contact2, new_others, new_master, new_assigned2, new_notify, new_comptext, new_otherreq, dt, 'No', itemsidno ) )		

			itemtitle = ''
			itemtext = ''

	# items query

	# all 3
	cursor3.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime from items \
	where date = '%s' order by itemtime" % ( date ) )
	numrows3_all = str( cursor3.rowcount ) 
	#numrows3_all = '0'

	# dc 4
	cursor4.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime from items \
	where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'DC' ) )
	numrows4_dc = str( cursor4.rowcount )
	#numrows4_dc = '0'

	# wp 5	
	#cursor5.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, realstart, realend from items \
	#where date = '%s' and logcrew = '%s' and status<>'Cancelled' order by itemtime" % ( date, 'WP' ) )
	cursor5.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, realstart, realend, dcassist from items \
	where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'WP' ) )
	numrows5_wp = str( cursor5.rowcount )
	#numrows5_wp = '0'

	# to 6
	cursor6.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, intervene from items \
	where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'TO' ) )
	numrows6_to = str( cursor6.rowcount )
	#numrows6_to = '0'

	# io 7
	cursor7.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, intervene from items \
	where date = '%s' and logcrew = '%s' order by itemtime" % ( date, 'IO' ) )
	numrows7_io = str( cursor7.rowcount )
	#numrows7_io = '0'

	# trouble 8
	cursor8.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, intervene from items \
	where date = '%s' and type = '%s' order by itemtime" % ( date, 'Trouble' ) )
	numrows8_trouble = str( cursor8.rowcount )
	#numrows8_trouble = '0' 

	# old_wp 10
	cursor10.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, dcassist from items \
	where user = '%s' and logcrew='WP' order by itemtime desc limit 20" % ( username ) )
	numrows10 = str( cursor10.rowcount )
	#numrows10 = '0'


	# movewp 11	
	#cursor11.execute("select idno, dayidno, date, day, logcrew, itemtime, itemtitle, itemtext, type, downtime, subsystem, status, user, assigned1, endtime, realstart, realend from items \
	#where user = '%s' and logcrew = '%s' and order by itemtime desc limit 20" % ( username, 'WP' ) )
	#numrows11_wp = str( cursor11.rowcount )


	buttontxt = '<center><table cellspacing=5 cellpadding=5 rules=all border=1>'

	numrows_night = int( numrows6_to ) + int( numrows7_io )
	#numrows_night = 0

	buttontxt += '<td bgcolor=lime><b>Daily Menu</b></td>' 

	if logcrew == 'All' :

		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>Summary - %s</a></td>' % ( 'blanchedalmond', date, 'All', numrows3_all  )
	else:	
		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>Summary - %s</a></td>' % ( 'white', date, 'All', numrows3_all )  

	if logcrew == 'DC' :

		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>DayCrew - %s</a></td>' % ( 'blanchedalmond', date, 'DC', numrows4_dc ) 
	else:
		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>DayCrew - %s</a></td>' % ( 'white', date, 'DC', numrows4_dc ) 

	if logcrew == 'WP' :

		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>WorkPlan - %s</a></td>' % ( 'blanchedalmond', date, 'WP', numrows5_wp ) 
	else: 
		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>WorkPlan - %s</a></td>' % ( 'white', date, 'WP', numrows5_wp ) 

	if logcrew == 'TO' or logcrew == 'IO' :

		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>TO-IO - %s</a></td>' % ( 'blanchedalmond', date, 'TO', numrows_night )
	else:
		buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>TO-IO - %s</a></td>' % ( 'white', date, 'TO', numrows_night )  

	if True :

		buttontxt += '<td bgcolor=%s><a href=%s?>%s</a></td>' % ( 'white' , 'fatslist.py' , 'FATS-test'  )

	buttontxt += "</table>( <b>'Delete Item'</b> is in <b>Summary</b> )</center>"




	# outside frame

	maintext = ''

	cursor.execute("select date, day, dc1, dc2, dcout, to1, toout, io1, ioout, idno, to1loc, \
	to2loc, io1loc, io2loc, to2, io2, sky, seeing, temp, wind, humid, \
	comment, dcin, toin, ioin from days where date = '%s' " % ( date ) )
	numrows=cursor.rowcount
	#numrows = 0
	maintext += 'rows: ' + str( numrows ) + '<br>'
	#maintext += "<form method=post action='./logone.py?'>"

	# buttons for DC-Night-WP



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
		toout_short = toout[5:16]
		toout_txt = "<input type=text name=toout value='%s' size=16>" % ( toout[0:16] )

		toin = str( row[23] )
		toin_short = toin[5:16]
	#	toin_txt = toin[5:16]
		toin_txt = "<input type=text name=toin value='%s' size=16>" % ( toin[0:16] )

		to1loc = str( row[10] )

		to2 = row[14]
		to2loc = str( row[11] )


		io1 = row[7]

		ioout = str( row[8] )
		ioout_short = ioout[5:16]
		ioout_txt = "<input type=text name=ioout value='%s' size=16>" % ( ioout[0:16] )

		ioin = str( row[24] )
		ioin_short = ioin[5:16]
		ioin_txt = "<input type=text name=ioin value='%s' size=16>" % ( ioin[0:16] )

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
		comment = comment.strip()

		sky_display = html.unescape( sky )
		seeing_display = html.unescape( seeing )
		temp_display = html.unescape( temp )
		wind_display = html.unescape( wind )
		humid_display = html.unescape( humid )
		comment_display = html.unescape( comment )



		if logcrew == 'TO' :

			formtxt = "<center><form method=post action='./logone.py?date=%s'><input type=submit name=action value='Edit'><br><a href=logmail2.py?date=%s>View TO Email</a> | \
			<a href=logmail2.py?date=%s&mail=yes>Send TO Email</a> | <a href=logone.py?date=%s&logcrew=All&todo=delete>Delete Item</a><br> <br>" % ( date, date, date, date )

		else:

			formtxt = "<center><form method=post action='./logone.py?date=%s'><input type=submit name=action value='Edit'><br><a href=planmail2.py?date=%s>View DC Email</a> | <a href=planmail2.py?date=%s&mail=yes>Send DC Email</a> | <br>" % ( date, date, date )
			formtxt += "<a href=logmail2.py?date=%s>View TO Email</a> | <a href=logmail2.py?date=%s&mail=yes>Send TO Email</a> | <a href=logone.py?date=%s&logcrew=All&todo=delete>Delete Item</a><br> <br>" % ( date, date, date )

		pagename = '<center>Summit Log - <b>' + date + '</b> - ' + day + ' | ' + username + " [" + end + ']<br><br>' + logproc.getMenu() + '<br>'

		pagename += '<table cellpadding=5 cellspacing=5 border=2 rules=all>'


		cursor2.execute("select idno, dayidno, date, day, seq, instr, alloc, pi, ao1, ao2, intime, \
		outtime, obs1, obs2, obs3, obs1loc, obs2loc, obs3loc, ss, ssloc, others1, \
		others2, others1loc, others2loc, gid, propid, ss2, ss2loc from progs where date = '%s' order by seq" % ( date ) )
	# Programs		
		progtxt = "<table cellpadding=3 cellspacing=3><tr><td colspan=5 bgcolor=lightgray><b>Observation Programs</b> || <a href=progone.py?date=%s&seq=0>Add Program</a> || <a href=proglist.py?date=%s>Remove Program</a></td></tr>" % ( date, date )

		numrows2 = cursor2.rowcount
	#	numrows2=0
		if numrows2 > 0 :
		
			seq2 = 0 

			for raw in cursor2.fetchall() :
			
				seq2 += 1
				
				seq2txt = str( seq2 )

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
				ss2 = raw[26]
				ss2loc = raw[27]

				
				
				progtxt += '<tr><td valign=top><a href=progone.py?idno=%s>Prog&nbsp;%s</a></td>' % ( progidno, seq2txt ) 
				progtxt += '<td>Instr: %s | Alloc: %s | AO1/2: %s / %s<br>' % ( instr, alloc, ao1, ao2 ) 
				progtxt += 'GID: %s | PropID: %s | PI: %s<br>' % ( gid, propid, pi ) 
				progtxt += 'Start: %s | End: %s<br>' % ( intime[5:16], outtime[5:16] ) 
				progtxt += 'Observers 1: %s @ %s<br>' % ( obs1, obs1loc )
				if len( obs2 ) > 0 : 
					progtxt += 'Observers 2: %s @ %s<br>' % ( obs2, obs2loc ) 
				if len( obs3 ) > 0 : 
					progtxt += 'Observers 3: %s @ %s<br>' % ( obs3, obs3loc ) 

				if len( ss2 ) > 0 :
					progtxt += 'SA: %s @ %s | SA2: %s @ %s<br>' % ( ss, ssloc, ss2, ss2loc )				
				else:
					progtxt += 'SA: %s @ %s<br>' % ( ss, ssloc )

				if len( others1 ) > 0 : 				
					progtxt += 'Others 1: %s @ %s<br>' % ( others1, others1loc ) 
				if len( others2 ) > 0 : 
					progtxt += 'Others 2: %s @ %s<br>' % ( others2, others2loc ) 
				progtxt += '</td></tr>' 


		else:
			progtxt += '<td colspan=5>No Programs for %s</td></tr>' % ( date ) 


		progtxt += '</table><br>'

	#	pagename += '<td valign=top>logcrew: <b>' + logcrew + '</b></td>'

		pagename += '<tr><td colspan=2 valign=top>' + buttontxt + '</td><tr>'

	#	if logcrew == 'TO' :

	#	else:
	#		pagename += '<td valign=top>'  + 'logcrew: <b>' + logcrew + '</b></td>'


		if logcrew == 'TO'  :


			pagename += "<td valign=top><center><form method=post action='./logone.py?'><input type=submit name=action value='Edit'><br><br><a href=logmail2.py?date=%s>View TO Email</a> | \
			<a href=logmail2.py?date=%s&mail=yes>Send TO Email</a> | <a href=logone.py?date=%s&logcrew=All&todo=delete>Delete Item</a> | <br>\
			<a href=logmail2.py?date=%s&mail=no&type=smoka>View SMOKA Email</a> | <a href=logmail2.py?date=%s&mail=yes&type=smoka>Send SMOKA Email</a>" % ( date, date, date, date, date )

			pagename += "<input type=hidden name=date value='%s'></center><br></form>" % ( date ) 

			pagename += '<b>Crew</b><br>TO1: ' + to1 + ' @ ' + to1loc + ' | TO2: ' + to2 + ' @ ' + to2loc + \
			'<br>IO1: ' + io1 + ' @ '+io1loc + ' | IO2: ' + io2 + ' @ '+io2loc + '<br>'

			pagename += 'Sky: ' + sky_display + ' | Seeing: ' + seeing_display + ' | Temp: ' + temp_display + '<br>Wind: ' + wind_display + ' | Humid: ' + humid_display
			
			if len ( comment_display ) > 0 :
			
				pagename += '<br>' + comment_display 
			
			pagename += '</td>'
			pagename += '<td valign=top>'  + progtxt + '</td></tr>'

	#

		if logcrew == 'DC' :

			pagename += '<td>DC2: ' + dc2 + '<br>DC1: ' + dc1 + '</td><td>' + formtxt + '</td></tr>'

		if logcrew == 'WP' :

			pagename += ''

	#	if logcrew == 'All'  :

	#		pagename += '<td></td><td></td></tr>'

		pagename += '</table>'
	#	pagename += '<br><a href=loglist.py>Return to Days List</a><br><br>' + buttontxt+'</center>'
	#	pagename += '<br><br>' + buttontxt+'</center>'
	#pagename = '<center><b>Summit Log - ' + date + '</b><br>' + '[ ' + username + ' ' + ' ]<br><br><a href=loglist.py>Return to LogList</a><br></center>'

		maintext = pagename

		maintext += '<table><tr><th>left</th><th>right</th></tr>'

	# left column
		maintext += "<tr><td valign=top width=600>"


	# crew section

	#	enterkey = field['action'].value
	#	enterkey = enterkey[0:5]

	#	enterkey = ''

		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter TO' or field['action'].value == 'Enter IO' \
		or field['action'].value == 'Enter DC' or field['action'].value == 'Cancel' ) ) : 
	#	if  method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter' ) : 

#			types = ( 'Comment', 'Trouble', 'Summary', 'Warning' )
			types = ( 'Comment', 'Trouble', 'Summary', 'Warning', 'Important' )

			subsystems = ( 'None', 'Tel', 'Inst', 'SOSS', 'Weather', 'Operations', 'Others', '' )

			statii = ( 'Completed', 'Cancelled', 'Incomplete' )

			status2 = "<select name=status size=1>"

			for stati in statii :

				if stati == status :
					status2 += "<option value=%s selected>%s" % ( stati, stati )
				else:
					status2 += "<option value=%s>%s" % ( stati, stati )

			status2 += "</select>"

			logtypes1 = "<select name=type size=1>"

			for typ in types:

				logtypes1 += "<option value='%s'>%s" % ( typ, typ )

			logtypes1 += "</select>"

			logtypes2 = "<select name=type2 size=1>"

			for typ in types:

				logtypes2 += "<option value='%s'>%s" % ( typ, typ )

			logtypes2 += "</select>"

			intervene1 = "<select name=intervene1 size=1><option value='Choose' selected>Choose<option value='No'>No<option value='Yes'>Yes</select>"

			intervene2 = "<select name=intervene2 size=1><option value='Choose' selected>Choose<option value='No'>No<option value='Yes'>Yes</select>"

			subsystems1 = "<select name=subsystem size=1><option value='None' selected>None<option value='Tel'>Tel<option value='Inst'>Inst"
			subsystems1 += "<option value=SOSS>SOSS<option value=Weather>Weather<option value=Operations>Operations<option value=Others>Others</select>"

			subsystems2 = "<select name=subsystem2 size=1><option value='None' selected>None<option value='Tel'>Tel<option value='Inst'>Inst"
			subsystems2 += "<option value=SOSS>SOSS<option value=Weather>Weather<option value=Operations>Operations<option value=Others>Others</select>"


	# Crews		
			crewtxt = ''
			crewtxt += '<table cellpadding=5 cellspacing=5><tr>'
			crewtxt += '<td colspan=4 align=left bgcolor=lightgray><b>Day Crew</b> || In: %s | Out: %s |</td></tr>' % ( dcin, dcout )
			crewtxt += '<td bgcolor=lime>DC1: </td><td colspan=3>' + dc1 + '</td></tr>'
			crewtxt += '<td bgcolor=lime>DC2: </td><td colspan=3>' + dc2  + '</td></tr>'
			crewtxt += '<td colspan=4 align=left bgcolor=lightgray><b>Night Crew</b> || In: %s | Out: %s |</td></tr>' % ( toin[5:16], toout[5:16] )
			crewtxt += '<td bgcolor=lime>TO1: </td><td>' + to1 + ' @ '+ to1loc + ' | </td><td bgcolor=lime>IO1: </td><td>' + io1 + ' @ '+ io1loc + ' | </td></tr>'
			crewtxt += '<td bgcolor=lime>TO2: </td><td>' + to2 + ' @ '+ to2loc + ' | </td><td bgcolor=lime>IO2: </td><td>' + io2 + ' @ '+ io2loc + ' | </td></tr>'
			crewtxt += '</table>'

			dcentry = "<form method=post action=./logone.py?date=%s><input type=hidden name=logcrew value='DC' size=3><table>" % ( date )
			dcentry += "<tr><td bgcolor=lightgray>DC Entry</td><td><input type=submit name=action value='Enter DC'></td></tr>"
	#		dcentry += "<tr><td>Time:</td><td>%s Type: %s DownTimeMin: %s Subsystem: %s Crew: %s</td></tr>" % ( itemtime, type, downtime, subsystem, logcrew )
			dcentry += "<tr><td>Title:</td><td><input type=text name=itemtitle value='%s' size=80></td></tr>" % ( itemtitle )
			dcentry += "<tr><td valign=top>Text:</td><td><textarea name=itemtext rows=20 cols=100>%s</textarea></td></tr>" % ( itemtext )		
			dcentry += "<tr><td valign=top>Time:</td><td><input type=text name=itemtime value='00:00' size=3> || "
			dcentry += "Type: " + logtypes2 + " || Status: " + status2 + "</td></tr>"

			dcentry += "</table></form>"

	#		itemtitle2 = ''
	#		itemtext2 = ''

#			toentry = "<form method=post action=logone.py?date=%s><input type=hidden name=logcrew value='TO' size=3>" % ( date )
			toentry = "<form method=post action=logone.py?date=%s>" % ( date )
	#		toentry += "<input type=hidden name=itemtitle2 value='%s'><input type=hidden name=itemtext2 value='%s'>" % ( itemtitle2, itemtext2 )
			toentry += "<table>"

			toentry += "<tr><td colspan=1 bgcolor=lightgray>TO Log</td><td><input type=submit name=action value='Enter TO'></td></tr>"
			toentry += "<tr><td>Title:</td><td><input type=text name=itemtitle value='%s' size=80></td></tr>" % ( itemtitle )
			toentry += "<tr><td valign=top>Text:</td><td><textarea name=itemtext rows=10 cols=80>%s</textarea></td></tr>" % ( itemtext )		
			toentry += "<tr><td valign=top>Time:</td><td><input type=text name=itemtime value='00:00' size=6> || "
			toentry += "Type: " + logtypes1 + " | Subsystem: " + subsystems1 + " | DownTimeMin: <input type=text name=downtime value='0' size=1> | SumAccess: " + intervene1 + "</td></tr>"
			toentry += "</table>"
	#		toentry += "</table></form>"


	#		itemtitle3 = ''
	#		itemtext3 = ''

	#		ioentry = "<form method=post action=logone.py?date=%s><input type=hidden name=logcrew value='IO' size=3>" % ( date )

	#		ioentry += "<input type=hidden name=itemtitle value='%s'><input type=hidden name=itemtext value='%s'>" % ( itemtitle, itemtext )
			ioentry = "<table>"
			ioentry += "<tr><td colspan=1 bgcolor=lightgray>IO Log</td><td><input type=submit name=action value='Enter IO'></td></tr>"
			ioentry += "<tr><td>Title:</td><td><input type=text name=itemtitle2 value='%s' size=80></td></tr>" % ( itemtitle2 )
			ioentry += "<tr><td valign=top>Text:</td><td><textarea name=itemtext2 rows=10 cols=80>%s</textarea></td></tr>" % ( itemtext2 )		
			ioentry += "<tr><td valign=top>Time:</td><td><input type=text name=itemtime2 value='00:00' size=6> || "
			ioentry += "Type: " + logtypes2 + " | Subsystem: " + subsystems2 + " | DownTimeMin: <input type=text name=downtime2 value='0' size=1> | SumAccess: " + intervene2 + "</td></tr>"
			ioentry += "</table></form>"


			oldwplog = ''

			if int( numrows10 ) > 0 :

				oldwplog += '<table cellpadding=2 cellspacing=2><tr><td align=left bgcolor=lightgray><b>Old WPs ||</b></td><tr>'
				for row in cursor10.fetchall() :

					item_idno = row[0]
					loglogcrew = row[4]
					logtime = str( row[5] )
					logdate = logtime[0:10]
					logdate2 = logtime[5:7] + '/' + logtime[8:10]
					logstart = logtime[11:16]
					logtitle = row[6]
					logtext = row[7]
					logtype = row[8]
					logdowntime = row[9]
					logsubsystem = row[10]
					logstatus= row[11]		
					loguser = row[12]		
					logassigned1 = row[13]		
					logendtime = str( row[14] )		
					logendtime = logendtime[11:16]

					dateArray = date.split('-')
					dateYear = dateArray[0]
					dateMonth = dateArray[1]
					dateDay = dateArray[2]

					dateOne = datetime.date( int( dateYear ), int( dateMonth ), int( dateDay ) )
					datex1 = dateOne.strftime( '%Y-%m-%d' )				

					dateTwo = dateOne + datetime.timedelta( days = 1 )
					datex2 = dateTwo.strftime( '%Y-%m-%d' )				

					dateThree = dateOne + datetime.timedelta( days = 2 )				
					datex3 = dateThree.strftime( '%Y-%m-%d' )				

					dateFour = dateOne + datetime.timedelta( days = 3 )				
					datex4 = dateFour.strftime( '%Y-%m-%d' )

					dateFive = dateOne + datetime.timedelta( days = 4 )				
					datex5 = dateFive.strftime( '%Y-%m-%d' )



	#				oldwplog += '<tr><td valign=top><a href=planone.py?date=%s&idno=0&copyid=%s&copyx=1><FONT SIZE=2>%s</a> | %s | %s&nbsp;|&nbsp;%s ( <a href=planone.py?date=%s&idno=0&copyid=%s&copyx=2>x2</a> )</td></tr>' % ( date, item_idno, logtime, logdate[5:10], logtitle[0:20], logstatus, date, item_idno,  )
					oldwplog += '<tr><td valign=top><FONT SIZE=3>%s %s-%s | %s | %s | %s&nbsp;|&nbsp;%s<br> - - <a href=planone.py?date=%s&idno=0&copyid=%s&copyx=1>(+1d %s)</a> ' % ( logdate2, logstart, logendtime, loguser, logstatus, logtitle[0:20], logstatus, date, item_idno, datex1[5:10] )

	#				if username == 'winegar' :

					oldwplog += '<a href=planone.py?date=%s&idno=0&copyid=%s&copyx=2>(+2d %s)</a> ' % ( date, item_idno, datex2[5:7] + '/' + datex2[8:10] )
					oldwplog += '<a href=planone.py?date=%s&idno=0&copyid=%s&copyx=3>(+3d %s)</a> ' % ( date, item_idno, datex3[5:7] + '/' + datex3[8:10] )
					oldwplog += '<a href=planone.py?date=%s&idno=0&copyid=%s&copyx=4>(+4d %s)</a> ' % ( date, item_idno, datex4[5:7] + '/' + datex4[8:10] )
					oldwplog += '<a href=planone.py?date=%s&idno=0&copyid=%s&copyx=5>(+5d %s)</a> ' % ( date, item_idno, datex5[5:7] + '/' + datex5[8:10] )

					oldwplog += '</td></tr>'

				oldwplog += '</table>' 

			else:
				oldwplog += 'No Items for Old WorkPlans'



	#		wpentry += "<center>Choose Time to Start WorkPlan on<br>[ <b>%s - %s </b> ]<br>" % ( date, day )
	#		wpentry += "<br><table cellpadding=3 cellspacing=3><tr><td bgcolor=white width=300>"
	#		wpentry += "<center>Choose Time to Start WorkPlan <b>%s</b> - %s<br>" % ( date, day )
	#		wpentry += "<table rules=all cellspacing=2 cellpadding=12 class='t1'>"
	#		wpentry += "<tr><td></td><td></td><td></td><td valign=bottom><a href=./planone.py?date=%s&idno=0&hr=12><img src='12.jpg'></a></td><td></td><td></td></tr>"
	#		wpentry += "<tr><td class=t1></td><td></td><td align=center class=t1><br><a href=./planone.py?date=%s&idno=0&hr=11><img src='11.jpg'></a></td><td class=t2>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=12><img src='12.jpg'></a></td><td align=bottom class=t1><a href=./planone.py?date=%s&idno=0&hr=01><img src='01.jpg'><br><a href=./planone.py?date=%s&idno=0&hr=13><img src='13.jpg'></a></a></td><td class=t1></td><td class=t1></td></tr>" % ( date, date, date, date )
	#		wpentry += "<tr><td></td><td align=right class=t1><b><a href=./planone.py?date=%s&idno=0&hr=10><img src='10.jpg'></b></td><td></td><td></td><td></td><td class=t1>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=14><img src='14.jpg'></a>&nbsp;<a href=./planone.py?date=%s&idno=0&hr=02><img src='02.jpg'></a></td><td></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
	#		wpentry += "<tr><td class=t1 align=right><a href=./planone.py?date=%s&idno=0&hr=09><img src='09.jpg'></a></td><td align=left></td><td></td><td></td><td></td><td align=right><a href=./planone.py?date=%s&idno=0&hr=15>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src='15.jpg'></a></td><td class=t1> <a href=./planone.py?date=%s&idno=0&hr=03><img src='03.jpg'></a></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
	#		wpentry += "<tr><td></td><td class=t1><a href=./planone.py?date=%s&idno=0&hr=08><img src='08.jpg'></td><td></td><td></td><td></td><td class=t1>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=16><img src='16.jpg'></a> <a href=./planone.py?date=%s&idno=0&hr=04><img src='04.jpg'></a></td><td></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td></td><td></td><td class=t1><a href=./planone.py?date=%s&idno=0&hr=07><img src='07.jpg'></a></td><td class=t1><br>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=06><img src='06.jpg'></a></td><td class=t1><b>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=17><img src='17.jpg'></a></b></td><td></td><td></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
	#		wpentry += "</table>"
	#		wpentry += "</td><td valign=top width=400> ... or Copy from Previous WorkPlans to <b>%s</b><br><br>" % ( date )
	#		wpentry += '</td></table></center>'

	#		wpentry += '<div id="tabs">'
	#		wpentry += "<ul>"
	#		wpentry += '<li><a href="#tabs-1">Tab1</a></li>'
	#		wpentry += '<li><a href="#tabs-2">Tab2</a></li>'
	#		wpentry += "</ul>"
	#		wpentry += '<div id="tabs-1">text for Tab1'
	#		wpentry += '</div>'
	#		wpentry += '<div id="tabs-2">text for Tab2'
	#		wpentry += '</div>'
	#		
	#		wpentry += '</div>'


	#		wplog = ""

			alllog = ''
			deletelog = ''

			if int( numrows3_all)  > 0 :

				alllog += '<table cellspacing=3 cellpadding=3>'
				deletelog += '<table>'
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
					logassigned1 = row[13]

	#				clean_logtext = tag_re.sub('', logtext )

	#				clean_logtext = re.sub('<[^<]+?>', '', logtext)

					clean_logtext = logproc.remove_html_markup( logtext )


	#				alllog += '<tr><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>[%s]</td><td valign=top><b>%s</b><br>%s</td></tr>' % ( item_idno, logtime, loglogcrew, logtitle, clean_logtext )

					if loglogcrew == 'WP' :
						alllog += '<tr><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>[%s]</td><td valign=top>%s</td><td valign=top><b>%s</b><br>%s</td></tr>' % ( item_idno, logtime, loglogcrew, logassigned1, logtitle, clean_logtext )
					else:
						alllog += '<tr><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>[%s]</td><td valign=top>%s</td><td valign=top><b>%s</b><br>%s</td></tr>' % ( item_idno, logtime, loglogcrew, loguser, logtitle, clean_logtext )

					deletelog += '<tr><td valign=top><a href=itemone.py?idno=%s&todo=delete>delete - %s</a></td><td valign=top>[%s]</td><td valign=top><b>%s</b><br>Text: %s</td></tr>' % ( item_idno, logtime, loglogcrew, logtitle, clean_logtext )

				alllog += '</table>' 
				deletelog += '</table>' 
			else:
				alllog += 'No Items for All Logs'
				deletelog += 'No Items for All Logs'


			dclog = ''

			if int( numrows4_dc ) > 0 :

				dclog += '<table>'
				for row in cursor4.fetchall() :

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

					clean_logtext = tag_re.sub('', logtext )		

					dclog += "<tr><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>[%s]</td><td valign=top>%s</td><td valign=top><FONT SIZE=3><b>%s</b>  ( %s ) - %s <br><FONT SIZE=3>%s</td></tr>" \
					% ( item_idno, logtime, loglogcrew, loguser, logtitle, logtype, logstatus, logtext )
#					% ( item_idno, logtime, loglogcrew, loguser, logtitle, logtext )

				dclog += '</table>' 
			else:
				dclog += 'No Items for DC Logs'


			tolog = ''

			if int( numrows6_to ) > 0 :

				tolog += '<table cellpadding=2 cellspacing=2>'
				for row in cursor6.fetchall() :

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
					logintervene = row[15]		

	#				clean_logtext = tag_re.sub('', logtext )		
	#				clean_logtext = re.sub('<[^<]+?>', '', logtext)

					clean_logtext = logproc.remove_html_markup( logtext )

					tolog += "<tr><td valign=top><a href=itemone.py?idno=%s><FONT SIZE=2>%s</a></td><td valign=top>[%s]</td><td valign=top><FONT SIZE=4><b>%s</b><FONT SIZE=2> ( %s ) - <FONT SIZE=2>%s" \
					% ( item_idno, logtime, loglogcrew, logtitle, logtype, loguser  )

					if logtype == 'Trouble' :

						tolog += '<FONT SIZE=2>| Subsys: <b>%s</b> | DownMin: <b>%s</b> | SumAccess: <b>%s</b>' % ( logsubsystem, logdowntime, logintervene )


					tolog += "<br><FONT SIZE=3>%s</td></tr>" % ( clean_logtext )

				tolog += '</table>' 

			else:
				tolog += 'No Items for TO Logs'

			iolog = ''

			if int( numrows7_io ) > 0 :

				iolog += '<table cellpadding=2 cellspacing=2>'
				for row in cursor7.fetchall() :

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
					logintervene = row[15]		

	#				clean_logtext = tag_re.sub('', logtext )		
					clean_logtext = re.sub('<[^<]+?>', '', logtext)

					iolog += '<tr><td valign=top><a href=itemone.py?idno=%s><FONT SIZE=2>%s</a></td><td valign=top>[%s]</td><td valign=top><FONT SIZE=4><b>%s</b><FONT SIZE=2> ( %s ) - <FONT SIZE=2>%s' % ( item_idno, logtime, loglogcrew, logtitle, logtype, loguser  )

					if logtype == 'Trouble' :

						iolog += '<FONT SIZE=2> | Subsys: <b>%s</b> | DownMin: <b>%s</b> | SumAccess: <b>%s</b>' % ( logsubsystem, logdowntime, logintervene )


					iolog += "<br><FONT SIZE=3>%s</td></tr>" % ( clean_logtext )

				iolog += '</table>' 

			else:
				iolog += 'No Items for TO Logs'

			troublelog = ''

			if int( numrows8_trouble ) > 0 :

				troublelog += '<table cellpadding=2 cellspacing=2><tr><td align=left bgcolor=lightgray><b>Trouble Summary ||</b></td><tr>'
				for row in cursor8.fetchall() :

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
					logintervene = row[15]		

					troublelog += '<tr><td valign=top><a href=itemone.py?idno=%s><FONT SIZE=2>%s</a> | %s | %s&nbsp;|&nbsp;%s&nbsp;min | SumAccess: %s</td></tr>' % ( item_idno, logtime, logsubsystem, logtitle, logdowntime, logintervene )

				troublelog += '</table>' 

			else:
				troublelog += 'No Items for Trouble Logs'

			wplog = ''

			if int( numrows5_wp ) > 0 :

				wplog += '<table rules=all border=2 cellpadding=5 cellspacing=5>'
				wplog += '<tr><th colspan=6 bgcolor=lime><FONT SIZE=4>WorkPlans - %s - %s</th></tr>' % ( date, day )
				wplog += '<tr><th>Date</th><th>User</th><th>Plan</th><th>Times</th><th>Status</th><th>DCAssist</th></tr>'
				for row in cursor5.fetchall() :

					item_idno = row[0]
					logdate = str( row[2] )
					logdate2 = logdate[5:7] + '/' + logdate[8:10]
					loglogcrew = row[4]
					logtime = str( row[5] )
					logtime = logtime[11:13]
					logtitle = row[6]
					logtext = row[7]
					logtype = row[8]
					logdowntime = row[9]
					logsubsystem = row[10]
					logstatus= row[11]		
					loguser = row[12]
					logassigned1 = row[13]
					logendtime = str( row[14] )
					logendtime = logendtime[11:13]
					logrealstart = str( row[15] )
					logrealstart = logrealstart[11:16]
					logrealend = str( row[16] )
					logrealend = logrealend[11:16]
					logdcassist = row[17]

					clean_logtext = tag_re.sub('', logtext )

					cursor12.execute("select code from itemreqs where planidno='%s'" % ( item_idno ) )

					numrows12 = cursor12.rowcount

					planreqs = ''

					if numrows12 > 0 :

						seq = 0

						for result12 in cursor12.fetchall() :

							seq += 1

							planreqs += result12[0]

							if seq < numrows12 :

								planreqs += ' | '

					else: 

						planreqs += 'none'

					bgcolor = 'white'

					if not logdcassist == '.none' :						

						bgcolor = 'yellow'
	#				wplog += '<tr><td valign=top><a href=planone.py?idno=%s>%s</a></td><td valign=top>[%s]</td><td valign=top><FONT SIZE=3><b>%s</b><br><FONT SIZE=3>%s</td></tr>' % ( item_idno, logtime, loglogcrew, logtitle, logtext )

					wplog += '<tr><td valign=top><a href=planone.py?idno=%s>%s %s-%s</a></td><td valign=top>%s</td><td valign=top><FONT SIZE=3><b>%s</b><br><FONT SIZE=2>Reqs: [ %s ]</td><td valign=top><a href=planone.py?idno=%s&stamp=start>Start:</a> %s<br><a href=planone.py?idno=%s&stamp=end>End:</a> %s</td><td>%s</td><td bgcolor=%s>%s</td></tr>' \
					% ( item_idno, logdate2, logtime, logendtime, logassigned1, logtitle, planreqs, item_idno, logrealstart, item_idno, logrealend, logstatus, bgcolor, logdcassist )

				wplog += '</table>' 
			else:
				wplog += 'No Items for WorkPlans'

			movewplog = ''
	#		
	#		if int( numrows11_wp ) > 0 :
	#		
	#			movewplog += '<table>'
	#			for row in cursor11.fetchall() :
	#
	#				item_idno = row[0]
	#				logdate = str( row[2] )
	#				logdate2 = logdate[5:7] + '/' + logdate[8:10]
	#				loglogcrew = row[4]
	#				logtime = str( row[5] )
	#				logtime = logtime[11:13]
	#				logtitle = row[6]
	#				logtext = row[7]
	#				logtype = row[8]
	#				logdowntime = row[9]
	#				logsubsystem = row[10]
	#				logstatus= row[11]		
	#				loguser = row[12]
	#				logassigned1 = row[13]
	#				logendtime = str( row[14] )
	#				logendtime = logendtime[11:13]
	#				logrealstart = str( row[15] )
	#				logrealstart = logrealstart[11:16]
	#				logrealend = str( row[16] )
	#				logrealend = logrealend[11:16]
	#						
	#				clean_logtext = tag_re.sub('', logtext )		

	##				wplog += '<tr><td valign=top><a href=planone.py?idno=%s>%s</a></td><td valign=top>[%s]</td><td valign=top><FONT SIZE=3><b>%s</b><br><FONT SIZE=3>%s</td></tr>' % ( item_idno, logtime, loglogcrew, logtitle, logtext )
	#				movewplog += '<tr><td valign=top><a href=planone.py?idno=%s>%s %s-%s</a></td><td valign=top>[%s]</td><td valign=top><FONT SIZE=3><b>%s</b> <FONT SIZE=3>| <td valign=top><a href=planone.py?idno=%s&stamp=start>Start:</a> %s <a href=planone.py?idno=%s&stamp=end>End:</a> %s ( %s )</td></tr>' % ( item_idno, logdate2, logtime, logendtime, logassigned1, logtitle, item_idno, logrealstart, item_idno, logrealend, logstatus )
	#
	#			movewplog += '</table>' 
	#		else:
	#			movewplog += 'No Items for WorkPlans'


			allhours = ( '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23' )

			if username == 'twin' :

				wpentry = "<center><a href=./planone.py?date=%s&idno=0&hr=08>Add New WorkPlan - %s @ 08</a><br><br></center>" % ( date, date[5:10] )

				for hr in allhours :

					wpentry += "<a href=./planone.py?date=%s&idno=0&hr=%s>%s:00</a> | " % ( date, hr, hr )

					if hr == '11' :

						wpentry += "<br>"				

			else:

				wpentry = "No New WorkPlans"

			wpentry = "<center>Choose <b>New Plan AM</b> | <b>New Plan PM</b> | <b>New Plan Copy</b><br>[ <b>%s - %s </b> ]<br><br>" % ( date, day )

			wpentry += '<div id="tabs">'
			wpentry += "<ul>"

	#		wpentry += '<li><a href="#tabs-1">WorkPlans Today</a></li>'

			wpentry += '<li><a href="#tabs-1">New Plan - AM</a></li>'
			wpentry += '<li><a href="#tabs-2">New Plan - PM</a></li>'
			wpentry += '<li><a href="#tabs-3">New Plan - Copy</a></li>'
			wpentry += '<li><a href="#tabs-4">not working</a></li>'
			wpentry += "</ul>"

			wpentry += '<div id="tabs-1">'
			wpentry += '<table cellpadding=3cellspacing=3><td valign=center>'
			wpentry += "<table rules=all cellspacing=0 cellpadding=14 class='t1'>"
	#		wpentry += "<tr><td></td><td></td><td></td><td valign=bottom><a href=./planone.py?date=%s&idno=0&hr=12><img src='12.jpg'></a></td><td></td><td></td></tr>"
			wpentry += "<tr><td></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=11><img src='./clock/11.png'></a></td><td><a href=./planone.py?date=%s&idno=0&hr=00><img src='./clock/00.png'></a></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=01><img src='./clock/01.png'></a></td><td></td></tr>" % ( date, date, date )
			wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=10><img src='./clock/10.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=02><img src='./clock/02.png'></a></td></tr>" % ( date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
			wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=09><img src='./clock/09.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=03><img src='./clock/03.png'></a></td></tr>" % ( date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
			wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=08><img src='./clock/08.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=04><img src='./clock/04.png'></a></td></tr>" % ( date, date )
			wpentry += "<tr><td></td><td><a href=./planone.py?date=%s&idno=0&hr=07><img src='./clock/07.png'></a></td><td><br>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=06><img src='./clock/06.png'></a></td><td><a href=./planone.py?date=%s&idno=0&hr=05><img src='./clock/05.png'></a></td><td></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
			wpentry += "</table>"


			wpentry += '</td><td>'

			wpentry += '<b>preset time</b><hr>'
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=09&hrout=13>%s 09-13</a><br>" % ( date, date[5:7]+'/'+date[8:10] )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=09&hrout=14>%s 09-14</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=09&hrout=15>%s 09-15</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=09&hrout=16>%s 09-16</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=09&hrout=17>%s 09-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=10&hrout=13>%s 10-13</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=10&hrout=14>%s 10-14</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=10&hrout=15>%s 10-15</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=10&hrout=16>%s 10-16</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )		
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=10&hrout=17>%s 10-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )		
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=11&hrout=14>%s 11-14</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=11&hrout=15>%s 11-15</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=11&hrout=16>%s 11-16</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=11&hrout=17>%s 11-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )


			wpentry += "</td></table>"
			wpentry += '</div>'




	#		wpentry += '<div id="tabs-2">'
	#		wpentry += "<table rules=all cellspacing=0 cellpadding=14 class='t1'>"
	##		wpentry += "<tr><td></td><td></td><td></td><td valign=bottom><a href=./planone.py?date=%s&idno=0&hr=12><img src='12.jpg'></a></td><td></td><td></td></tr>"
	#		wpentry += "<tr><td></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=11><img src='./clock/11.png'></a></td><td><a href=./planone.py?date=%s&idno=0&hr=00><img src='./clock/00.png'></a></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=01><img src='./clock/01.png'></a></td><td></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=10><img src='./clock/10.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=02><img src='./clock/02.png'></a></td></tr>" % ( date, date )
	##		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
	#		wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=09><img src='./clock/09.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=03><img src='./clock/03.png'></a></td></tr>" % ( date, date )
	##		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
	#		wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=08><img src='./clock/08.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=04><img src='./clock/04.png'></a></td></tr>" % ( date, date )
	#		wpentry += "<tr><td></td><td><a href=./planone.py?date=%s&idno=0&hr=07><img src='./clock/07.png'></a></td><td><br>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=06><img src='./clock/06.png'></a></td><td><a href=./planone.py?date=%s&idno=0&hr=05><img src='./clock/05.png'></a></td><td></td></tr>" % ( date, date, date )
	##		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
	#		wpentry += "</table>"
	#		wpentry += '</div>'

			wpentry += '<div id="tabs-2">'

			wpentry += '<table cellpadding=3cellspacing=3><td valign=center>'

			wpentry += "<table rules=all cellspacing=0 cellpadding=14 class='t1'>"
	#		wpentry += "<tr><td></td><td></td><td></td><td valign=bottom><a href=./planone.py?date=%s&idno=0&hr=12><img src='12.jpg'></a></td><td></td><td></td></tr>"
			wpentry += "<tr><td></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=23><img src='./clock/23.png'></a></td><td><a href=./planone.py?date=%s&idno=0&hr=12><img src='./clock/12.png'></a></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=13><img src='./clock/13.png'></a></td><td></td></tr>" % ( date, date, date )
			wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=22><img src='./clock/22.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=14><img src='./clock/14.png'></a></td></tr>" % ( date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
			wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=21><img src='./clock/21.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=15><img src='./clock/15.png'></a></td></tr>" % ( date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
			wpentry += "<tr><td><a href=./planone.py?date=%s&idno=0&hr=20><img src='./clock/20.png'></a></td><td></td><td></td><td></td><td><a href=./planone.py?date=%s&idno=0&hr=16><img src='./clock/16.png'></a></td></tr>" % ( date, date )
			wpentry += "<tr><td></td><td><a href=./planone.py?date=%s&idno=0&hr=19><img src='./clock/19.png'></a></td><td><br><br><a href=./planone.py?date=%s&idno=0&hr=18><img src='./clock/18.png'></a></td><td><a href=./planone.py?date=%s&idno=0&hr=17><img src='./clock/17.png'></a></td><td></td></tr>" % ( date, date, date )
	#		wpentry += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
			wpentry += "</table>"

			wpentry += '</td><td>'

			wpentry += '<b>preset time</b><hr>'
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=12&hrout=14>%s 12-14</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=12&hrout=15>%s 12-15</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=12&hrout=16>%s 12-16</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=12&hrout=17>%s 12-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=13&hrout=15>%s 13-15</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=13&hrout=16>%s 13-16</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=13&hrout=17>%s 13-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=14&hrout=16>%s 14-16</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )		
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=14&hrout=17>%s 14-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )		
			wpentry += "<a href=./planone.py?date=%s&idno=0&hr=15&hrout=17>%s 15-17</a><br>" % ( date, date[5:7]+'/'+date[8:10]  )		



			wpentry += "</td></table>"

			wpentry += '</div>'


			wpentry += '<div id="tabs-3">'

			wpentry += oldwplog

			wpentry += '</div>'

			wpentry += '<div id="tabs-4">'

			wpentry += movewplog

			wpentry += '</div>'

			wpentry += '</div>'



	# left column end - start right column



	# 1-2 column break

			columntxt = "</td><td valign=top width=600>"

	# Weather

			weathertxt = '<table cellpadding=3 cellspacing=3><tr><td colspan=10 align=left bgcolor=lightgray><b>Weather</b> ||</td><tr>'
			weathertxt += '<td align=right bgcolor=lime>Sky: </td><td>' + sky + ' | </td><td bgcolor=lime>Seeing: </td><td>' + seeing + ' | </td><td bgcolor=lime>Temp: </td><td>' + temp + ' | </td><td bgcolor=lime>Wind: </td><td>' + wind + ' | </td><td bgcolor=lime>Humid: </td><td>' + humid + ' | </td></tr>'
			weathertxt += '<tr><td align=right bgcolor=lime>Comment:</td><td colspan=9>' + comment + ' | </td>'
			weathertxt += '</tr></table>'



	# end right column

			column2txt = '</td></tr></table>'

	#		maintext = maintext + crewtxt + buttontxt + weathertxt + progtxt

			if logcrew == 'All' :

				if todo == 'delete' :

					maintext += '<hr>' + deletelog
					maintext = maintext + columntxt + formtxt + crewtxt + weathertxt + troublelog + progtxt

				else :

					maintext += '<hr>' + alllog

	#				maintext = maintext + columntxt + formtxt + crewtxt + weathertxt + troublelog + progtxt
					maintext = maintext + columntxt + formtxt + crewtxt + weathertxt + troublelog + progtxt

			if logcrew == 'DC' :

				maintext += dcentry + '<hr>' + dclog

	#			maintext = maintext + columntxt + formtxt + crewtxt + weathertxt + progtxt + column2txt
				maintext = maintext + columntxt + crewtxt + weathertxt + progtxt + column2txt

			if logcrew == 'TO' or logcrew == 'IO' :

				maintext += toentry + '<hr>' + tolog

				maintext = maintext + columntxt + ioentry + iolog

			if logcrew == 'WP' :

				maintext +=  wplog + columntxt + wpentry 

	#			maintext = maintext + columntxt + ioentry + iolog


	#		maintext += 


	#	if  method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter' ) : 
		else :

			maintext = "<form method=post action=./logone.py?date=%s><center>Summit Log - %s - Crews & Weather<br>" % ( date, date )
			maintext += "{ %s ]<br><br>" % ( username )
			maintext += "<input type=submit name=action value='Save'>  <input type=submit name=action value='Cancel'>"
	#		maintext += "<input type=submit name=action value='DC In'> <input type=submit name=action value='DC Out'> || " 
	#		maintext += "<input type=submit name=action value='TO In'> <input type=submit name=action value='TO Out'> || " 
	#		maintext += "<input type=submit name=action value='IO In'> <input type=submit name=action value='IO Out'>" 

			dc1_txt = "<input type=text name=dc1 value='%s' width=40 maxlength=40>" % ( dc1 )	

			dc2_txt = "<input type=text name=dc2 value='%s' width=40 maxlength=40>" % ( dc2 )

			to1_txt = "<input type=text name=to1 value='%s' width=20 maxlength=20>" % ( to1 )

			to2_txt = "<input type=text name=to2 value='%s' width=30 maxlength=30>" % ( to2 )	

			io1_txt = "<input type=text name=io1 value='%s' width=20 maxlength=20>" % ( io1 )	

			io2_txt = "<input type=text name=io2 value='%s' width=30 maxlength=30>" % ( io2 )

			tolocs = ( 'Choose', 'Summit', 'Hale Pohaku' )

			to1loc_txt = "<select size=1 name=to1loc>"

			for loc in tolocs :

				if to1loc == loc :

					to1loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

				else:

					to1loc_txt += "<option value='%s'>%s" % ( loc, loc )	

			to1loc_txt += "</select>"	

			to2loc_txt = "<select size=1 name=to2loc>"

			for loc in tolocs :

				if to2loc == loc :

					to2loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

				else:

					to2loc_txt += "<option value='%s'>%s" % ( loc, loc )	

			to2loc_txt += "</select>"

			iolocs = ( 'Choose', 'Summit', 'Hale Pohaku', 'Base', 'Mitaka' )

			io1loc_txt = "<select size=1 name=io1loc>"

			for loc in iolocs :

				if io1loc == loc :

					io1loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

				else:

					io1loc_txt += "<option value='%s'>%s" % ( loc, loc )	

			io1loc_txt += "</select>"	

			io2loc_txt = "<select size=1 name=io2loc>"

			for loc in iolocs :

				if io2loc == loc :

					io2loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

				else:

					io2loc_txt += "<option value='%s'>%s" % ( loc, loc )	

			io2loc_txt += "</select>"

			sky_txt = "<input type=text name=sky value='%s' size=20 maxlength=20>" % ( sky )	

			seeing_txt = "<input type=text name=seeing value='%s' size=20 maxlength=20>" % ( seeing )

			temp_txt = "<input type=text name=temp value='%s' size=20 maxlength=20>" % ( temp )

			wind_txt = "<input type=text name=wind value='%s' size=20 maxlength=20>" % ( wind )	

			humid_txt = "<input type=text name=humid value='%s' size=20 maxlength=20>" % ( humid )	

			comment_txt = "<input type=text name=comment value='%s' size=100 maxlength=100>" % ( comment )

			crewtxt = ''

			crewtxt += '<table cellpadding=5 cellspacing=5><tr><td colspan=6 align=left><hr><b>Crews</b></td><tr>'

	#		crewtxt += '<td bgcolor=lime>DC1: </td><td>' + dc1_txt + ' | </td><td bgcolor=lime>TO1: </td><td>' + to1_txt + ' @ '+ to1loc + ' | </td><td bgcolor=lime>IO1: </td><td>' + io1_txt + '@ '+ io1loc_txt + ' | </td></tr>'
	#		crewtxt += '<td bgcolor=lime>DC2: </td><td>' + dc2_txt + ' | </td><td bgcolor=lime>TO2: </td><td>' + to2_txt + ' @ '+ to2loc + ' | </td><td bgcolor=lime>IO2: </td><td>' + io2_txt + '@ '+ io2loc_txt + ' | </td></tr>'

			crewtxt += '<td bgcolor=lime>DC1: </td><td>' + dc1_txt + '</td><td bgcolor=lime>TO1: </td><td>' + to1_txt + ' @ ' + to1loc_txt +  '</td><td bgcolor=lime>IO1: </td><td>' + io1_txt  + ' @ '+ io1loc_txt + '</td></tr>'
			crewtxt += '<td bgcolor=lime>DC2: </td><td>' + dc2_txt + '</td><td bgcolor=lime>TO2: </td><td>' + to2_txt + ' @ ' + to2loc_txt + '</td><td bgcolor=lime>IO2: </td><td>' + io2_txt  + ' @ '+ io2loc_txt + '</td></tr>'
			crewtxt += '<td bgcolor=lime>In Out</td><td>In: ' + dcin + ' | Out: ' + dcout + '</td><td bgcolor=lime>In Out</td><td>In: ' + toin_txt + ' | Out: ' + toout_txt + '</td><td bgcolor=lime>In Out</td><td>In: ' + ioin_txt  + ' | Out: '+ ioout_txt + '</td></tr>'
			crewtxt += "<td></td><td><input type=submit name=action value='DC In'> <input type=submit name=action value='DC Out'></td><td></td>" 
			crewtxt += "<td><input type=submit name=action value='TO In'> <input type=submit name=action value='TO Out'></td><td></td>" 
			crewtxt += "<td><input type=submit name=action value='IO In'> <input type=submit name=action value='IO Out'></td>" 

			crewtxt += '</tr></table><br>'


			weathertxt = '<table cellpadding=3 cellspacing=3><tr><td colspan=10 align=left><hr><b>Weather</b></td><tr>'
			weathertxt += '<td align=right bgcolor=lime>Sky: </td><td>' + sky_txt + '</td><td bgcolor=lime>Seeing: </td><td>' + seeing_txt + '</td><td bgcolor=lime>Temp: </td><td>' + temp_txt + '</td><td bgcolor=lime>Wind: </td><td>' + wind_txt + '</td><td bgcolor=lime>Humid: </td><td>' + humid_txt + '</td></tr>'
			weathertxt += '<tr><td align=right bgcolor=lime>Comment:</td><td colspan=9>' + comment_txt + ' | </td></tr>'
			weathertxt += '</tr><table></form></center>'

			maintext = maintext + crewtxt + weathertxt


	else :

		maintext += '<tr><td colspan=8>No SummitLog Available for' + date + '</td></tr>'

	maintext += '</table>'

else :

#	maintext = "OPAL Login Required <a href='../login.php'>Here</a>"
        maintext = logproc.returnLogin()

#maintext = 'tom ' + method	
#maintext = 'tom ' + method	
printHTML( maintext )
	
