#! /usr/local/python

import os
import sys
import datetime
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import dbconnect

dbconn=dbconnect.dbconn()
db=MySQLdb.connect(host=dbconn[0],user=dbconn[1],passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor=db.cursor()
cursor2=db.cursor()

now = datetime.datetime.now()
today = now.strftime( '%Y-%m-%d' )
yesterday2 = now - datetime.timedelta( days = 1 )
yesterday = yesterday2.strftime( '%Y-%m-%d' )

cursor.execute("select mailed, mailtime from days where date = '%s'" % ( yesterday ) )
numrows = cursor.rowcount

if numrows == 1 :

	row = cursor.fetchone()
	mailedFlag = row[0]
	mailtime = row[1]
	
	if mailedFlag == 'F' :

		cmd = '/var/www/html/sumlogs/logmail2.py ' + yesterday + ' yes log'
		print( cmd )
		os.system( cmd )
#below update is done by the logmail2 above
#		cursor2.execute("update days set mailed='T', mailtime='%s' where date='%s'" % ( now, yesterday ) )
			
	else:
		print("Summit Log Mail already sent: " + mailedFlag + ' @ ' + str( mailtime ) + " for " + yesterday )
