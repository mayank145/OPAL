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
referer='Fats Display'

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
nowstamp = now.strftime('%Y-%m-%d %H:%M')

dbconn=dbconnect.fatsconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
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
	css_text += "<script src='https://code.jquery.com/jquery-1.12.4.js'></script>"
	css_text += "<script src='https://code.jquery.com/ui/1.12.1/jquery-ui.js'></script>"
	css_text += "<script src='https://cdn.tiny.cloud/1/wew3bls4o7rcb9bz5e5fbsims2qe8k35v6ydly22743hjexy/tinymce/7/tinymce.min.js' referrerpolicy='origin'></script>"
	css_text += "<script> tinymce.init({ selector: '#mytextarea', menubar: false, statusbar: false });</script>"

	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<!DOCTYPE html>"
	printpg += "<HTML><HEAD>"
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY>"
	printpg += maintext
	printpg += "</BODY></HTML>"
	print( printpg )	

	
#
#def main() :


if 'idno' in field :

	idno = field['idno'].value

else:

	idno = '4719'

idno = idno.strip()

if 'fatsidno' in field :

	fatsidno = field['fatsidno'].value

else:

	fatsidno = '0'

fatsidno = fatsidno.strip()


if 'solution' in field :

	solution = field['solution'].value

else:

	solution = ''

solution = solution.strip()

if 'sdescribe' in field :

	sdescribe = field['sdescribe'].value

else:

	sdescribe = ''

sdescribe = sdescribe.strip()

if 'section' in field :

	section = field['section'].value

else:

	section = ''

section = section.strip()

if 'section2' in field :

	section2 = field['section2'].value

else:

	section2 = ''

section2 = section2.strip()

if 'datein' in field :

	datein = field['datein'].value

else:

	datein = ''

datein = datein.strip()

if 'operator' in field :

	operator = field['operator'].value

else:

	operator = ''

operator = operator.strip()

if 'status' in field :

	status = field['status'].value

else:

	status = ''

status = status.strip()

if 'todo' in field :

	todo = field['todo'].value

else:

	todo = ''

todo = todo.strip()

username, end, term, logcrew2 = logproc.getUsername()

if method == 'POST' and  field['action'].value == 'Save' and int( idno ) > 0  :

	fail_Issue = False
	fail_IDescribe = False
	fail_Solution= False
	fail_SDescribe = False

	clean_Issue = ''
	clean_IDescribe = ''
	clean_Solution = ''
	clean_SDescribe = ''

	validOrd = range ( 32, 126 )

	for char3 in solution :
	
		if not ord( char3 ) in validOrd :
			fail_Solution = True					
		else :
			clean_Solution += char3

	if fail_Solution == True:

		solution = clean_Solution

	for char4 in sdescribe :

		if not ord( char4 ) in validOrd :
			fail_SDescribe = True
		else :
			clean_SDescribe += char4

	if fail_SDescribe == True :

		sdescribe = clean_SDescribe				

#	cursor.execute( "update fault set issue = '%s', idescribe = '%s', solution = '%s', sdescribe = '%s', section = '%s', datein = '%s', \
#	section2 = '%s', operator = '%s', status = '%s', todo = '%s' where idno = %s" \
#	% ( issue, idescribe, solution, sdescribe, section, datein, section2, operator, status, todo, idno ) ) 

#	cursor.execute( "update fcomments set solution = '%s', sdescribe = '%s', datein = '%s', \
	cursor2.execute( "update fcomments set solution = '%s', sdescribe = '%s',  \
	operator = '%s', todo = '%s' where idno = %s " \
	% ( solution, sdescribe, operator, todo, idno ) ) 


if method == 'GET' and  int( idno ) == 0 and int( fatsidno ) > 0 :


#	cursor.execute( "insert into fault ( issue, idescribe, solution, sdescribe, section, section2, datein, operator, status, todo ) values \
#	( 'newIssue', '', '', '', '.none', '.none', nowstamp, 'none', 'Active', '' ) " ) 

	cursor2.execute( "insert into fcomments ( solution, sdescribe, datein, operator, todo, faultidno ) values \
	( 'newSolution', '', '%s', '%s', '', '%s' ) " % ( nowstamp, username, fatsidno ) ) 
	
	cursor2.execute("select last_insert_id()")
	auto_idno = cursor2.fetchone()
	idno = str( auto_idno[0] )

