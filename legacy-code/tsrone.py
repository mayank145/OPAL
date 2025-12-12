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

def getMenu() :

	maintext = '<table><tr>'
	maintext += '<td bgcolor=lime><New OPAL</td>'	
	maintext += '<td><a href=proplist.py>Proposals</a></td>'
	maintext += '<td><a href=tsrlist.py>TSRs</a></td>'
	maintext += '</tr><table>'
	
	return ( maintext )


now=datetime.datetime.now()
today=now.strftime('%Y-%m-%d')



if 'idno' in field :

	idno = field['idno'].value
	
else:
	
	idno = '0'
	
if 'propidno' in field :

	propidno = field['propidno'].value

else:

	propidno = '0'
	

if 'allocidno' in field :

	allocidno = field['allocidno'].value
	
else:
	
	allocidno = '0'

if 'date' in field :

	date = field['date'].value
	
else:
	
	date = ''

if 'instr' in field :

	instr = field['instr'].value
	
else:
	
	instr = ''

if 'focus' in field :

	focus = field['focus'].value

else:

	focus = ''
	
if 'm2' in field :

	m2 = field['m2'].value

else:

	m2 = ''
	
if 'm2offset' in field :

	m2offset = field['m2offset'].value

else:

	m2offset = ''
	
if 'm3' in field :

	m3 = field['m3'].value

else:

	m3 = ''
	
if 'location' in field :

	location = field['location'].value

else:

	location = ''
	
if 'remhilo' in field :

	remhilo = field['remhilo'].value

else:

	remhilo = ''
	
if 'remmtk' in field :

	remmtk = field['remmtk'].value

else:

	remmtk = ''	
	
if 'ag' in field :

	ag = field['ag'].value

else:

	ag = ''	
	
if 'sh' in field :

	sh = field['sh'].value

else:

	sh = ''	
	
if 'sv' in field :

	sv = field['sv'].value

else:

	sv = ''	
	
if 'cal' in field :

	cal = field['cal'].value

else:

	cal = ''
	
if 'adc' in field :

	adc = field['adc'].value

else:

	adc = ''
	
if 'instrot' in field :

	instrot = field['instrot'].value

else:

	instrot = 'No'
	
if 'imr' in field :

	imr = field['imr'].value

else:

	imr = ''
	
if 'flats' in field :

	flats = field['flats'].value

else:

	flats = ''
	
if 'polar' in field :

	polar = field['polar'].value

else:

	polar = ''


if 'wpulgs' in field :

	wpulgs = field['wpulgs'].value

else:

	wpulgs = ''	
	
if 'ao' in field :

	ao = field['ao'].value

else:

	ao = ''	
	
if 'ao2' in field :

	ao2 = field['ao2'].value

else:

	ao2 = ''
	
if 'chop' in field :

	chop = field['chop'].value

else:

	chop = ''
	
if 'queue' in field :

	queue = field['queue'].value

else:

	queue = ''
	
if 'agcomm' in field :

	agcomm = field['agcomm'].value

else:

	agcomm = ''
	
if 'calcomm' in field :

	calcomm = field['calcomm'].value

else:

	calcomm = ''
	
if 'adccomm' in field :

	adccomm = field['adccomm'].value

else:

	adccomm = ''
	
if 'imrcomm' in field :

	imrcomm = field['imrcomm'].value

else:

	imrcomm = ''
	
if 'flatcomm' in field :

	flatcomm = field['flatcomm'].value

else:

	flatcomm = ''
	
if 'propid' in field :

	propid = field['propid'].value

else:

	propid = ''

if 'gid' in field :

	gid = field['gid'].value

else:

	gid = ''

if 'alloc' in field :

	alloc = field['alloc'].value

else:

	alloc = ''	
	
if 'last' in field :

	last = field['last'].value

else:

	last = ''
	
if 'ss' in field :

	ss = field['ss'].value

else:

	ss = ''	
	
if 'sslist' in field :

	sslist = field['sslist'].value

else:

	sslist = ''
		
if 'oplist' in field :

	oplist = field['oplist'].value

else:

	oplist = ''	

if 'arrive' in field :

	arrive = field['arrive'].value

else:

	arrive = ''		

if 'observers' in field :

	observers = field['observers'].value

else:

	observers = ''	

if 'obsarrive' in field :

	obsarrive = field['obsarrive'].value

else:

	obsarrive = ''	
		
if 'others' in field :

	others = field['others'].value

else:

	others = ''	
	
if 'comments' in field :

	comments = field['comments'].value

else:

	comments = ''
	
if 'program' in field :

	program = field['program'].value

else:

	program = ''	

if 'pmdusk' in field :

	pmdusk = field['pmdusk'].value

else:

	pmdusk = ''
	
if 'pmdome' in field :

	pmdome = field['pmdome'].value

else:

	pmdome = ''
	
if 'pmcal' in field :

	pmcal = field['pmcal'].value

else:

	pmcal = ''
	
if 'pmcomm' in field :

	pmcomm = field['pmcomm'].value

else:

	pmcomm = ''
	
if 'amdawn' in field :

	amdawn = field['amdawn'].value

else:

	amdawn = ''

if 'amdome' in field :

	amdome = field['amdome'].value

else:

	amdome = ''
	
if 'amcal' in field :

	amcal = field['amcal'].value

else:

	amcal = ''
	
if 'amfini' in field :

	amfini = field['amfini'].value

else:

	amfini = ''
	
if 'amcomm' in field :

	amcomm = field['amcomm'].value

else:

	amcomm = ''
	
if 'flatrun' in field :

	flatrun = field['flatrun'].value

else:

	flatrun = ''
#if 'datein' in field :

#	datein = field['datein'].value
	
#else:
	
#	datein = '00'
	




if 'copy' in field :

	copy = field['copy'].value

else:

	copy = 'first'
	
if 'order1' in field :

	order1 = field['order1'].value

