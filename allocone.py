#! /usr/local/python

import datetime
import cgi
import os
import sys
import cgitb; cgitb.enable();
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import logproc3 as logproc
import dbconnect
import calendar
from io import BytesIO
import base64

sys.path.insert( 0, '/usr/lib64/python3.6/site-packages/' )
#import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

field=cgi.FieldStorage()

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

#maxday = now + datetime.timedelta( days = 15 )


def orderTable ( order ) :

	orderTable = '<table rules=all border=2><tr>'
	
	if '1' in order : 
		orderTable += '<td bgcolor=pink width=6>1</td>'
	else :
		orderTable += '<td bgcolor=white width=6></td>'
	if '2' in order : 
		orderTable += '<td bgcolor=pink width=6>2</td>'
	else :
		orderTable += '<td bgcolor=white width=6></td>'
	if '3' in order : 
		orderTable += '<td bgcolor=pink width=6>3</td>'
	else :
		orderTable += '<td bgcolor=white width=6></td>'
	if '4' in order : 
		orderTable += '<td bgcolor=pink width=6>4</td>'
	else :
		orderTable += '<td bgcolor=white width=10></td>'
		
	orderTable += '</tr></table>'
		

	return ( orderTable )

def orderTableEdit ( order ) :

	orderTable = '<table rules=all border=2><tr>'

	if '1' in order : 
		orderTable += "<td bgcolor=pink width=60 class=center>1<br><input type=checkbox name=order1 value='1' checked><br>(18-21)</td>"
	else :
		orderTable += "<td bgcolor=white width=60 class=center>1<br><input type=checkbox name=order1 value='1'><br>(18-21)</td>"
	if '2' in order : 
		orderTable += "<td bgcolor=pink width=60 class=center>2<br><input type=checkbox name=order2 value='2' checked><br>(21-00)</td>"
	else :
		orderTable += "<td bgcolor=white width=60 class=center>2<br><input type=checkbox name=order2 value='2' ><br>(21-00)</td>"
	if '3' in order : 
		orderTable += "<td bgcolor=pink width=60 class=center>3<br><input type=checkbox name=order3 value='3' checked><br>(00-03)</td>"
	else :
		orderTable += "<td bgcolor=white width=60 class=center>3<br><input type=checkbox name=order3 value='3' ><br>3<br>(00-03)</td>"
	if '4' in order : 
		orderTable += "<td bgcolor=pink width=60 class=center>4<br><input type=checkbox name=order4 value='4'  checked><br>(03-06)</td>"
	else :
		orderTable += "<td bgcolor=white width=60 class=center>4<br><input type=checkbox name=order4 value='4' ><br>4<br>(03-06)</td>"
	
	orderTable += "</tr></table>"
	

	return ( orderTable )

if 'observers' in field:

	observers=field[ 'observers' ].value
	
else:

	observers=''


if 'remote' in field:

	remote=field[ 'remote' ].value
	
else:
	
	remote=''

if 'staff' in field:

	staff=field[ 'staff' ].value
	
else:
	
	staff = ''


if 'idno' in field:

	idno=field[ 'idno' ].value
	
else:
	
	idno = '0'

if 'date' in field:

	date=field[ 'date' ].value
	
else:

	date = '0000-00-00'

if 'cal' in field:

	cal = field[ 'cal' ].value

else:

	cal = 'Y'


if 'order1' in field:

	order1 = field[ 'order1' ].value

else:

	order1 = '0'
	
if 'order2' in field:

	order2 = field[ 'order2' ].value

else:

	order2 = '0'
	

if 'order3' in field:

	order3 = field[ 'order3' ].value

else:

	order3 = '0'

if 'order4' in field:

	order4 = field[ 'order4' ].value

else:

	order4 = '0'

orderString = ''

if order1 == '1' :

	orderString += order1

if order2 == '2' :

	orderString += order2
		
if order3 == '3' :

	orderString += order3

if order4 == '4' :

	orderString += order4

if 'pid' in field:

	pid = field[ 'pid' ].value

else:

	pid = '0'

