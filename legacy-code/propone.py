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

from io import BytesIO
import base64

import random

sys.path.insert( 0, '/usr/lib64/python3.6/site-packages/' )
#import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


method=os.environ.get("REQUEST_METHOD","")

field = cgi.FieldStorage()

dbconn=dbconnect.opalconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor = db.cursor()
cursor2 = db.cursor()
cursor2.execute("set autocommit = 1")
cursor3 = db.cursor()
cursor4 = db.cursor()
cursor5 = db.cursor()

def getMembers ( gid ) :

	from ldap3 import Server, Connection, ALL

#	s = Server( host='squery.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	s = Server( host='sreg6.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	conn = Connection(s, auto_bind=True)
#conn.search('memberuid=winegar,ou=Group,dc=subaru,dc=nao,dc=ac,dc=jp', '(objectClass=*)' , 'SUBTREE', attributes=['dn'] )
	members = []
	maintext = '<table cellpadding=3 cellspacing=4><tr><th colspan=4 bgcolor=lime>STARS LDAP assigned USERS ( %s )</th></tr>' % ( len( members ) ) 
	
	try :
	
		conn.search('ou=Group,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=' +  gid + ')' , 'SUBTREE', attributes=['memberUid'] )

		for entry in conn.entries[0] :

			for entry2 in entry :

				group = str( entry2 )
				members.append ( group )


		if len( members ) > 0 :

			seq = 0

			for member in members :

				seq += 1

	#			memberuid, gecos, mail = getGecos( member )

#				conn2 = Connection(s, auto_bind=True)
				conn.search('ou=People,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=' +  member + ')' , 'SUBTREE', attributes=['gecos', 'mail'] )
				gecos = conn.entries[0]['gecos']
				mail = conn.entries[0]['mail']

				maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, member, gecos, mail )		
#				maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, member, '', '' )		
	except :
	
		maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( '0', 'none', 'none', 'none' )
			

	maintext += '</table>'
		
	return ( maintext )
	

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
	css_text += "</style>"


	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

#def main() :

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')




if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'

if 'propid' in field :

	propid = field['propid'].value
	
else:
	
	propid = ''

if 'gid' in field :

	gid = field['gid'].value
	
else:
	
	gid = ''

if 'instr' in field :

	instr = field['instr'].value
	
else:
	
	instr = ''


	
if 'sem' in field :

	sem = field['sem'].value
	
else:
	
	sem = 'S22A'
    
if 'comment' in field :

	comment = field['comment'].value
	
else:
	
	comment = ''

if 'engseq' in field :

	engseq = field['engseq'].value

else:

	engseq = '04'

if 'allocid' in field :

	allocid = field['allocid'].value

else:

	allocid = '0'

if 'alloc2_order' in field :

	order1 = field['alloc2_order'].value

else:

	order1 = '1234'

if 'alloc2_datein' in field :

	datein = field['alloc2_datein'].value

else:

	datein = today

if 'alloc2_instr' in field :

	instrAlloc = field['alloc2_instr'].value

else:

	instrAlloc = ''

if 'cal' in field :

	cal = field['cal'].value

else:

	cal = 'N'	
	
if 'uid' in field :

	uid = field['uid'].value

else:

	uid = '0'
	
#if 'instr2' in field :

#instr2 = field.getlist['instr2']

#else:

#	instr2 = ( )

thisid3 = 'start'	

if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )


	if method == 'POST' and field['action'].value == 'Save' and int( idno ) > 0 :

#		cursor2.execute("update cars set car = '%s', loc = '%s', phone = '%s', seq = '%s', status='%s', wheels='%s', comment='%s', type='%s' where idno = '%s'" \
#		% ( car, loc, phone, seq, status, wheels, comment, type, idno ) )
#		cursor2.execute("update cars set car = '%s', loc = '%s', phone = '%s', seq = '%s', status='%s', wheels='%s', comment='%s', type='%s', pass='%s' where idno = '%s'" \
#		% ( car, loc, phone, seq, status, wheels, comment, type, pass2,  idno ) )

