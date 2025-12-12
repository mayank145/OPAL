#! /usr/local/python

import datetime
import urllib.request, json
import re, cgi

#weather_url='https://www-stage.subaru.nao.ac.jp/Weather/data/SensorDump.json'
weather_url = 'https://www.naoj.org/Weather/data/SensorDump.json'
weather_url2 = 'http://mkwc.ifa.hawaii.edu/current/'

# weather now HST

now = datetime.datetime.now()
today = now.strftime( "%Y-%m-%d %H:%M:%S" )
minFile = now.strftime( "%y%m%d" )

utcnow = datetime.datetime.utcnow()
utctoday = utcnow.strftime( "%Y-%m-%d %H:%M:%S" )


#write = 'No'
write = 'yes'


se_temp = -99
se_humid = -98

keck_temp = -99
keck_humid = -98

msg = ''

source = 'Subaru' 
source2 = 'Subaru' 

bad_results = ( '-99', '-98', '--' )

try :
	url = urllib.request.urlopen( weather_url )

except HTTPError as e: 

	msg += 'HTTP-Error: Subaru Weather server trouble - ' + e.reason + "\n"

except URLError as e:

	msg += 'URL-Error: Subaru Weather fail to reach - ' + e.reason + "\n"

else : 

	try :
		data = json.load ( url )

	except ValueError as e:

		msg += 'JSON.load FAILS: Subaru - ' + e.reason + "\n"
	
	else :

		f1 = data['F1']
		se_temp = f1['P2']['Value']
		se_temp_int = float( se_temp )
		se_temp_label = f1['P2']['Label']
		f0 = data['F0']
		se_humid = f0['P2']['Value']
		se_humid_int = int( se_humid )

		se_humid_label = f0['P2']['Label']
	#	print( data )
		print( 'F1-P2-SE_Temp: '+ se_temp_label+ ' '  +str( se_temp ) )
		print( 'F0-P2-SE_Humidity: ' + se_humid_label + ' ' + str( se_humid_int ) )


try :
	url2 = urllib.request.urlopen( weather_url2 )

except HTTPError as e: 

	msg += 'HTTP-Error: MKWC server trouble - ' + e.reason + "\n"

except URLError as e:

	msg += 'URL-Error: MKWC fail to reach - ' + e.reason + "\n"

else : 

#with urllib.request.urlopen( weather_url2 ) as url2 :

	mkwc2 = url2.read()
	mkwc2String = str( mkwc2 )
	result2 = mkwc2String.split("</tr>")
	seq = 0
	seq2 = 0
	
	source2 = 'KECK'
	
	tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
	
	for line in result2 :

		seq += 1

		if source2 in line :

			startPos = line.find( source2 )
			sub_line = line[startPos:6000]
			sub_line2 = sub_line.split("</td>")

			for line2 in sub_line2:
			
	

				seq2 += 1
#				line2 = line2.lstrip("\n")
				
				
				line2 = tag_re.sub('', line2)
								
#				if line2[2:3] == '/' and line2[5:6] == '/' and seq2 == 2 :
				
				print( str( seq2 ) + ' ' + line2 )
				
#				line2=line2.replace("\n", '')
				
				if seq2 == 4:
				
					keck_temp = line2[2:]
					
				if seq2 == 6 :
				
					keck_humid = line2[2:]
			
			keck_temp_int = int( float( keck_temp ) )

			keck_humid_int = int( keck_humid )


			print('Keck Temp: ' + str( keck_temp ) )
			print('Keck Humid: ' + str( keck_humid ) )
			

if se_temp_int in bad_results or se_humid_int in bad_results :

	if keck_temp_int not in bad_results and keck_humid_int not in bad_results :
	
		source = 'Keck'
		
		se_temp = keck_temp
		se_temp_int = float( se_temp )
	
		se_humid = keck_humid
		se_humid_int = int( se_humid )


bgcolor='yellow'
alarmText = ''

if se_temp_int < 0 :

	bgcolor='yellow'
	alarmText += '<i>Warning!</i> <b>Temp %s</b> is below 0<br>' \
	% ( se_temp )

if se_humid_int > 90 :

	bgcolor='yellow'
	alarmText += '<i>Warning!</i> <b>RH %s</b> is above 90<br>' \
	% ( se_humid_int )

if se_temp_int < 0 and se_humid > 90 :

	bgcolor='pink'
	alarmText += '<i>------| <b>ICE</b> Now! | ------</i> <b>Temp %s & RH %s</b><br>' \
	% ( se_temp_int, se_humid_int )

if len( alarmText ) == 0 :

	bgcolor = 'white'
	alarmText2 = "<table><td bgcolor=%s>No Alarm <FONT SIZE=-1>(%s)<FONT SIZE=+1></td><td bgcolor=lime>Temp = <b>%s</b></td> \
	<td bgcolor=lime>RH = <b>%s</b></td></table>\n" \
	% ( bgcolor, source, se_temp, se_humid_int )

else :

	alarmText2 = "<table><td bgcolor=%s><center><FONT SIZE=+1 COLOR=blue> \
	<b>Alarms <FONT SIZE=-1>(%s) <FONT SIZE=+1>%s %s:</b><br></center></td></table>\n" \
	% ( bgcolor, source, alarmText )

tempString = today + " " + str( se_temp ) + " " + str( se_humid_int ) + " " + utctoday + "UTC\n"
	

if write == 'yes' :

#	FILE1 = open('/var/www/html/sumlogs/weather_json.txt', 'w' )
	minWeather = '/var/www/html/sumlogs/weather.txt'
	FILE1 = open( minWeather, 'w' )

	FILE1.write('TEMP: ' + str( se_temp_int ) + "\n" )
	FILE1.write('RH: ' + str( se_humid_int ) + "\n" )


	FILE1.write( alarmText2 + "\n" )
	FILE1.close()

	minFile2='/var/www/html/sumlogs/weather/'+minFile+'.txt'
	FILE2=open( minFile2, 'a')

#	FILE2.write( today + " " + se_temp + " " + se_humid + " " + utctoday + "UTC\n" )
	FILE2.write( tempString )
	FILE2.close()	

else :

	print( 'No Write - alarms: ' + alarmText2 )

print( 'alarmText: ' + alarmText2 )
print( 'tempString: ' + tempString )
print('end status: '+ msg)		
