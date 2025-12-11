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
import html
import logproc3 as logproc

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()


opalconn=dbconnect.opalconn()
dbopal=MySQLdb.connect( host = opalconn[0], user = opalconn[1], passwd = opalconn[2], db = opalconn[3])
cursor5 = dbopal.cursor()
cursor6 = dbopal.cursor()

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold }"
	css_text += "</style>"

	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
#	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += "<META http-equiv='Content-Type' content='text/html; charset=UTF-8'>"
	printpg += css_text

	printpg += "</HEAD><BODY><center>"
	printpg += maintext
	printpg += "</center></BODY></HTML>"
	print( printpg )	

#def main() :

now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')

today2 = datetime.date.today()
tmrw = today2 + datetime.timedelta( days = 1 )
tmrw_txt = tmrw.strftime('%Y-%m-%d')

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

#if field.has_key('seq'):
if 'seq' in field :

	seq = field['seq'].value
	
else:
	
	seq = '1'

#if field.has_key('instr'):
if 'instr' in field :

	instr = field['instr'].value
	
else:
	
	instr = ''

#if field.has_key('alloc'):
if 'alloc' in field :

	alloc = field['alloc'].value
	
else:
	
	alloc = ''

#if field.has_key('pi'):
if 'pi' in field :

	pi = field['pi'].value
	
else:
	
	pi = ''

#if field.has_key('gid'):
if 'gid' in field :

	gid = field['gid'].value
	
else:
	
	gid = ''

#if field.has_key('propid'):
if 'propid' in field :

	propid = field['propid'].value
	
else:
	
	propid = ''

#if field.has_key('ao1'):
if 'ao1' in field :

	ao1 = field['ao1'].value
	
else:
	
	ao1 = ''

#if field.has_key('ao2'):
if 'ao2' in field :

	ao2 = field['ao2'].value
	
else:
	
	ao2 = ''

#if field.has_key('obs1'):
if 'obs1' in field :

	obs1 = field['obs1'].value
	
else:
	
	obs1 = ''

#if field.has_key('obs1loc'):
if 'obs1loc' in field :

	obs1loc = field['obs1loc'].value
	
else:
	
	obs1loc = 'Choose'
	

#if field.has_key('obs2'):
if 'obs2' in field :

	obs2 = field['obs2'].value
	
else:
	
	obs2 = ''

#if field.has_key('obs2loc'):
if 'obs2loc' in field :

	obs2loc = field['obs2loc'].value
	
else:
	
	obs2loc = ''
	
#if field.has_key('obs3'):
if 'obs3' in field :

	obs3 = field['obs3'].value
	
else:
	
	obs3 = ''

#if field.has_key('obs3loc'):
if 'obs3loc' in field :

	obs3loc = field['obs3loc'].value
	
else:
	
	obs3loc = ''

#if field.has_key('ss'):
if 'ss' in field :

	ss = field['ss'].value
	
else:
	
	ss = ''

#if field.has_key('ssloc'):
if 'ssloc' in field :

	ssloc = field['ssloc'].value
	
else:
	
	ssloc = ''

#if field.has_key('ss2'):
if 'ss2' in field :

	ss2 = field['ss2'].value
	
else:
	
	ss2 = ''

#if field.has_key('ss2loc'):
if 'ss2loc' in field :

	ss2loc = field['ss2loc'].value
	
else:
	
	ss2loc = ''


#if field.has_key('others1'):
if 'others1' in field :

	others1 = field['others1'].value
	
else:
	
	others1 = ''

#if field.has_key('others1loc'):
if 'others1loc' in field :

	others1loc = field['others1loc'].value
	
else:
	
	others1loc = ''

#if field.has_key('others2'):
if 'others2' in field :

	others2 = field['others2'].value
	
else:
	
	others2 = ''

#if field.has_key('others2loc'):
if 'others2loc' in field :

	others2loc = field['others2loc'].value
	
else:
	
	others2loc = ''

#if field.has_key('comment'):
if 'comment' in field :

	comment = field['comment'].value
	
else:
	
	comment = ''

#if field.has_key('allocidno'):
if 'allocidno' in field :

	allocidno = field['allocidno'].value
	
else:
	
	allocidno = '0'

#if field.has_key('stamp'):
if 'stamp' in field :

	stamp = field['stamp'].value
	
else:
	
	stamp = 'none'

