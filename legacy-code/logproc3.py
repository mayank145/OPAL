#! /usr/local/python

import os
import sys
import cgi
import datetime
import http.cookies as Cookie
#import Cookie
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import dbconnect

import textwrap

import smtplib
import html

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3] )
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
#cursor3=db.cursor()
#cursor4=db.cursor()
#cursor4.execute("set autocommit = 1")

def getSemID( date ) :

	semY = date[ 2:4 ]
	semM = date[ 5:7 ]
	
	if int( semM ) > 1:
	
		semID = 'S' + semY + 'A'
		
		if int( semM ) > 7 :
		
			semID = 'S' + semY + 'B'
	else :
	
		lastyear = int( semY ) - 1
		lastYear = str( lastyear )
		
		semID = 'S' + lastYear + 'B'
		
	return ( semID )

def getCookie() :

	today=datetime.date.today()
	now=datetime.datetime.now()
	
	thiscookie=Cookie.SimpleCookie()

#	continue = False
	username = 'None'
			
	try:
		string_cookie=cgi.os.environ['HTTP_COOKIE']
	
	except KeyError:
	
		string_cookie='none'
		return False
#		continue = False

	else:
	
		try:
			thiscookie.load( string_cookie )

		except NameError:
				
			return False
#			continue = False

		except TypeError:
				
			return False
#			continue = False

		except KeyError:
		
			return False
#			continue = False

		else:		
#			sid2=thiscookie['sid'].value
			try:
				username=thiscookie[ 'username' ].value

			except KeyError:

				return False
#				continue = False
			
			else:

				return True
#				continue = True
	
#	return ( continue ) 


def getCookieTrue() :

	return ( True )
	

def html_escape( html_text ) :

#		"&": "&amp;" ,
#		'"': "&quot;" ,
#		"'": "&apos;" ,
#		">": "&gt;" ,
#		"<": "&lt;" ,


	html_escape_table = {
	
		"&": "&amp;" ,
		'"': "&quot;" ,
		"'": "&apos;" ,
		">": "&gt;" ,
		"<": "&lt;" ,
     	}
	
	return "".join( html_escape_table.get( c, c ) for c in html_text )



def getMenu() :

	now=datetime.datetime.now()
	today=now.strftime('%Y-%m-%d')

	now2 = now - datetime.timedelta( days = 1 )
	yesterday=now2.strftime('%Y-%m-%d')
	
#	username, end, term, logcrew2 = logproc.getUsername()
	username2, end2, term2, logcrew2 = getUsername()


#	maintext += '<br>writecookie: ' + writecookie + '<table>'
	buttontxt = '<table cellpadding=4 cellspacing=4 border=2 rules=all><tr>'
#	maintext += '<tr><td><a href = ./loglist.py?>All Logs Listing</a></td></tr>' % ( username )
	buttontxt += '<td bgcolor=lime><b>Main Menu</b></td>'
	buttontxt += '<td bgcolor=white><a href = ./sumcal.py?>Calendar Grid</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./loglist.py?>Calendar List</a></td>'
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s>Today - %s</a></td>" % ( today, today[5:7] + '/' + today[8:10] )
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s>Yesterday - %s</a></td>" % ( yesterday, yesterday[5:7] + '/' + yesterday[8:10] )

	buttontxt += "<td bgcolor=white><a href = ./logone.py?date=%s&logcrew=%s>Today - %s</a></td>" % ( today, logcrew2, today[5:7] + '/' + today[8:10] )
	buttontxt += "<td bgcolor=white><a href = ./logone.py?date=%s&logcrew=%s>Yesterday - %s</a></td>" % ( yesterday, logcrew2, yesterday[5:7] + '/' + yesterday[8:10] )



	buttontxt += '<td bgcolor=white><a href = ./itemsearch.py?>Search</a></td>'
	buttontxt += '<td bgcolor=white><a href = ../menu.php?>Old OPAL</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./proplist.py?>Semester IDs</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./resday.py?>Cars</a></td>'
	buttontxt += '<td bgcolor=gainsboro><a href = ./logout.py?>Logout</a></td></tr>'
	
	buttontxt += '</table>'
	
	return ( buttontxt )