else:

	order1 = '0'



       
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

		cursor2.execute("update tsr set date = '%s', instr = '%s', focus = '%s', m2 = '%s', m2offset = '%s', \
		m3 = '%s', location = '%s', remhilo = '%s', remmtk = '%s', ag = '%s', sh = '%s', sv = '%s', \
		cal = '%s', adc = '%s', instrot = '%s', imr = '%s' where idno = '%s'" \
		% ( date, instr, focus, m2, m2offset, m3, location, remhilo, remmtk, ag, sh, sv, cal, adc, instrot, imr, idno) )		
		
		cursor2.execute("update tsr set flats = '%s', wpulgs = '%s', ao = '%s', ao2 = '%s', chop = '%s', queue = '%s', \
		agcomm = '%s', calcomm = '%s', adccomm = '%s', imrcomm = '%s', flatcomm = '%s', propid = '%s', gid = '%s', alloc = '%s', \
		last = '%s', ss = '%s', sslist = '%s', oplist = '%s', arrive = '%s', observers = '%s', obsarrive = '%s', others = '%s', comments = '%s', \
		program = '%s' where idno = '%s'" \
		% ( flats, wpulgs, ao, ao2, chop, queue, agcomm, calcomm, adccomm, imrcomm, flatcomm, propid, gid, alloc, last, ss, sslist, oplist, \
			arrive, observers, obsarrive, others, comments, program, idno ) )		


		cursor2.execute("update tsr set amdawn = '%s', amdome = '%s', amcal = '%s', flatrun = '%s', amfini = '%s', amcomm = '%s', \
		pmdusk = '%s', pmdome = '%s', pmcal='%s', pmcomm='%s' , polar='%s' where idno = '%s'" \
		% ( amdawn, amdome, amcal, flatrun, amfini, amcomm, pmdusk, pmdome, pmcal, pmcomm, polar, idno ) )	
		
		
#				cursor2.execute("update tsr set flats = '%s', wpulgs = '%s', ao = '%s', ao2 = '%s', chop = '%s', queue = '%s', \
#				agcomm = '%s', calcomm = '%s', adccomm = '%s', imrcomm = '%s', flatcomm = '%s', propid = '%s', gid = '%s', alloc = '%s', \
#				last = '%s', ss = '%s', sslist = '%s', oplist = '%s', arrive = '%s', observers = '%s', others = '%s', comments = '%s', \
#				program = '%s' where idno = '%s'" \
#				% ( flats, wpulgs, ao, ao2, chop, queue, agcomm, calcomm, adccomm, imrcomm, flatcomm, propid, gid, alloc, last, ss, sslist, oplist, \
#					arrive, observers, others, comments, program, idno ) )		


#				cursor2.execute("update tsr set amdawn = '%s', amdome = '%s', amcal = '%s', flatrun = '%s', amfini = '%s', amcomm = '%s', \
#				pmdusk = '%s', pmdome = '%s', pmcal='%s', pmcomm='%s' where idno = '%s'" \
#				% ( amdawn, amdome, amcal, flatrun, amfini, amcomm, pmdusk, pmdome, pmcal, pmcomm, idno ) )	
				
			

#		cursor2.execute("update tsr set amdawn = '%s', amdome = '%s', amcal = '%s', flatrun = '%s', amfini = '%s', amcomm = '%s' where idno = '%s'" \
#		% ( amdawn, amdome, amcal, flatrun, amfini, amcomm, idno ) )		

	if method == 'GET' and int( idno ) == 0 and int ( allocidno ) > 0 :
	
		cursor3.execute("select datein, instr, propid, gid, propidno, order1, observers, remote, staff, last, first \
		from alloc where idno = '%s'" % ( allocidno ) )	
		numrows3 = cursor3.rowcount
		if numrows3 == 1 :
		
		

			ruw = cursor3.fetchone()
			alloc_date = ruw[0]
			alloc_instr = ruw[1]
			alloc_propid = ruw[2]		
			alloc_gid = ruw[3]		
			alloc_propidno = ruw[4]				
			alloc_order = ruw[5]				
			alloc_observers = ruw[6]				
			alloc_remote = ruw[7]				
			alloc_staff = ruw[8]				
			alloc_last = ruw[9]				
			alloc_first = ruw[10]				
			
			cursor2.execute("select number from counter where file = '%s'" % ( 'tsr' ) )
			numrows2 = cursor2.rowcount
			counted = cursor2.fetchone()
			newid = counted[0]
			nextid = int( newid ) + 1
			cursor2.execute("update counter set number = '%s' where file = '%s'" % ( nextid, 'tsr' ) )
			
			dow = alloc_date.strftime('%a')
			
			cursor2.execute("insert into tsr ( idno, date, instr, allocidno, propid, gid, propidno, day ) values \
			( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" \
			% ( newid, alloc_date, alloc_instr, allocidno, alloc_propid, alloc_gid, alloc_propidno, dow ) )	
		
			idno = newid
			
			cursor2.execute("update tsr set focus = '%s', m2 = '%s', m2offset = '%s', m3 = '%s', location = '%s', remhilo = '%s', remmtk = '%s', \
			ag = '%s', sh = '%s', sv = '%s', cal = '%s', adc = '%s', instrot = '%s', imr = '%s', confirm='%s', ordering='%s', ocs='%s', \
			polar = '%s', irm2 = '%s', pmdusk='%s', pmdome='%s', pmcal='%s', pmcomm='%s', amdawn='%s', amdome='%s', amcal='%s', amcomm='%s', \
			flatrun='%s', calrun='%s', amfini='%s', obsarrive='%s' \
			where idno = '%s'" \
			% ( 'CsOpt', 'CsOpt', 'CsOpt', 'No', '' , 'None', 'None', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 0, alloc_order, 'Gen2', 'Out', 'No', 'No', 'No', 'No', '', \
			'No', 'No', 'No', '', 'No', 'No', '', '', newid ) )
			
