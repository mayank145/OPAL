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
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()
cursor5=db.cursor()
cursor6=db.cursor()

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
	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<!DOCTYPE html>"
	printpg += "<HTML><HEAD>"
#	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += "<META http-equiv='Content-Type' content='text/html; charset=UTF-8'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	


#MariaDB [sumlogs]> desc items;
#+-----------+------------+------+-----+---------+----------------+
#| Field     | Type       | Null | Key | Default | Extra          |
#+-----------+------------+------+-----+---------+----------------+
#| idno      | int(11)    | NO   | PRI | NULL    | auto_increment |
#| dayidno   | int(11)    | YES  |     | NULL    |                |
#| date      | date       | YES  |     | NULL    |                |
#| day       | char(10)   | YES  |     | NULL    |                |
#| logcrew   | char(2)    | YES  |     | NULL    |                |
#| itemtime  | datetime   | YES  |     | NULL    |                |
#| itemtitle | char(200)  | YES  |     | NULL    |                |
#| itemtext  | mediumtext | YES  |     | NULL    |                |
#| user      | char(20)   | YES  |     | NULL    |                |
#| type      | char(10)   | YES  |     | NULL    |                |
#| downtime  | char(3)    | YES  |     | NULL    |                |
#| subsystem | char(10)   | YES  |     | NULL    |                |
#| status    | char(15)   | YES  |     | NULL    |                |
#| timestamp | datetime   | YES  |     | NULL    |                |
#| history   | mediumtext | YES  |     | NULL    |                |
#+-----------+------------+------+-----+---------+----------------+
#15 rows in set (0.00 sec)


now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')

today2=datetime.date.today()
tmrw = today2 + datetime.timedelta( days = 1 )
tmrw_txt = tmrw.strftime('%Y-%m-%d')

#referpage=cgi.os.environ['HTTP_REFERER']
clientip=cgi.os.environ['REMOTE_ADDR']


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
	
	logcrew = 'All'

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

#if 'updatestamp' in field :

#	updatestamp = field['updatestamp'].value

#else:

#	updatestamp = 'query'

if 'intervene' in field :

	intervene = field['intervene'].value

else:

#	intervene = 'NoIntervene'
	intervene = 'Choose'


if logproc.validCookie() :
#if True :

	username, end, term, logcrew2 = logproc.getUsername()
			
	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :
		
		now = datetime.datetime.now()
		dt = now.strftime('%Y-%m-%d %H:%M:%S')


		clean_itemtitle = html.escape( itemtitle, quote=True )
		clean_itemtext = html.escape( itemtext, quote=True )

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
		history_text += '<br>**********<br>timestamp: ' + dt + ' ( ' + username + ' ) <br>' 

		history_text += 'title: ' + clean_itemtitle + '<br>' 
		history_text += 'text: ' + clean_itemtext + '<br>' 

		cursor.execute("update items set itemtime = '%s', itemtitle = '%s', itemtext = '%s', type = '%s', downtime = '%s', subsystem = '%s', \
		status = '%s', user = '%s', logcrew = '%s', history = concat( '%s', history ), updatestamp = '%s', intervene = '%s' where idno = '%s'" \
		% ( itemtime, clean_itemtitle, clean_itemtext, type, downtime, subsystem, status, user, logcrew, history_text, dt, intervene, idno ) )

#		cursor.execute("update items set itemtime = '%s', itemtitle = '%s', itemtext = '%s', type = '%s', downtime = '%s', \
#		subsystem = '%s', status = '%s', user = '%s', logcrew = '%s', history = concat( '%s', history ) where idno = '%s'" \
#		% ( itemtime, clean_itemtitle, clean_itemtext, type, downtime, subsystem, status, user, logcrew, history_text, idno ) )

	pagename = '<center><b>Summit Log Item</b><br><FONT SIZE=2>[ ' + username  + ' expires: ' + end + ' ]<FONT SIZE=3><br></center>'

	maintext = pagename

	#maintext = ''

	cursor.execute("select idno, dayidno, date, day, itemtime, itemtitle, itemtext, \
	user, type, downtime, subsystem, status, timestamp, history, logcrew, contact1, coalesce( updatestamp, ''), coalesce( intervene, '') from items where idno = '%s'" % ( idno ) )