#if field.has_key('intime'):
if 'intime' in field :

	intime = field['intime'].value
	
else:
	
	intime = '0000-00-00 00:00:00'

#if field.has_key('outtime'):
if 'outtime' in field :

	outtime = field['outtime'].value
	
else:
	
	outtime = '0000-00-00 00:00:00'


if 'obs4' in field :

	obs4 = field['obs4'].value

else:

	obs4 = ''

#if field.has_key('obs3loc'):
if 'obs4loc' in field :

	obs4loc = field['obs4loc'].value

else:

	obs4loc = ''

			
if method == 'POST' and field['action'].value == 'Save' :

	cursor.execute("update progs set gid = '%s', propid = '%s', pi = '%s', instr = '%s', alloc = '%s', obs1 = '%s', \
	obs1loc = '%s', obs2 = '%s', obs2loc = '%s', obs3 = '%s', obs3loc = '%s', ss = '%s', ssloc = '%s', ss2 = '%s', ss2loc = '%s', \
	others1 = '%s', others1loc = '%s', others2 = '%s', others2loc = '%s', ao1 = '%s', ao2 = '%s', comment = '%s', intime='%s', outtime='%s', \
	obs4='%s', obs4loc='%s' where idno = '%s'" % ( gid, propid, pi, instr, alloc, obs1, obs1loc, obs2, obs2loc, obs3, obs3loc, ss, ssloc, ss2, ss2loc, others1, others1loc, \
	others2, others2loc, ao1, ao2, comment, intime, outtime, obs4, obs4loc, idno ) )

else :
	
	if method == 'POST' and field['action'].value == 'Copy-Program' :
	
		if int( idno ) > 0 and int( allocidno ) > 0 :
		
			cursor5.execute("select idno, gid, propid, first, last, instr from alloc where idno = '%s' " % ( allocidno ) )
			numrows5 = cursor5.rowcount

			if numrows5 == 1 :

				riw = cursor5.fetchone()

				alloc_idno = riw[0]
				alloc_gid = riw[1]
				alloc_propid = riw[2]
				alloc_first = riw[3]
				alloc_last = riw[4]
				alloc_instr = riw[5]
				alloc_pi = alloc_first + ' ' + alloc_last

				cursor4.execute("update progs set gid = '%s', propid = '%s', pi = '%s', instr = '%s' where idno = '%s'" % ( alloc_gid, alloc_propid, alloc_pi, alloc_instr, idno ) )
#				cursor4.execute("update progs set gid = '%s', propid = '%s', pi = '%s' \
#				instr = '%s' where idno = '%s'" % ( alloc_gid, alloc_propid, alloc_pi, alloc_instr, idno ) )
				
				cursor6.execute("select idno, ss, observers, location, sslist, others, alloc, comments from tsr where allocidno = '%s' " % ( allocidno ) )
				numrows6 = cursor6.rowcount
#
				if numrows6 == 1 :
				
					rew = cursor6.fetchone()
					
					tsr_ss = rew[1]
					tsr_observers = rew[2]
					tsr_obs1loc = rew[3]
					tsr_sslist = rew[4]
#					tsr_sslist = ''
					tsr_others = rew[5]
#					tsr_others = ''
					tsr_alloc = rew[6]
					tsr_comments = rew[7]

#					cursor4.execute("update progs set alloc = '%s', obs1 = '%s' where idno = '%s'" % ( tsr_alloc, tsr_observers, idno ) )

					cursor4.execute("update progs set alloc = '%s', obs1 = '%s', obs1loc = '%s', \
					ss = '%s', others1 = '%s', comment = '%s' where idno = '%s'" % ( tsr_alloc, tsr_observers, tsr_obs1loc, tsr_sslist, \
					tsr_others, tsr_comments, idno ) )

	if method == 'GET' and seq == '0' :
		
		cursor3.execute("select idno, day from days where date='%s'" % ( date ) )
		numrows3=cursor3.rowcount

		dayidno = 1
		day = 'Sunday'
		
		if numrows3 == 1 :
		
			ruw=cursor3.fetchone()
			dayidno = ruw[0]
			day = ruw[1]

		nextseq = '1'
		cursor2.execute("select seq from progs where date='%s' order by seq" % ( date ) )
		numrows2=cursor2.rowcount

		if numrows2 > 0 :
		
			for riw in cursor2.fetchall():
			
				progseq = riw[0]
				
			nextseq = str( int( progseq ) + 1 ) 
			
		nulltime = '0000-00-00 00:00'
		
		dt1 = datetime.date( int( date[0:4] ), int( date[5:7] ), int( date[8:10] ) )
		dt2 = dt1 + datetime.timedelta( days = 1 )
		
		