#		cursor2.execute("update props set propid = '%s', gid = '%s', instr = '%s', datein = '%s', sem = '%s', comment = '%s' where idno = '%s'" \
#		% ( propid, gid, instr, datein, sem, comment, idno ) )		
		
		cursor2.execute("update props set propid = '%s', gid = '%s', instr = '%s', sem = '%s', comment = '%s' where idno = '%s'" \
		% ( propid, gid, instr, sem, comment, idno ) )		

		cursor2.execute("update alloc set propid = '%s', gid = '%s', comment = '%s' where propidno = '%s'" \
		% ( propid, gid, comment, idno ) )
		
		cursor2.execute("select instr from alloc where propidno = '%s'" \
		% ( idno ) )
		
		numrows2 = cursor2.rowcount
		
		if numrows2 == 1 :

			cursor2.execute("update alloc set instr = '%s' where propidno = '%s'" \
			% ( instr, idno ) )
			
		
		
		
		
	if method == 'POST' and field['action'].value == 'Save Night' and int( idno ) > 0 and int ( allocid ) > 0 and len( instrAlloc ) > 0 :
	
		cursor2.execute("update alloc set datein = '%s', order1 = '%s', instr = '%s'  where idno = '%s'" \
		% ( datein, order1, instrAlloc, allocid ) )	
		allocid = '0'	


	if method == 'GET' and int( uid ) > 0 and int( idno ) > 0 :

		cursor3.execute("select idno, first, last, username from users where idno='%s'" % ( uid ) )
		ruw=cursor3.fetchone()

		numrows3 = cursor3.rowcount

		if numrows3 == 1 :

			users_idno = ruw[0]
			users_first = ruw[1]
			users_last = ruw[2]
			users_username = ruw[3]	
	#		props_propid = 'propid'
	#		props_gid = 'gid'
	#		props_instr = 'instr'
#			thisid3 += user_first
			cursor2.execute("update props set piidno = '%s', first = '%s', last = '%s', username = '%s' where idno = '%s'" \
			% ( uid, users_first, users_last, users_username, idno ) )

			cursor2.execute("update alloc set piidno = '%s', first = '%s', last = '%s', username = '%s' where propidno = '%s'" \
			% ( uid, users_first, users_last, users_username, idno ) )

	if method == 'GET' and int( uid ) > 0 and int( idno ) == 0 :

		cursor2.execute("select number from counter where file = '%s' " % ( 'props' ) )
		raw=cursor2.fetchone()
		thisidno = raw[0]
	#	thisid += 'get>0==0 - ' + str( thisidno )
	#	thisidno = raw[0]
		thisid = str( thisidno )
		thisid = thisid.strip()

		thisid3 = thisid

		nextid = thisidno + 1
		cursor2.execute("update counter set number=%s where file='%s'" % ( nextid, 'props' ) )

		cursor2.execute("select idno, first, last, username from users where idno='%s'" % ( uid ) )
		ruw=cursor2.fetchone()

		numrows2 = cursor2.rowcount

		if numrows2 == 1 :

			users_idno = ruw[0]
			users_first = ruw[1]
			users_last = ruw[2]
			users_username = ruw[3]	
	#		props_propid = 'propid'
	#		props_gid = 'gid'
	#		props_instr = 'instr'
#			thisid3 += user_first
			thisid3 += users_last + ' ' + users_first + ' ' + str( users_idno ) + ' ' + users_username

			pepA = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', \
			'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' ]

			newpep = ''

			for i in random.sample( pepA , 12 ) :
				newpep += i

# Props insert

			cursor3.execute("insert into props ( idno, propid, name, piidno, pw, gid, nights, instr, datein, dateout, \
			sem, first, last, username, comment, subidno, eng, engseq, pwo, stn_flag, \
			ulogin, public, pep ) \
			values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
			'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
			'%s', '%s', '%s' )" \
			% ( thisid, 'S22B-999', 'testname', users_idno, '', 'o22015', 1, 'HSC', '2022-07-12', '2022-07-12', \
			'S22B', users_first, users_last, users_username, '', 0, 1, '', '', '', '', '', newpep ) )

			thisid3 += " thisid: " + thisid + '<br>'

			idno = thisid