#	cursor.execute("select idno, dayidno, date, day, itemtime, itemtitle, itemtext, \
#	user, type, downtime, subsystem, status, timestamp, history, logcrew, contact1 from items where idno = '%s'" % ( idno ) )

	numrows=cursor.rowcount
#	numrows = 0
#	maintext += 'rows: ' + str( numrows ) + '<br>'
	#maintext += "<form method=post action='./logone.py?'>"

	# outside frame
#	maintext += '<table><tr><th>Reports<hr></th><th>Status<hr></th></tr></table>'

	# left column
	#maintext += '<tr><td valign=top>'

	if numrows == 1 :

		row = cursor.fetchone()

		item_idno = row[0]
		item_dayidno = row[1]


		item_date = row[2]
		item_day = row[3]

		item_time = row[4]
		item_title = row[5]
		item_text = row[6]

		item_user = row[7]

		item_type = row[8]

		item_downtime = row[9]
		item_subsystem = row[10]

		item_status = row[11]

		item_timestamp = row[12]

		item_history = row[13]

		item_logcrew = row[14]
		item_contact1 = row[15]
		
		item_updatestamp = str( row[16] )

		item_intervene = row[17]
		
		item_intervene = item_intervene.strip()
		
		if item_intervene == 'NoIntervene' :
			
			item_intervene = 'Choose'

		types = ( 'Comment', 'Trouble', 'Summary', 'Warning', 'Important' )

		types2 = "<select name=type size=1>"

		for typ in types :

			if typ == item_type :

				types2 += "<option value=%s selected>%s" % ( typ, typ )

			else:

				types2 += "<option value=%s>%s" % ( typ, typ )

		types2 += "</select>"

		subsystem2 = "<select name=subsystem size=1>"

		subsystems = ( '-none-', 'Tel', 'Inst', 'SOSS', 'Weather', 'Operations', 'Others' )

		for subsys in subsystems :

			if subsys == item_subsystem :

				subsystem2 += "<option value=%s selected>%s" % ( subsys, subsys )

			else:

				subsystem2 += "<option value=%s>%s" % ( subsys, subsys )

		subsystem2 += "</select>"


		statii = ( 'Completed', 'Cancel', 'Incomplete' )

		status2 = "<select name=status size=1>"

		for stati in statii :

			if stati == item_status :

				status2 += "<option value=%s selected>%s" % ( stati, stati )

			else:

				status2 += "<option value=%s>%s" % ( stati, stati )

		status2 += "</select>"


	#	logcrews = ( 'DC', 'TO', 'IO', 'All' )
		logcrews = ( 'DC', 'TO', 'IO' )
		logcrew3 = "<select name=logcrew size=1>"

		for lcrew in logcrews:

			if lcrew == item_logcrew :

				logcrew3 += "<option value=%s selected>%s" % ( lcrew, lcrew )

			else:

				logcrew3 += "<option value=%s>%s" % ( lcrew, lcrew )

		logcrew3 += "</select>"


#		intervenes = ( 'NoIntervene', 'Operator-Required', 'SA-Required', 'TelDiv-Required', 'OCS-Required', 'DC-Required' )