if 'instr' in field:

	instr = field[ 'instr' ].value

else:

	instr = 'HSC'

if 'cal2' in field:

	cal2 = field[ 'cal2' ].value

else:

	cal2 = ''	

if 'del2' in field:

	del2 = field[ 'del2' ].value

else:

	del2 = ''	
	
method=os.environ.get("REQUEST_METHOD","")


def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
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
	toppg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	toppg += css_text
	
	bottompg = "</HEAD><BODY>"
	bottompg += maintext
	bottompg += "</BODY></HTML>"
	
	print( toppg )
	
	print( bottompg )



dbconn2=dbconnect.opalconn()
db2=MySQLdb.connect( host=dbconn2[0], user=dbconn2[1], passwd=dbconn2[2], db=dbconn2[3] )
db2.autocommit(1)

cursor1 = db2.cursor()

cursor2 = db2.cursor()
cursor3 = db2.cursor()
cursor4 = db2.cursor()
cursor5 = db2.cursor()

logcrew = 'WP'

maintext = "<center><b>Subaru Calender - Night Allocation</b><br><br>" + logproc.getMenu() + '<br>' 
maintext += logproc.getOPALMenu() + '<br>' 

if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 and date != '0000-00-00' :
	
#	cursor2.execute("update alloc set observers = '%s', remote = '%s', staff = '%s', cal = '%s', datein = '%s' where idno = '%s'" \
#	% ( observers, remote, staff, cal, date, idno ) )
	cursor2.execute("update alloc set observers = '%s', remote = '%s', staff = '%s', datein = '%s', cal = '%s', order1 = '%s', instr = '%s' where idno = '%s'" \
	% ( observers, remote, staff, date, cal, orderString, instr, idno ) )


if method == 'GET' and int( idno ) > 0 and ( cal2 == 'Y' or cal2 == 'N' ) :

	cursor2.execute("update alloc set cal='%s' where idno = '%s'" \
	% ( cal2,  idno ) )

if method == 'GET' and int( idno ) > 0 and ( del2 == 'H' or del2 == 'D') :

	cursor2.execute("update alloc set delivery = '%s' where idno = '%s'" \
	% ( del2,  idno ) )
	
thisid = 'none'

if method == 'GET' and int( pid ) > 0 and int( idno ) == 0 :

	cursor2.execute("select number from counter where file = '%s' " % ( 'alloc' ) )
	raw=cursor2.fetchone()
	thisidno = raw[0]
#	thisid += 'get>0==0 - ' + str( thisidno )
#	thisidno = raw[0]
#	thisid = str( thisidno )
	nextid = thisidno + 1
	cursor2.execute("update counter set number=%s where file='%s'" % ( nextid, 'alloc' ) )

	cursor2.execute("select idno, propid, name, piidno, pw, gid, nights, instr, datein, dateout, sem, \
	first, last, username, comment, subidno, stn_flag, ulogin, eng, public, engseq, pwo \
	from props where idno = '%s'" % ( pid ) )


	ruw=cursor2.fetchone()
	
	numrows2 = cursor2.rowcount
#	maintext += 'numrows2: ' + str( numrows2 )
	if numrows2 == 1 :

		props_piidno = ruw[3]
		props_sem = ruw[10]

		props_propid = ruw[1]
		props_gid = ruw[5]
		props_instr = ruw[7]
		props_name = ruw[11] + ' ' + ruw[12]
		props_first= ruw[11]
		props_last= ruw[12]
		props_username = ruw[13]
		
#		props_propid = 'propid'
#		props_gid = 'gid'
#		props_instr = 'instr'

	#	cursor2.execute("update alloc set observers = '%s', remote = '%s', staff = '%s', cal = '%s', datein = '%s' where idno = '%s'" \
	#	% ( observers, remote, staff, cal, date, idno ) )