# Alloc inserrt
			
			cursor2.execute("select number from counter where file = '%s' " % ( 'alloc' ) )
			raw=cursor2.fetchone()
			thisidno = raw[0]
		#	thisid += 'get>0==0 - ' + str( thisidno )
		#	thisidno = raw[0]
			thisid2 = str( thisidno )
			thisid2 = thisid2.strip()

			thisid3 = thisid2

			nextid = thisidno + 1

			cursor2.execute("update counter set number=%s where file='%s'" % ( nextid, 'alloc' ) )
			
#			cursor2.execute("insert into alloc ( idno, propidno, instr, propid, gid, datein, dateout, cal, order1, first, last, sem, piidno, nights, delivery, \
#				observers, remote, staff, username, comment ) \
#				values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " \
#				% ( thisid2, idno, 'HSC', 'S22B-999', 'o22015', '2022-07-12', '2022-07-12', 'N', '1234', \
#				users_first, users_last, 'S22B', users_idno, 1, 'Y', '', '', '', users_username, '' ) )
# 240205 modify alloc.idno for auto_increment

			cursor2.execute("insert into alloc ( idno, propidno, instr, propid, gid, datein, dateout, cal, order1, first, last, sem, piidno, nights, delivery, \
			observers, remote, staff, username, comment ) \
			values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'  ) " \
			% ( 0, idno, 'HSC', 'S22B-999', 'o22015', '2022-07-12', '2022-07-12', 'N', '1234', \
			users_first, users_last, 'S22B', users_idno, 1, 'Y', '', '', '', users_username, '' ) )

			
			thisid2 = cursor2.execute("select last_insert_id()")
			
			cursor2.execute("insert into propinst ( propidno, instr, code, propid ) \
				values ( '%s', '%s', '%s', '%s'  ) " \
				% ( idno, 'HSC', 'HSC', 'S22B-099' ) )

		#	cursor2.execute("update alloc set observers = '%s', remote = '%s', staff = '%s', cal = '%s', datein = '%s' where idno = '%s'" \
		#	% ( observers, remote, staff, cal, date, idno ) )
#			cursor2.execute("insert into props ( idno, propid, name, piidno, datein, dateout ) values \
#			( '%s', '%s', '%s', '%s', '%s', '%s' )" % ( thisid, 'PropID', 'Name', users_idno, '2022-07-12', '2022-07-12' ) )

#			cursor4.execute("insert into props ( idno, propid, name, piidno, pw, gid, nights, instr, datein, dateout, \
#			sem, first, last, username, comment, subidno, stn_flag, ulogin, eng, public, \
#			engseq, pwo ) values \
#			( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
#			 '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
#			 '%s', '%s' )" \
#			% ( thisid, 'PropID', ''. users_idno, '', 'GID', 1, 'HSC', '2022-07-12', '2022-07-12', \
#				'S22B', users_first, users_last, users_username, '', 0, '', '', 0, '' , '', '' ) )

#			idno = thisid
	
	pagename = '<center><b>Proposal Display</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'
	

	cmd = "select idno, propid, name, piidno, pw, gid, nights, instr, datein, dateout, sem, \
	first, last, username, comment, subidno, stn_flag, ulogin, eng, public, engseq, pwo \
	from props where idno = '%s'" % ( idno )
#	pagename += '<br>cmd: ' + cmd + '<br>'
	cursor.execute( cmd )

	
#	idno2 = 7997

#	cursor.execute("select idno, propid from props where idno = '%s' " % ( idno ) ) 
		
	numrows=cursor.rowcount
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
#	maintext += '<table cellpadding=3 cellspacing=3>'
	admin_users = ( 'winegar', 'noriko', 'letawsky', 'roth', 'takagi', 'pyo' )
	
#	if numrows == 0 :
	
