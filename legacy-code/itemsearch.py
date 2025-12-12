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

field = cgi.FieldStorage()

method=os.environ.get("REQUEST_METHOD","")

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()

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


#if field.has_key('qone'):

if 'qone' in field :

	qone = field['qone'].value
	
else:
	
	qone = ''

#if field.has_key('qtwo'):
#if 'qtwo' in field :
#
#	qtwo = field['qtwo'].value
#	
#else:
#	
#	qtwo = ''

#validcookie, validtext = logproc.validCookie2()

validcookie = logproc.validCookie()
validtext='none'

if logproc.validCookie() :
#if True :

	username, end, term, logcrew2 = logproc.getUsername()

	maintext = "<b>Summit Log Search</b> | " + username + " [" + end + "] " + "<br><br>" + logproc.getMenu() +'<br>'+ validtext
	maintext += "<form method=POST action='itemsearch.py?'>Search: <input type=text value='%s' name='qone' size=20> | " % ( qone )
	maintext += "<input type=submit value='Search'></form>" 

	table_text = ''

	if len( qone ) > 0 :

		qone = qone.strip()

		qone_text = "%" + qone + "%"

		cursor.execute("select idno, itemtitle, substr( itemtext, 1 ,100 ), date from items where itemtitle like '%s' or itemtext like '%s' order by date desc limit 200" % ( qone_text, qone_text ) )

		numrows = cursor.rowcount

	#	numrows = 0

		table_text += 'rows: ' + str( numrows ) + '<br><br>'

		table_text += "<table cellpadding=2 cellspacing=2 border=2 rules=all><tr><th>Seq</th><th>IDNo</th><th>Date</th><th>Title</th><th>Text</th></tr>"

		if numrows > 0 :

			seq = 0

			for row in cursor.fetchall() :

				seq += 1
				items_idno = str( row[0] )
				if items_idno is None:
					items_idno = '0'	

				items_itemtitle = str( row[1] )

				if items_itemtitle is None:
					items_itemtitle = ''	

				items_itemtext = str( row[2] )

				if items_itemtext is None:

					items_itemtext = ''	

				items_date = str( row[3] ) 

				if items_date is None:

					items_date='0000-00-00'



	#			items_idno = '0'	
	#			items_itemtitle = 'title'	
	#			items_itemtext = 'text'
	#			items_date = '2019-01-01'

		#		items_itemtext2 = items_itemtext[0:100]	

				table_text += "<tr><td>%s</td><td valign=top><a href=itemone.py?idno=%s>%s</a></td><td valign=top>%s</td><td valign=top>%s</td><td>%s</td></tr>\n" % ( str( seq ), items_idno, items_idno, items_date, items_itemtitle, items_itemtext )
		else:
				table_text += "<tr><td colspan=5>No Entries Match - %s</td></tr>\n" % ( qone )

		table_text += "</table><br>"

	else:
		table_text += "No Search Words!"


	maintext = maintext + table_text

else :

#	maintext = "OPAL Login Required <a href='../login.php'>Here</a>"
	maintext = logproc.returnLogin()

#maintext = 'tom'

printHTML( maintext ) 
