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
import logproc3 as logproc

import smtplib
import html

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import logproc


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

def orderTable ( order ) :

	orderTable = '<table rules=all border=1><tr>'
	
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
		orderTable += '<td bgcolor=white width=6></td>'
		
	orderTable += '</tr></table>'
		

	return ( orderTable )

def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:12px }"
#	css_text += "tr:nth-child(even) { background: #CCC; }"
#	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 16px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 16px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 14px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 14px; font-weight: bold }"
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
dow=now.strftime('%a')



if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '11060'
	
  

if 'mail' in field :

	mail = field['mail'].value

else:

	mail = 'yes'
	     
if logproc.validCookie() :

#if True :

	username, end, term, logcrew2 = logproc.getUsername()
#	username='tom'
#	end='now'
#	termlimit = str( now + term )

#	pagename=' top of page'
	pagename = '<center><b>TSR Mail</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu() + '<br>' 
	pagename += logproc.getOPALMenu() + '<br>' 
#	pagename += getMenu()
	
#	pagename += '<br>' + logproc.getCarMenu() + '<br>'
	

#	cursor.execute("select idno, propid, name, piidno, pw, gid, nights, instr, datein, dateout, sem, \
#	first, last, username, comment, subidno, stn_flag, ulogin, eng, public, engseq \
#	from props where idno = '%s'" % ( idno ) )

	cursor.execute("select idno, propidno, allocidno, date, instr, ss, last, first, propid, focus, arrive, \
	ag, sv, adc, imr, cal, flats, polar, ao, irm2, pmdusk, \
	pmdome, amdawn, amdome, flatrun, calrun, comments, calcomm, imrcomm, day, gid, \
	pmcomm, amcomm, observers, obsarrive, location, sh, chop, m2, m3, adccomm, \
	amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, program, ordering, \
	wpulgs, ocs, m2offset, others, alloc, confirm, ao2, queue, agcomm, pmcal \
	from tsr where idno = '%s'" % ( idno ) )
#	idno2 = 7997

#	cursor.execute("select idno, propidno, allocidno, date, instr, ss, last, first, propid, focus, arrive from tsr where idno = '%s'" % ( idno ) )

#	cursor.execute("select idno, propid from props where idno = '%s' " % ( idno ) ) 
		
	numrows=cursor.rowcount
#	maintext = pagename 
	pagename += 'rows: ' + str( numrows ) + '<br>'
	
#	maintext += '<table cellpadding=3 cellspacing=3>'
	admin_users = ( 'winegar', 'noriko', 'letawsky', 'roth' )

	maintext = ''	
	maintext1 = ''
	maintext2 = ''
	
#	if numrows == 0 :
	
#		maintext += 'zero records'
	
#	else:
#	if False :

	if numrows == 1 :
	
		row = cursor.fetchone()

		tsr_idno = str( row[0] )
		tsr_propidno = row[1]
		tsr_allocidno = row[2]
		tsr_date = row[3]
		tsr_instr = row[4]
		tsr_ss = row[5]
		
		tsr_last = row[6]
		tsr_first = row[7]
		tsr_propid = row[8]
		tsr_focus = row[9]
		tsr_arrive = row[10]

		tsr_ag = row[11]
		tsr_sv = row[12]
		tsr_adc = row[13]
		tsr_imr = row[14]
		tsr_cal = row[15]

		tsr_flats = row[16]
		tsr_polar = row[17]
		tsr_ao = row[18]
		tsr_irm2 = row[19]
		tsr_pmdusk = row[20]
		
#	pmdome, amdawn, amdome, flatrun, calrun, comments, calcomm, imrcomm, day, gid, \

		tsr_pmdome= row[21]
		tsr_amdawn = row[22]
		tsr_amdome = row[23]
		tsr_flatrun = row[24]
		tsr_calrun = row[25]

		tsr_comments = row[26]
		tsr_calcomm = row[27]
		tsr_imrcomm = row[28]
		tsr_day = row[29]
		tsr_gid = row[30]

#	pmcomm, amcomm, observers, obsarrive, location, sh, chop, m2, m3, adccomm, \

		tsr_pmcomm = row[31]
		tsr_amcomm = row[32]
		tsr_observers = row[33]
		tsr_obsarrive = row[34]
		tsr_location = row[35]

		tsr_sh = row[36]
		tsr_chop = row[37]
		tsr_m2 = row[38]
		tsr_m3 = row[39]
		tsr_adccomm = row[40]