#		monthday1 = date[5:10]

		monthday1 = str( dt1 )

		monthday1a = monthday1[5:10]
		
#		monthday2 = tmrw_txt[5:10]

		monthday2 = str( dt2 )
		
		monthday2a = monthday2[5:10]

		cursor2.execute("select intime, outtime from nights where substr( date1, 6, 5 ) <= '%s' and substr( date2, 6, 5 ) >= '%s'" % ( monthday1a, monthday1a ) )
		numrows2=cursor2.rowcount

		if numrows2 == 1 :

			ruw = cursor2.fetchone()

			intime1 = ruw[0]
			outtime1 = ruw[1]

#			intime2 = today + ' ' + intime1
#			outtime2 = tmrw_txt + ' ' + outtime1

			intime2 = monthday1 + ' ' + intime1
			outtime2 = monthday2 + ' ' + outtime1
			
		else:
			intime2 = today + ' 19:00'
			outtime2 = tmrw_txt + ' 06:00'

#		if nextseq > '1' :
#
#			intime2 = now
#			outtime2 = outtime2
			
		comment_txt = ''		
#		comment_txt = monthday1 + ' numrows2: ' + str( numrows2 ) + 'intime2: ' + intime1 + ' outtime: ' + outtime1		
#		comment_txt = monthday1 + ' numrows2: ' + str( numrows2 ) 		
#		cursor2.execute("insert into progs ( dayidno, date, seq, instr, alloc, pi, day ) values ( %s, '%s', '%s', '', '', '', '%s' ) " % ( dayidno, date, nextseq, day ) )
		cursor2.execute("insert into progs ( date, seq, day, dayidno ) values ( '%s', '%s', '%s', %s ) " % ( date, nextseq, day, dayidno ) )
		idno = cursor2.lastrowid
		cursor2.execute("update progs set instr='', alloc = '', pi = '', ao1 = '', ao2 = '', intime = '%s', outtime = '%s', obs1 = '', obs2 = '', obs3 = '', \
		obs1loc = '', obs2loc = '', obs3loc = '', ss = '', ssloc = '', others1 = '', others2 = '', others1loc = '', others2loc = '', gid = '', \
		propid = '', ss2 = '', ss2loc = '', comment = '%s', obs4='', obs4loc='' where idno = %s " % ( intime2, outtime2, comment_txt, idno ) )
		
	if method == 'GET' and stamp == 'start'  :
		
		cursor3.execute("update progs set intime = '%s' where idno='%s'" % ( now, idno ) )

	if method == 'GET' and stamp == 'end'  :
		
		cursor3.execute("update progs set outtime = '%s' where idno='%s'" % ( now, idno ) )
		
				
pagename = '<b>Summit Log Program - ' + str( idno ) + '</b><br>' + logproc.getMenu() + '<br><br>'

maintext = pagename

cursor.execute("select idno, dayidno, date, day, seq, instr, alloc, pi, ao1, ao2, intime, \
outtime, obs1, obs2, obs3, obs1loc, obs2loc, obs3loc, ss, ssloc, others1, \
others2, others1loc, others2loc, gid, propid, ss2, ss2loc, comment, obs4, obs4loc from progs where idno = '%s'" % ( idno ) )
numrows=cursor.rowcount
maintext += 'rows: ' + str( numrows ) + '<br>'
#numrows=0
#maintext += "<form method=post action='./progone.py?'>"
#maintext += '<table><tr><th>Date</th><th>Day</th><th>DayCrew</th><th>DC Out</th><th>TO</th><th>TO Out</th><th>IO</th><th>IO Out</th></tr>'