#if logproc.validCookie() :

if int( idno ) > 0 :


#	username = 'winegar'	
#	end = 'none'

	pagename = '<center><b>Fault Comments Display</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
#	pagename += '<br>' + logproc.getOPALMenu() + '<br>'

#	orderby = "order by %s" % ( order )

		
#	if order == 'section' :

#		orderby = "order by section"
	
		
				
#	cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes, operator, section2, todo, status from fault where idno = %s" % ( idno ) )	
	cursor.execute("select idno, solution, sdescribe, datein, operator, todo, faultidno from fcomments where idno = %s" % ( idno ) )	


	numrows=cursor.rowcount

		
	


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
	maintext += 'idno: ' + idno + '<br>'
	
	maintext += '<br><b>FATS Comments Display</b><br><br>'

#	maintext += year_spin + '<br>'
	
#	maintext += 'OrderBy: <a href=fatslist.py?order=date>IDNo</a> | ' 
#	maintext += '<a href=fatslist.py?order=section>Section</a> | ' 
	mprogram = 'fatscomment.py'

	maintext += "<form  method=POST action=%s?><br>" % ( mprogram )

#	maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Type</th><th>Value</th></tr>'
	seq = 0

#	if False :
	faultText = ''

	if numrows == 1 :

		seq += 1
#	cursor.execute("select idno, issue, idescribe, solution, sdescribe, section, datein, likes, dislikes from fault %s" % ( orderby )	

		row = cursor.fetchone()

		fats_idno = str( row[0] )
#		fats_issue = row[1]
#		fats_idescribe = row[2]
		fats_solution = row[1]
		fats_sdescribe = row[2]
#		fats_section = row[5]
		fats_date = row[3]
		fats_operator = row[4]
#		fats_section2 = row[10]
		fats_todo = row[5]
		faultidno = row[6]
#		fats_status = row[12]

#		fats_issue = fats_issue.strip()
#		fats_idescribe = fats_idescribe.strip()
		fats_solution = fats_solution.strip()
		fats_sdescribe = fats_sdescribe.strip()
#		fats_section = fats_section.strip()
		fats_operator = fats_operator.strip()
#		fats_section2 = fats_section2.strip()
		fats_todo = fats_todo.strip()
#		fats_status = fats_status.strip()

		fats_date = str( fats_date )
		fats_date = fats_date[0:16]

		cursor2.execute( "select idno, issue, idescribe, solution, sdescribe, section, section2, datein, operator, status, todo from fault where idno = %s " \
		% ( faultidno )  ) 

		numrows2=cursor2.rowcount
		if numrows2 == 1 :
			faultText += '<b>The Main Fault # ' + str( faultidno ) + '</b><br><br>'
			faultText += '<table border=1 rules=all>'
			row2 = cursor2.fetchone()
			fault_idno = str( row2[0] )
			fault_issue = row2[1]
			fault_idescribe = row2[2]
			fault_solution = row2[3]
			fault_sdescribe = row2[4]
			fault_section = row2[5]
			fault_section2 = row2[6]
			fault_date = str( row2[7] )
			fault_operator = row2[8]
#			fault_status = row[9]
#			fault_todo = row2[10]
			faultText += '<tr><td>FATS IDNo#</td><td>' + fault_idno + '</td></tr>'
			faultText += '<tr><td>Issue:</td><td> ' + fault_issue + '</td></tr>'
			faultText += '<tr><td>IssueDescribe:</td><td> ' + fault_idescribe + '</td></tr>'
			faultText += '<tr><td>Solution:</td><td> ' + fault_solution + '</td></tr>'
			faultText += '<tr><td>SolutionDescribe:</td><td> ' + fault_sdescribe + '</td></tr>'
			faultText += '<tr><td>Operator</td><td> ' + fault_operator + ' | Date: ' + fault_date[0:16] + '</td></tr>'
			faultText += '</table><br><hr>'
		

	savePOSTs = ( 'Cancel', 'Save' )

	maintext += faultText