#			cursor2.execute("update tsr set focus = '%s' where idno = '%s'" % ( 'CsOpt', newid ) )

			cursor2.execute("update tsr set flats = '%s', wpulgs = '%s', ao = '%s', ao2 = '%s', chop = '%s', queue = '%s', \
			agcomm = '%s', calcomm = '%s', adccomm = '%s', imrcomm = '%s', flatcomm = '%s', alloc = '%s', last = '%s', first = '%s', \
			ss = '%s', sslist = '%s', oplist = '%s', arrive = '%s', observers = '%s', others = '%s', comments = '%s', \
			program = '%s' where idno = '%s'" \
			% ( 'No', 'No', 'AO188', 'No', 'No', 'No', '', '', '', '', '', '', alloc_last, alloc_first, username, alloc_remote, alloc_staff, \
				'', alloc_observers, '', '', '', newid ) )		

			if copy == 'first' or copy == 'last' :
	
				instrcode='ALL'
	
				cursor3.execute("select code from instr where name = '%s'" % ( alloc_instr ) )
				numrows3 = cursor3.rowcount
				if numrows3 == 1 :
					raw = cursor3.fetchone()
					instrcode=raw[0]

				if copy == 'last' :
				
					cursor3.execute("select idno from tsr where instr='%s' and idno < '%s' order by idno desc" % ( alloc_instr, newid ) )
				
				else:

					cursor3.execute("select idno from tsr where instr='%s' and date='1901-01-01'" % ( alloc_instr ) )
				
					
				numrows3 = cursor3.rowcount
		
				if numrows3 > 0:
		
					raw = cursor3.fetchone()
					firstid = raw[0]				
	
					cursor3.execute("select date, instr, focus, last, first, ss, propid, arrive, ag, sv, adc, \
					imr, cal, flats, polar, ao, irm2, pmdusk, pmdome, pmcal, amdawn, \
					amdome, flatrun, calrun, comments, idno, calcomm, imrcomm, day, gid, pmcomm, \
					amcomm, observers, obsarrive, location, sh, chop, m2, m3, adccomm, propidno, \
					amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, wpulgs, ocs, \
					m2offset, others, queue, agcomm, ao2, alloc from tsr where idno='%s'" % ( firstid ) )
			
					riw = cursor3.fetchone()

					cursor2.execute("update tsr set focus = '%s', m2 = '%s', m2offset = '%s', \
					m3 = '%s', location = '%s', remhilo = '%s', remmtk = '%s', ag = '%s', sh = '%s', sv = '%s', \
					cal = '%s', adc = '%s', instrot = '%s', imr = '%s' where idno = '%s'" \
					% ( riw[2], riw[37], riw[51], riw[38], riw[34], riw[46], riw[47], riw[8], riw[35], riw[9], riw[12], \
						riw[10], riw[42], riw[11], idno ) )		

					cursor2.execute("update tsr set ocs='%s', polar='%s', irm2 = '%s', pmdusk='%s', pmdome='%s', pmcal='%s', \
					pmcomm='%s', amdawn='%s', amdome='%s', amcal='%s', amcomm='%s', flatrun='%s', calrun='%s', amfini='%s', obsarrive='%s' \
					where idno='%s'" \
					% ( riw[50], riw[14], riw[16], riw[17], riw[18], riw[19], riw[30], riw[20], riw[21], riw[48], riw[31], \
						riw[22], riw[23], riw[41], riw[33], idno ) )						

					cursor2.execute("update tsr set flats = '%s', wpulgs = '%s', ao = '%s', ao2 = '%s', chop = '%s', queue = '%s', \
					agcomm = '%s', calcomm = '%s', adccomm = '%s', imrcomm = '%s', flatcomm = '%s', alloc = '%s', last = '%s', first = '%s', \
					ss = '%s', arrive = '%s', others = '%s', comments = '%s' \
					where idno='%s'" \
					% ( riw[13], riw[49], riw[15], riw[54], riw[36], riw[53], riw[54], riw[26], riw[39], riw[27], riw[43], \
						riw[56], alloc_last, alloc_first, username, riw[7], riw[52], riw[24], idno ) )

					# 230420 Alloc.last/first should stay PI

#						% ( riw[13], riw[49], riw[15], riw[54], riw[36], riw[53], riw[54], riw[26], riw[39], riw[27], riw[43], \
#							riw[56], riw[3], riw[4], username, riw[7], riw[52], riw[24], idno ) )

					
	pagename = '<center><b>TSR Display</b> | ' + username + " [" + end + ']<br><br>' 
	
	pagename += logproc.getMenu()
#	pagename += getMenu()
	
	pagename += '<br>' + logproc.getOPALMenu() + '<br>'
	

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
	maintext = pagename 
	maintext += 'rows: ' + str( numrows ) + '<br>'
	
	
#	maintext += '<table cellpadding=3 cellspacing=3>'
	admin_users = ( 'winegar', 'noriko', 'letawsky', 'roth', 'terai' )
	
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
		
		tsr_orderTable = orderTable( tsr_ordering )

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
		
#		tsr_ordering = row[60]
		dayText = tsr_date.strftime('%a')
	
	
		safeGets = ( 'Save', 'Cancel' )


#		maintext += "<tr><td>%s</td><td><a href=carone.py?car=%s>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( seq, car, car, loc, phone, pass2, type )

#		if method == 'GET' or ( method == 'POST' and ( field['action'].value == 'Save' or field['action'].value == 'Cancel' ) ) :
#		if method == 'GET' or ( method == 'POST' and field['action'].value == 'Save'  ) :
		if method == 'GET' or ( method == 'POST' and field['action'].value in safeGets  ) :

#			if username in admin_users :
			
			maintext += "<form method=post action='tsrone.py?idno=%s'><input name=action type=submit value='Edit'></form>" % ( tsr_idno )


			maintext += "<a href=tsrmail.py?idno=%s&mail=yes>Email to TelSetup</a> | <a href=tsrmail.py?idno=%s&mail=self>Email to Self: %s@naoj.org</a> \
			| <a href=tsrmail.py?idno=%s&mail=no>Display-only Test</a><br>" % ( tsr_idno, tsr_idno, username, tsr_idno )
	# outside main box boundary
	
			maintext += '<table cellpadding=3 cellspacing=3><td valign=top><center>'

			# telescope table

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2 bgcolor=lime>Telescope (9)</th></tr>'
			
			maintext += "<tr><td class=right>Date:</td><td>%s %s</td></tr>" % ( tsr_date, dayText ) 
			
			maintext += "<tr><td class=right>Instr:</td><td>%s</td></tr>" % ( tsr_instr ) 
			
			focusAdds = ''

			if tsr_adc == 'In':	
			
				focusAdds += 'ADC '

			if tsr_imr == 'Yes':	
			
				focusAdds += 'ImR '

			if tsr_ao == 'Yes':	
		
				focusAdds += 'AO '
			
			maintext += "<tr><td class=right>Focus:</td><td>%s %s</td></tr>" % ( tsr_focus, focusAdds )
			maintext += "<tr><td class=right>M2:</td><td>%s</td></tr>" % ( tsr_m2 )
			maintext += "<tr><td class=right>M2-Offset:</td><td>%s</td></tr>" % ( tsr_m2offset ) 
			maintext += "<tr><td class=right>M3:</td><td>%s</td></tr>" % ( tsr_m3 )
			maintext += "<tr><td class=right>Operator Location:</td><td>%s</td></tr>" % ( tsr_location ) 
			maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
			maintext += "<tr><td class=right>Remote Mitaka:</td><td>%s</td></tr>" % ( tsr_remmtk )
			
			maintext += '</table><br>'

			# Options table


			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=4 bgcolor=lime>Options (14)</th></tr>'
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

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=3 bgcolor=lime>Program (14)</th></tr>'
			
			maintext += "<tr><td class=right>Proposal ID:</td><td><a href=propone.py?idno=%s>%s</a></td></tr>" % ( tsr_propidno, tsr_propid  ) 
			maintext += "<tr><td class=right>Group ID:</td><td>%s</td></tr>" % ( tsr_gid ) 
			maintext += "<tr><td class=right>Alloc:</td><td>%s</td></tr>" % ( tsr_alloc )
			maintext += "<tr><td class=right>PI:</td><td>%s</td></tr>" % ( tsr_last )
			maintext += "<tr><td class=right>SS:</td><td>%s</td></tr>" % ( tsr_ss ) 
			maintext += "<tr><td class=right>SS List:</td><td>%s</td></tr>" % ( tsr_sslist )
			maintext += "<tr><td class=right>Ops List:</td><td>%s</td></tr>" % ( tsr_oplist ) 
			maintext += "<tr><td class=right>Ops Arrive:</td><td>%s</td></tr>" % ( tsr_arrive )
			maintext += "<tr><td class=right>Observers:</td><td>%s</td></tr>" % ( tsr_observers )
			maintext += "<tr><td class=right>Observers Arrive:</td><td>%s</td></tr>" % ( tsr_obsarrive )
			maintext += "<tr><td class=right>Others:</td><td>%s</td></tr>" % ( tsr_others )
			maintext += "<tr><td class=right>Comments:</td><td>%s</td></tr>" % ( tsr_comments )
			maintext += "<tr><td class=right>Program:</td><td>%s</td></tr>" % ( tsr_program ) 
