#! /usr/local/python

import os
import ldap3
import dbconnect
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

dbconn=dbconnect.opalconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
db.autocommit(1)
cursor=db.cursor()

def getMember ( gid ) :

	from ldap3 import Server, Connection, ALL

	s = Server( host='squery.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	conn = Connection(s, auto_bind=True)
#conn.search('memberuid=winegar,ou=Group,dc=subaru,dc=nao,dc=ac,dc=jp', '(objectClass=*)' , 'SUBTREE', attributes=['dn'] )


	conn.search('ou=Group,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=' +  gid + ')' , 'SUBTREE', attributes=['memberUid'] )


	members = []

	if len( conn.entries ) > 0 :

		print('conn.entries: ' + str( conn.entries ) )
		for entry in conn.entries[0] :

			for entry2 in entry :

				group = str( entry2 )
				members.append ( group )
	

	
#	print( str ( members ) + ' members' )
	
#	maintext = '<table cellpadding=3 cellspacing=4><tr><th colspan=4 bgcolor=lime>STARS LDAP assigned USERS ( %s )</th></tr>' % ( len( members ) ) 
	
	maintext = ''
	
	if len( members ) > 0 :
	
	
		for member in members :
		
			seq += 1
	
#			memberuid, gecos, mail = getGecos( member )
			
#			conn.search('ou=People,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=' +  member + ')' , 'SUBTREE', attributes=['gecos', 'mail', 'uid', 'uidnumber'] )

#			gecos = conn.entries[0]['gecos']
#			mail = conn.entries[0]['mail']
			mail=''
#			uid = conn.entries[0]['uidnumber']
			
#			maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, member, gecos, mail, uid )
#			maintext += '"%s","%s","%s","%s"."%s"%s' % ( seq, member, gecos, mail, uid, "\n" )
#			maintext += '"%s","%s","%s","%s"%s' % ( seq, member, mail, uid, "\n" )
			maintext += '"%s","%s","%s","%s"' % ( seq, member, gid, "\n" )

	else :
		
		maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( '0', 'none', 'none', 'none' )

	maintext += '</table>'
	return ( maintext )


def main() :

#	gids = ( 'o22600', )
	returnText = ''
#! /usr/local/python

import os
import ldap3
import dbconnect
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

dbconn=dbconnect.opalconn()
db=MySQLdb.connect( host=dbconn[0], user=dbconn[1], passwd=dbconn[2], db=dbconn[3])
cursor = db.cursor()
cursor2 = db.cursor()

def getMember ( gid ) :

	from ldap3 import Server, Connection, ALL

	s = Server( host='squery.subaru.nao.ac.jp', port=389, use_ssl=False, get_info='ALL' )
	conn = Connection(s, auto_bind=True)
#conn.search('memberuid=winegar,ou=Group,dc=subaru,dc=nao,dc=ac,dc=jp', '(objectClass=*)' , 'SUBTREE', attributes=['dn'] )


	conn.search('ou=Group,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=' +  gid + ')' , 'SUBTREE', attributes=['memberUid'] )


	members = []
	maintext = ''

	if len( conn.entries ) > 0 :

#		print('conn.entries: ' + str( conn.entries ) )
		for entry in conn.entries[0] :

			for entry2 in entry :

				group = str( entry2 )
				members.append ( group )
	

	
#	print( str ( members ) + ' members' )
	
#	maintext = '<table cellpadding=3 cellspacing=4><tr><th colspan=4 bgcolor=lime>STARS LDAP assigned USERS ( %s )</th></tr>' % ( len( members ) ) 

	
	if len( members ) > 0 :
	
		seq = 0
	
		for member in members :
		
			seq += 1
	
#			memberuid, gecos, mail = getGecos( member )
			
#			conn.search('ou=People,dc=stars,dc=nao,dc=ac,dc=jp', '(cn=' +  member + ')' , 'SUBTREE', attributes=['gecos', 'mail', 'uid', 'uidnumber'] )

#			gecos = conn.entries[0]['gecos']
#			mail = conn.entries[0]['mail']
			mail = ''
#			uid = conn.entries[0]['uidnumber']
			uid = member
			
#			maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( seq, member, gecos, mail, uid )
#			maintext += '"%s","%s","%s","%s"."%s"%s' % ( seq, member, gecos, mail, uid, "\n" )
			maintext += "%s %s\n" % ( member, gid  )
			
			cursor2.execute("insert into starsldap ( gid, username ) values ( '%s', '%s' )" % ( gid, member )  )

#	else :
		
#		maintext += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ( '0', 'none', 'none', 'none' )
	else :

		maintext = ''
#	maintext += '</table>'
	return ( maintext )


def main() :

#	gids = ( 'o22600', )
#	returnText = ''

	gids = ( 'cacadm', 'chsadm', 'ciaadm', 'comadm', 'crsadm', 'fcsadm', 'fldadm', 'fmsadm', 'hdsadm', 'hicadm', 'hscadm', \
	'ircadm', 'irdadm', 'k3dadm', 'logadm', 'mcsadm', 'miradm', 'mmzadm', 'ohsadm', 'pfsadm', 'scxadm', 'skyadm', 'sukadm', \
	'supadm', 'swsadm', 'vgwadm', 'vmpadm' )


#	cursor.execute("select gid from props where gid is not null group by gid order by gid")

#	for row in cursor.fetchall() :
	for row in gids :

#		gid = row[0]
		gid = row
#		print( 'GIDs: ' + gid )
		returnText = getMember( gid )
		returnText=returnText.strip()
		if len( returnText ) > 0 : 
			print( returnText )	
				
#	print( 'gids: ' +  str( gids ) )
#	returnText = ''
#	for gid in gids:
#		print( 'gid: ' +  gid )
#		returnText += getMember( gid )
#	print( returnText )
	
main()
	
#	print( 'gids: ' +  str( gids ) )
#	returnText = ''
#	for gid in gids:
#		print( 'gid: ' +  gid )
#		returnText += getMember( gid )
#	print( returnText )
	
