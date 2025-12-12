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
#today='2021-05-18'
cursor.execute("select mailday, maildtime from days where date = '%s'" % ( today ) )
numrows = cursor.rowcount

if numrows == 1 :

	row = cursor.fetchone()
	mailday = row[0]
	maildtime = row[1]
	
	if mailday == 'F' :

		cmd = '/var/www/html/sumlogs/planmail2.py ' + today + ' yes'

		os.system( cmd )

		cursor2.execute("update days set mailday='T', maildtime='%s' where date='%s'" % ( now, today ) )
			
	else:
		print("SummitLog Day Mail already sent: " + mailday + ' @ ' + str( mailstime ) + " for " + today )
