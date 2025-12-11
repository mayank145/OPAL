#! /usr/local/python

import os
import dbconnect

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

dbconn=dbconnect.opalconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
#db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()
#cursor2.execute("set autocommit = 1")
cursor3=db.cursor()
cursor3.execute("set autocommit = 1")

sem = 'S25B'

#cursor.execute("select idno, propid from props where sem='S23B' order by idno")
cursor.execute("select idno, propid from props where sem='%s' order by idno" % ( sem ) )

seq = 0

for row in cursor.fetchall() :

	seq += 1
	
	props_idno = row[0]	
	props_propid = row[1]
	
	print( str( seq ) + ' ' +str( props_idno ) + ' ' + props_propid )
	
	cursor2.execute("select min( datein ) from alloc where propidno = %s and cal='Y'" % ( props_idno ) )
	numrows2 = cursor2.rowcount
	if numrows2 == 1 :
		rows2=cursor2.fetchone()
		mindate = rows2[0]
		print('minDate: ' + str( mindate ) )
		cmd3 = "update props set datein = '%s' where idno=%s" % ( mindate, props_idno )
		print('cmd: ' + cmd3 )
		cursor3.execute( cmd3 )
	