#			maintext += "<tr><td class=right>Ordering:</td><td>%s</td></tr>" % ( tsr_ordering )
			maintext += "<tr><td class=right>Ordering:</td><td>%s</td></tr>" % ( tsr_orderTable )
			maintext += "<tr><td class=right>Confirm:</td><td>%s</td></tr>" % ( tsr_confirm )
			
			maintext += '</table><br>'

			# PM Calib table

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=3 bgcolor=lime>PM Calibration  (4)</th></tr>'
			
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

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=3 bgcolor=lime>AM Calibration  (6)</th></tr>'
			
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

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2 bgcolor=lime>Admin (2)</th></tr>'
			
			maintext += "<tr><td class=right>IDNo:</td><td class=center>%s</td></tr>" % ( tsr_idno ) 
			maintext += "<tr><td class=right>Alloc IDNo:</td><td class=center>%s</td></tr>" % ( tsr_allocidno ) 
			
			maintext += '</table>'

			
			maintext += '</center></td></table>'
			
			# end of TSR table
			if False :
			
				maintext += '<table cellpadding=3 cellspacing=3><td valign=top>'
			
				maintext += '<table cellpadding=3 cellspacing=3>'
				maintext += "<tr><td class=right>1 IDNo</td><td>%s</td></tr>" % ( tsr_idno ) 
				maintext += "<tr><td class=right>2 PropIDNo</td><td>%s</td></tr>" % ( tsr_propidno ) 
			
				maintext += "<tr><td class=right>3 Alloc IDNO:</td><td>%s</td></tr>" % ( tsr_allocidno ) 		
				maintext += "<tr><td class=right>Date:</td><td>%s</td></tr>" % ( tsr_date ) 
				maintext += "<tr><td class=right>Instr:</td><td>%s</td></tr>" % ( tsr_instr ) 
				maintext += "<tr><td class=right>SA:</td><td>%s</td></tr>" % ( tsr_ss ) 
				maintext += "<tr><td class=right>PI Last:</td><td>%s</td></tr>" % ( tsr_last ) 
				maintext += "<tr><td class=right>PI First:</td><td>%s</td></tr>" % ( tsr_first )
				maintext += "<tr><td class=right>Comment</td><td>%s</td></tr>" % ( tsr_allocidno )
				maintext += "<tr><td class=right>10 PropID</td><td>%s</td></tr>" % ( tsr_propid )
				maintext += "<tr><td class=right>Focus</td><td>%s</td></tr>" % ( tsr_focus )
				maintext += "<tr><td class=right>12 Arrive</td><td>%s</td></tr>" % ( tsr_arrive )

	#			ag, sv, adc, imr, cal, flats, polar, ao, irm2, pmdusk, \

				maintext += "<tr><td class=right>AG:</td><td>%s</td></tr>" % ( tsr_ag ) 		
				maintext += "<tr><td class=right>SV:</td><td>%s</td></tr>" % ( tsr_sv ) 
				maintext += "<tr><td class=right>ADC:</td><td>%s</td></tr>" % ( tsr_adc ) 
				maintext += "<tr><td class=right>ImR:</td><td>%s</td></tr>" % ( tsr_imr ) 
				maintext += "<tr><td class=right>Cal:</td><td>%s</td></tr>" % ( tsr_cal ) 
				maintext += "<tr><td class=right>Flats:</td><td>%s</td></tr>" % ( tsr_flats )
				maintext += "<tr><td class=right>Polar:</td><td>%s</td></tr>" % ( tsr_polar )
				maintext += "<tr><td class=right>AO:</td><td>%s</td></tr>" % ( tsr_ao )
				maintext += "<tr><td class=right>IRM2:</td><td>%s</td></tr>" % ( tsr_irm2 )
				maintext += "<tr><td class=right>22 PM Dusk:</td><td>%s</td></tr>" % ( tsr_pmdusk )

	#	pmdome, amdawn, amdome, flatrun, calrun, comments, calcomm, imrcomm, day, gid, \

				maintext += "<tr><td class=right>PM Dome:</td><td>%s</td></tr>" % ( tsr_pmdome ) 		
				maintext += "<tr><td class=right>AM Dawn:</td><td>%s</td></tr>" % ( tsr_amdawn ) 
				maintext += "<tr><td class=right>AM Dome:</td><td>%s</td></tr>" % ( tsr_amdome ) 
				maintext += "<tr><td class=right>Flat Run:</td><td>%s</td></tr>" % ( tsr_flatrun ) 
				maintext += "<tr><td class=right>Cal Run:</td><td>%s</td></tr>" % ( tsr_calrun ) 
				maintext += "<tr><td class=right>Comments:</td><td>%s</td></tr>" % ( tsr_comments )
				maintext += "<tr><td class=right>29 Cal Comments:</td><td>%s</td></tr>" % ( tsr_calcomm )

				maintext += "</table>"
				maintext += "</td><td valign=top>"
				maintext += "<table>"

				maintext += "<tr><td class=right>ImR Comments:</td><td>%s</td></tr>" % ( tsr_imrcomm )
				maintext += "<tr><td class=right>Day:</td><td>%s</td></tr>" % ( tsr_day )
				maintext += "<tr><td class=right>32 GID:</td><td>%s</td></tr>" % ( tsr_gid )

	#	pmcomm, amcomm, observers, obsarrive, location, sh, chop, m2, m3, adccomm, \
			
				maintext += "<tr><td class=right>PM Comments:</td><td>%s</td></tr>" % ( tsr_pmcomm ) 
				maintext += "<tr><td class=right>AM Comments:</td><td>%s</td></tr>" % ( tsr_amcomm ) 
				maintext += "<tr><td class=right>Observers:</td><td>%s</td></tr>" % ( tsr_observers ) 
				maintext += "<tr><td class=right>Obs Arrive:</td><td>%s</td></tr>" % ( tsr_obsarrive ) 
				maintext += "<tr><td class=right>Operator Location:</td><td>%s</td></tr>" % ( tsr_location ) 
				maintext += "<tr><td class=right>SH:</td><td>%s</td></tr>" % ( tsr_sh )
				maintext += "<tr><td class=right>Chop:</td><td>%s</td></tr>" % ( tsr_chop )
				maintext += "<tr><td class=right>M2:</td><td>%s</td></tr>" % ( tsr_m2 )
				maintext += "<tr><td class=right>M3:</td><td>%s</td></tr>" % ( tsr_m3 )
				maintext += "<tr><td class=right>42 ADC Comments:</td><td>%s</td></tr>" % ( tsr_adccomm )

	#		amfini, instrot, flatcomm, sslist, oplist, remhilo, remmtk, amcal, program, ordering, \

				maintext += "<tr><td class=right>AM Fini:</td><td>%s</td></tr>" % ( tsr_amfini ) 		
				maintext += "<tr><td class=right>Inst Rot:</td><td>%s</td></tr>" % ( tsr_instrot ) 
				maintext += "<tr><td class=right>Flat Comments:</td><td>%s</td></tr>" % ( tsr_flatcomm ) 
				maintext += "<tr><td class=right>SS List:</td><td>%s</td></tr>" % ( tsr_sslist ) 
				maintext += "<tr><td class=right>Operator List:</td><td>%s</td></tr>" % ( tsr_oplist ) 
				maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
				maintext += "<tr><td class=right>Remote Mitaka:</td><td>%s</td></tr>" % ( tsr_remmtk )
				maintext += "<tr><td class=right>AM Cal:</td><td>%s</td></tr>" % ( tsr_amcal )
				maintext += "<tr><td class=right>Program:</td><td>%s</td></tr>" % ( tsr_program )
				maintext += "<tr><td class=right>52 Ordering:</td><td>%s</td></tr>" % ( tsr_ordering )

	# 	wpulgs, ocs, m2offset, others, alloc, confirm, ao2, queue, agcomm \

				maintext += "<tr><td class=right>WPU LGS:</td><td>%s</td></tr>" % ( tsr_wpulgs ) 		
				maintext += "<tr><td class=right>OCS:</td><td>%s</td></tr>" % ( tsr_ocs ) 
				maintext += "<tr><td class=right>M2 Offset:</td><td>%s</td></tr>" % ( tsr_m2offset ) 
				maintext += "<tr><td class=right>Others:</td><td>%s</td></tr>" % ( tsr_others ) 
				maintext += "<tr><td class=right>Alloc:</td><td>%s</td></tr>" % ( tsr_alloc ) 
				maintext += "<tr><td class=right>Confirm:</td><td>%s</td></tr>" % ( tsr_confirm )
				maintext += "<tr><td class=right>AO2:</td><td>%s</td></tr>" % ( tsr_ao2 )
				maintext += "<tr><td class=right>Queue:</td><td>%s</td></tr>" % ( tsr_queue )
				maintext += "<tr><td class=right>61 AG Comments:</td><td>%s</td></tr>" % ( tsr_agcomm )
	#			maintext += "<tr><td class=right>Ordering:</td><td>%s</td></tr>" % ( tsr_ordering )

				maintext += "</table>"
		
				maintext += "</td></table>"
			

		else:


#			status1 = ( 'Active', 'Removed', 'Garage' )
#			statusCtrl = '<select size=1 name=status>'
#			for status2 in status1 :
#				if car_status == status2 :
#					statusCtrl += '<option value=%s selected>%s' % ( status2, status2 )
#				else:
#					statusCtrl += '<option value=%s>%s' % ( status2, status2 )           
#			statusCtrl += '</select>'

			maintext += "<form method=post action='tsrone.py?idno=%s'><input name=action type=submit value='Save'> \
			<input name=action type=submit value='Cancel'>" % ( tsr_idno )
			
			#column table - 1st col
			maintext += '<table cellpadding=3 cellspacing=3><td valign=top><center>'

			
			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2>'
			maintext += '<tr><th colspan=2 bgcolor=lime>Telescope</th></tr>'
			
			tsr_date_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'date', 20, tsr_date )
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Date', tsr_date_f ) 


			cursor3.execute("select name, code from instr where status='Active' order by name")

			tsr_instr_spin = "<select name='%s' size=%s>" % ( 'instr', 1 )
			for row in cursor3.fetchall() :
				instr_name = row[0]
				instr_code = row[1]
				if tsr_instr == instr_name :
					tsr_instr_spin += "<option value='%s' selected>%s | %s" % ( instr_name, instr_name, instr_code )
				else :
					tsr_instr_spin += "<option value='%s'>%s | %s" % ( instr_name, instr_name, instr_code )
			tsr_instr_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Instr', tsr_instr_spin )

#			tsr_instr_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'instr', 20, tsr_instr )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Instr', tsr_instr_f )


			cursor3.execute("select file, text from refer where file='FOCUS' order by text")

			tsr_focus_spin = "<select name='%s' size=%s>" % ( 'focus', 1 )
			for row in cursor3.fetchall() :
				refer_file = row[0]
				refer_text = row[1]
				if tsr_focus == refer_text :
					tsr_focus_spin += "<option value='%s' selected>%s" % ( refer_text, refer_text)
				else :
					tsr_focus_spin += "<option value='%s'>%s" % ( refer_text, refer_text )
			tsr_focus_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Focus', tsr_focus_spin )

#			tsr_focus_f = "<input type=text name=%s size=%s value='%s'>" % ( 'focus', 20, tsr_focus )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Focus', tsr_focus_f )
			 
#			maintext += "<tr><td class=right>Focus:</td><td>%s</td></tr>" % ( tsr_focus )