#		cursor2.execute("insert into alloc ( idno, propidno, instr, propid, gid, datein, dateout, cal, order1, first, last, sem, piidno, nights, delivery, \
#			observers, remote, staff, username, comment ) \
#			values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " \
#		% ( thisid, pid, props_instr, props_propid, props_gid, today, today, 'N', '1234', \
#		props_first, props_last, props_sem, props_piidno, 1, 'D', '', '', '', props_username, '' ) )

		cursor2.execute("insert into alloc ( idno, propidno, instr, propid, gid, datein, dateout, cal, order1, first, last, sem, piidno, nights, delivery, \
		observers, remote, staff, username, comment ) \
		values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " \
		% ( 0, pid, props_instr, props_propid, props_gid, today, today, 'N', '1234', \
		props_first, props_last, props_sem, props_piidno, 1, 'D', '', '', '', props_username, '' ) )

#		thisid2 = cursor2.execute("select last_insert_id()")
		cursor2.execute("select last_insert_id()")
#		thisid = cursor2.execute("select mysql_insert_id()")
#		thisid = str( thisid2 )
#		cursor2.execute("select max( idno ) from alloc")
		auto_idno = cursor2.fetchone()
		thisid = auto_idno[0]
	
	idno = str( thisid )

safeGets = ( 'Save', 'Save Night', 'Cancel' )

if int( idno )  >  0 :

	cursor4.execute("select idno, propid, gid, last, first, observers, remote, staff, datein, instr, cal, order1, propidno, comment, delivery \
	from alloc where idno='%s'" % ( idno ) )
							
	numrows4 = cursor4.rowcount
	
	maintext += 'numrows4: ' + str( numrows4 )
#	maintext += 'numrows2: ' + str( numrows2 )

	daywarning = ''
	
	nitewarning = ''

#	maintext += 'numrows4: ' + str( numrows4 ) + '<br>' 
#	maintext += '<br><a href = ./sumcal.py?date=%s>return to Calendar<br>%s</a><br><br>' % ( date, date )
#	maintext += '<br><a href = ./sumcal.py?date=%s>return to Calendar<br>%s</a><br><br>' % ( date, date )
#	maintext += "<br><a href = ./sumcal.py?>return to Calendar</a><br><br>"
	
	if method == 'GET' or ( method == 'POST' and field['action'].value in safeGets  )  :
	
#		itemstext = "<form method=post action='./allocone.py?'><input type=hidden name=idno value=%s><input type=hidden name=date value=%s><input type=submit name=action value='Save'><br><br>" % ( idno, date )
		itemstext = "<form method=POST action='./allocone.py?'><input type=hidden name=idno value=%s><input type=submit name=action value='Edit'> \
		<br><br>" % ( idno )
		
	else : 
	
		itemstext = "<form method=POST action='./allocone.py?'><input type=hidden name=idno value=%s> \
		<input type=submit name=action value='Save'> <input type=submit name=action value='Cancel'><br><br>" % ( idno )
#		itemstext = "<form method=get action='./allocone.py?'><input type=hidden name=idno value=%s><input type=submit name=action value='Edit'><br><br>" % ( idno )
	

	itemstext += '<table><td valign=top>'
		
	itemstext += '<table>'
	
	
	if numrows4 == 1:
	
		result4 = cursor4.fetchone()
		
		alloc_idno = str( result4[0] )
		alloc_propid = result4[1]
		alloc_gid = result4[2]
		alloc_last = result4[3]
		alloc_first = result4[4]
		alloc_observers = result4[5]
		alloc_remote = result4[6]
		alloc_staff = result4[7]
		alloc_datein = str( result4[8] )
		alloc_datein2 = result4[8]
		alloc_instr = result4[9]
		alloc_cal = result4[10]
		alloc_order1 = result4[11]
		alloc_propidno = result4[12]
		alloc_comment = result4[13]
		alloc_delivery = result4[14]
		
		alloc_orderTable = orderTable ( alloc_order1 )
		alloc_orderTableEdit = orderTableEdit ( alloc_order1 )
		
		alloc_day = alloc_datein2.strftime('%a')

#		cursor5.execute("select name, code from instr order by name" )
#		cursor5.execute("select instr, code from propinst where propidno = %s" % ( alloc_propidno ) )
							
