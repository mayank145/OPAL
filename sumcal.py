#! /usr/local/python

import datetime
import cgi
import os
import cgitb; cgitb.enable();
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
#import logproc
import logproc3 as logproc
import dbconnect
import calendar
#from dateutil.relativedelta import relativedelta

field=cgi.FieldStorage()

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

#maxday = now + datetime.timedelta( days = 15 )


if 'year' in field:

	year=field[ 'year' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	year=today[0:4]


if 'month' in field:

	month=field[ 'month' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	month=today[5:7]

if 'type' in field:

	type=field[ 'type' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	type = 'All'


if 'logcrew' in field:

	logcrew=field[ 'logcrew' ].value
	
else:
#	today=datetime.datetime.today()
#	todaydate=str(today.date())
	
	logcrew = 'WP'


method=os.environ.get("REQUEST_METHOD","")


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
	
#/* Style the tab */
	css_text += ".tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1;}"

#/* Style the buttons that are used to open the tab content */
	css_text += ".tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s;}"

#/* Change background color of buttons on hover */
	css_text += ".tab button:hover { background-color: #ddd; }"

#/* Create an active/current tablink class */
	css_text += ".tab button.active { background-color: #ccc; }"

#/* Style the tab content */
	css_text += ".tabcontent { display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }"	
	
	css_text += "</style>"

	toppg = ''
	toppg += "Content-type: text/html;\n\n"
	toppg += "<!DOCTYPE html>"
	toppg += "<HTML><HEAD>"
	toppg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	toppg += css_text
	
	bottompg = "</HEAD><BODY>"
	bottompg += maintext
	bottompg += "</BODY></HTML>"
	
	print( toppg )
	
	print( bottompg )


dbconn=dbconnect.dbconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])

cursor=db.cursor()
cursor2=db.cursor()
cursor3=db.cursor()
cursor4=db.cursor()


dbconn2=dbconnect.opalconn()
db2 = MySQLdb.connect( host=dbconn2[0], user=dbconn2[1], passwd=dbconn2[2], db=dbconn2[3] )

cursorOPAL = db2.cursor()
cursorOPAL2 = db2.cursor()
cursorOPAL3 = db2.cursor()
#cursor4=db.cursor()

#logcrew = 'WP'

if method == "POST" : 

	logcrew = field['action'].value

if logproc.validCookie() :
#if True :


	username, end, term, logcrew2 = logproc.getUsername()

	day = '1'

	nyear = int( year )

	nmonth = int( month )	

	nday = int( day )

	daystext =  "Year: " + year
	daystext += "Month: " + month
	daystext += "Day: " + day 
	#	 	get the date offset correct

	#	print out the days of the week
#	months = [ 'Zero', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
	months = [ 'Zero', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec' ]

	weekdays = [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri',  'Sat' ]

	instr2 = { 'COMICS':'COM', 'FOCAS':'FCS', 'IRCS':'IRC', 'IRCS+AO':'IRC', 'CHARIS':'CRS', 'HSC':'HSC', 'MOIRCS':'MCS', 'HDS':'HDS', 'IRD':'IRD', \
	'SUKA':'SUK', 'PFS':'PFS', 'SWIMS':'SWS', 'MIMIZUKU':'MMZ', 'VAMPIRES':'VMP', 'SCEXAO':'SCX', '-None':'NON' }


	#		print("<table rules=all border=1 cellpadding=3 cellspacing=3>")



	#lmonth2 = nmonth
	#lyear2 = nyear
	#nmonth2 = nmonth
	#nyear2 = nyear

	#if lmonth < 10 :

	#	if lmonth == 0:

	#		lmonth2 = 12
	#		lyear2= year - 1

	#	lastmonth = '0' + str( lmonth )
	#else:		
	#	lastmonth = str( lmonth )	

	#nmonth = nmonth + 1

	#if nmonth < 10 :

	#	nextmonth = '0' + str( lmonth )

	#else:

	#	if nmonth == 13:

	#		nmonth = 1
	#		nyear2= year + 1
	#	
	#	nextmonth = str( nmonth )

	#lmonth_link = "<a href= ./sumcal.py?year=%s&month=%s>%s-%s</a>" % ( str( lyear2 ), lastmonth, str( lyear2 ), lastmonth )	
	#nmonth_link = "<a href= ./sumcal.py?year=%s&month=%s>%s-%s</a>" % ( str( nyear2 ), nextmonth, str( nyear2 ), nextmonth )

	types = ( 'All', 'Comment', 'Trouble', 'Summary', 'Warning', 'Important' )

	logtypes1 = "<select name=type size=1>"

	for typ in types:

		if typ == type :

			logtypes1 += "<option value='%s' selected>%s" % ( typ, typ )
		else:
			logtypes1 += "<option value='%s'>%s" % ( typ, typ )


	logtypes1 += "</select>"


	maintext = "<center><b>Subaru SummitLog Calendar</b> | " + username + " [" + end + "] " + "<br><br>" + logproc.getMenu() + '<br>' + 'logcrew: ' + logcrew + '<br>'
	#maintext += "<form method=post action='./sumcal.py?date=%s'>%s | " % ( today, logtypes1 )
	maintext += "<form method=post action='./sumcal.py?date=%s'>" % ( today )

	if logcrew == 'DC' :

		maintext += "<input type=submit name=action value='DC' style='background-color:lime'> "
	else:
		maintext += "<input type=submit name=action value='DC''> "

	if logcrew == 'WP' :

		maintext += "<input type=submit name=action value='WP' style='background-color:lime'> "
	else:
		maintext += "<input type=submit name=action value='WP'> "

	if logcrew == 'TO' :

		maintext += "<input type=submit name=action value='TO' style='background-color:lime'> "
	else:
		maintext += "<input type=submit name=action value='TO'> "

	#if logcrew == 'MyPlans' :

	#	maintext += "<input type=submit name=action value='MyPlans'  style='background-color:lime'> "
	#else:
	#	maintext += "<input type=submit name=action value='MyPlans''> "

	#maintext += "<input type=submit name=action value='OPAL'> "
	maintext += "</form><br>"
	#maintext = "<input type=radio name=logcrew value='TO'> TO | <input name=logcrew type=radio value='DC'> DC | <input name=logcrew type=radio value='WP'> WP |"

	kmonth = nmonth - 2

	kyear = nyear

	if kmonth == 0 :

		kyear = str( int( kyear ) - 1 )
		kmonth = 12
		
	if kmonth == -1 :

		kyear = str( int( kyear ) - 1 )
		kmonth = 11

	if kmonth < 10 :
	#
		kmonthFull = '0' + str( kmonth )
	#
	else:
	#
		kmonthFull = str( kmonth )

	kmonthText = months[ kmonth ] + '-' + str( kyear )

	lmonth = nmonth - 1

	lyear = nyear

	if lmonth == 0 :

		lyear = str( int( year ) - 1 )
		lmonth = 12

	if lmonth < 10 :
	#
		lmonthFull = '0' + str( lmonth )
	#
	else:
	#
		lmonthFull = str( lmonth )

	lmonthText = months[ lmonth ] + '-' + str( lyear )

	omonth = nmonth + 1

	oyear = nyear

	if omonth == 13 :

		oyear = int( oyear ) + 1
		omonth = 1

	omonthText = months[ omonth ] + '-'+ str( oyear )

	if omonth < 10 :

		omonthFull = '0' + str( omonth )
	else:
		omonthFull = str( omonth )


	pmonth = nmonth + 2

	pyear = nyear

	if pmonth == 13 :

		pyear = int( pyear ) + 1
		pmonth = 1
	
	if pmonth == 14:

		pyear = str( int( pyear ) + 1 )
		pmonth = 2


	pmonthText = months[ pmonth ] + '-'+ str( pyear )

	if pmonth < 10 :

		pmonthFull = '0' + str( pmonth )

	else:
		pmonthFull = str( pmonth )

	#maintext += "<a href=./sumcal.py?year=" + lyear + "&month=" + lmonthFull + ">"
	#maintext += months[ lmonth ] + "-" + lyear + "</a> | "
	#maintext += months[ nmonth ] + "-" + year + " | "
	#maintext += "<a href=./sumcal.py?year=" + oyear + "&month=" + omonthFull + ">"
	#maintext += months[ omonth ] + " - " + oyear + "</a>"

	maintext += "<a href=./sumcal.py?year=" + str( kyear ) + "&month=" + kmonthFull + "&logcrew=" + logcrew + '>' + kmonthText + '</a> | '

	maintext += "<a href=./sumcal.py?year=" + str( lyear ) + "&month=" + lmonthFull + "&logcrew=" + logcrew + '>' + lmonthText + '</a> | '

	maintext += '<b><FONT SIZE=+1>' + months[ nmonth ] + " - " + year + '</b></FONT> | '

	maintext += "<a href=./sumcal.py?year=" + str( oyear ) + "&month=" + omonthFull + "&logcrew=" + logcrew + '>' + omonthText + '</a> | '

	maintext += "<a href=./sumcal.py?year=" + str( pyear ) + "&month=" + pmonthFull + "&logcrew=" + logcrew + '>' + pmonthText + '</a><br>'

	maintext += "<table cellpadding=3 cellspacing=3 rules=all border=2>"
	maintext += "<tr><td colspan=7 class=center bgcolor=lime><FONT FACE='Arial,Helvetica' SIZE=3>" + months[ nmonth ] + " - " + year + " - [" + logcrew + "]</td></tr>"
	#maintext += "<tr><td colspan=7 align=center bgcolor=lime><FONT FACE='Arial,Helvetica' SIZE=3>"+lmonth_link + " || " + nmonth_link+"</td></tr>"


	startdate = datetime.date( nyear, nmonth, nday )

	dayno = startdate.strftime("%w")

	offset, totaldays = calendar.monthrange( nyear, nmonth )

	#offset = int( dayno )

	#offset += 1

	#maintext += 'offset: ' + str( offset ) + ' totaldays: ' + str( totaldays )

	maintext += "<tr>"

	for dow in weekdays:

		maintext += "<td class=center><FONT FACE='Arial,Helvetica' SIZE=3><b>%s</b></td>" % ( dow )

	maintext += "</tr>"


	#startdate = datetime.date( nyear, nmonth, nday)


	#maintext += "<tr>" 

	i = -1

	#totaldays = totaldays + 15


	if offset <  6 : 

	#	maintext += "</tr>"

		while i < offset:

	#		maintext += "<td>start-offset</td>"
			maintext += "<td>&nbsp;</td>"
			i += 1


	#if offset ==  6 : 

	#	maintext += "</tr>"

	if offset == 6 :

		tempoffset = -1 
	else: 
		tempoffset = offset

	while nday <= totaldays:

		if nmonth < 10:

			montext = '0'+str( nmonth )

		else:

			montext = str( nmonth )

		if nday< 10:

			daytext = '0'+str( nday )

		else:
			daytext = str( nday )



		fulldate =  year + '-' + montext + '-' + daytext

		fulldate2 = datetime.date( nyear, nmonth, nday )

	#	monthText = fulldate2.strftime('%b') + ' ' + fulldate2.strftime( '%m/%d' )
		monthText = fulldate2.strftime( '%m/%d' )

		bgcolor = 'white'

		if today == fulldate :

			bgcolor='lemonchiffon'	

		if logcrew == 'WP' :

#			maintext += "<td valign=top bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>[ %s ]</a> <a href=./planone.py?date=%s&idno=0&hr=08> +WP</a><br><br>" % ( bgcolor, fulldate, logcrew, monthText,  fulldate )
			maintext += "<td valign=top bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>[ %s ]</a>&nbsp;&nbsp;<a href=./planone.py?date=%s&idno=0&hr=08>+Add WP</a><br><br>" % ( bgcolor, fulldate, logcrew, monthText,  fulldate )

		else:

			maintext += "<td valign=top bgcolor=%s><a href=logone.py?date=%s&logcrew=%s>[ %s ]</a><br><br>" % ( bgcolor, fulldate, logcrew, monthText )


	#	if logcrew == 'All' :
	#	
	#		if type == 'All' :
	#	
	#			cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect from items where date='%s'" % ( fulldate ) )
	#		else:
	#			cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect from items where date='%s' and type='%s'" % ( fulldate, type ) )
	#			
	#	else:

	#		if type == 'All' :
	#		
	#			cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect from items where date='%s' and logcrew = '%s'" % ( fulldate, logcrew ) )
	#		
	#		else :

	#			if logcrew == 'MyPlans' :
	#		
	#				cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect from items where date='%s' and logcrew = '%s' and type='%s' \
	#				and user == '%s'" % ( fulldate, 'WP', type, username ) )
	#				
	#			else :

		if logcrew == 'TO' :

			cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect, assigned1, idno from items where date='%s' and ( logcrew = 'IO' or logcrew='TO') order by itemtime" % ( fulldate ) )

		if logcrew == 'WP' :

			cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect, assigned1, idno from items where date='%s' and logcrew = '%s' \
			 and status<>'Cancelled' order by itemtime" % ( fulldate, 'WP' ) )

	#		cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect from items where date='%s' and logcrew = '%s'" % ( fulldate, 'WP' ) )

		if logcrew == 'DC' :

			cursor4.execute("select itemtime, logcrew, substr(itemtitle,1,60), type, downtime, dayeffect, niteeffect, assigned1, idno from items where date='%s' and logcrew = '%s' order by itemtime" % ( fulldate, 'DC' ) )


		numrows4=cursor4.rowcount
		
		cursorOPAL3.execute("select zoomid, zoompw, join_url from days where date = '%s' " % ( fulldate ) )
		numrowsOPAL3 = cursorOPAL3.rowcount

		zoomid = 'none'
		zoompw = 'none'
		zoomjoin = 'none'

		if numrowsOPAL3 == 1 :

			raw = cursorOPAL3.fetchone()

			zoomid = raw[0]
			zoompw = raw[1]
			zoomjoin = raw[2]
			
#		numrows4=0
		
		zoomString = "<hr><FONT SIZE=1><a href=%s?>ZoomNow</a></FONT> <FONT SIZE=2><a href=%s?date=%s>%s / %s</a></FONT>" % ( zoomjoin, './zoomlist.py', fulldate, zoomid, zoompw )
#		zoomString += "<FONT SIZE=1><a href=%s>%s</a></FONT>" % ( zoomjoin, 'JoinURL' )
	#	maintext += 'numrows4: ' + str( numrows4 )<br>

		daywarning = ''

		nitewarning = ''

		itemstext = ''

		if numrows4 > 0 and not logcrew == 'OPAL':
		
			itemstext += '<table>'
			

			for result4 in cursor4.fetchall() :

				item_time = str( result4[0] )
				item_time = item_time[11:16]
				item_logcrew = result4[1]
				item_title = result4[2]
				item_type = result4[3][0:1]
				item_downtime = result4[4]
				item_dayeffect = result4[5]
				item_niteeffect = result4[6]
				item_dayeffect = item_dayeffect.strip()
				item_niteeffect = item_niteeffect.strip()
				item_assigned1 = result4[7]
				item_idno = str( result4[8] )

				if len( item_dayeffect ) > 0 :

					daywarning += item_dayeffect + '<br>'

				if len( item_niteeffect ) > 0 :

					nitewarning += item_niteeffect + '<br>'

				if logcrew == 'TO'  or logcrew=='DC' :

	#				itemstext += '<a href=planone.py?idno=%s><b>'+item_time + '</b></a>&nbsp;' +item_title + ' -' + item_downtime +' (' + item_type +')<br>' % ( item_idno )
					itemstext += '<tr><td valign=top><a href=itemone.py?idno=' + item_idno + '>'+item_time + '</a></td><td>' +item_title + ' -' + item_downtime +' (' + item_type +')</td><tr>' 
#					itemstext += '<a href=itemone.py?idno=' + item_idno + '>'+item_time + '</a>&nbsp;' +item_title + ' -' + item_downtime +' (' + item_type +')<br>' 

				else :

#					itemstext += '<a href=planone.py?idno='+item_idno +'>'+item_time + '</a>&nbsp;' +item_title + ' (' + item_assigned1 +')<br>'
					itemstext += '<tr><td valign=top><a href=planone.py?idno='+item_idno +'>'+item_time + '</a></td><td>' +item_title + ' (' + item_assigned1 +')</td><tr>'
			
			itemstext += '</table><hr>'
			

		else:

			if not logcrew == 'OPAL' :

				itemstext += "<center>%s ( 0 )</center>" % ( logcrew )

		if len( nitewarning ) > 0 or len( nitewarning ) > 0 :

			if len( daywarning ) > 0 :

				maintext += '&nbsp;<b>warnD: ' + daywarning + '</b>&nbsp;<br>' + itemstext

			if len( nitewarning ) > 0 :

				maintext += itemstext + '<br>&nbsp;<b>warnN' + nitewarning + '</b>&nbsp;'
		else: 
			maintext += itemstext	

		cursorOPAL.execute("select propid, instr, last, observers, remote, staff, idno, order1, comment from alloc where datein = '%s' and cal = 'Y' order by order1" % ( fulldate ) )
		numrowsOPAL = cursorOPAL.rowcount

#		numrowsOPAL = 0

		maintext += "<table><tr><th colspan=3>[ Obs Programs ]</th></tr>"			

		if numrowsOPAL > 0 :

	#		opal_text = ''

			for resultOPAL in cursorOPAL.fetchall() :

				observers = str( resultOPAL[3] )
				remote = str( resultOPAL[4] )
				staff = str( resultOPAL[5] )
				allocidno = str( resultOPAL[6] )
				alloc_order = resultOPAL[7]
				alloc_order = alloc_order.strip()
				alloc_comment = resultOPAL[8]

				ordertable ='<table border=1 rules=all><tr>'

				if '1' in alloc_order:

					ordertable += '<td bgcolor=pink>1</td>'
				else:
					ordertable += '<td>&nbsp;</td>'

				if '2' in alloc_order:

					ordertable += '<td bgcolor=pink>2</td>'
				else:
					ordertable += '<td>&nbsp;</td>'

				if '3' in alloc_order:

					ordertable += '<td bgcolor=pink>3</td>'
				else:
					ordertable += '<td>&nbsp;</td>'

				if '4' in alloc_order:

					ordertable += '<td bgcolor=pink>4</td>'
				else:
					ordertable += '<td>&nbsp;</td>'

				ordertable += '</tr></table>'

				instrOPAL = instr2 [ resultOPAL[1] ]
#				instrOPAL = 'test'

#				maintext += '<tr><td><FONT SIZE=2><a href=allocone.py?idno=' + allocidno + '&date=' + fulldate + '>' + resultOPAL[0][0:10] + \
#				'</a></td><td>' +  instrOPAL + ' ' + alloc_comment + ' (' +  resultOPAL[2]+ ')</td><td>' + ordertable 
				maintext += "<tr><td><FONT SIZE=2><a href=allocone.py?idno=%s&date=%s>%s</a></td><td>%s %s (%s) %s" \
				% ( allocidno, fulldate, resultOPAL[0][0:10], instrOPAL, alloc_comment, resultOPAL[2], ordertable )

				cursorOPAL2.execute("select idno from tsr where allocidno = '%s'" % ( allocidno ) )
				numrowsOPAL2 = cursorOPAL2.rowcount

		#		numrowsOPAL = 0
				if numrowsOPAL2 > 0 :

					ruws = cursorOPAL2.fetchone()
					tsridno = ruws[0]
					maintext += '<a href=tsrone.py?idno=%s>(TSR)</a>' % ( tsridno )

				else :

					maintext += 'NoTSR'
					

				maintext += '</td></tr>'
				
				staffstring = ''

				if len( observers ) > 0 or len( remote ) > 0 or len( staff ) > 0 :

					if len( observers ) > 0 :
						staffstring += 'Observers: '+ observers + ' | '

					if len( remote ) > 0 :
						staffstring += 'SAs: '+ remote + ' | '

					if len( staff ) > 0 :
						staffstring += 'Operators: '+ staff
						
				maintext += '<tr><td colspan=3>'+ staffstring + ' </td></tr>'

	#			maintext += '<tr><td colspan=3><hr></td></tr>'




		maintext += '</table>'

		maintext += ''+ zoomString + ''

		maintext += '</td>'


	#	breakday = ( 5, 12, 19, 26 )

	#	if nday in breakday :

	#		maintext += "</tr>"

		tempoffset += 1

		if tempoffset == 6:

			maintext += "</tr>"
			tempoffset = -1


		nday += 1

	if tempoffset > 0:

		tempoffset = 6 - tempoffset
		i = 0
		while i < tempoffset:

	#		maintext +="<td>endoffset: &nbsp;</td>"
			maintext +="<td>&nbsp;</td>"
			i += 1

	maintext += "</tr></table> offset / totaldays: " + str( tempoffset ) + ' / ' + str( totaldays ) + ' dayno: ' + str( dayno )


	#startdate1 = now + datetime.timedelta( months = 1 )
	#datetime.date( nyear, nmonth1, nday )
	#starty1 = startdate1.strftime('%Y')
	#startm1 = startdate1.strftime('%m')
	#starts1 = startdate1.strftime('%Y-%m')
	#button1 = '<a href=sumcal.py?year=%s&month=%s&logcrew=WP>%s</a>' % ( starty1, startm1, starts1 )

	#startdate2 = startdate + datetime.timedelta ( month = 2 )
	#startdate2 = datetime.date( nyear, nmonth2, nday )
	#starty2 = startdate2.strftime('%Y')
	#startm2 = startdate2.strftime('%m')
	#starts2 = startdate2.strftime('%Y-%m')
	#button2 = '<a href=sumcal.py?year=%s&month=%s&logcrew=WP>%s</a>' % ( starty2, startm2, starts2 )

	#startdate3 = startdate + datetime.timedelta ( month = 3 )
	##startdate3 = datetime.date( nyear, nmonth + 3, nday )
	#starty3 = startdate3.strftime('%Y')
	#startm3 = startdate3.strftime('%m')
	#starts3 = startdate3.strftime('%Y-%m')
	#button3 = '<a href=sumcal.py?year=%s&month=%s&logcrew=WP>%s</a>' % ( starty3, startm3, starts3 )

	#startdate4 = datetime.date( nyear, nmonth + 4, nday )
	#startdate5 = datetime.date( nyear, nmonth + 5, nday )
	#startdate6 = datetime.date( nyear, nmonth + 6, nday )
	#startdate5 = datetime.date( nyear, nmonth + 7, nday )
	#startdate6 = datetime.date( nyear, nmonth + 8, nday )

	#print( 'Months: ' + button1 + ' | ' + button2 + ' | ' + button3 )
	#maintext='tom'

else :

#	maintext = "OPAL Login Required <a href='../login.php'>Here</a>"
	maintext = logproc.returnLogin()

printHTML( maintext )


