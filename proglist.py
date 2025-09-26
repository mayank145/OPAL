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
import logproc
import html
import re

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")
#method=os.environ["REQUEST_METHOD"]

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
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
	toppg += "Content-type: text/html;\n\n"
	toppg += "<!DOCTYPE html>"
	toppg += "<HTML><HEAD>"
	toppg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	toppg += css_text
	
	bottompg = "</HEAD><BODY><center>"
	bottompg += maintext
	bottompg += "</center></BODY></HTML>"
	
	print( toppg )
	
	print( bottompg )

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
	
if logproc.validCookie() :
#if True :

	pagename = '<b>SummitLog - ' + str( date ) + '</b><br>' + logproc.getMenu() + '<br><br>'

	maintext = pagename

	username, end, term, logcrew2 = logproc.getUsername()

	cursor2.execute("select idno, dayidno, date, day, seq, instr, alloc, pi, ao1, ao2, intime, \
	outtime, obs1, obs2, obs3, obs1loc, obs2loc, obs3loc, ss, ssloc, others1, \
	others2, others1loc, others2loc, gid, propid, ss2, ss2loc from progs where date = '%s' order by seq" % ( date ) )
# Programs		


	numrows2 = cursor2.rowcount
#	numrows2=0
	if numrows2 > 0 :
	
		maintext += "<table cellpadding=3 cellspacing=3><tr><td><b>Program Deletion from %s</b></td></tr>" % ( date )
	
		for raw in cursor2.fetchall() :
		
			
			progidno = raw[0]
			date2 = raw[2]
			seq = raw[4]

			instr = raw[5]	
			alloc = raw[6]
			pi = raw[7]
			
			if len( pi ) == 0:
			
				pi = '{No PI}'
			
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
			
			if len( propid ) == 0:
			
				propid = '{No PropID}'
				
			ss2 = raw[26]
			ss2loc = raw[27]
			
			maintext += "<tr><td valign=top><a href=progdelete.py?idno=%s&rm=yes>Delete - [%s] Prog&nbsp;%s - %s - %s</a></td>" % ( progidno, date2, seq, propid, pi ) 


		maintext += "</table>"


	else:
		maintext += "No Programs for %s<br>" % ( date )

else :

#	maintext = "OPAL Login Required <a href='../login.php'>Here</a>"
        maintext = logproc.returnLogin()

#maintext = 'tom ' + method	
#maintext = 'tom ' + method	
printHTML( maintext )