#		amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, program, ordering, \

		tsr_amfini = row[41]
		tsr_instrot = row[42]
		tsr_flatcomm = row[43]
		tsr_sslist = row[44]
		tsr_oplist = row[45]

		tsr_remhilo = row[46]
		tsr_remmtk = row[47]
		tsr_amcal = row[48]
		tsr_program = row[49]
		tsr_ordering = row[50]

# 	wpulgs, ocs, m2offset, others, alloc, confirm, ao2, queue, agcomm \

		tsr_wpulgs = row[51]
		tsr_ocs = row[52]
		tsr_m2offset = row[53]
		tsr_others = row[54]
		tsr_alloc = row[55]

		tsr_confirm = row[56]
		tsr_ao2 = row[57]
		tsr_queue = row[58]
		tsr_agcomm = row[59]
		tsr_pmcal = row[60]

		dayText = tsr_date.strftime('%a')

		focusAdds = ''

		if tsr_adc == 'In':	
		
			focusAdds += 'ADC '

		if tsr_imr == 'Yes':	
		
			focusAdds += 'ImR '

		if tsr_ao == 'Yes':	
	
			focusAdds += 'AO '

		tsr_orderTable = orderTable( tsr_ordering )

		
#		tsr_ordering = row[60]
	
	
		safeGets = ( 'Save', 'Save Night', 'Cancel' )


#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

#		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' ) ) :
#		if method == 'GET'  :
		if True :

#			if username in admin_users :
			
#			maintext += "<a href=tsrmailpy?idno=%s&mail=yes>Send TSR Email | <a href=tsrmail.py?idno=%s&mail=no>Print-only TSR Email<br>" % ( tsr_idno, tsr_idno )

	# outside main box boundary
			if mail == 'no' :
			
				maintext += 'Telescope Setup Request - %s %s %s<br><br>' % ( tsr_date, dayText, tsr_instr )
			
			maintext += '<table cellpadding=3 cellspacing=3><td valign=top><center>'

			# telescope table

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2>Telescope (9)</th></tr>'
			
			maintext += "<tr><td class=right>Date:</td><td>%s %s</td></tr>" % ( tsr_date, dayText ) 
			
			maintext += "<tr><td class=right>Instr:</td><td>%s</td></tr>" % ( tsr_instr ) 
			maintext += "<tr><td class=right>Focus:</td><td>%s %s</td></tr>" % ( tsr_focus, focusAdds )
			maintext += "<tr><td class=right>M2:</td><td>%s</td></tr>" % ( tsr_m2 )
			maintext += "<tr><td class=right>M2-Offset:</td><td>%s</td></tr>" % ( tsr_m2offset ) 
			maintext += "<tr><td class=right>M3:</td><td>%s</td></tr>" % ( tsr_m3 )
			maintext += "<tr><td class=right>Operator Location:</td><td>%s</td></tr>" % ( tsr_location ) 
			maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
			maintext += "<tr><td class=right>Remote Mitaka:</td><td>%s</td></tr>" % ( tsr_remmtk )
			
			maintext += '</table><br>'

#			maintext2 += "Telescope: \n"
#			maintext2 += "Date: %s \n" % ( tsr_date ) 			
#			maintext2 += "Instr: %s \n" % ( tsr_instr ) 
#			maintext2 += "Focus: %s \n" % ( tsr_focus )
#			maintext2 += "M2: %s \n" % ( tsr_m2 )
#			maintext2 += "M2-Offset: %s \n" % ( tsr_m2offset ) 
#			maintext2 += "M3: %s \n" % ( tsr_m3 )
#			maintext2 += "Operator Location: %s \n" % ( tsr_location ) 
#			maintext2 += "Remote Hilo: %s\n" % ( tsr_remhilo )
#			maintext2 += "Remote Mitaka: %s \n" % ( tsr_remmtk )
			
			# Options table