if numrows == 1 :

	row = cursor.fetchone()
	
	progidno = str( row[0] )
	
	dayidno = str( row[1] )
	
	date = row[2]

	day = row[3]
	seq = row[4]

	proginstr = row[5]
	progalloc = row[6]
	progpi = row[7]

	ao1 = row[8]
	ao2 = row[9]
	
	intime = str( row[10] )
	intime = intime[0:16]
	
	outtime = str( row[11] )
	outtime = outtime[0:16]

	obs1 = row[12]
	obs2 = row[13]	
	obs3 = row[14]
	obs1loc = row[15]
	obs2loc = row[16]	
	obs3loc = row[17]
	ss = row[18]
	ssloc = row[19]
	others1 = row[20]
	others2 = row[21]
	others1loc = row[22]
	others2loc = row[23]
	gid = row[24]
	propid = row[25]
	ss2 = row[26]
	ss2loc = row[27]
	comment = row[28]
	
	obs4 = row[29]
	obs4loc = row[30]

#	if method == 'GET' and rm == 'yes'  and idno > 0 :
#		
#		cursor3.execute("delete from progs where idno='%s'" % ( idno ) )


	cursor5.execute("select idno, gid, propid, first, last, instr from alloc where datein = '%s' and cal='Y'" % ( date ) )
	numrows5 = cursor5.rowcount

	alloc_text = 'OPAL Programs for %s<br>' % ( date )

	if numrows5 > 0 :

		alloc_text += '<table>'

		for allocs in cursor5.fetchall() :

			alloc_idno = allocs[0]
			alloc_gid = allocs[1]
			alloc_propid = allocs[2]
			alloc_first = allocs[3]
			alloc_last = allocs[4]
			alloc_instr = allocs[5]
			alloc_post = "<form method=post action='./progone.py?'>"
			alloc_post += "<input type=hidden name=idno value=%s>" % ( idno )
			alloc_post += "<input type=hidden name=allocidno value=%s>" % ( alloc_idno )
			alloc_post += "<input type=submit name=action value='Copy-Program'></form>"
			
			alloc_text += '<tr><td>%s</td><td>%s</td><td>%s %s</td><td>%s</td><td valign=bottom>%s</td><td>%s</td></tr>' % ( alloc_gid, alloc_propid, alloc_first, alloc_last, alloc_instr, alloc_post, alloc_idno )

		alloc_text += '</table>'

# instrument spinner

	instr_txt = "<select name=instr size=1>"
	
	cursor4.execute("select code, text, seq from refer where code='INSTR' order by seq")
	numrows4=cursor4.rowcount
	for raw in cursor4.fetchall() :

		value = raw[1]

		if value == proginstr :
			
			instr_txt += "<option value='%s' selected>%s" % ( value, value )
		
		else :
				
			instr_txt += "<option value='%s'>%s" % ( value, value )
	
	instr_txt += "</select>"
	
	
#	cursor4.execute("select opw from gidpw where gid='%s'" % ( gid ) )
#	numrows4=cursor4.rowcount
#	opw = '.none.'
#	if numrows4 == 1 :
#		raw = cursor4.fetchone()
#		opw = raw[1]


# allocation spinner

	alloc_txt = "<select name=alloc size=1>"
	
	cursor4.execute("select code, text, seq from refer where code='ALLOC' order by seq")
	
	numrows4=cursor4.rowcount
	
	for raw in cursor4.fetchall() :

		value = raw[1]

		if value == progalloc :
			
			alloc_txt += "<option value='%s' selected>%s" % ( value, value )
		
		else :
				
			alloc_txt += "<option value='%s'>%s" % ( value, value )
	
	alloc_txt += "</select>"
		

	obslocs = ( 'Choose', 'Summit', 'Base', 'HP', 'Mitaka', 'Other', 'Zoom', 'GERS' )

	obs1loc_txt = "<select size=1 name=obs1loc>"

	for loc in obslocs :

		if obs1loc == loc :

			obs1loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			obs1loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	obs1loc_txt += "</select>"	

	obs2loc_txt = "<select size=1 name=obs2loc>"

	for loc in obslocs :

		if obs2loc == loc :

			obs2loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			obs2loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	obs2loc_txt += "</select>"	

	obs3loc_txt = "<select size=1 name=obs3loc>"

	for loc in obslocs :

		if obs3loc == loc :

			obs3loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			obs3loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	obs3loc_txt += "</select>"	
	
	obs4loc_txt = "<select size=1 name=obs4loc>"

	for loc in obslocs :

		if obs4loc == loc :

			obs4loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			obs4loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	obs4loc_txt += "</select>"	
	
	sslocs = ( 'Choose', 'Summit', 'Base', 'HP', 'Mitaka', 'Zoom', 'GERS' )

	ssloc_txt = "<select size=1 name=ssloc>"

	for loc in sslocs :

		if ssloc == loc :

			ssloc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			ssloc_txt += "<option value='%s'>%s" % ( loc, loc )	

	ssloc_txt += "</select>"	