def getCarMenu() :

	now=datetime.datetime.now()
	today=now.strftime('%Y-%m-%d')

	now2 = now - datetime.timedelta( days = 1 )
	yesterday=now2.strftime('%Y-%m-%d')
	
#	username, end, term, logcrew2 = logproc.getUsername()
#	username2, end2, term2, logcrew2 = getUsername()


#	maintext += '<br>writecookie: ' + writecookie + '<table>'
	buttontxt = '<table cellpadding=4 cellspacing=4 border=2 rules=all><tr>'
#	maintext += '<tr><td><a href = ./loglist.py?>All Logs Listing</a></td></tr>' % ( username )
	buttontxt += '<td bgcolor=lime><b>Car Menu</b></td>'
	buttontxt += '<td bgcolor=white><a href = ./carcal.py?>Cars Calendar</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./resday.py?>Cars Today</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./restimes.py?>Cars Times</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./restimesOpen.py?>CarTimes OPEN</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./reslist.py?>Reservations List</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./shifts.py?>Shift Lists</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./carlist.py?>Cars</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./userlist.py?>Users</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./helper.py?>Help</a></td>'
#	buttontxt += '<td bgcolor=yellow><a href = ./destlist.py?>Destinations</a></td>'
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s>Today - %s</a></td>" % ( today, today[5:7] + '/' + today[8:10] )
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s>Yesterday - %s</a></td>" % ( yesterday, yesterday[5:7] + '/' + yesterday[8:10] )

#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s&logcrew=%s>Today - %s</a></td>" % ( today, logcrew2, today[5:7] + '/' + today[8:10] )
#	buttontxt += "<td bgcolor=yellow><a href = ./logone.py?date=%s&logcrew=%s>Yesterday - %s</a></td>" % ( yesterday, logcrew2, yesterday[5:7] + '/' + yesterday[8:10] )



#	buttontxt += '<td bgcolor=yellow><a href = ./itemsearch.py?>Search</a></td>'
#	buttontxt += '<td bgcolor=yellow><a href = ../menu.php?>OPAL</a></td>'
#	buttontxt += '<td bgcolor=yellow><a href = ./logout.py?>Logout</a></td></tr>'
	
	buttontxt += '</tr></table>'
	
	return ( buttontxt )

def getOPALMenu() :

	now=datetime.datetime.now()
	today=now.strftime('%Y-%m-%d')

	now2 = now - datetime.timedelta( days = 1 )
	yesterday=now2.strftime('%Y-%m-%d')

	buttontxt = '<table cellpadding=4 cellspacing=4 border=2 rules=all><tr>'
	buttontxt += '<td bgcolor=lime><b>Semester IDs Menu</b></td>'
	buttontxt += '<td bgcolor=white><a href = ./proplist.py?>Proposal IDs</a></td>'
#	buttontxt += '<td bgcolor=white><a href = ./tsrlist.py?>TSRs</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./starslist.py?>OPAL Users</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./ldaplist.py?>STARS LDAP</a></td>'
	buttontxt += '<td bgcolor=white><a href = ./tsrlist.py?>TSRs</a></td> '
	buttontxt += '<td bgcolor=white><a href = ./zoomlist.py?>ZoomIDs</a></td>'
	buttontxt += '</tr></table>'

	return ( buttontxt )

	
def getUsername() :

	username='None'
#	username='winegar'
	
	thiscookie=Cookie.SimpleCookie()
	string_cookie=cgi.os.environ['HTTP_COOKIE']
	thiscookie.load( string_cookie )
#	username = thiscookie[ 'username' ].value
	username = thiscookie[ 'opaluser' ].value
	username = username.lower()
#	start = thiscookie[ 'start' ].value
#	start = start[0:16]
	term = thiscookie[ 'term' ].value
#	term='86800'
	term = str( int( term ) / 60 ) + ' min'
	end = thiscookie[ 'end' ].value
#	end = '10-05 21:50'
	end = end[5:16]
	logcrew = thiscookie[ 'logcrew' ].value