#	if False :
	if int(idno) > 0 and method == 'POST' and field['action'].value == 'Edit' : 

		maintext += "<br><b>This Comment #" + fats_idno + '</b><br><br>'

		cursor3.execute("select name from fstaff order by name"  )	
		numrows3=cursor3.rowcount

		staff_spinner = '<select option=1 name=operator>'
		if numrows3 > 0 :
			for ruw in cursor3.fetchall() :

				if ruw[0] == fats_operator: 

					staff_spinner += '<option value=%s selected>%s' % ( ruw[0], ruw[0] )
				else: 
					staff_spinner += '<option value=%s>%s' % ( ruw[0] , ruw[0])

		staff_spinner += '</select>'



		maintext += "<input type=submit name=action value=Save> | <input type=submit name=action value=Cancel>"
		maintext += "<input type=hidden name=idno value=%s><br><br>" % ( idno ) 

		maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Type</th><th>Value</th></tr>'

		maintext += "<tr><td>%s</td><td>%s | Date: %s | Comment IDNo: %s</td></tr>" % ( 'Operator:', fats_operator,  fats_date, fats_idno )
#			maintext += "<tr><td>%s</td><td>%s | Section2: %s</td></tr>" % ( 'Section1:', section_spinner, section2_spinner )
#			maintext += "<tr><td>%s</td><td><input name=%s type=text size=200 value='%s'></a></td></tr>" % ( 'Issue: ',  'issue', fats_issue )
#			maintext += "<tr><td>%s</td><td><textarea id='mytextarea' name=%s rows=14 cols=60>%s</textarea></td></tr>" % (  'Issue Describe: ', 'idescribe', fats_idescribe )
		maintext += "<tr><td>%s</td><td><input name=%s type=text size=100 value='%s'></a></td></tr>" % ( 'To Do: ',  'todo', fats_todo )

		maintext += "<tr><td>%s</td><td><input name=%s type=text size=200 value='%s'></td></tr>" % ( 'Solution:', 'solution', fats_solution )
		maintext += "<tr><td>%s</td><td><textarea id='mytextarea' name=%s rows=14 cols=60>%s</textarea></td></tr>" % ( 'Solution Describe:', 'sdescribe', fats_sdescribe )

#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Section:', fats_section )
#			maintext += "<tr><td>%s</td><td>%s | Section2: %s</td></tr>" % ( 'Section1:', section_spinner, section2_spinner )
#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Section2:', section2_spinner )

		maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Operator: ', staff_spinner )
#			maintext += "<tr><td>%s</td><td><input name=%s type=text size=20 value='%s'></td></tr>" % ( 'Date:', 'datein', fats_date )

#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Status', fats_status )
#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Status', status_spinner )

		maintext += '</table>'

	savePOSTs = ( 'Cancel', 'Save' )

	if int( idno ) > 0 and ( method == 'GET' or ( method == 'POST' and  field['action'].value in savePOSTs ) ) :

# FATS Fields
		maintext += "<br><b>This Comment #" + fats_idno + '</b><br><br>'
		maintext += "<input type=submit name=action value=Edit>"
		maintext += "<input type=hidden name=idno value=%s><br><br>" % ( idno ) 
		

		seq = 0

		if numrows == 1 :

			seq += 1

			maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3><tr><th>Type</th><th>Value</th></tr>'
			maintext += "<tr><td>%s</td><td><b>%s</b> | Date: %s |  Comment IDNo: %s</td></tr>" % ( 'Operator:', fats_operator, fats_date, fats_idno )
#			maintext += "<tr><td>%s</td><td>%s | %s</td></tr>" % ( 'Section1 | 2:', fats_section, fats_section2 )
#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Section2:', fats_section2 )
#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Status:', fats_status )
			maintext += "</table><br><br>"

			maintext += '<table rules=all border=2 cellpadding=3 cellspacing=3>'
#			maintext += "<tr><td>%s</td><td><b>%s</b></td></tr>" % ( 'Issue: ',  fats_issue )
#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Issue Describe: ',  fats_idescribe )

			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'To Do: ',  fats_todo )

			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Solution:', fats_solution )
			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Solution Describe:', fats_sdescribe )
			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Date:', fats_date )
#			maintext += "<tr><td>%s</td><td>%s</td></tr>" % ( 'Status:', fats_status )

			maintext += "</table><br><br>"

	
	
	maintext += "</form>" 

# POST			

else :
	
	maintext += "No Fault Comment to Display, IDNO == 0 <br>"	
		
#	maintext = logproc.returnLogin()

#maintext = 'tom'
printHTML( maintext )