#	sslocs = ( 'Choose', 'Summit', 'Base', 'HP', 'Mitaka', 'Zoom', 'GERS' )

	ss2loc_txt = "<select size=1 name=ss2loc>"

	for loc in sslocs :

		if ss2loc == loc :

			ss2loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			ss2loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	ss2loc_txt += "</select>"	


	others1loc_txt = "<select size=1 name=others1loc>"

	for loc in sslocs :

		if others1loc == loc :

			others1loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			others1loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	others1loc_txt += "</select>"	

	others2loc_txt = "<select size=1 name=others2loc>"

	for loc in sslocs :

		if others2loc == loc :

			others2loc_txt += "<option value='%s' selected>%s" % ( loc, loc )	

		else:

			others2loc_txt += "<option value='%s'>%s" % ( loc, loc )	

	others2loc_txt += "</select>"	

	ao1s = ( 'None', 'AO188', 'SCExAO', 'RAVEN' )
	
	ao1_txt = "<select size=1 name=ao1>"

	for ao in ao1s :
		if ao1 == ao :
			ao1_txt += "<option value='%s' selected>%s" % ( ao, ao ) 
		else:
			ao1_txt += "<option value='%s'>%s" % ( ao, ao ) 
	ao1_txt += "</select>"
			
	ao2s = ( 'None', 'SCExAO' )
	ao2_txt = "<select size=1 name=ao2>"
	for ao in ao2s :
		if ao2 == ao :
			ao2_txt += "<option value='%s' selected>%s" % ( ao, ao ) 
		else:
			ao2_txt += "<option value='%s'>%s" % ( ao, ao ) 
	
	ao2_txt += "</select>"
	

# crew section

	if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Copy-Program' or field['action'].value == 'Cancel' ) ) : 

		maintext += "<form method=post action='./progone.py?idno=%s'>" % ( progidno ) 
		maintext += "<input type=submit name=action value='Edit'>"
		
		progtxt = ''

		progtxt += "<hr><table><tr><td><b>Program %s</td><td><a href=logone.py?date=%s>%s</a></b></td></tr>" % ( seq, date, date )
		
#	progtxt += "<tr><td valign=top colspan=3>Program ( %s )</td></tr>" % ( seq )
		progtxt += "<tr><td>GID :</td><td>%s</td><td>PropID: %s</td></tr>" % ( gid, propid ) 
		progtxt += "<tr><td>Instr : </td><td>%s</td><td>Allocation : %s</td></tr>" % ( proginstr, progalloc)
#		progtxt += "<tr><td>Instr:</td><td>%s</td></tr>" ( progpi )
#		progtxt += "<tr><td>Instr:</td><td>%s | Allocation: %s | PI: %s</td></tr>" ( instr, alloc, pi )
#		progtxt += "<tr><td>PI:</td><td>%s</td></tr>" ( instr )
		progtxt += "<tr><td>PI :</td><td>%s</td><td>AO1 / AO2 : %s | %s</td></td><td></tr>" % (  progpi, ao1, ao2 ) 