#		else :

			if True:
			
				maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=4>Options (14)</th></tr>'
				maintext += '<tr><th>Desc</th><th>Yes</th><th>No</th><th>Comments</th></tr>'
			
			
				if tsr_ag == 'Yes':
					maintext += "<tr><td class=right>AG:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_ag, '', tsr_agcomm ) 
				else:
					maintext += "<tr><td class=right>AG:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_ag, tsr_agcomm ) 

				if tsr_sh == 'Yes':				
					maintext += "<tr><td class=right>SH:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_sh, '', '' )
				else :
					maintext += "<tr><td class=right>SH:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_sh, '' )

				if tsr_sv == 'Yes':				
					maintext += "<tr><td class=right>SV:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_sv, '', '' )
				else :
					maintext += "<tr><td class=right>SV:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_sv, '' )

				if tsr_cal == 'Yes':				
					maintext += "<tr><td class=right>CAL:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_cal, '', tsr_calcomm )
				else :
					maintext += "<tr><td class=right>CAL:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_cal, tsr_calcomm )
			 
	#			maintext += "<tr><td class=right>CAL:</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsr_cal, 'Yes', '' )

				if tsr_adc == 'In':				
					maintext += "<tr><td class=right>ADC:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_adc, '', tsr_adccomm )
				else :
					maintext += "<tr><td class=right>ADC:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_adc, tsr_adccomm )

	#			maintext += "<tr><td class=right>ADC:</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsr_adc, 'Yes', '' ) 

				if tsr_instrot == 'Yes':				
					maintext += "<tr><td class=right>InstRot:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_instrot, '', '' )
				else :
					maintext += "<tr><td class=right>InstRot:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_instrot, '' )

	#			maintext += "<tr><td class=right>InstRot:</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsr_instrot, 'Yes', '' )
				if tsr_imr == 'Yes':				
					maintext += "<tr><td class=right>ImR:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_imr, '', tsr_imrcomm )
				else :
					maintext += "<tr><td class=right>ImR:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_imr, tsr_imrcomm )
				
	#			maintext += "<tr><td class=right>ImR:</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsr_imr, 'Yes', '' ) 
				if tsr_flats == 'Yes':				
					maintext += "<tr><td class=right>Dome Flats:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_flats, '', tsr_flatcomm )
				else :
					maintext += "<tr><td class=right>Dome Flats:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_flats, tsr_flatcomm )
				
	#			maintext += "<tr><td class=right>Dome Flats:</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsr_flats, 'Yes', '')
				if tsr_polar == 'In':				
					maintext += "<tr><td class=right>Wave Plate:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_polar, '', '' )
				else :
					maintext += "<tr><td class=right>Wave Plate:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_polar, '' )
			
	#			maintext += "<tr><td class=right>WavePlate:</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( tsr_wpulgs, 'Yes', '' )
				if tsr_ao == 'AO188':				
					maintext += "<tr><td class=right>AO-1:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_ao, '', '' )
				else :
					maintext += "<tr><td class=right>AO-1:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_ao, '' )

				if tsr_ao2 == 'Yes':				
					maintext += "<tr><td class=right>AO-2:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_ao2, '', '' )
				else :
					maintext += "<tr><td class=right>AO-2:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_ao2, '' )

				if tsr_wpulgs == 'Yes':				
					maintext += "<tr><td class=right>LGS:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_wpulgs, '', '' )
				else :
					maintext += "<tr><td class=right>LGS:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_wpulgs, '' )

				if tsr_chop == 'Yes':				
					maintext += "<tr><td class=right>Chopping:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_chop, '', '' )
				else :
					maintext += "<tr><td class=right>Chopping:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_chop, '' )

				if tsr_queue == 'Yes':				
					maintext += "<tr><td class=right>Queue:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( tsr_queue, '', '' )
				else :
					maintext += "<tr><td class=right>Queue:</td><td class=center>%s</td><td class=center>%s</td><td>%s</td></tr>" % ( '', tsr_queue, '' )
			
				maintext += '</table>'

			# outside boundary column split
			
				maintext += '</center></td><td valign=top><center>'

				# Program table

				maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=3>Program (14)</th></tr>'
			
				maintext += "<tr><td class=right>Proposal ID:</td><td>%s</td></tr>" % ( tsr_propid ) 
				maintext += "<tr><td class=right>Group ID:</td><td>%s</td></tr>" % ( tsr_gid ) 
				maintext += "<tr><td class=right>Alloc:</td><td>%s</td></tr>" % ( tsr_alloc )
				maintext += "<tr><td class=right>PI:</td><td>%s</td></tr>" % ( tsr_last )
				maintext += "<tr><td class=right>SS:</td><td>%s</td></tr>" % ( tsr_ss ) 
				maintext += "<tr><td class=right>SS List:</td><td>%s</td></tr>" % ( tsr_sslist )
				maintext += "<tr><td class=right>Ops List:</td><td>%s</td></tr>" % ( tsr_oplist ) 
				maintext += "<tr><td class=right>Ops Arrive:</td><td>%s</td></tr>" % ( tsr_arrive )
				maintext += "<tr><td class=right>Observers:</td><td>%s</td></tr>" % ( tsr_observers )
				maintext += "<tr><td class=right>Obs Arrive:</td><td>%s</td></tr>" % ( tsr_obsarrive )
				maintext += "<tr><td class=right>Others:</td><td>%s</td></tr>" % ( tsr_others )
				maintext += "<tr><td class=right>Comments:</td><td>%s</td></tr>" % ( tsr_comments )
				maintext += "<tr><td class=right>Program:</td><td>%s</td></tr>" % ( tsr_program ) 