#		numrows5 = cursor5.rowcount
#		instrString='No Instruments'
#		instrCtrl = '<select size=1 name=instr>'
#		if numrows5 > 0 :
#			instrString=' [ '

#			for result5 in cursor5.fetchall() :

#				propinstr = result5[0]
#				propinstrcode = result5[1]
#
#				if alloc_instr == propinstr :
#					instrCtrl += "<option value=%s selected>%s - %s" % ( propinstr, propinstr, propinstrcode )
#				else: 
#					instrCtrl += "<option value=%s>%s - %s" % ( propinstr, propinstr, propinstrcode )
##				instrString += propinstr + ', ' 
#			instrString += ' ] (' + str( numrows5 )+ ')'
#		instrCtrl += '</select>'


		opw = 'none'
		prop_gid = ''
		prop_propid = ''
		prop_engseq = 0
		
		first_idno = 1
		first_propid = ''
		first_instr= ''
		first_date='0000-00-00'

		last_idno = 1
		last_propid = ''
		last_instr= ''
		last_date='0000-00-00'
		
		shell_tsr = 'None'
		last_tsr = 'None'

		cursor5.execute("select idno, propid, instr, date from tsr where date = '%s' and instr='%s' " % ( '1901-01-01', alloc_instr ) )
		numrows5 = cursor5.rowcount
		if numrows5 > 0 :

			raw = cursor5.fetchone()
			first_idno = raw[0]
			first_propid= raw[1]
			first_instr= raw[2]
			first_date = raw[3]
			
			shell_tsr = "<a href=tsrone.py?idno=%s>%s %s - %s</a>" % ( first_idno, first_date, first_instr, first_propid )
		
		cursor5.execute("select idno, propid, instr, date from tsr where instr='%s' order by date desc" % ( alloc_instr ) )
		numrows5 = cursor5.rowcount
		if numrows5 > 0 :

			raw = cursor5.fetchone()
			last_idno = raw[0]
			last_propid= raw[1]
			last_instr= raw[2]
			last_date= raw[3]
		
			last_tsr = "<a href=tsrone.py?idno=%s>%s %s - %s</a>" % ( last_idno, last_date, last_instr, last_propid )
		

		cursor3.execute("select gid, engseq, propid from props where idno = '%s' " % ( alloc_propidno ) )
		numrows3 = cursor3.rowcount
		#		opw = 'none'

		if numrows3 == 1:

			ruw = cursor3.fetchone()
			prop_gid = ruw[0]
			prop_engseq = ruw[1]
			prop_propid = ruw[2]
			prop_propid = prop_propid.strip()
			
			
			if "EN" in alloc_propid and len( prop_engseq ) == 3 :

				cursor3.execute("select pwo from props where sem='S22A' and engseq = '%s'" % ( prop_engseq ) )
				numrows3 = cursor3.rowcount

				if numrows3 == 1:

					raw = cursor3.fetchone()
					opw = raw[0]
					opw = opw.strip()
	

			else :

				cursor3.execute("select opw from gidpw where gid='%s'" % ( prop_gid ) )
				numrows3 = cursor3.rowcount

				if numrows3 == 1:

					raw = cursor3.fetchone()
					opw = raw[0]
					opw = opw.strip()
#		else :
#
#			prop_gid = ''
#			prop_propid = ''
#			prop_engseq = 0
#			opw = 'none'
		img = Image.open('../bluebox.jpg')
		I1 = ImageDraw.Draw(img)
		myFont = ImageFont.truetype('DejaVuSans.ttf', 50 )
		I1.text((24, 10), opw, font=myFont, fill="#000000")
# blanched almond #ffebcd")
#		img.save( '/etc/httpd/logs/bb3.jpg' )
#		os.mkdir( './image/' )
#		img.save( '/tmp/bb3.jpg', 'JPEG' )
		byte_io = BytesIO()

		img.save( byte_io, 'JPEG' )

		str_equivalent_image = base64.b64encode(byte_io.getvalue()).decode()

		imageSource = "<img src='data:image/png;base64," + str_equivalent_image + "'/>"
		