#		progtxt += "<tr><td>StartTime:</td><td>%s | EndTime: %s</td></tr>" % ( intime, outtime ) 
		progtxt += "<tr><td><a href = ./progone.py?idno=%s&stamp=start>StartTime:</a></td><td>%s</td><td><a href = ./progone.py?idno=%s&stamp=end>EndTime:</a> %s</td></tr>" % ( idno, intime, idno, outtime ) 
		progtxt += "<tr><td>Observers-1 :</td><td>%s</td><td>@ %s</td></tr>" % ( obs1, obs1loc ) 
		progtxt += "<tr><td>Observers-2 :</td><td>%s</td><td>@ %s</td></tr>" % ( obs2, obs2loc ) 
		progtxt += "<tr><td>Observers-3 :</td><td>%s</td><td>@ %s</td></tr>" % ( obs3, obs3loc ) 
		progtxt += "<tr><td>Observers-4 :</td><td>%s</td><td>@ %s</td></tr>" % ( obs4, obs4loc ) 
		progtxt += "<tr><td>SS-1 :</td><td>%s</td><td>@ %s</td></tr>" % ( ss, ssloc ) 
		progtxt += "<tr><td>SS-2 :</td><td>%s</td><td>@ %s</td></tr>" % ( ss2, ss2loc ) 
		progtxt += "<tr><td>Others-1 :</td><td>%s</td><td>@ %s</td></tr>" % ( others1, others1loc ) 
		progtxt += "<tr><td>Others-2 :</td><td>%s</td><td>@ %s</td></tr>" % ( others2, others2loc ) 
		progtxt += "<tr><td>Comment :</td><td colspan=2>%s</td></tr>" % ( comment ) 
		progtxt += "</table><br></form>"

				
		maintext = maintext + progtxt + alloc_text

	else :
	
		if method == 'POST' and field['action'].value == 'Edit' :
		
	
			maintext += "<form method=post action='./progone.py?idno=%s'>" % ( progidno ) 
			maintext += "<input type=submit name=action value='Save'>  <input type=submit name=action value='Cancel'> <input type=hidden name=date value='%s'>" % ( date ) 

			progtxt = ''
			progtxt += "<hr><table><tr><td><b>Program %s</td><td><a href=logone.py?date=%s>%s</a></b></td></tr>" % ( seq, date, date )

	#		progtxt += "<tr><td valign=top>Program %s</td>" % ( seq ) 
			progtxt += "<tr><td>GID :</td><td><input type=text name=gid value='%s' size=10></td><td>PropID : <input type=text name=propid value='%s' size=15></td></tr>" % ( gid, propid ) 
			progtxt += "<tr><td>Instr :</td><td>%s</td><td>Allocation : %s</td></tr>" % ( instr_txt, alloc_txt )
			progtxt += "<tr><td>PI :</td><td><input type=text name=pi value='%s' size=30></td><td>AO1 / AO2 : %s | %s</td></tr>" % ( progpi, ao1_txt, ao2_txt ) 
			progtxt += "<tr><td>StartTime :</td><td><input type=text name=intime value='%s' size=20></td><td>EndTime: <input type=text name=outtime value='%s' size=20></td></tr>" % ( intime, outtime ) 
			progtxt += "<tr><td>Observers-1 :</td><td><input type=text name=obs1 value='%s' size=50 maxlength=50></td><td>@ %s</td></tr>" % ( obs1, obs1loc_txt ) 
			progtxt += "<tr><td>Observers-2 :</td><td><input type=text name=obs2 value='%s' size=50 maxlength=50></td><td>@ %s</td></tr>" % ( obs2, obs2loc_txt ) 
			progtxt += "<tr><td>Observers-3 :</td><td><input type=text name=obs3 value='%s' size=50 maxlength=50></td><td>@ %s</td></tr>" % ( obs3, obs3loc_txt ) 
			progtxt += "<tr><td>Observers-4 :</td><td><input type=text name=obs4 value='%s' size=50 maxlength=50></td><td>@ %s</td></tr>" % ( obs4, obs4loc_txt ) 
			progtxt += "<tr><td>SS-1 :</td><td><input type=text name=ss value='%s' size=30 maxlength=30></td><td>@ %s</td></tr>" % ( ss, ssloc_txt ) 
			progtxt += "<tr><td>SS-2 :</td><td><input type=text name=ss2 value='%s' size=30 maxlength=30></td><td>@ %s</td></tr>" % ( ss2, ss2loc_txt ) 
			progtxt += "<tr><td>Others-1 :</td><td><input type=text name=others1 value='%s' size=50 maxlength=50></td><td>@ %s</td></tr>" % ( others1, others1loc_txt ) 
			progtxt += "<tr><td>Others-2 :</td><td><input type=text name=others2 value='%s' size=50 maxlength=50></td><td>@ %s</td></tr>" % ( others2, others2loc_txt ) 
			progtxt += "<tr><td>Comment :</td><td colspan=2><input type=text name=comment value='%s' size=60></td></tr>" % ( comment ) 
#			progtxt += "</td></tr>"
			progtxt += "</table><br></form>"

	#		maintext = maintext + crewtxt + weathertxt
			maintext = maintext + progtxt 


else :

	maintext = '<tr><td colspan=8>No SummitLog Available for' + date+ '</td></tr>'
	
maintext += '</table>'
#maintext='tom'
printHTML( maintext )
	