#		maintext += 'zero records'
	
#	else:

#	if False :
	if numrows == 1 :
	
		row = cursor.fetchone()

		prop_idno = row[0]
		prop_propid = row[1]
#		prop_name = row[2]
		prop_piidno = str( row[3] )

#		prop_pw = row[4]

		prop_gid = row[5]

#		prop_nights = row[6]

		prop_instr = row[7]
		prop_datein = row[8]
#		prop_dateout = row[9]
		prop_sem = row[10]
		prop_first = row[11]
		prop_last = row[12]
		prop_username = row[13]
		prop_comment = row[14]
		prop_subidno = row[15]
#		prop_stn_flag = row[16]
#		prop_ulogin = row[17]
		prop_eng = row[18]
#		prop_public = row[19]
		prop_engseq = row[20]
		prop_pwo = row[21]

		opw='.none.'
		
		if "EN" in prop_propid and len( prop_engseq ) == 3 :

			cursor3.execute("select pwo from props where sem='S22A' and engseq = '%s' " % ( prop_engseq ) )
			numrows3 = cursor3.rowcount

			if numrows3 == 1:

				raw = cursor3.fetchone()
				opw = raw[0]
				opw = opw.strip()

		else :
		
			if len( prop_gid ) == 6 and prop_gid[0:1] == 'o' :
		
				cursor3.execute("select opw from gidpw where gid = '%s' " % ( prop_gid ) )
				numrows3 = cursor3.rowcount

				if numrows3 == 1:

					raw = cursor3.fetchone()
					opw = raw[0]
			
#			opw = prop_pwo
				
		img = Image.open('../bluebox.jpg')
		I1 = ImageDraw.Draw(img)
		myFont = ImageFont.truetype('DejaVuSans.ttf', 50 )
		# black text 00000 white FFFFFFF
		I1.text( ( 24, 10 ), opw, font=myFont, fill="#000000" )

		byte_io = BytesIO()

		img.save( byte_io, 'JPEG' )

		str_equivalent_image = base64.b64encode(byte_io.getvalue()).decode()

		imageSource = "<img src='data:image/png;base64," + str_equivalent_image + "'/>"

		
		safeGets = ( 'Save', 'Save Night', 'Cancel' )


#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

#		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' ) ) :
		if method == 'GET' or ( method == 'POST' and field['action'].value in safeGets  ) :
#		if False :

			if username in admin_users and allocid == "0" :

				maintext += "<form method=post action='propone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( prop_idno )


			maintext += '<table cellpadding=3 cellspacing=3><td valign=top>'
			
			maintext += '<table cellpadding=3 cellspacing=3>'
			maintext += "<tr><td class=right>IDNo</td><td>%s</td></tr>" % ( prop_idno ) 
			maintext += "<tr><td class=right>PropID</td><td>%s</td></tr>" % ( prop_propid ) 
			maintext += "<tr><td class=right>PI IDNO:</td><td>%s | ( <a href=starslist.py?propidno=%s>Assign-PI</a> )</td></tr>" % ( prop_piidno, prop_idno ) 
			maintext += "<tr><td class=right>PI Name:</td><td>%s</td></tr>" % ( prop_first + ' ' + prop_last ) 
			
			maintext += "<tr><td class=right>GID</td><td>%s</td></tr>" % ( prop_gid ) 
			maintext += "<tr><td class=right>Instr</td><td>%s</td></tr>" % ( prop_instr ) 
			maintext += "<tr><td class=right>DateIn</td><td>%s</td></tr>" % ( prop_datein ) 
			propbutton = "<a href=./proplist.py?sem=%s>%s</a>" % ( prop_sem, prop_sem)
			maintext += "<tr><td class=right>Sem</td><td>%s</td></tr>" % ( propbutton ) 
