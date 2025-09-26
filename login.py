#! /usr/local/python

import os
import cgi
import datetime


def printHTML( maintext ) :

	css_text = "<style type='text/css'>"
	css_text += "body { text-align: left; font-family: Arial, Helvetica, sans-serif; font-weight: font-size:12px }"
	css_text += "table { cell-padding: 2; cell-spacing: 2; }"
	css_text += "th { text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:14px }"
	css_text += "th.center { background-color: yellow; text-align: center; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size:10px }"
	css_text += "tr:nth-child(even) { background: #CCC; }"
	css_text += "tr:nth-child(odd) { background: #FFF; }"
	css_text += "td { text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.center { text-align:center; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.right { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 12px }"
	css_text += "td.label { text-align:right; font-family: Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold }"
	css_text += "</style>"


	printpg = ''
	printpg += "Content-type: text/html;\n\n"
	printpg += "<HTML><HEAD>"
	printpg += "<META HTTP-EQUIV='pragma' CONTENT='no-cache'>"
	printpg += css_text
	printpg += "</HEAD><BODY><center>"
	printpg += maintext
	printpg += "</center></BODY></HTML>"
	print( printpg )	


maintext  = "<form method=post action='./login3.py?'><br><br>"
maintext += "<table>"
maintext += "<td><center><FONT SIZE=4><i><b>New OPAL</b></i><br><br>"
maintext += "<b>Summit Calendar, Logs, Cars<br>Login</b><br><br>"
maintext += "</center></td>"
maintext += '<td bgcolor=white><center><img src=./Aurora-Australias-2.jpeg></center></td></tr>'
maintext += "<tr><td bgcolor=white><hr></td><td bgcolor=white><hr></td></tr>"
maintext += "<tr><td class=right>UserName:</td><td><input type=text name='username' value=''></td></tr>"
#maintext += "<tr><td>Password:</td><td><input type=text name='pw' value=''></td></tr>"
maintext += "<tr><td class=right>Password:</td><td><input type=password name='pw' value=''></td></tr>"
#maintext += "<tr><td></td><td><input type=submit name=action value='Login'></td></tr>"
#maintext += '<td><center><img src=./Aurora-Australias-2.jpeg></center></td>'
maintext += "</table><br>"
maintext += "<input type=submit name=action value='Login'>"
maintext += "</form>"

printHTML( maintext )