#				maintext += "<tr><td class=right>Ordering:</td><td>%s</td></tr>" % ( tsr_ordering )
				maintext += "<tr><td class=right>Ordering:</td><td>%s</td></tr>" % ( tsr_orderTable )
				maintext += "<tr><td class=right>Confirm:</td><td>%s</td></tr>" % ( tsr_confirm )
			
				maintext += '</table><br>'

			# PM Calib table

				maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=3>PM Calibration  (4)</th></tr>'
			
				if tsr_pmdusk == 'Yes':				
					maintext += "<tr><td class=right>Twilight Flats:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( tsr_pmdusk, '' )
				else :
					maintext += "<tr><td class=right>Twilight Flats:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( '', tsr_pmdusk )
				
	#			maintext += "<tr><td class=right>Twilight Flats:</td><td>%s</td><td>%s</td></tr>" % ( '', tsr_queue )

				if tsr_pmdome == 'Yes':		
					maintext += "<tr><td class=right>Dome Flats:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( tsr_pmdome, '' )
				else :
					maintext += "<tr><td class=right>Dome Flats:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( '', tsr_pmdome )
			
	#			maintext += "<tr><td class=right>Twilight Flats:</td><td>%s</td><td>%s</td></tr>" % ( '', tsr_queue )
	#			maintext += "<tr><td class=right>Dome Flats:</td><td>%s</td></tr>" % ( tsr_gid ) 
				if tsr_pmcal == 'Yes':		
					maintext += "<tr><td class=right>CAL:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( tsr_pmcal, '' )
				else :
					maintext += "<tr><td class=right>CAL:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( '', tsr_pmcal )

	#			maintext += "<tr><td class=right>CAL:</td><td>%s</td></tr>" % ( tsr_alloc )
				maintext += "<tr><td class=right>PM Comments:</td><td colspan=2>%s</td></tr>" % ( tsr_pmcomm )
			
				maintext += '</table><br>'

			# AM Calib table

				maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=3>AM Calibration  (6)</th></tr>'
			
				if tsr_amdawn == 'Yes':		
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'Twilight Flats', tsr_amdawn, '' )
				else :
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'Twilight Flats', '', tsr_amdawn )
				
	#			maintext += "<tr><td class=right>Twilight Flats:</td><td>%s</td></tr>" % ( tsr_amdawn ) 
	#			maintext += "<tr><td class=right>Dome Flats:</td><td>%s</td></tr>" % ( tsr_amdome ) 
				if tsr_amdome == 'Yes':		
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'Dome Flats', tsr_amdome, '' )
				else :
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'Dome Flats', '', tsr_amdome )
				if tsr_amcal == 'Yes':		
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'CAL', tsr_amcal, '' )
				else :
					maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'CAL', '', tsr_amcal )

	#			maintext += "<tr><td class=right>CAL:</td><td>%s</td></tr>" % ( tsr_amcal )
				if tsr_flatrun == 'Yes':		
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'Darks Running', tsr_flatrun, '' )
				else :
					maintext += "<tr><td class=right>%s:</td><td class=center>%s</td><td class=center>%s</td></tr>" % ( 'Darks Running', '', tsr_flatrun )
	#			maintext += "<tr><td class=right>DARKs Running:</td><td>%s</td></tr>" % ( tsr_flatrun )
				maintext += "<tr><td class=right>%s:</td><td colspan=2>%s</td></tr>" % ( 'Finish Time', tsr_amfini )
				maintext += "<tr><td class=right>%s:</td><td colspan=2>%s</td></tr>" % ( 'Comments', tsr_amcomm )
			
				maintext += '</table><br>'

				# Admin table

				maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2>Admin (2)</th></tr>'
			
				maintext += "<tr><td class=right>IDNo:</td><td class=center>%s</td></tr>" % ( tsr_idno ) 
				maintext += "<tr><td class=right>Alloc IDNo:</td><td class=center>%s</td></tr>" % ( tsr_allocidno ) 
			
				maintext += '</table>'

			
			maintext += '</center></td></table>'
			
			# end of TSR table

			if mail == 'yes'  or mail == 'self' :

				smtpserver=( 'mail.subaru.nao.ac.jp' )