#			maintext += "<tr><td class=right>Sem</td><td>%s</td></tr>" % ( prop_sem ) 
			maintext += "<tr><td class=right>Username</td><td>%s</td></tr>" % ( prop_username )
			maintext += "<tr><td class=right>Comment</td><td>%s</td></tr>" % ( prop_comment )
			maintext += "<tr><td class=right>Eng?</td><td>%s</td></tr>" % ( prop_eng )
			maintext += "<tr><td class=right>EngSeq</td><td>%s</td></tr>" % ( prop_engseq )
##			maintext += "<tr><td class=right>Main Alloc IDNo</td><td>%s</td></tr>" % ( prop_subidno )

#			maintext += "<tr><td class=right>oAccount PW</td><td bgcolor=lemonchiffon><FONT SIZE=+2>%s</font></td></tr>" % ( opw )
#			maintext += "<tr><td class=right>oAccount PW2</td><td bgcolor=lemonchiffon><FONT SIZE=+2>%s</font></td></tr>" % ( prop_pwo )

			maintext += "<tr><td class=right>oAccount PW Image</td><td bgcolor=lemonchiffon><FONT SIZE=+2>%s</font></td></tr>" % ( imageSource )
#
			maintext += "</table>"
			maintext += "</td><td valign=top>"
			maintext += "<center><FONT SIZE=+1><b>Night Allocations</b> | <a href=./allocone.py?idno=0&pid=%s>Add Night</a><br></font></center><hr>" % ( idno )



			maintext += "<table cellspacing=3 cellpadding=3><th colspan=5></th></tr>"
			maintext += "<tr><th>Date</th><th>Instr</th><th>PI</th><th>Order</th><th>Cal?</th><th colspan=3 bgcolor=lime>Make TSR</th></tr>"
			
			cursor3.execute("select idno, propid, datein, instr, order1, cal, last from alloc where propidno = '%s' order by datein desc" % ( idno ) )
			
#			if False :
			for raw in cursor3.fetchall() :
			
				alloc_idno = raw[0]
				alloc_propid = raw[1]
				alloc_datein = str( raw[2] )
				alloc_instr = raw[3]
				alloc_order1 = raw[4]
				alloc_cal = raw[5]
				alloc_last = raw[6]

#				if alloc_idno == prop_subidno :
#				
#					alloc_idno = '<b>Master-</b>' 

				cursor4.execute("select idno from tsr where allocidno = '%s' " % ( alloc_idno ) )
				numrows4 = cursor4.rowcount
				
				tsridno = 0
				if numrows4 > 0 :
					ruw = cursor4.fetchone()
					tsridno = ruw[0]

				alloc_orderTable = orderTable( alloc_order1 )
				
				
#				maintext += "<tr><td><a href= propone.py?idno=%s&allocid=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
#				% ( idno, alloc_idno, alloc_datein, alloc_instr, alloc_last, alloc_orderTable, alloc_cal )
#				maintext += "<tr><td><a href= allocone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
#				% ( alloc_idno, alloc_datein, alloc_instr, alloc_last, alloc_orderTable, alloc_cal )

				maintext += "<tr><td><a href= allocone.py?idno=%s>%s</a></td>" %  ( alloc_idno, alloc_datein )
				maintext += "<td><a href=propone.py?idno=%s&allocid=%s>%s</a></td>" % ( prop_idno, alloc_idno, alloc_instr,  )
				maintext += "<td>%s</td><td>%s</td><td>%s</td>" % (  alloc_last, alloc_orderTable, alloc_cal )
				
				tsrfirst = 'none'
				tsrlast = 'none'

				
				if alloc_cal == 'Y' and numrows4 == 0 :