#			tsr_focus_f = "<input type=text name=%s size=%s value='%s'>" % ( 'focus', 20, tsr_focus )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Focus', tsr_focus_f )

			cursor3.execute("select file, text from refer where file='M2' order by text")

			tsr_m2_spin = "<select name='%s' size=%s>" % ( 'm2', 1 )
			for row in cursor3.fetchall() :
				refer_file = row[0]
				refer_text = row[1]
				if tsr_m2 == refer_text :
					tsr_m2_spin += "<option value='%s' selected>%s" % ( refer_text, refer_text)
				else :
					tsr_m2_spin += "<option value='%s'>%s" % ( refer_text, refer_text )
			tsr_m2_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'M2', tsr_m2_spin )


#			tsr_m2_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'm2', 20, tsr_m2 )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'M2', tsr_m2_f )

#			maintext += "<tr><td class=right>M2:</td><td>%s</td></tr>" % ( tsr_m2 )
			cursor3.execute("select file, text from refer where file='M2OFFSET' order by text")
			tsr_m2offset_spin = "<select name='%s' size=%s>" % ( 'm2offset', 1 )
			for row in cursor3.fetchall() :
				refer_file = row[0]
				refer_text = row[1]
				if tsr_m2offset == refer_text :
					tsr_m2offset_spin += "<option value='%s' selected>%s" % ( refer_text, refer_text)
				else :
					tsr_m2offset_spin += "<option value='%s'>%s" % ( refer_text, refer_text )
			tsr_m2offset_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'M2-Offset', tsr_m2offset_spin )

#			tsr_m2offset_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'm2offset', 20, tsr_m2offset )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'M2-Offset', tsr_m2offset_f )

#			maintext += "<tr><td class=right>M2 Offset:</td><td>%s</td></tr>" % ( tsr_m2offset )
			
			cursor3.execute("select file, text from refer where file='M3' order by text")

			tsr_m3_spin = "<select name='%s' size=%s>" % ( 'm3', 1 )
			for row in cursor3.fetchall() :
				refer_file = row[0]
				refer_text = row[1]
				if tsr_m3 == refer_text :
					tsr_m3_spin += "<option value='%s' selected>%s" % ( refer_text, refer_text)
				else :
					tsr_m3_spin += "<option value='%s'>%s" % ( refer_text, refer_text )
			tsr_m3_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'M3', tsr_m3_spin )

#			tsr_m3_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'm3', 20, tsr_m3 )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'M3', tsr_m3_f )

#			maintext += "<tr><td class=right>M3:</td><td>%s</td></tr>" % ( tsr_m3 )
			tsr_location_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'location', 20, tsr_location )
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Location', tsr_location_f )

#			maintext += "<tr><td class=right>Operator Location:</td><td>%s</td></tr>" % ( tsr_location ) 
#			tsr_remhilo_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'remhilo', 20, tsr_remhilo )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Remote-Hilo', tsr_remhilo_f )

			remOptions = ( 'None', 'Control', 'View' ) 
			tsr_remhilo_spin = "<select name='%s' size=%s>" % ( 'remhilo', 1 )
			for remOption in remOptions :		
				if tsr_remhilo == remOption :
					tsr_remhilo_spin += "<option value='%s' selected>%s" % ( remOption, remOption )
				else :
					tsr_remhilo_spin += "<option value='%s'>%s" % ( remOption, remOption )
			tsr_remhilo_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Remote-Hilo', tsr_remhilo_spin )


#			maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
#			tsr_remmtk_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'remmtk', 20, tsr_remmtk )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Remote MTK', tsr_remmtk_f )

			remOptions = ( 'None', 'Control', 'View' ) 
			tsr_remmtk_spin = "<select name='%s' size=%s>" % ( 'remmtk', 1 )
			for remOption in remOptions :		
				if tsr_remmtk == remOption :
					tsr_remmtk_spin += "<option value='%s' selected>%s" % ( remOption, remOption )
				else :
					tsr_remmtk_spin += "<option value='%s'>%s" % ( remOption, remOption )
			tsr_remmtk_spin += "</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Remote-Mitaka', tsr_remmtk_spin )

#			maintext += "<tr><td class=right>Remote Mitaka:</td><td>%s</td></tr>" % ( tsr_remmtk )
#			maintext += "<tr><td class=right>Status</td><td>%s</td></tr>" % ( statusCtrl ) 
#			maintext += "<tr><td class=right>Wheels</td><td>%s</td></tr>" % ( wheelsCtrl ) 

#			tsr_comments_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'comments', 20, tsr_comments )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Comments', tsr_comments_f )

			maintext += '</table><br>'

			maintext += '<table rules=all border=1><tr><th colspan=3 bgcolor=lime>Options</th></tr>'

#			maintext += "<tr><td class=right>Comment</td><td><input type=text name=comment size=100 value='%s'></td></tr>" % ( prop_comment ) 
			tsr_ag_spin = "<select name='%s' size=%s>" % ( 'ag', 1 )
			if tsr_ag == 'Yes' :
				tsr_ag_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_ag_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
#			maintext += tsr_ag_spin
			tsr_agcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'agcomm', 60, tsr_agcomm )
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'AG', tsr_ag_spin, tsr_agcomm_f )

#			tsr_ag_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'ag', 20, tsr_ag )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'AG', tsr_ag_f, tsr_agcomm_f )

#			maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
			tsr_sh_spin = "<select name='%s' size=%s>" % ( 'sh', 1 )
			if tsr_sh == 'Yes' :
				tsr_sh_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_sh_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
#			maintext += tsr_sh_spin
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'SH', tsr_sh_spin )

#			tsr_sh_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'sh', 20, tsr_sh )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'SH', tsr_sh_f )

			tsr_sv_spin = "<select name='%s' size=%s>" % ( 'sv', 1 )
			if tsr_sv == 'Yes' :
				tsr_sv_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_sv_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
#			maintext += tsr_sv_spin
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'SV', tsr_sv_spin )