#		intervenes = ( 'No', 'Yes', )
		intervenes = ( 'Choose', 'No', 'Yes' )

		intervene2 = "<select name=intervene size=1>"

		for inter in intervenes :

			if inter == item_intervene :

				intervene2 += "<option value=%s selected>%s" % ( inter, inter )

			else:

				intervene2 += "<option value=%s>%s" % ( inter, inter )

		intervene2 += "</select>"


	# buttons for DC-Night-WP

		buttontxt = '<center><table cellspacing=5 cellpadding=5 rules=all border=1>'

		if logcrew == 'All' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>All</a></td>' % ( 'pink', date, 'All' )
		else:	
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>All</a></td>' % ( 'yellow', date, 'All' )  

		if logcrew == 'DC' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>DayCrew</a></td>' % ( 'pink', date, 'DC' ) 
		else:
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>DayCrew</a></td>' % ( 'yellow', date, 'DC' ) 

		if logcrew == 'WP' :
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>WorkPlan</a></td>' % ( 'pink', date, 'WP' ) 
		else: 
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>WorkPlan</a></td>' % ( 'yellow', date, 'WP' ) 

		if logcrew == 'TO' :

			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>Night</a></td>' % ( 'pink', date, 'TO' )
		else:
			buttontxt += '<td bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>Night</a></td>' % ( 'yellow', date, 'TO' )  


		buttontxt += '</table></center><br>'



	# items query

	# crew section

	#	if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Enter' ) ) : 
	#	if  method == 'POST' and field['action'].value == 'Save'  : 
		if  method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' or field['action'].value == 'Delete') ): 

			formtxt = "<br><center><a href = logone.py?date=%s>Return to NightLogs<br>%s</a><br><br>" % ( item_date, item_date )

	# left column end - start right column
			
			if  int( idno ) > 0 and ( ( method == 'GET' and  todo == 'delete' ) or ( method == 'POST' and field['action'].value == 'Delete') ):
				
				cursor.execute("delete from items where idno = '%s'" % ( idno ) )
				itemtxt = "<b>This Item is Deleted</b><br><br>"
			
			else:
				formtxt += "<form method=post action=./itemone.py?idno=%s><input type=submit name=action value='Edit'> <input type=submit name=action value='Delete'></form>" % ( idno )

				formtxt += "<form method=post action=../fatsedit.php?idno=0><input type=hidden name=item2 value='%s'>" % ( item_title )
				formtxt += "<input type=hidden name=text2 value='%s'><input type=hidden name=logsidno value='%s'><center><input type=submit name=action value='Make FATS'></form>" % ( item_text, idno )

				itemtxt = ""

			itemtxt += '<table cellpadding=3 cellspacing=3>'
			itemtxt += '<tr><td class=right>Date:</td><td><b>%s</b> - %s</td></tr>' % ( item_date, item_day )
	#		itemtxt += '<tr><td class=right>LogCrew:</td><td>%s</td></tr>' % ( item_logcrew )
			itemtxt += '<tr><td class=right>Time:</td><td><b>%s</b></td></tr>' % ( item_time )
#			itemtxt += '<tr><td class=right>Type:</td><td>%s | Status: %s | SubSystem: %s | Down: %s | Intervene: %s</td></tr>' % ( item_type, item_status, item_subsystem, item_downtime, item_intervene )
			itemtxt += '<tr><td class=right>Type:</td><td><b>%s</b> | Status: <b>%s</b> | SubSystem: <b>%s</b> | Down: <b>%s</b> | SummitAccess: <b>%s</b></td></tr>' % ( item_type, item_status, item_subsystem, item_downtime, item_intervene )
#			itemtxt += '<tr><td class=right>Time:</td><td><FONT SIZE=3>%s | Type: %s | Status: %s | SubSystem: %s | Down: %s</td></tr>' % ( item_time, item_type, item_status, item_subsystem, item_downtime )
			itemtxt += '<tr><td class=right colspan=2><hr></td></tr>'
			itemtxt += '<tr><td class=right>Title:</td><td><FONT SIZE=5>%s</td></tr>' % ( item_title )
			itemtxt += '<tr><td class=right valign=top>Text:</td><td><FONT SIZE=5><pre>%s</pre></td></tr>' % ( item_text )
			itemtxt += '<tr><td class=right>User:</td><td>%s [ %s ] | Crew: %s</td></tr>' % ( item_user, item_contact1, item_logcrew )
	#		itemtxt += '<tr><td>Type:</td><td>%s</td></tr>' % ( item_type )
	#		itemtxt += '<tr><td>DownTime:</td><td>%s</td></tr>' % ( item_downtime )
	#		itemtxt += '<tr><td>Status:</td><td>%s</td></tr>' % ( item_status )
	#		itemtxt += '<tr><td>Subsystem:</td><td>%s</td></tr>' % ( item_subsystem )
	#		itemtxt += '<tr><td>IDNo:</td><td>%s</td></tr>' % ( item_idno )
			itemtxt += '<tr><td class=right>TimeStamp:</td><td>%s | IDNo: %s</td></tr>' % ( item_timestamp, item_idno )
			itemtxt += '<tr><td class=right>UpdateStamp:</td><td>%s</tr>' % ( item_updatestamp )