#		cmd = '/var/www/html/sumlogs/testimage.py ' + prop_gid + ' ' + opw
#		os.system( cmd )
		
		cursor5.execute("select name, code from instr where status='Active' order by name")

		foundInstr = False
									
		numrows5 = cursor5.rowcount
		instrString='No Instruments'
		instrCtrl = '<select size=1 name=instr>'
		if numrows5 > 0 :
#			instrString=' [ '
			for result5 in cursor5.fetchall() :

				instrname = result5[0]
				instrcode = result5[1]

				if alloc_instr == instrname :
					
					foundInstr = True

					instrCtrl += "<option value=%s selected>%s - %s" % ( instrname, instrname, instrcode )

				else: 

					instrCtrl += "<option value=%s>%s - %s" % ( instrname, instrname, instrcode )

#				instrString += instrname + ', ' 
#			instrString += ' ] (' + str( numrows5 )+ ')'

		if foundInstr == False :
		
			instrCtrl += "<option value=%s selected>%s - %s" % ( alloc_instr, alloc_instr, 'retired' )		
			
		instrCtrl += '</select>'
		
				#			statusCtrl = '<select size=1 name=status>'
				#			for status2 in status1 :
				#				if car_status == status2 :
				#					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
				#				else:
				#					statusCtrl += '<option value=%s>%s' % ( status2, status2 )           
				#			statusCtrl += '</select>'
		


		
		if method == 'GET' or ( method == 'POST' and field['action'].value in safeGets  ) :

			if alloc_cal == 'Y':

				alloc_cal2 = 'Yes'
			
				buttontext = "( <a href=allocone.py?idno=%s&cal2=%s>to %s</a> )" % ( alloc_idno, 'N', 'No' )
			
			else :

				alloc_cal2 = 'NO'
			
				buttontext = "( <a href=allocone.py?idno=%s&cal2=%s>to %s</a> )"  % ( alloc_idno, 'Y', 'Yes' )

			if alloc_delivery == 'D':

				alloc_del2 = 'Deliver'
		
				buttontext2 = "( <a href=allocone.py?idno=%s&del2=%s>to %s</a> )" % ( alloc_idno, 'H', 'Hold' )
		
			else :

				alloc_del2 = 'Hold'
		
				buttontext2 = "( <a href=allocone.py?idno=%s&del2=%s>to %s</a> )"  % ( alloc_idno, 'D', 'Deliver' )
			
#			itemstext += '<tr><td>Calendar?</td><td>%s</td></tr>' % ( alloc_cal ) 
#			itemstext += '<tr><td>Calendar? %s</td><td>%s</td><td></td></tr>' % ( buttontext, alloc_cal ) 
#			itemstext += '<tr><td>Delivery %s</td><td>%s</td><td></td></tr>' % ( buttontext2, alloc_delivery ) 

			itemstext += '<tr><td bgcolor=lime colspan=4>Current Info</td></tr>' 		
			itemstext += '<tr><td>Date</td><td>%s %s</td><td></td><td></td></tr>' % ( alloc_datein, alloc_day )
			itemstext += '<tr><td>PropID</td><td><a href=propone.py?idno=%s>%s</a></td><td></td><td></td></tr>' % ( alloc_propidno, alloc_propid ) 
			itemstext += '<tr><td>Ordering</td><td>%s</td><td></td><td></td></tr>' % ( alloc_orderTable ) 
			
#			itemstext += '<tr><td>GID</td><td>%s</td><td>Calendar? <b>%s</b></td><td>%s</td></tr>' % ( alloc_gid, alloc_cal, buttontext )
			itemstext += '<tr><td>GID</td><td>%s</td><td>Calendar? <b>%s</b></td><td>%s</td></tr>' % ( alloc_gid, alloc_cal2, buttontext )