#			tsr_sv_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'sv', 20, tsr_sv )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'SV', tsr_sv_f )

			tsr_cal_spin = "<select name='%s' size=%s>" % ( 'cal', 1 )
			if tsr_cal == 'Yes' :
				tsr_cal_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_cal_spin += "<option value=Yes>Yes<option value=No selected>No</select>"				
			tsr_calcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'calcomm', 60, tsr_calcomm )
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'CAL', tsr_cal_spin, tsr_calcomm_f )


			tsr_adc_spin = "<select name='%s' size=%s>" % ( 'adc', 1 )
			if tsr_adc == 'In' :
				tsr_adc_spin += "<option value=In selected>In<option value=Out>Out</select>"
			else :
				tsr_adc_spin += "<option value=In>In<option value=Out selected>Out</select>"
			tsr_adccomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'adccomm', 60, tsr_adccomm )
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'ADC', tsr_adc_spin, tsr_adccomm_f )

			tsr_instrot_spin = "<select name='%s' size=%s>" % ( 'instrot', 1 )
			
			if tsr_instrot == 'Yes' :
				tsr_instrot_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_instrot_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'InstRot', tsr_instrot_spin, '' )

			tsr_imr_spin = "<select name='%s' size=%s>" % ( 'imr', 1 )
			if tsr_imr == 'Yes' :
				tsr_imr_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_imr_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			tsr_imrcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'imrcomm', 60, tsr_imrcomm )
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'ImR', tsr_imr_spin, tsr_imrcomm_f )

			tsr_flats_spin = "<select name='%s' size=%s>" % ( 'flats', 1 )
			if tsr_flats == 'Yes' :
				tsr_flats_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_flats_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			tsr_flatcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'flatcomm', 60, tsr_flatcomm )
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'Flats', tsr_flats_spin, tsr_flatcomm_f )

			tsr_polar_spin = "<select name='%s' size=%s>" % ( 'polar', 1 )
			if tsr_polar == 'In' :
				tsr_polar_spin += "<option value=In selected>In<option value=Out>Out</select>"
			else :
				tsr_polar_spin += "<option value=In>In<option value=Out selected>Out</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'Wave Plate', tsr_polar_spin, '' )

			aoOptions = ( 'AO188', 'SCExAO', 'RAVEN', 'No' ) 
			
			tsr_ao_spin = "<select name='%s' size=%s>" % ( 'ao', 1 )
			for aoOption in aoOptions :		
				if tsr_ao == aoOption :
					tsr_ao_spin += "<option value='%s' selected>%s" % ( aoOption, aoOption )
				else :
					tsr_ao_spin += "<option value='%s'>%s" % ( aoOption, aoOption )
			tsr_ao_spin += "</select>"
					
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'AO-1', tsr_ao_spin, '' )

			aoOptions = ( 'No', 'SCExAO' ) 
			tsr_ao2_spin = "<select name='%s' size=%s>" % ( 'ao2', 1 )
			for aoOption in aoOptions :		
				if tsr_ao2 == aoOption :
					tsr_ao2_spin += "<option value='%s' selected>%s" % ( aoOption, aoOption )
				else :
					tsr_ao2_spin += "<option value='%s'>%s" % ( aoOption, aoOption )
			tsr_ao2_spin += "</select>"
					
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'AO-2', tsr_ao2_spin, '' )


			tsr_wpulgs_spin = "<select name='%s' size=%s>" % ( 'wpulgs', 1 )
			if tsr_wpulgs == 'Yes' :
				tsr_wpulgs_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_wpulgs_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'LGS', tsr_wpulgs_spin, '' )

			tsr_chop_spin = "<select name='%s' size=%s>" % ( 'chop', 1 )
			if tsr_chop == 'Yes' :
				tsr_chop_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_chop_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'Chopping', tsr_chop_spin, '' )

			tsr_queue_spin = "<select name='%s' size=%s>" % ( 'queue', 1 )
			if tsr_queue == 'Yes' :
				tsr_queue_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_queue_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'Queue', tsr_queue_spin, '' )

			maintext += '</table>'

#			tsr_calcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'calcomm', 20, tsr_calcomm )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'CAL', tsr_cal_f, tsr_calcomm_f )

#			maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
#			tsr_adc_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'adc', 20, tsr_adc )
#			tsr_adccomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'adccomm', 20, tsr_adccomm )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'ADC', tsr_adc_f, tsr_adccomm_f  )

#			tsr_instrot_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'instrot', 20, tsr_instrot )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'InstRot', tsr_instrot_f )

#			tsr_imr_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'imr', 20, tsr_imr )
#			tsr_imrcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'imrcomm', 20, tsr_imrcomm )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'ImR', tsr_imr_f, tsr_imrcomm_f )
			
#			tsr_flats_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'flats', 20, tsr_flats )
#			tsr_flatcomm_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'flatcomm', 20, tsr_flatcomm )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td>%s</td></tr>" % ( 'FLAT', tsr_flats_f, tsr_flatcomm_f )

#			maintext += "<tr><td class=right>Remote Hilo:</td><td>%s</td></tr>" % ( tsr_remhilo )
#			tsr_polar_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'polar', 20, tsr_polar )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'Wave Plate', tsr_polar_f )

#			tsr_ao_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'ao', 20, tsr_ao )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'AO-1', tsr_ao_f )

#			tsr_ao2_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'ao2', 20, tsr_ao2 )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'AO-2', tsr_ao2_f )

#			tsr_wpulgs_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'wpulgs', 20, tsr_wpulgs )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'LGS', tsr_wpulgs_f )

#			tsr_chop_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'chop', 20, tsr_chop )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'Chopping', tsr_chop_f )

#			tsr_queue_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'queue', 20, tsr_queue )
#			maintext += "<tr><td class=right>%s:</td><td>%s</td><td></td></tr>" % ( 'Queue', tsr_queue_f )

#			maintext += "</table>"

# column table - 2nd col
			
			maintext += '</center></td><td valign=top><center>'

			
			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2 bgcolor=lime>Program (14)</th></tr>'
			
			tsr_propid_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'propid', 20, tsr_propid )
			maintext += "<tr><td class=right>Proposal ID:</td><td>%s</td></tr>" % ( tsr_propid_f ) 
			
			tsr_gid_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'gid', 20, tsr_gid )
			maintext += "<tr><td class=right>Group ID:</td><td>%s</td></tr>" % ( tsr_gid_f ) 

			cursor3.execute("select file, text from refer where file='OBS' order by text")

			tsr_alloc_spin = "<select name='%s' size=%s>" % ( 'alloc', 1 )
			for row in cursor3.fetchall() :
				refer_file = row[0]
				refer_text = row[1]
				if tsr_alloc == refer_text :
					tsr_alloc_spin += "<option value='%s' selected>%s" % ( refer_text, refer_text)
				else :
					tsr_alloc_spin += "<option value='%s'>%s" % ( refer_text, refer_text )
			tsr_alloc_spin += "</select>"

			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Alloc', tsr_alloc_spin )
			