#			itemtxt += '<tr><td class=right>Intervene:</td><td>%s</tr>' % ( item_intervene )
			itemtxt += '<tr><td class=right valign=top>History:</td><td>%s</td></tr>' % ( item_history )
			itemtxt += '</table></center>'


	# 1-2 column break

			columntxt = '</td><td valign=top>'


	#		maintext = maintext + buttontxt + columntxt + formtxt + crewtxt + weathertxt + progtxt
			maintext = maintext + formtxt + itemtxt 

	#	else :

		if  method == 'POST' and field['action'].value == 'Edit' : 

			formtxt = "<form method=post action=./itemone.py?idno=%s>" % ( idno )
			formtxt += "<center><input type=submit name=action value='Save'>  <input type=submit name=action value='Cancel'><br>" 

			itemtxt = ""
			itemtxt += '<br><table>'

			itemtxt += "<tr><td>LogDate:</td><td><b>%s</b> - %s</td></tr>" % ( item_date, item_day )

			itemtxt += "<tr><td>Time:</td><td><b><input type=text name=itemtime value='%s' size=25></b></td></tr>" % ( item_time )

#			itemtxt += "<tr><td>Time:</td><td><input type=text name=itemtime value='%s'> Type: %s Status: %s SubSystem: %s Down: <input type=text name=downtime value='%s' size=5></td></tr>" % ( item_time, types2, status2, subsystem2, item_downtime )	
			itemtxt += "<tr><td>Type:</td><td>%s Status: %s SubSystem: %s Down: <input type=text name=downtime value='%s' size=5> SummitAccess: %s</td></tr>" % ( types2, status2, subsystem2, item_downtime, intervene2 )	

			itemtxt += "<tr><td>Title:</td><td><input type=text name=itemtitle value='%s' size=80 maxsize=200></td></tr>" % ( item_title )

			itemtxt += "<tr><td valign=top>Text:</td><td><textarea name=itemtext rows=30 cols=102>%s</textarea></td></tr>" % ( item_text )			

#			itemtxt += "<tr><td>User:</td><td><input type=text name=user value='%s' size=20> | Crew: %s </td></tr>" % ( item_user, logcrew2 )	
			itemtxt += "<tr><td>User:</td><td><input type=text name=user value='%s' size=20> | Crew: %s </td></tr>" % ( item_user, logcrew3 )	

	#		itemtxt += "<tr><td>Type:</td><td>%s</td></tr>" % ( types2 )

	#		itemtxt += "<tr><td>DownTimeMin:</td><td><input type=text name=downtime value='%s' size = 5></td></tr>" % ( item_downtime )

	#		itemtxt += "<tr><td>Status:</td><td>%s</td></tr>" % ( status2 )

	#		itemtxt += "<tr><td>SubSystem:</td><td><input type=text name=subsystem value='%s'></td></tr>" % ( item_subsystem )	


			itemtxt += '<tr><td>TimeStamp:</td><td>%s</td></tr>' % ( item_timestamp )

			itemtxt += '<tr><td class=right>UpdateStamp:</td><td>%s</tr>' % ( item_updatestamp )
#			itemtxt += '<tr><td class=right>Intervene:</td><td><input type=text name=intervene value=%s></tr>' % ( item_intervene )

			itemtxt += '<tr><td>History:</td><td>%s</td></tr>' % ( item_history )
			itemtxt += '</table></center>'
			itemtxt += '</form>'
			
			
			

	#		maintext = maintext + crewtxt + weathertxt
			maintext = maintext

			maintext = maintext + formtxt + itemtxt 



	else :

		maintext += '<tr><td colspan=8>No Summit Item Available ' + str( idno ) + '</td></tr>'

else:

#	maintext = "OPAL Login Required <a href='../login.php'>Here</a><br>"
        maintext = logproc.returnLogin()		

#maintext += '</table></form>'

#maintext = ''	
printHTML( maintext )
	