#				session = smtplib.SMTP( smtpserver )
				sender = 'winegar@naoj.org'

				gecos = 'Tom Winegar'
				mailaddress = 'winegar@naoj.org'	
#				recipient = 'twinegar7@gmail.com
#				recipient = [  'twinegar7@gmail.com', 'winegar@naoj.org' ]
				
				if username == 'winegar' or mail == 'self' :
				
					usermail = username + '@naoj.org'
					recipient = [ usermail, 'twinegar7@gmail.com' ]
					mailTo = usermail
								
				else :
				
					recipient = [ 'twinegar7@gmail.com', 'telsetup@naoj.org' ]
					mailTo =  'telsetup@naoj.org'
						
				mailSubject = "TSR Telescope Setup Request %s %s %s - %s %s" % ( tsr_date, dayText, tsr_instr, tsr_focus, focusAdds )

				mailFrom = "OPAL Mailer <winegar@naoj.org>"
				mailCC = "Tom Winegar <winegar@naoj.org>"
				mailHeader = "From: %s\r\nTo: %s\r\nSubject: %s\r\nCC: %s\r\n" % ( mailFrom, mailTo, mailSubject, mailCC )

	#			mailText = ("<FONT SIZE=4>Subaru DayCrew SummitWork<br><FONT SIZE=3>%s - %s<br><FONT SIZE=2>[ %s ]<br><br>" % ( date, dow, now2[0:16] ) )
				mailText1 = maintext
				mailText2 = maintext2
#				msg = MIMEText ( mailText )
				msg=MIMEMultipart()
				

				msgattach = MIMEText( mailText2.encode('utf-8'), 'plain', 'UTF-8')
				msg.attach( msgattach )

				msgattach = MIMEText( mailText1.encode('utf-8'), 'html', 'UTF-8')
				msg.attach( msgattach )
#				msg = MIMEText ( 'test msg' )
#				msg = 'test msg' 

				s = smtplib.SMTP( smtpserver )
				
				msg['From'] = mailFrom
				msg['To'] = mailTo
				msg['Subject'] = mailSubject
				msg['CC'] = mailCC
				
#				s.send_message ( msg )
		# simpetext send
#				s.send_message ( msg )

		# multipart code        
				s.sendmail( sender, recipient, msg.as_string())

		#       smtpresult=session.sendmail( sender, recipient, msg.as_string())

#				cursor2.execute("update tsr set confirm='%s' where idno='%s'" % ( True, idno ) )

				s.quit()

				if not mail == 'self' :
				
					cursor2.execute("update tsr set confirm = True where idno = '%s'" % ( tsr_idno ) )
			
				tsrLink = "<a href=tsrone.py?idno=%s>back to TSR: %s %s %s</a>" % ( tsr_idno, str( tsr_date ), tsr_instr, tsr_propid )
				
				maintext = pagename + "<br>Email SENT: %s %s<br>%s" % ( mailTo, tsrLink, maintext )
				
				
			else:
			
				tsrLink = "<a href=tsrone.py?idno=%s>back to TSR: %s %s %s</a>" % ( tsr_idno, str( tsr_date ), tsr_instr, tsr_propid )
			
				maintext = pagename + "<br>Email NOT SENT. %s<br>%s" % ( tsrLink, maintext )

			
	else :
		
		maintext += pagename + "No Records!<br>"
				
#	maintext += "</table>"
else :

	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
