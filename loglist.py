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

field = cgi.FieldStorage()

dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()

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


maxday = now + datetime.timedelta( days = 7 )

#if field.has_key('username'):

if 'username' in field :

	username = field['username'].value
	
else:
	
	username = 'winegar'


#if field.has_key('year'):

if 'year' in field:

	year = field['year'].value
	
else:
	
	year = today[0:4]




referpage=cgi.os.environ['HTTP_REFERER']
clientip=cgi.os.environ['REMOTE_ADDR']


#if referpage[:-4] == '.php':
#if referpage[:-4] == '.php'and not username == 'None':

#	newcookie=Cookie.SimpleCookie()
#	newcookie[ 'username' ] = '%s' % ( username )
#	newcookie[ 'username' ][ 'max-age' ]= 18 * 60 * 60					
#	term=str( 18 * 60 * 60 )
#	newcookie[ 'start' ]='%s' % ( now )
#	newcookie[ 'term' ]='%s' % ( term )
#	print newcookie


if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	termlimit = str( now + term )
	
#	pagename = '<center>Summit Logs Listing - All Logs<br> [ user: ' + username + ' expires: ' + end + ' ]<br>' + '<a href=itemsearch.py?>Search</a><br>' + referpage
#	pagename = '<center>Summit Logs Listing - All Logs<br> [ user: ' + username + ' expires: ' + end + ' ]<br><br>' 
	pagename = '<center><b>Summit Logs Listing</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
	
	years  = (  '2028', '2027', '2026', '2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', \
	'2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999' )

	year_text = "Choose Year: "

	seq = 0
	for yr in years:
		seq += 1
		
		if seq == 12 or seq == 24 :
			year_text += '<br>'

		if today[0:4] == yr :


			year_text += "<b><a href=loglist.py?year=%s>%s</a></b> | " % ( yr, yr )

		else :
			year_text += "<a href=loglist.py?year=%s>%s</a> | " % ( yr, yr )
		
	#year='2019'
#	maintext = pagename + "<br><a href=../menu.php>( return to OPAL )</a><br><br>" + year_text + "<br><br>"
	maintext = pagename + "<br><br>" + year_text + "<br><br>"
	#cursor.execute("select date, day, dc1, dc2, dcout, to1, toout, io1, ioout, idno from days where substring(date, 1, 4)='%s' and  date<='%s' order by date desc" % ( year, today ) )
#	cursor.execute("select date, day, dc1, dc2, dcout, to1, toout, io1, ioout, idno from days where date<='%s' and substring(date, 1, 4) = '%s' order by date desc" % ( today, year ) )
	cursor.execute("select date, day, dc1, dc2, dcout, to1, toout, io1, ioout, idno from days where date<='%s' and substring(date, 1, 4) = '%s' order by date desc" % ( maxday, year ) )
	numrows=cursor.rowcount
	maintext += 'rows: ' + str( numrows ) + '<br>'
	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Date</th><th>Day</th><th>DayCrew</th><th>DC Out</th><th>TO</th><th>TO Out</th><th>IO</th><th>IO Out</th><th>Instr</th></tr>'

	for row in cursor.fetchall() :

		date = str( row[0] )
		day = row[1]
		dc1 = row[2]
		dc2 = row[3]
		dcout = str( row[4] )
		dcout = dcout[0:16]
		to1 = row[5]
		toout = str( row[6] )
		toout = toout[0:16]
		io1 = row[7]
		ioout = str( row[8] )
		ioout = ioout[0:16]
		idno = str( row[9] )
		
		instr = 'None'

		cursor2.execute("select instr from progs where date='%s' and seq='1'" % ( date ) )
		numrows2 = cursor2.rowcount

		if numrows2 == 1 :
		
			raw=cursor2.fetchone()
			instr=raw[0]

		bgcolor = 'white'
		if date == today :
			bgcolor = 'yellow'
		
		maintext += '<tr><td bgcolor=' + bgcolor + '><a href=logone.py?date=' + date + '>' + date + '</a></td><td>'+ day + '</td><td>'+ dc2 + '</td><td>'+ str( dcout ) + '</td><td>'+ to1 + '</td><td>'+ str( toout ) + '</td><td>'+ io1 + '</td><td>'+ str( ioout ) + '</td><td>'+ instr+ '</td></tr>'

	maintext += '</table></center>'
else:

#	maintext = "OPAL Login Required <a href = '../login.php'>Here</a><br>"
        maintext = logproc.returnLogin()

#maintext = 'tom'		
printHTML( maintext )
	