#				if False :
				
					tsrfirst = "<a href=tsrone.py?idno=0&allocidno=%s&copy=first>%s</a>" % ( alloc_idno, 'Copy Shell-TSR' ) 
					tsrlast = "<a href=tsrone.py?idno=0&allocidno=%s&copy=last>%s</a>" % ( alloc_idno, 'Copy Last-TSR' )  

					maintext += "<td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsrlast, tsrfirst, 'New' )
				
				else:

					maintext += "<td>%s</td><td>%s</td><td><a href=tsrone.py?idno=%s>%s</a></td></tr>" % ( 'Copy Shell-TSR', 'Copy Last-TSR', tsridno, 'TSR (' + alloc_datein[5:10] + ')' )
				
				editText = ''
		
				if int( allocid ) > 0 :
				
		

					cursor4.execute("select idno, propid, datein, instr, order1, cal, last from alloc where idno = '%s'" % ( allocid ) )
					numrows4 = cursor.rowcount

					if numrows4 == 1 :
			
						ruw = cursor4.fetchone()
						alloc2_idno = ruw[0]
						alloc2_propid = ruw[1]
						alloc2_datein = ruw[2]
						alloc2_instr = ruw[3]
						alloc2_order1 = ruw[4]
						alloc2_cal = ruw[5]
						alloc2_last = ruw[6]
				
						alloc2_orderTable = orderTable( alloc2_order1 )

						cmd5 = "select name, code, status from instr where status='Active' order by name"
						cursor5.execute( cmd5 )

						numrows5 = cursor5.rowcount
						instrCtrl3 = "<select name=alloc2_instr size=1>"
						instrString = ''
						if numrows5 > 0 :
							for result5 in cursor5.fetchall() :
								ainstr = result5[0]
								ainstrcode = result5[1]
								if alloc2_instr == ainstr :

									instrCtrl3 += "<option value=%s selected>%s - %s" % ( ainstr, ainstr, ainstrcode )

								else: 

									instrCtrl3 += "<option value=%s>%s - %s" % ( ainstr, ainstr, ainstrcode )
				#				instrString += propinstr + ', ' 
				#			instrString += ' ] (' + str( numrows5 )+ ')'
						instrCtrl3 += '</select>'
			
					
						editText += "<form method=post action='propone.py?idno=%s&allocid=%s'><input name=action type=submit value='Save Night'> | " \
						% ( prop_idno, allocid )
						editText += '<table cellpadding=3 cellspacing=3><tr><th>Edit Night</th><th>'
						editText += '</th></tr>'
						editText += "<tr><td class=right>Alloc IDNo</td><td>%s</td></tr>" % ( alloc2_idno ) 
						editText += "<tr><td class=right>Alloc PropID</td><td>%s</td></tr>" % ( alloc2_propid ) 
						editText += "<tr><td class=right>Alloc DateIn</td><td>%s</td></tr>" % ( alloc2_datein ) 
						editText += "<tr><td class=right>%s</td><td><input type=text name=%s size=12 value='%s'></td></tr>" % ( 'Alloc Date', 'alloc2_datein', alloc2_datein  )
						editText += "<tr><td class=right>Alloc Instr</td><td>%s</td></tr>" % ( alloc2_instr ) 
						editText += "<tr><td class=right>Alloc Instr</td><td>%s</td></tr>" % ( instrCtrl3 ) 
#						editText += "<tr><td class=right>Alloc Order</td><td>%s</td></tr>" % ( alloc2_order1 ) 
						editText += "<tr><td class=right>%s</td><td><input type=text name=%s size=6 value='%s'></td></tr>" % ( 'Alloc Order', 'alloc2_order', alloc2_order1 )
						editText += "<tr><td class=right>Alloc Table</td><td>%s</td></tr>" % ( alloc2_orderTable ) 
						editText += "<tr><td class=right>Alloc Calendar?:</td><td>%s</td></tr>" % ( alloc2_cal ) 
						editText += '</table></form>'

#				else :
#					editText += "<hr>No AllocID Editing"


				if alloc_idno == allocid :
				
					maintext += "<td colspan=6><hr>%s<hr></td></tr>"  % ( editText )

				
			maintext += "</table><hr>"

			
			
			maintext += "</td></table>"
			

			members = getMembers ( prop_gid )
			maintext += "Members:"
			maintext += str( members )

#			maintext += instrCtrl
			
#			for member in members :
#				maintext += member + ',' 
#				
			

		else:

#			cmd5 = "select name, code, status from instr where status='Active' order by name"
#			cursor5.execute( cmd5 )

