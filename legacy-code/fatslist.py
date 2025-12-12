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

method=os.environ.get("REQUEST_METHOD","")
referer='Fats Listing'

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

dbconn=dbconnect.fatsconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()

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

	
#
#def main() :


if 'order' in field :

	order = field['order'].value

else:

	order = 'idno desc'

order = order.strip()

if 'search1' in field :

	search1 = field['search1'].value

else:

	search1 = ''

search1 = search1.strip()

if 'search2' in field :

	search2 = field['search2'].value

else:

	search2 = ''

search1 = search1.strip()

if 'fid' in field :

	fid = field['fid'].value

else:

	fid = '4719'

search1 = search1.strip()

mprogram = 'fatslist.py'

if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()

#	username='winegar'	
#	end='none'
	
	pagename = '<center><b>Faults Listing</b> | ' + username + " [" + end + ']<br><br>' 


	pagename += logproc.getMenu()
#	pagename += '<br>' + logproc.getOPALMenu() + '<br>'
	
	addFault = "<a href=fatsone.py?idno=0>%s</a> | <br><br>" % ( '+Add Fault' )
	pagename += '<br>' + addFault + '<br>'

		
#	if order == 'section' :

#		orderby = "order by section"

	if order == 'date' :

		order = "datein desc"
	
	orderby = "order by %s" % ( order )

	
	search1full = '%' + search1 +'%'
	search2full = '%' + search2 +'%'
		
	if len( search1 ) == 0  and len ( search2 ) == 0 :				

		cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault %s" % ( orderby ) )	

		numrows=cursor.rowcount

	else :

		if len( search2 ) == 0 :
				
# 240221			cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault where issue like '%s' %s" % ( search1full, orderby ) )	
			cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault where issue like '%s' or ( idescribe like '%s' or solution like '%s' or sdescribe like '%s' )  %s" % ( search1full, search1full, search1full, search1full, orderby ) )	

			numrows=cursor.rowcount

		else : 		
		
			cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault where issue like '%s' and issue like '%s' %s" % ( search1full, search2full, orderby ) )	

			numrows=cursor.rowcount
	
	cursor2.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault where idno = %s" % ( fid ) )	

	numrows2=cursor2.rowcount
	
	if numrows2 == 1 :
	
		raw2 = cursor2.fetchone()
		single_idno = str( raw2[0] )
		single_issue = raw2[1]
		single_idescribe = raw2[2]
		single_solution = raw2[3]
		single_sdescribe = raw2[4]
		single_section = raw2[5]
#		single_datein = raw2[6]
			
	
		
#	cursor2.execute("select sem from props where sem is not null group by sem desc" )
#	year_spin = "<select name='%s' size=1>" % ( 'year' )''
#	year_spin = ""
#	seq = 0
#	for row2 in cursor2.fetchall() :
#		seq += 1
#		year_spin += "<a href=proplist.py?sem=%s>%s</a>  " % ( row2[0], row2[0] )
#		if seq == 15 or seq==30 or seq==45 or seq==60 :
#			year_spin += "| <br>"
		
		
#	year_spin += "</select>"
	

	maintext = pagename 
	
	maintext += 'rows: ' + str( numrows ) + '<br>'
	
	maintext += '<br><b>FATS Listing</b><br>'


#	maintext += year_spin + '<br>'
	
	maintext += 'OrderBy: <a href=fatslist.py?order=date>IDNo</a> | ' 
	maintext += '<a href=fatslist.py?order=section>Section</a> | ' 
	maintext += '<a href=fatslist.py?order=date>Date</a> | <br><br>' 

	maintext += "<form method=POST action=%s?>" % ( mprogram ) 

	maintext += "Search for:<input type=text name=search1 value='%s' size=30> | <input type=text name=search2 value='%s' size=30> <input type=submit name=action value='Search'><br><br>" % ( search1, search2 ) 	

	maintext += '<table rules=none border=0 cellpadding=3 cellspacing=3><tr><td width=600>'
	

	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Seq</th><th>IDNo</th><th>Date/TimeStamp</th><th>Issue</th><th>Solution</th><th>Date</th></tr>'
	
	seq = 0

	for row in cursor.fetchall() :

		seq += 1
#	cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault %s" % ( orderby )	

		fats_idno = str( row[0] )
		fats_issue = row[1]
		fats_solution = row[3]
		fats_section = row[5]
		fats_date = row[6]
		fats_date2 = str( fats_date )
		fats_date2 = fats_date2[2:10]
		
		bgcolor2 = 'white'
		if fats_idno == fid :
			bgcolor2 = 'blanchedalmond'
				
#		maintext += "<tr><td>%s</td><td><a href=propone.py?idno=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
#		% ( seq, prop_idno, prop_propid, prop_instr, prop_datein, prop_datein, prop_last, prop_cal )

		maintext += "<tr><td>%s</td><td><a href=fatsone.py?idno=%s>%s</a></td><td>%s</td><td bgcolor=%s><a href=fatslist.py?fid=%s>%s</a></td><td>%s</td><td bgcolor=%s>%s</td></tr>" \
		% ( seq, fats_idno, fats_idno, fats_date2, bgcolor2, fats_idno, fats_issue, fats_solution, bgcolor2, fats_section )

	maintext += "</table>"
	maintext += '</td><td valign=top>'

	if numrows2 == 1 :
		
		maintext += '<table>' 

		maintext += '<tr><td bgcolor=%s>%s </td><td>%s</td></tr>' % ( bgcolor2, 'IDNO: ' , single_idno )
		maintext += '<tr><td>%s </td><td>%s</td></tr>' % ( 'Issue: ' , single_issue )
		maintext += '<tr><td>%s </td><td>%s</td></tr>' % ( 'Issue Describe: ' , single_idescribe )
		maintext += '<tr><td>%s </td><td>%s</td></tr>' % ( 'Solution: ' , single_solution )
		maintext += '<tr><td>%s </td><td>%s</td></tr>' % ( 'Solution Describe: ' , single_sdescribe )		
		maintext += '<tr><td>%s </td><td>%s</td></tr>' % ( 'Section: ' , single_section )
#		maintext += 'Date: ' + single_datein + '<br>'

		maintext += '</table>' 
	
	maintext += '</td></table>' + '<br>'
	
	maintext += "</form>"




else :
	
	maintext = logproc.returnLogin()

#maintext = 'tom'
printHTML( maintext )