#	logcrew = 'WP'
	
	return ( username, end, term, logcrew )
	

def validCookie() :
	
	validated = False
	
	username = 'None'
	term = '0'
	end = 'none'

	thiscookie = Cookie.SimpleCookie()
		
	try:
		string_cookie=cgi.os.environ['HTTP_COOKIE']
	
	except KeyError:

		string_cookie='none'
		
		validated = False
	else:
		try:
			thiscookie.load( string_cookie )

		except NameError:		

			validated = False

		except TypeError:		

			validated = False

		except KeyError:

			validated = False
		else:		
			
			try:
#				user2=thiscookie['username'].value
				user2=thiscookie['opaluser'].value
				
			except KeyError:
			
				validated = False
			else:

# 210224 add check term value to prevent disappearing term value error

				try:

					term=thiscookie[ 'term' ].value

				except KeyError:

					return False
#				continue = False
			
				else:


					validated = True
					

	return ( validated )

def validCookie2() :
	
	validated = False
	validfail = ''
	
	username = 'None'
	term = '0'
	end = 'none' 		

	thiscookie=Cookie.SimpleCookie()
	
	try:
		string_cookie = cgi.os.environ['HTTP_COOKIE']
	
	except KeyError:

		string_cookie='none'
		
		validated = False

		validfail += 'environ key'
	else:
		try:
			thiscookie.load( string_cookie )

		except NameError:		

			validated = False
			validfail += 'load-name'

		except TypeError:		

			validated = False
			validfail += 'load-type'

		except KeyError:

			validated = False
			validfail += 'load-key'
		else:		
			
			try:
				user2=thiscookie['username'].value
				
			except KeyError:
			
				validated = False
				validfail += 'load-username-key'
			else:
				validated = True

	return ( validated, validfail )
		
def remove_html_markup( s ):

    tag = False
    quote = False
    out = ""

    for c in s:
    
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out



def returnLogin() :

	returnButton = ''
	returnButton += '<center><table><td>'
	returnButton += '<b>OPAL Summit Calendar</b><br><br>[ your session expired ]</td>'
#	returnButton += "Login OPAL <a href='../login.php'>Here</a><br><br>"
	returnButton += "<td><img src=./Aurora-Australias-2.jpeg><br><br><a href='./login.py'>Login OPAL</a></td></table>"

	return ( returnButton )
	

	
def sendemail( user, emailsubject, emailtext ) :	
	
	smtpserver=( 'mail.subaru.nao.ac.jp' )
	session=smtplib.SMTP( smtpserver )
	sender='winegar@naoj.org'

	user = user.strip()
	
	now=datetime.datetime.now()
	today = now.strftime( '%y-%m-%d %H:%M' )
	
	cursor2.execute("select email from users where user = '%s'" % ( user ) )
	numrows2=cursor2.rowcount

	emailaddress = ''

	if numrows2 == 1 :

			rows=cursor2.fetchone()
			emailaddress = rows[0]
			emailaddress = emailaddress.strip()
	
#	recipient = [ 'winegar@naoj.org', 'twinegar7@gmail.com' ]
	if len ( emailaddress ) > 0 and '@' in emailaddress :
		
		mailTo =  '<' + emailaddress + '>'
	
#		mailSubject = emailsubject + ' - ' + today
		mailSubject = emailsubject 

		mailFrom = "Subaru Cars <winegar@naoj.org>"
		mailCC = "Tom Winegar <winegar@naoj.org>"
	#	mailHeader = "From: %s\r\nTo: %s\r\nSubject: %s\r\nCC: %s\r\n" % ( mailFrom, mailTo, mailSubject, mailCC )
	
		mailMsg = emailtext
	
		msg = MIMEText ( mailMsg )

		msg['From'] = mailFrom
		msg['To'] = mailTo
		msg['Subject'] = mailSubject
		msg['CC'] = mailCC


		s = smtplib.SMTP( smtpserver )

		# simpletext send
		s.send_message ( msg )

		s.quit()
	
	return ()
	