#			itemstext += '<tr><td>Instr</td><td>%s</td><td>Delivery? <b>%s</b></td><td>%s</td></tr>' % ( alloc_instr, alloc_delivery, buttontext2 )
			itemstext += '<tr><td>Instr</td><td>%s</td><td>Delivery? <b>%s</b></td><td>%s</td></tr>' % ( alloc_instr, alloc_del2, buttontext2 )

			itemstext += '<tr><td>PI</td><td>%s %s</td><td></td><td></td></tr>' % ( alloc_first, alloc_last ) 
			itemstext += '<tr><td>Password</td><td>%s</td><td></td><td></td></tr>' % ( opw )
			itemstext += '<tr><td>PW Image</td><td>%s</td><td></td><td></td></tr>' % ( imageSource )

	##		itemstext += '<tr><td>Ordering</td><td>%s</td></tr>' % ( alloc_order1 ) 
#			itemstext += '<tr><td>Instruments:</td><td>%s</td></tr>' % ( instrString )

			itemstext += '<tr><td>Comment:</td><td colspan=2>%s</td><td></td></tr>' % ( alloc_comment )


#			itemstext += '<tr><td>OrderPosts:</td><td>%s %s %s %s</td></tr>' % ( order1, order2, order3, order4 )
#			itemstext += '<tr><td>OrderString:</td><td>%s</td></tr>' % ( orderString )
			
			itemstext += '<tr><td>Observers</td><td colspan=2>%s</td><td></td><td></td></tr>' % ( alloc_observers ) 
			itemstext += '<tr><td>SAs</td><td>%s</td><td colspan=2></td><td></td></tr>' % ( alloc_remote ) 		
			itemstext += '<tr><td>Operators</td><td>%s</td><td colspan=2></td><td></td></tr>' % ( alloc_staff )
			itemstext += '<tr><td>PropIDNo</td><td>%s</td><td colspan=2></td><td></td></tr>' % ( alloc_propidno )
			itemstext += '<tr><td>AllocIDNo</td><td>%s</td><td colspan=2></td><td></td></tr>' % ( alloc_idno )


				
		else:

			itemstext += '<tr><td bgcolor=lime colspan=2>Edit Info</td></tr>' 		

#			itemstext += '<tr><td>Date</td><td>%s %s</td></tr>' % ( alloc_datein, alloc_day )
			itemstext += "<tr><td>Date</td><td><input type=text name=date value='%s' size=20> %s</td></tr>" % ( alloc_datein, alloc_day )
#			itemstext += "<tr><td>PropID</td><td><a href=propone.py?idno=%s>%s</a></td></tr>" % ( alloc_propidno, alloc_propid ) 
#			itemstext += "<tr><td>GID</td><td>%s</td></tr>" % ( alloc_gid )
#			itemstext += "<tr><td>Instr</td><td>%s</td></tr>" % ( alloc_instr )
#			itemstext += "<tr><td>PI</td><td>%s %s</td></tr>" % ( alloc_first, alloc_last ) 
			itemstext += "<tr><td>Calendar?</td><td><input type=text name=cal value='%s' size=10</td></tr>" % ( alloc_cal ) 
#			itemstext += '<tr><td>Calendar?</td><td>%s</td></tr>' % ( alloc_cal ) 
#			itemstext += "<tr><td>%s</td><td><input type=text name=cal value='%s' size=10</td></tr>" % ( 'Delivery? ', alloc_delivery ) 
	#		itemstext += '<tr><td>Ordering</td><td>%s</td></tr>' % ( alloc_order1 ) 
			itemstext += '<tr><td>Instruments:</td><td>%s</td></tr>' % ( instrCtrl )
			itemstext += "<tr><td>Ordering</td><td>%s</td></tr>" % ( alloc_orderTableEdit ) 

			itemstext += "<tr><td>Observers</td><td><input type=text name=observers value='%s' size=50></td></tr>" % ( alloc_observers ) 
			itemstext += "<tr><td>SAs</td><td><input type=text name=remote value='%s' size=50></td></tr>" % ( alloc_remote ) 		
			itemstext += "<tr><td>Operators</td><td><input type=text name=staff value='%s' size=50></td></tr>" % ( alloc_staff )

			itemstext += '<tr><td>OrderPosts:</td><td>%s %s %s %s</td></tr>' % ( order1, order2, order3, order4 )
			itemstext += '<tr><td>OrderString:</td><td>%s</td></tr>' % ( orderString )

			itemstext += '<tr><td>PropIDNo</td><td>%s</td></tr>' % ( alloc_propidno )
			itemstext += '<tr><td>AllocIDNo</td><td>%s</td></tr>' % ( alloc_idno )

