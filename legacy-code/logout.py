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
import logproc3 as logproc
import http.cookies as Cookie

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.opalconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor=db.cursor()
#cursor2=db.cursor()
#cursor3=db.cursor()

now = datetime.datetime.now()
nowC = now.strftime('%Y-%m-%d %H:%M:%S')

utcnow = datetime.datetime.utcnow()

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
#	css_text += "<script>tinymce.init({selector:'textarea'});</script>"


	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<!DOCTYPE html>"
	printpg += "<HTML><HEAD>"
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY><center>"
	printpg += maintext
	printpg += "</BODY></center></HTML>"
	print( printpg )	




#validcookie, validtext = logproc.validCookie2()

#validcookie = logproc.validCookie()
#validtext='none'

#if logproc.validCookie() :
#if True :

#	username, end, term = logproc.getUsername()

#      then = now + datetime.timedelta( hours = termhours )

#     thenC = then.strftime('%Y-%m-%d %H:%M')

term0 = 0 

newcookie=Cookie.SimpleCookie()

#username='willis'

newcookie[ 'username' ] = '%s' % ( 'willis' )

newcookie[ 'username' ][ 'max-age' ] = term0  

#newcookie[ 'username' ][ 'expires' ] = utcnow.strftime("%a, %d %b %Y %H:%M:%S GMT")
newcookie[ 'username' ][ 'expires' ] = 'Thu, 01 Jan 1970 00:00:00 GMT'
              

newcookie[ 'opaluser' ] = '%s' % ( 'willis' )
newcookie[ 'opaluser' ][ 'expires' ] = 'Thu, 01 Jan 1970 00:00:00 GMT'
#	newcookie[ 'start' ] = '%s' % ( nowC )

newcookie[ 'term' ] = '%s' % ( term0 )
newcookie[ 'term' ][ 'expires' ] = 'Thu, 01 Jan 1970 00:00:00 GMT'

newcookie[ 'end' ] = '%s' % ( nowC )
newcookie[ 'end' ][ 'expires' ] = 'Thu, 01 Jan 1970 00:00:00 GMT'

newcookie[ 'logcrew' ] = '%s' % ( 'WP' )
newcookie[ 'logcrew' ][ 'expires' ] = 'Thu, 01 Jan 1970 00:00:00 GMT'
print( newcookie )

maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext ) 