#			numrows5 = cursor5.rowcount
#			instrCtrl = '<table>'
#			instrString = ''
#			if numrows5 > 0 :
#				for result5 in cursor5.fetchall() :
#					propinstr = result5[0]
#					propinstrcode = result5[1]
#					if prop_instr == propinstr :
#						instrCtrl += "<tr><td><input type=checkbox name=instr2 value=%s selected>%s</td><td>%s</td></tr>" % ( propinstr, propinstr, propinstr, propinstrcode )
#					else: 
#						instrCtrl += "<tr><td><input type=checkbox name=instr2 value=%s>%s</td><td>%s</td></tr>" % ( propinstr, propinstr, propinstr, propinstrcode )
	#				instrString += propinstr + ', ' 
	#			instrString += ' ] (' + str( numrows5 )+ ')'
#			instrCtrl += '</table>'

			cmd5 = "select name, code, status from instr where status='Active' order by name"
			cursor5.execute( cmd5 )

			numrows5 = cursor5.rowcount
			instrCtrl2 = "<select name=instr size=1>"
			instrString = ''
			if numrows5 > 0 :
				for result5 in cursor5.fetchall() :
					propinstr = result5[0]
					propinstrcode = result5[1]
					if prop_instr == propinstr :

						instrCtrl2 += "<option value=%s selected>%s - %s" % ( propinstr, propinstr, propinstrcode )

					else: 

						instrCtrl2 += "<option value=%s>%s - %s" % ( propinstr, propinstr, propinstrcode )
	#				instrString += propinstr + ', ' 
	#			instrString += ' ] (' + str( numrows5 )+ ')'
			instrCtrl2 += '</select>'


#			status1 = ( 'Active', 'Removed', 'Garage' )
#			statusCtrl = '<select size=1 name=status>'
#			for status2 in status1 :
#				if car_status == status2 :
#					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
#				else:
#					statusCtrl += '<option value=%s>%s' % ( status2, status2 )           
#			statusCtrl += '</select>'

			maintext += "<form method=post action='propone.py?idno=%s'><input name=action type=submit value='Save'> <input name=action type=submit value='Cancel'>" % ( prop_idno )
			maintext += "<table cellpadding=3 cellspacing=3>"
			maintext += "<td valign=top><table cellpadding=3 cellspacing=3>"
			maintext += "<tr><td class=right>IDNo</td><td>%s</td></tr>" % ( prop_idno ) 
			maintext += "<tr><td class=right>PropID</td><td><input type=text name=propid size=20 value='%s'></td></tr>" % ( prop_propid ) 
			maintext += "<tr><td class=right>GID</td><td><input type=text name=gid size=20 value='%s'></td></tr>" % ( prop_gid ) 
#			maintext += "<tr><td class=right>Instr</td><td><input type=text name=instr size=10 value='%s'></td></tr>" % ( prop_instr ) 
			maintext += "<tr><td class=right>Instr</td><td>%s</td></tr>" % ( instrCtrl2 ) 
			maintext += "<tr><td class=right>DateIn</td><td>%s</td></tr>" % ( prop_datein ) 
			maintext += "<tr><td class=right>Sem</td><td><input type=text name=sem size=10 value='%s'></td></tr>" % ( prop_sem ) 
#			maintext += "<tr><td class=right>Status</td><td>%s</td></tr>" % ( statusCtrl ) 
#			maintext += "<tr><td class=right>Wheels</td><td>%s</td></tr>" % ( wheelsCtrl ) 
			maintext += "<tr><td class=right>Comment</td><td><input type=text name=comment size=100 value='%s'></td></tr>" % ( prop_comment ) 
			maintext += "</table>"
			maintext += "</td><td valign=top>"
#			maintext += instrCtrl
			maintext += "</td></table>"
			maintext += "</form>"
			

	else :
		
		maintext += "No Records!"
		maintext += "thisid3 " + thisid3 + ' ' + str( numrows )
				
#	maintext += "</table>"
else :

	maintext = logproc.returnLogin()

#aintext='tom'
printHTML( maintext )