#			itemstext += '<tr><td>Date</td><td>%s %s</td></tr>' % ( alloc_datein, alloc_day )
#			itemstext += '<tr><td>PropID</td><td><a href=propone.py?idno=%s>%s</a></td></tr>' % ( alloc_propidno, alloc_propid ) 
#			itemstext += '<tr><td>GID</td><td>%s</td></tr>' % ( alloc_gid )
#			itemstext += '<tr><td>Instr</td><td>%s</td></tr>' % ( alloc_instr )
#			itemstext += '<tr><td>PI</td><td>%s %s</td></tr>' % ( alloc_first, alloc_last ) 
#			itemstext += '<tr><td>Calendar?</td><td>%s</td></tr>' % ( alloc_cal ) 
	#		itemstext += '<tr><td>Ordering</td><td>%s</td></tr>' % ( alloc_order1 ) 
#			itemstext += '<tr><td>Ordering</td><td>%s</td></tr>' % ( alloc_orderTable ) 
		  
		

	else:

		itemstext += 'No Allocation'
	
	
	itemstext += '</table>'

	itemstext += '</td><td valign=top>'
	
	itemstext += '<table cellspacing=3 cellpadding=3><th colspan=7 bgcolor=lime>Make New TSR</font></th></tr><th>Date</th><th>Instr</th><th>PI</th><th>Cal?</th><th colspan=3><b>Choose Default - Latest - Existing TSR</b></th></tr>'
	
	cursor5.execute("select idno from tsr where allocidno = '%s' " % ( alloc_idno ) )
	numrows5 = cursor5.rowcount
		
	tsridno = 0

	tsrfirst = "<a href=tsrone.py?idno=0&allocidno=%s&copy=first>%s</a>" % ( alloc_idno, 'Copy Shell-TSR' ) 
	tsrlast = "<a href=tsrone.py?idno=0&allocidno=%s&copy=last>%s</a>" % ( alloc_idno, 'Copy Last-TSR' )  

	if numrows5 > 0 :
	
		ruw = cursor5.fetchone()
		tsridno = ruw[0]
		
				
		tsrfirst = 'none'
		tsrlast = 'none'
		
		if alloc_cal == 'Y' and numrows5 == 0 :

			itemstext += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
			% ( alloc_datein, alloc_instr, alloc_last, alloc_cal, tsrlast, tsrfirst, 'New' )
		
		else:

			itemstext += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=tsrone.py?idno=%s>%s</a></td></tr>" \
			% ( alloc_datein, alloc_instr, alloc_last, alloc_cal, 'Copy Last-TSR', 'Copy Shell-TSR', tsridno, 'TSR (' + alloc_datein[5:10] + ')' )
	else :	
	
		itemstext += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
		% ( alloc_datein, alloc_instr, alloc_last, alloc_cal, tsrlast, tsrfirst, 'No-TSR' )
##		% ( alloc_datein, alloc_instr, alloc_last, alloc_cal, tsrfirst, tsrlast, 'No-TSR' )
				
	itemstext += '</td></table><br><hr><center>'
	
	itemstext += '<br>Last-TSR for %s: %s <br>' % (  alloc_instr, last_tsr )
	itemstext += '<br>Shell-TSR for %s: %s <br>' % (  alloc_instr, shell_tsr )

	itemstext += '</center></td></table>'
	
	itemstext += '</form>'
	
	maintext += itemstext + '</center>'
	
else:

#	maintext += 'No Allocation for IDNo: ' + idno + ' ' + thisid
	maintext += 'No Allocation for IDNo: ' + idno 

#maintext = 'tom text'
printHTML( maintext )