#			tsr_alloc_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'alloc', 20, tsr_alloc )
#			maintext += "<tr><td class=right>Alloc:</td><td>%s</td></tr>" % ( tsr_alloc_f )
			
			tsr_last_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'last', 20, tsr_last )
			maintext += "<tr><td class=right>PI Last:</td><td>%s</td></tr>" % ( tsr_last_f )
			
			tsr_ss_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'ss', 20, tsr_ss )
			maintext += "<tr><td class=right>SS:</td><td>%s</td></tr>" % ( tsr_ss_f ) 
			
			tsr_sslist_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'sslist', 40, tsr_sslist )
			maintext += "<tr><td class=right>SS List:</td><td>%s</td></tr>" % ( tsr_sslist_f )

			tsr_oplist_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'oplist', 40, tsr_oplist )
			maintext += "<tr><td class=right>Operator List:</td><td>%s</td></tr>" % ( tsr_oplist_f ) 

			tsr_arrive_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'arrive', 40, tsr_arrive )
			maintext += "<tr><td class=right>Ops Arrive:</td><td>%s</td></tr>" % ( tsr_arrive_f )
			
			tsr_observers_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'observers', 40, tsr_observers )
			maintext += "<tr><td class=right>Observers:</td><td>%s</td></tr>" % ( tsr_observers_f )

			tsr_obsarrive_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'obsarrive', 40, tsr_obsarrive )
			maintext += "<tr><td class=right>Observers Arrive:</td><td>%s</td></tr>" % ( tsr_obsarrive_f )
			
			tsr_others_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'others', 60, tsr_others )
			maintext += "<tr><td class=right>Others:</td><td>%s</td></tr>" % ( tsr_others_f )

			tsr_comments_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'comments', 60, tsr_comments )
			maintext += "<tr><td class=right>Comments:</td><td>%s</td></tr>" % ( tsr_comments_f )
			
			tsr_program_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'program', 60, tsr_program )
			maintext += "<tr><td class=right>Program:</td><td>%s</td></tr>" % ( tsr_program_f ) 
			
#			maintext += "<tr><td class=right>Ordering:</td><td>%s</td></tr>" % ( tsr_ordering )
#			maintext += "<tr><td class=right>Confirm:</td><td>%s</td></tr>" % ( tsr_confirm )

			maintext += '</table><br>'

			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2 bgcolor=lime>PM Calibration</th></tr>'

#			tsr_pmdusk_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'pmdusk', 20, tsr_pmdusk )
#			maintext += "<tr><td class=right>Twilight Flats:</td><td>%s</td></tr>" % ( tsr_pmdusk_f )
			
			tsr_pmdusk_spin = "<select name='%s' size=%s>" % ( 'pmdusk', 1 )
			if tsr_pmdusk == 'Yes' :
				tsr_pmdusk_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_pmdusk_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Twilight Flats', tsr_pmdusk_spin )
			

#			tsr_pmdome_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'pmdome', 20, tsr_pmdome )
#			maintext += "<tr><td class=right>Dome Flats:</td><td>%s</td></tr>" % ( tsr_pmdome_f )

			tsr_pmdome_spin = "<select name='%s' size=%s>" % ( 'pmdome', 1 )
			if tsr_pmdome == 'Yes' :
				tsr_pmdome_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_pmdome_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Dome Flats', tsr_pmdome_spin )

#			tsr_pmcal_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'pmcal', 20, tsr_pmcal )
#			maintext += "<tr><td class=right>CAL:</td><td>%s</td></tr>" % ( tsr_pmcal_f ) 

			tsr_pmcal_spin = "<select name='%s' size=%s>" % ( 'pmcal', 1 )
			if tsr_pmcal == 'Yes' :
				tsr_pmcal_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_pmcal_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'CAL', tsr_pmcal_spin )

			tsr_pmcomm_f = "<input type=text name='%s' size=%s maxsize=100 value='%s'>" % ( 'pmcomm', 60, tsr_pmcomm )
			maintext += "<tr><td class=right>Comments:</td><td>%s</td></tr>" % ( tsr_pmcomm_f ) 
			
			maintext += '</table><br>'
			
			maintext += '<table cellpadding=3 cellspacing=3 rules=all border=2><th colspan=2 bgcolor=lime>AM Calibration</th></tr>'

#			tsr_amdawn_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'amdawn', 20, tsr_amdawn )
#			maintext += "<tr><td class=right>Twilight Flats:</td><td>%s</td></tr>" % ( tsr_amdawn_f )

			tsr_amdawn_spin = "<select name='%s' size=%s>" % ( 'amdawn', 1 )
			if tsr_amdawn == 'Yes' :
				tsr_amdawn_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_amdawn_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Twilight Flats', tsr_amdawn_spin )


#			tsr_amdome_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'amdome', 20, tsr_amdome )
#			maintext += "<tr><td class=right>Dome Flats:</td><td>%s</td></tr>" % ( tsr_amdome_f )

			tsr_amdome_spin = "<select name='%s' size=%s>" % ( 'amdome', 1 )
			if tsr_amdome == 'Yes' :
				tsr_amdome_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_amdome_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Dome Flats', tsr_amdome_spin )

#			tsr_amcal_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'amcal', 20, tsr_amcal )
#			maintext += "<tr><td class=right>CAL:</td><td>%s</td></tr>" % ( tsr_amcal_f ) 

			tsr_amcal_spin = "<select name='%s' size=%s>" % ( 'amcal', 1 )
			if tsr_amcal == 'Yes' :
				tsr_amcal_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_amcal_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'CAL', tsr_amcal_spin )


#			tsr_flatrun_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'flatrun', 20, tsr_flatrun )
#			maintext += "<tr><td class=right>Darks Running:</td><td>%s</td></tr>" % ( tsr_flatrun_f ) 

			tsr_flatrun_spin = "<select name='%s' size=%s>" % ( 'flatrun', 1 )
			if tsr_flatrun == 'Yes' :
				tsr_flatrun_spin += "<option value=Yes selected>Yes<option value=No>No</select>"
			else :
				tsr_flatrun_spin += "<option value=Yes>Yes<option value=No selected>No</select>"
			maintext += "<tr><td class=right>%s:</td><td>%s</td></tr>" % ( 'Darks Running', tsr_flatrun_spin )


			tsr_amfini_f = "<input type=text name='%s' size=%s value='%s'>" % ( 'amfini', 30, tsr_amfini )
			maintext += "<tr><td class=right>Finish Time:</td><td>%s</td></tr>" % ( tsr_amfini_f ) 

			tsr_amcomm_f = "<input type=text name='%s' size=%s maxsize=100 value='%s'>" % ( 'amcomm', 60, tsr_amcomm )
			maintext += "<tr><td class=right>Comments:</td><td>%s</td></tr>" % ( tsr_amcomm_f ) 
			
			maintext += '</table>'

# col table end 2nd col
		
			maintext += '</center></td></table>'
			
			maintext += "</form>"

	else :
		
		maintext += "No Records!"
				
#	maintext += "</table>"
else :
	maintext = logproc.returnLogin()

#maintext='tom'
printHTML( maintext )
