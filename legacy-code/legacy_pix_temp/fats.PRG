* Tom Winegar
* National Astromonical Observatory of Japan
* (c) 1999-2000
*
* comments 1/17/99 nishi noumaru tom
* 1. DONE need user's screen just a few buttons, add, search lists
* 2. DONE need to link fault to log comment in summit log: log field in FAT, Fat field in Log
*         user can go back and forth. Can dump log comment to new fat from log item show.
* 3. DONE need formatting for procedures in problem description,
*         solution description, CR - ok, indent-use spaces
* 4. DONE Date browses, yesterday, last week, last month. Date only searches ok.
* 5. DONE need to change category in editfat, and have providors change
* 6. STARTED solution needs escalation-redirect button, closes first FAT and archives info
*    from first to second fat, through addlink in solution
* 7. user is away - mark as out, hot list forwarded to new user?
* 8. DONE FOR ASSIGNMENTS. email connection - notifies you of new faults, overdue items,
* 9. japanese pages.
* 10. DONE - bigger solution description field, 15 lines down.
* 11. DONE each category of solutions, possible solutions, comments in chronological order.
* 12. DONE limit size of solution description on search window.
* 13. DONE - cookie of username lasts past current session until 12/31/2001
* 14. work on flink addition, deletion
* 15. DONE - HotList deletion for reporter notification.
* 16. write number of times acces from different IP localhost - 127.0.0.1
*     ts05 from base - 192.168.1.8

* elvis
* 1. need to replace board, therefore re-orient table vertical cars, horizontal - days.
* 2. show days/eve on same day.
* 3. multiple day reserve.
*
proc iplock
public ipfail,cgiadd
ipfail="F"
m.cgiadd=allt(cgi.remoteaddress)
*if substr(m.cgiadd,1,6) != "133.40"
if allt(m.cgiadd) = "133.40.143.228" or allt(m.cgiadd) = "133.40.143.229"
	ipfail="T"
endif
return    

proc editsave

m.idno=formfield("idno")
m.sidno=m.idno
m.reporter=formfield("reporter")
m.assigned=formfield("assigned")
m.repmail=formfield("repmail")
m.section=formfield("section")
m.cat=formfield("cat")
m.subcat=formfield("subcat")
m.issue=formfield("issue")
m.idescribe=formfield("idescribe")
m.datein=formfield("datein")
m.priority=formfield("priority")
m.status=formfield("status")
m.itype=formfield("itype")
m.keyin=formfield("keyin")
m.action=formfield("action")
m.solution=formfield("solution")
m.sdescribe=formfield("sdescribe")
m.sfinal=formfield("sfinal")
m.keyout=formfield("keyout")
m.issuej=formfield("issuej")
m.idescribej=formfield("idescribej")
m.solutionj=formfield("solutionj")
m.sdescribej=formfield("sdescribej")
m.actionj=formfield("actionj")

m.opeaction=formfield("opeaction")
m.incharge=formfield("incharge")
m.agrees=formfield("sagrees")
m.response1=formfield("sresponse")
m.cause=formfield("scause")
m.scheduled=formfield("sscheduled")


select datein,priority,section from fault into cursor one_datein where idno=val(m.idno)
m.mdatein=ttod(one_datein.datein)
m.mpriority=one_datein.priority
m.msection=allt(one_datein.section)
if m.msection<>m.section and m.status<>"Solved"
	select ass1,ass1mail,ass2,ass2mail,super,supermail from fcat ;
	into cursor one_ass where section=m.section
	m.ass1=allt(one_ass.ass1)
	m.ass1mail=allt(one_ass.ass1mail)
	m.ass2=allt(one_ass.ass2)
	m.ass2mail=allt(one_ass.ass2mail)
	m.super=allt(one_ass.super)
	m.supermail=allt(one_ass.supermail)
	update fault set ass1=m.ass1,ass1mail=m.ass1mail,ass2=m.ass2,ass2mail=m.ass2mail,super=m.super, ;
	supermail=m.supermail where idno=val(m.idno)
endif
update fault set issue=allt(m.issue),idescribe=allt(m.idescribe), ;
priority=m.priority,status=m.status,itype=m.itype,keyin=m.keyin,action=allt(m.action), ;
solution=allt(m.solution),sdescribe=allt(m.sdescribe),sfinal=m.sfinal,keyout=m.keyout, ;
section=m.section,issuej=allt(m.issuej),idescribej=allt(m.idescribej),solutionj=allt(m.solutionj), ;
sdescribej=allt(m.sdescribej),actionj=allt(m.actionj), ;
opeaction=m.opeaction,incharge=m.incharge,agrees=m.agrees, ;
response=m.response1,cause=m.cause,scheduled=m.scheduled ;
where idno=val(m.idno)
if (m.mpriority<>m.priority or m.msection<>m.section) and m.status<>"Solved"
	do case
 	case m.priority="Low"
 		m.to_ass1="T"
 		m.to_ass2="F"
 		m.to_super="F"
		m.a_ass1=m.mdatein
		m.a_ass2=m.mdatein+3
		m.a_super=m.mdatein+6
		m.s_ass1=m.mdatein+2
		m.s_ass2=m.mdatein+5
		m.s_super=m.mdatein+7
 	case m.priority="Med"
 		m.to_ass1="T"
 		m.to_ass2="F"
 		m.to_super="F"
		m.a_ass1=m.mdatein
		m.a_ass2=m.mdatein+1
		m.a_super=m.mdatein+2
		m.s_ass1=m.mdatein+1
		m.s_ass2=m.mdatein+3
		m.s_super=m.mdatein+3
 	case m.priority="Hi"
 		m.to_ass1="T"
 		m.to_ass2="T"
 		m.to_super="T"
		m.a_ass1=m.mdatein
		m.a_ass2=m.mdatein
		m.a_super=m.mdatein
		m.s_ass1=m.mdatein+1
		m.s_ass2=m.mdatein+1
		m.s_super=m.mdatein+1
	otherwise
	 	m.to_ass1="T"
 		m.to_ass2="F"
 		m.to_super="F"
		m.a_ass1=m.mdatein
		m.a_ass2=m.mdatein+3
		m.a_super=m.mdatein+6
		m.s_ass1=m.mdatein+2
		m.s_ass2=m.mdatein+5
		m.s_super=m.mdatein+7
	endcase
	if m.a_ass2<=date()
		m.to_ass2="T"
	endif
	if m.a_super<=date()
		m.to_super="T"
	endif
	update fault set to_ass1=m.to_ass1,to_ass2=m.to_ass2,to_super=m.to_super, ;
	a_ass1=m.a_ass1,a_ass2=m.a_ass2,a_super=m.a_super, ;
	s_ass1=m.s_ass1,s_ass2=m.s_ass2,s_super=m.s_super ;
	where idno=val(m.idno)
endif
do f1 with m.sidno
return


proc f1
parameter sidno
m.sidno=allt(formfield("sidno"))
m.cgiadd=allt(cgi.remoteaddress)
do case
	case substr(m.cgiadd,1,10)="192.168.9."
		update fault set acc_sum=acc_sum+1,accessed=accessed+1 where idno=val(m.sidno) 
	case substr(m.cgiadd,1,10)="192.168.1."
		update fault set acc_base=acc_base+1,accessed=accessed+1 where idno=val(m.sidno)
*	case substr(m.cgiadd,1,3)="127"
*		update fault set acc_base=acc_base+1,accessed=accessed+1 where idno=val(m.sidno)
	otherwise		 
		update fault set accessed=accessed+1 where idno=val(m.sidno)
endcase
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_rep,to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super,log,logdate,fattrans,soltrans, ;
accessed,acc_base,acc_sum,opeaction,incharge,agrees,response,cause,scheduled from fault ;
where idno=val(m.sidno) into cursor f1
m.idno=str(f1.idno,4)
m.reporter=allt(f1.reporter)
m.repmail=allt(f1.repmail)
m.section=allt(f1.section)
m.cat=allt(f1.cat)
m.subcat=allt(f1.subcat)
m.issue=allt(f1.issue)
m.idescribe=allt(f1.idescribe)
*m.idescribe='<TEXTAREA WRAP="physical" NAME="idescribe" rows="10" cols="42">'+allt(f1.idescribe)+'</TEXTAREA>'
m.tdatein=ttoc(f1.datein)
m.tdateout=ttoc(f1.dateout)
m.datein=allt(dtoc(ttod(f1.datein)))
m.timein=substr(ttoc(f1.datein),10,5)+substr(ttoc(f1.datein),19,2)
m.dateout=allt(dtoc(ttod(f1.dateout)))
m.timeout=substr(ttoc(f1.dateout),10,5)+substr(ttoc(f1.dateout),19,2)
m.action=allt(f1.action)
m.solution=allt(f1.solution)
*m.sdescribe=allt(f1.sdescribe)
*m.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="10" cols="42">'+allt(f1.sdescribe)+'</TEXTAREA>'
m.sdescribe=allt(f1.sdescribe)
m.priority=allt(f1.priority)
m.status=allt(f1.status)
m.sfinal=allt(f1.sfinal)
m.ass1=allt(f1.ass1)
m.ass1mail=allt(f1.ass1mail)
m.ass2=allt(f1.ass2)
m.ass2mail=allt(f1.ass2mail)
m.super=allt(f1.super)
m.supermail=allt(f1.supermail)
m.to_rep=allt(f1.to_rep)
m.to_ass1=f1.to_ass1
m.to_ass2=f1.to_ass2
m.to_super=f1.to_super
m.itype=allt(f1.itype)
m.keyin=allt(f1.keyin)
m.keyout=allt(f1.keyout)
m.s_ass1=dtoc(f1.s_ass1)
m.s_ass2=dtoc(f1.s_ass2)
m.s_super=dtoc(f1.s_super)
m.a_ass1=dtoc(f1.a_ass1)
m.a_ass2=dtoc(f1.a_ass2)
m.a_super=dtoc(f1.a_super)
m.r_ass1=dtoc(f1.r_ass1)
m.r_ass2=dtoc(f1.r_ass2)
m.r_super=dtoc(f1.r_super)
m.logdate=dtoc(f1.logdate)
m.log=allt(str(f1.log))
m.logdate='<A HREF="' + ;
	UrlEncode(CGI.ExecutablePath+'/logentry@'+CGI.ProgramPath+'elvis?date=')+ ;
    UrlEncode(m.logdate)+'">'+m.logdate+'</A><B>'
m.fattrans=ttoc(f1.fattrans)
m.soltrans=ttoc(f1.soltrans)
m.accessed=str(f1.accessed)
m.acc_base=str(f1.acc_base)
m.acc_sum=str(f1.acc_sum)
m.inout=str((f1.dateout-f1.datein)/3600,5,2)+" hours"
m.dinout=str((f1.dateout-f1.datein)/86400 ,5,2)+" days"
m.finout=str((f1.fattrans-f1.datein)/86400 ,5,2)+" days"
m.sinout=str((f1.soltrans-f1.dateout)/86400 ,5,2)+" days"
m.opeaction=allt(f1.opeaction)
m.incharge=allt(f1.incharge)
m.agrees=allt(f1.agrees)
m.response1=allt(f1.response)
m.cause=allt(f1.cause)
m.scheduled=allt(f1.scheduled)

select idno,fidno,imgname from faultpic into cursor all_pic where fidno=val(m.sidno) 
m.ImgText="<table>"
m.ImgLink=""
if reccount()>0
	scan
		m.ImgText=m.ImgText+"<tr><td>"+allt(all_pic.imgname)+'<br><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/deleteimg@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(m.sidno)+'&'+'pixidno='+UrlEncode(allt(str(all_pic.idno)))+'">Delete Img</A></td>'
		m.ImgText=m.ImgText+'<td><IMG SRC="/fpix/'+m.sidno+'_'+allt(all_pic.imgname)+'"></td></tr>'
	endscan
endif
if allt(m.ImgText)==""
		m.ImgText=m.ImgText+"No Images"
endif
m.ImgText=m.ImgText+'</table>'


select idno,providor,pmail,action,solution,sdescribe,stype,solid,solout from fsol ;
order by stype,solout desc ;
into cursor all_sol where idno=val(m.sidno)
if reccount()>0
   	 	M.ListTxt1 = '<TABLE borders=1 rules=all><TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.solid)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A><BR><FONT SIZE=-1>'+allt(all_sol.providor)+'</TD><TD>'+'Action: '+allt(all_sol.action)+'<BR>'+ ;
    	'Solution: '+allt(all_sol.solution)+'<BR>'+ ;
    	'Descript: '+allt(all_sol.sdescribe)+"<BR>"+ ;
    	ttoc(all_sol.solout)+" - "+str(all_sol.solid,5)+" "+ ;
    	'<FONT SIZE=-1><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/addlink@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'&'+'solid='+UrlEncode(allt(str(all_sol.solid)))+'">Add Link</TD></TR>'
		select idno,link,linktxt from flink into cursor all_link where solid=all_sol.solid
		if reccount()>0
			select issue from fault into cursor one_f where idno=all_link.link
			m.fissue=one_f.issue
			sele all_link
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    		m.fissue+'</TD></TR>'
	   		skip
	   	 	scan rest
			select issue from fault into cursor one_f where idno=all_link.link
			m.fissue=one_f.issue
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    		m.fissue+'</TD></TR>'
    		sele all_link
    		endscan
		endif
		sele all_sol
   		skip
   	 	scan rest
   	 	M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.solid)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A><BR><FONT SIZE=-1>'+allt(all_sol.providor)+'</TD><TD>'+'Action: '+allt(all_sol.action)+'<BR>'+ ;
    	'Solution: '+allt(all_sol.solution)+'<BR>'+ ;
    	'Descript: '+allt(all_sol.sdescribe)+"<BR>"+ ;
    	ttoc(all_sol.solout)+" - "+str(all_sol.solid,5)+" "+ ;
    	'<FONT SIZE=-1><A HREF="' + ;
  		UrlEncode(CGI.ExecutablePath+'/addlink@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'&'+'solid='+UrlEncode(allt(str(all_sol.solid)))+'">Add Link</TD></TR>'    	
		select idno,link,linktxt from flink into cursor all_link where solid=all_sol.solid
		if reccount()>0
			select issue from fault into cursor one_f where idno=all_link.link
				m.fissue=one_f.issue
				sele all_link
   	 			M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    			UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    			UrlEncode(allt(str(all_link.link))) ;
    			+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    			m.fissue+'</TD></TR>'
    		sele all_link
	   		skip
	   	 	scan rest
			select issue from fault into cursor one_f where idno=all_link.link
				m.fissue=one_f.issue
   	 			M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    			UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    			UrlEncode(allt(str(all_link.link))) ;
    			+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    			m.fissue+'</TD></TR>'
    		endscan
		endif
    	endscan
		M.ListTxt1=M.ListTxt1+"</TABLE>"
else

		M.ListTxt1 = "No solutions for this fault!"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'fault1' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc f3
parameter sidno
m.sidno=allt(formfield("sidno"))
m.cgiadd=allt(cgi.remoteaddress)
do case
	case substr(m.cgiadd,1,10)="192.168.9."
		update fault set acc_sum=acc_sum+1,accessed=accessed+1 where idno=val(m.sidno) 
	case substr(m.cgiadd,1,10)="192.168.1."
		update fault set acc_base=acc_base+1,accessed=accessed+1 where idno=val(m.sidno)
*	case substr(m.cgiadd,1,3)="127"
*		update fault set acc_base=acc_base+1,accessed=accessed+1 where idno=val(m.sidno)
	otherwise		 
		update fault set accessed=accessed+1 where idno=val(m.sidno)
endcase
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_rep,to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super,log,logdate,fattrans,soltrans, ;
accessed,acc_base,acc_sum,opeaction,incharge,agrees,response,cause,scheduled from fault ;
where idno=val(m.sidno) into cursor f1
m.idno=str(f1.idno,4)
m.reporter=allt(f1.reporter)
m.repmail=allt(f1.repmail)
m.section=allt(f1.section)
m.cat=allt(f1.cat)
m.subcat=allt(f1.subcat)
m.issue=allt(f1.issue)
m.idescribe=allt(f1.idescribe)
m.idescribe='<PRE><FONT SIZE=+1>'+allt(f1.idescribe)+'</PRE>'
*m.idescribe='<TEXTAREA WRAP="physical" NAME="idescribe" rows="10" cols="42">'+allt(f1.idescribe)+'</TEXTAREA>'
m.tdatein=ttoc(f1.datein)
m.tdateout=ttoc(f1.dateout)
m.datein=allt(dtoc(ttod(f1.datein)))
m.timein=substr(ttoc(f1.datein),10,5)+substr(ttoc(f1.datein),19,2)
m.dateout=allt(dtoc(ttod(f1.dateout)))
m.timeout=substr(ttoc(f1.dateout),10,5)+substr(ttoc(f1.dateout),19,2)
m.action=allt(f1.action)
m.solution=allt(f1.solution)
*m.sdescribe=allt(f1.sdescribe)
*m.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="10" cols="42">'+allt(f1.sdescribe)+'</TEXTAREA>'
m.sdescribe='<PRE><FONT SIZE=+1>'+allt(f1.sdescribe)+'</PRE>'
m.priority=allt(f1.priority)
m.status=allt(f1.status)
m.sfinal=allt(f1.sfinal)
m.ass1=allt(f1.ass1)
m.ass1mail=allt(f1.ass1mail)
m.ass2=allt(f1.ass2)
m.ass2mail=allt(f1.ass2mail)
m.super=allt(f1.super)
m.supermail=allt(f1.supermail)
m.to_rep=allt(f1.to_rep)
m.to_ass1=f1.to_ass1
m.to_ass2=f1.to_ass2
m.to_super=f1.to_super
m.itype=allt(f1.itype)
m.keyin=allt(f1.keyin)
m.keyout=allt(f1.keyout)
m.s_ass1=dtoc(f1.s_ass1)
m.s_ass2=dtoc(f1.s_ass2)
m.s_super=dtoc(f1.s_super)
m.a_ass1=dtoc(f1.a_ass1)
m.a_ass2=dtoc(f1.a_ass2)
m.a_super=dtoc(f1.a_super)
m.r_ass1=dtoc(f1.r_ass1)
m.r_ass2=dtoc(f1.r_ass2)
m.r_super=dtoc(f1.r_super)
m.logdate=dtoc(f1.logdate)
m.log=allt(str(f1.log))
m.logdate='<A HREF="' + ;
	UrlEncode(CGI.ExecutablePath+'/logentry@'+CGI.ProgramPath+'elvis?date=')+ ;
    UrlEncode(m.logdate)+'">'+m.logdate+'</A><B>'
m.fattrans=ttoc(f1.fattrans)
m.soltrans=ttoc(f1.soltrans)
m.accessed=str(f1.accessed)
m.acc_base=str(f1.acc_base)
m.acc_sum=str(f1.acc_sum)
m.inout=str((f1.dateout-f1.datein)/3600,5,2)+" hours"
m.dinout=str((f1.dateout-f1.datein)/86400 ,5,2)+" days"
m.finout=str((f1.fattrans-f1.datein)/86400 ,5,2)+" days"
m.sinout=str((f1.soltrans-f1.dateout)/86400 ,5,2)+" days"
m.opeaction=allt(f1.opeaction)
m.incharge=allt(f1.incharge)
m.agrees=allt(f1.agrees)
m.response1=allt(f1.response)
m.cause=allt(f1.cause)
m.scheduled=allt(f1.scheduled)

select idno,fidno,imgname from faultpic into cursor all_pic where fidno=val(m.sidno) 
m.ImgText="<table>"
m.ImgLink=""
if reccount()>0
	scan
		m.ImgText=m.ImgText+"<tr><td>"+allt(all_pic.imgname)+'<br><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/deleteimg@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(m.sidno)+'&'+'pixidno='+UrlEncode(allt(str(all_pic.idno)))+'">Delete Img</A></td>'
		m.ImgText=m.ImgText+'<td><IMG SRC="/fpix/'+m.sidno+'_'+allt(all_pic.imgname)+'"></td></tr>'
	endscan
endif
if allt(m.ImgText)==""
		m.ImgText=m.ImgText+"No Images"
endif
m.ImgText=m.ImgText+'</table>'


select idno,providor,pmail,action,solution,sdescribe,stype,solid,solout from fsol ;
order by stype,solout desc ;
into cursor all_sol where idno=val(m.sidno)
if reccount()>0
   	 	M.ListTxt1 = '<TABLE borders=1 rules=all><TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.solid)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A><BR><FONT SIZE=-1>'+allt(all_sol.providor)+'</TD><TD><PRE>'+'Action: '+allt(all_sol.action)+'<BR>'+ ;
    	'Solution: '+allt(all_sol.solution)+'<BR>'+ ;
    	'Descript: '+allt(all_sol.sdescribe)+"<BR>"+ ;
    	ttoc(all_sol.solout)+" - "+str(all_sol.solid,5)+" </PRE>"+ ;
    	'<FONT SIZE=-1><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/addlink@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'&'+'solid='+UrlEncode(allt(str(all_sol.solid)))+'">Add Link</TD></TR>'
		select idno,link,linktxt from flink into cursor all_link where solid=all_sol.solid
		if reccount()>0
			select issue from fault into cursor one_f where idno=all_link.link
			m.fissue=one_f.issue
			sele all_link
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    		m.fissue+'</TD></TR>'
	   		skip
	   	 	scan rest
			select issue from fault into cursor one_f where idno=all_link.link
			m.fissue=one_f.issue
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    		m.fissue+'</TD></TR>'
    		sele all_link
    		endscan
		endif
		sele all_sol
   		skip
   	 	scan rest
   	 	M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.solid)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A><BR><FONT SIZE=-1>'+allt(all_sol.providor)+'</TD><TD><PRE>'+'Action: '+allt(all_sol.action)+'<BR>'+ ;
    	'Solution: '+allt(all_sol.solution)+'<BR>'+ ;
    	'Descript: '+allt(all_sol.sdescribe)+"<BR>"+ ;
    	ttoc(all_sol.solout)+" - "+str(all_sol.solid,5)+" </PRE>"+ ;
    	'<FONT SIZE=-1><A HREF="' + ;
  		UrlEncode(CGI.ExecutablePath+'/addlink@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'&'+'solid='+UrlEncode(allt(str(all_sol.solid)))+'">Add Link</TD></TR>'    	
		select idno,link,linktxt from flink into cursor all_link where solid=all_sol.solid
		if reccount()>0
			select issue from fault into cursor one_f where idno=all_link.link
				m.fissue=one_f.issue
				sele all_link
   	 			M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    			UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    			UrlEncode(allt(str(all_link.link))) ;
    			+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    			m.fissue+'</TD></TR>'
    		sele all_link
	   		skip
	   	 	scan rest
			select issue from fault into cursor one_f where idno=all_link.link
				m.fissue=one_f.issue
   	 			M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    			UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    			UrlEncode(allt(str(all_link.link))) ;
    			+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    			m.fissue+'</TD></TR>'
    		endscan
		endif
    	endscan
		M.ListTxt1=M.ListTxt1+"</TABLE>"
else
		M.ListTxt1 = "No solutions for this fault!"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'fault2' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return


proc f1j
parameter sidno
m.sidno=allt(formfield("sidno"))
m.cgiadd=allt(cgi.remoteaddress)
do case
	case substr(m.cgiadd,1,10)="192.168.9."
		update fault set acc_sum=acc_sum+1,accessed=accessed+1 where idno=val(m.sidno) 
	case substr(m.cgiadd,1,10)="192.168.1."
		update fault set acc_base=acc_base+1,accessed=accessed+1 where idno=val(m.sidno)
*	case substr(m.cgiadd,1,3)="127"
*		update fault set acc_base=acc_base+1,accessed=accessed+1 where idno=val(m.sidno)
	otherwise		 
		update fault set accessed=accessed+1 where idno=val(m.sidno)
endcase
select idno,reporter,repmail,section,cat,subcat,issuej,idescribej,datein,dateout,actionj, ;
solutionj,sdescribej,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_rep,to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super,log,logdate,fattrans,soltrans, ;
accessed,acc_base,acc_sum,opeaction,incharge,agrees,response,cause,scheduled from fault ;
where idno=val(m.sidno) into cursor f1
m.idno=str(f1.idno,4)
m.reporter=allt(f1.reporter)
m.repmail=allt(f1.repmail)
m.section=allt(f1.section)
m.cat=allt(f1.cat)
m.subcat=allt(f1.subcat)
m.issue=allt(f1.issuej)
*m.idescribe=allt(f1.idescribe)
m.idescribe='<TEXTAREA WRAP="physical" NAME="idescribe" rows="10" cols="42">'+allt(f1.idescribej)+'</TEXTAREA>'
m.tdatein=ttoc(f1.datein)
m.tdateout=ttoc(f1.dateout)
m.datein=allt(dtoc(ttod(f1.datein)))
m.timein=substr(ttoc(f1.datein),10,5)+substr(ttoc(f1.datein),19,2)
m.dateout=allt(dtoc(ttod(f1.dateout)))
m.timeout=substr(ttoc(f1.dateout),10,5)+substr(ttoc(f1.dateout),19,2)
m.action=allt(f1.actionj)
m.solution=allt(f1.solutionj)
m.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="10" cols="42">'+allt(f1.sdescribej)+'</TEXTAREA>'
*m.sdescribe=allt(f1.sdescribe)
m.priority=allt(f1.priority)
m.status=allt(f1.status)
m.sfinal=allt(f1.sfinal)
m.ass1=allt(f1.ass1)
m.ass1mail=allt(f1.ass1mail)
m.ass2=allt(f1.ass2)
m.ass2mail=allt(f1.ass2mail)
m.super=allt(f1.super)
m.supermail=allt(f1.supermail)
m.to_rep=allt(f1.to_rep)
m.to_ass1=f1.to_ass1
m.to_ass2=f1.to_ass2
m.to_super=f1.to_super
m.itype=allt(f1.itype)
m.keyin=allt(f1.keyin)
m.keyout=allt(f1.keyout)
m.s_ass1=dtoc(f1.s_ass1)
m.s_ass2=dtoc(f1.s_ass2)
m.s_super=dtoc(f1.s_super)
m.a_ass1=dtoc(f1.a_ass1)
m.a_ass2=dtoc(f1.a_ass2)
m.a_super=dtoc(f1.a_super)
m.r_ass1=dtoc(f1.r_ass1)
m.r_ass2=dtoc(f1.r_ass2)
m.r_super=dtoc(f1.r_super)
m.logdate=dtoc(f1.logdate)
m.log=allt(str(f1.log))
m.logdate='<A HREF="' + ;
	UrlEncode(CGI.ExecutablePath+'/logentry@'+CGI.ProgramPath+'elvis?date=')+ ;
    UrlEncode(m.logdate)+'">'+m.logdate+'</A><B>'
m.fattrans=ttoc(f1.fattrans)
m.soltrans=ttoc(f1.soltrans)
m.accessed=str(f1.accessed)
m.acc_base=str(f1.acc_base)
m.acc_sum=str(f1.acc_sum)
m.inout=str((f1.dateout-f1.datein)/3600,5,2)+" hours"
m.dinout=str((f1.dateout-f1.datein)/86400 ,5,2)+" days"
m.finout=str((f1.fattrans-f1.datein)/86400 ,5,2)+" days"
m.sinout=str((f1.soltrans-f1.dateout)/86400 ,5,2)+" days"
m.opeaction=allt(f1.opeaction)
m.incharge=allt(f1.incharge)
m.agrees=allt(f1.agrees)
m.response1=allt(f1.response)
m.cause=allt(f1.cause)
m.scheduled=allt(f1.scheduled)


select idno,providor,pmail,action,solution,sdescribe,stype,solid,solout from fsol ;
order by stype,solout desc ;
into cursor all_sol where idno=val(m.sidno)
if reccount()>0
   	 	M.ListTxt1 = '<TABLE borders=1 rules=all><TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.solid)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A><BR><FONT SIZE=-1>'+allt(all_sol.providor)+'</TD><TD>'+'Action: '+allt(all_sol.action)+'<BR>'+ ;
    	'Solution: '+allt(all_sol.solution)+'<BR>'+ ;
    	'Descript: '+allt(all_sol.sdescribe)+"<BR>"+ ;
    	ttoc(all_sol.solout)+" - "+str(all_sol.solid,5)+" "+ ;
    	'<FONT SIZE=-1><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/addlink@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'&'+'solid='+UrlEncode(allt(str(all_sol.solid)))+'">Add Link</TD></TR>'
		select idno,link,linktxt from flink into cursor all_link where solid=all_sol.solid
		if reccount()>0
			select issue from fault into cursor one_f where idno=all_link.link
			m.fissue=one_f.issue
			sele all_link
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    		m.fissue+'</TD></TR>'
	   		skip
	   	 	scan rest
			select issue from fault into cursor one_f where idno=all_link.link
			m.fissue=one_f.issue
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    		m.fissue+'</TD></TR>'
    		sele all_link
    		endscan
		endif
		sele all_sol
   		skip
   	 	scan rest
   	 	M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.solid)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A><BR><FONT SIZE=-1>'+allt(all_sol.providor)+'</TD><TD>'+'Action: '+allt(all_sol.action)+'<BR>'+ ;
    	'Solution: '+allt(all_sol.solution)+'<BR>'+ ;
    	'Descript: '+allt(all_sol.sdescribe)+"<BR>"+ ;
    	ttoc(all_sol.solout)+" - "+str(all_sol.solid,5)+" "+ ;
    	'<FONT SIZE=-1><A HREF="' + ;
  		UrlEncode(CGI.ExecutablePath+'/addlink@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'&'+'solid='+UrlEncode(allt(str(all_sol.solid)))+'">Add Link</TD></TR>'    	
		select idno,link,linktxt from flink into cursor all_link where solid=all_sol.solid
		if reccount()>0
			select issue from fault into cursor one_f where idno=all_link.link
				m.fissue=one_f.issue
				sele all_link
   	 			M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    			UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    			UrlEncode(allt(str(all_link.link))) ;
    			+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    			m.fissue+'</TD></TR>'
    		sele all_link
	   		skip
	   	 	scan rest
			select issue from fault into cursor one_f where idno=all_link.link
				m.fissue=one_f.issue
   	 			M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    			UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    			UrlEncode(allt(str(all_link.link))) ;
    			+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<BR>Fault: '+ ;
    			m.fissue+'</TD></TR>'
    		endscan
		endif
    	endscan
		M.ListTxt1=M.ListTxt1+"</TABLE>"
else
		M.ListTxt1 = "No solutions for this fault!"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'fault1j' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return



proc flist
m.inorder=allt(formfield("order"))
m.stated=allt(formfield("status"))
m.quser=allt(formfield("quser"))
m.qfilter=formfield("qfilter")
m.indetail=allt(formfield("detail"))
m.filter=allt(formfield("filt"))
m.hotpotato=formfield("hotpotato")
if m.inorder="idno"
	m.inorder="idno desc"
endif

M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
*select idno,reporter,issue,ass1,ass2,super,s_ass1,s_ass2,s_super,to_ass1, ;
*to_ass2,to_super,to_rep,status from fault into cursor all_hot ;
*where (ass1=m.cook and to_ass1="T" and status="Open") ;
*or (ass2=m.cook and to_ass2="T" and status="Open") ;
*or (super=m.cook and to_super="T" and status="Open") ;
*or (reporter=m.cook and to_rep="T" and status="Solved")
*m.hottext=""
*if reccount()>0
*	m.hottext="<BR>These are hot!<BR>"
*	scan
*	if reporter=m.cook and to_rep="T" and status="Solved"
*	m.hottext=m.hottext+'<A HREF="' + ;
*    	UrlEncode(CGI.ExecutablePath+'/clear_rep@'+CGI.ProgramPath+'fats?sidno=')+ ;
*    	UrlEncode(str(all_hot.idno))+'">'+str(all_hot.idno)+' - '+allt(all_hot.reporter)+' - '+ ;
*    	substr(allt(all_hot.issue),1,40)+' - '
*	else
*		m.hottext=m.hottext+'<A HREF="' + ;
*    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
*    	UrlEncode(str(all_hot.idno))+'">'+str(all_hot.idno)+' - '+allt(all_hot.reporter)+' - '+ ;
*    	substr(allt(all_hot.issue),1,40)+' - '
*    endif
*	do case
*		case all_hot.ass1=m.cook and all_hot.to_ass1="T"
*			m.hottext=m.hottext+"Assigned Due: "+dtoc(all_hot.s_ass1)
*		case all_hot.ass2=m.cook and all_hot.to_ass2="T"
*			m.hottext=m.hottext+"Assigned2 Due: "+dtoc(all_hot.s_ass2)
*		case all_hot.super=m.cook and all_hot.to_super="T"
*			m.hottext=m.hottext+"Supervisor Due: "+dtoc(all_hot.s_super)
*		case all_hot.reporter=m.cook and all_hot.to_rep="T"
*			m.hottext=m.hottext+"Your Trouble Solved!"
*	endcase
*	m.hottext=m.hottext+'</A><BR>'
*	endscan
*else
	m.hottext="<BR>Nothing Hot!<BR>"
*endif


mrep=""
mst=""
* do case
*	case m.quser="All"
*		mrep=""
*	case formfield("ACTION")="Reporter"
*		mrep=" where reporter='"+m.quser+"'"
*	case formfield("ACTION")="Assigned"
*		mrep=" where ass1='"+m.quser+"'"
* endcase

do case
	case m.hotpotato="Assigned2"
		mrep=" where ass2='"+m.quser+"'"
	case m.hotpotato="Assigned"
		mrep=" where ass1='"+m.quser+"'"
	case m.hotpotato="Reporter"
		mrep=" where reporter='"+m.quser+"'"
	case m.hotpotato="Supervisor"
		mrep=" where super='"+m.quser+"'"
	case m.hotpotato="All"
		mrep=""
endcase
if m.stated = "All" or len(allt(m.stated))=0
else
	if len(allt(mrep))=0
		mrep=mrep+" where status='"+m.stated+"'"
	else	
		mrep=mrep+" and status='"+m.stated+"'"
	endif
endif
*if len(allt(mrep))=0
*	mrep=" where ass1="+m.cook+"and status='Open'"
*endif
do case
	case substr(m.inorder,1,4)="idno"
		querystring=mrep+ " order by idno"
	case substr(m.inorder,1,7)="section"
		querystring=mrep+ " order by section,idno"
	case substr(m.inorder,1,3)="cat"
		querystring=mrep+ " order by cat,idno"
	case substr(m.inorder,1,6)="datein"
		querystring=mrep+ " order by datein desc"
	case substr(m.inorder,1,8)="reporter"
		querystring=mrep+ " order by reporter,datein"
	otherwise
		querystring=mrep+ " order by idno"
endcase
do case 
	case m.indetail = "Issue"
	case m.indetail = "Issue Describe"
	case m.indetail = "Solution"
endcase

m.hp='<SELECT NAME="hotpotato" size=1><OPTION VALUE="Assigned">Assigned<OPTION VALUE="Reporter"> ;
Reporter<OPTION VALUE="Assigned2">Assigned2<OPTION VALUE="Supervisor">Supervisor'


select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1, to_ass2,to_super,itype,keyin,keyout from fault  ;
into cursor all_faults &querystring

* querystring
if reccount()>0
   	 	M.ListTxt = '<TABLE>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B><A HREF="' + ;
   	UrlEncode(CGI.ExecutablePath+'/flist@'+CGI.ProgramPath+'fats?order=idno')+ ;
  		'"><B>ID No</B></A></TD>'
*   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>ID No</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Issue</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B><A HREF="' + ;
   	UrlEncode(CGI.ExecutablePath+'/flist@'+CGI.ProgramPath+'fats?order=reporter')+ ;
  		'">Reporter</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B><A HREF="' + ;
   	UrlEncode(CGI.ExecutablePath+'/flist@'+CGI.ProgramPath+'fats?order=datein')+ ;
  		'">DateIn</B></TD>'
*   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>DateOut</B></TD>'

    	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B><A HREF="' + ;
   	UrlEncode(CGI.ExecutablePath+'/flist@'+CGI.ProgramPath+'fats?order=section')+ ;
  		'"><B>Section</B></TD></TR>'
   	 	M.ListTxt = M.ListTxt+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD>'+allt(all_faults.issue)+'</TD> ;
    	<TD>'+allt(all_faults.reporter)+'</TD><TD>' ;
    	+dtoc(ttod(all_faults.datein))+'</TD><TD>'+allt(all_faults.section)+'</TD></TR>'
   		skip
   	 	scan rest
   	 	M.ListTxt = M.ListTxt+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD>'+allt(all_faults.issue)+'</TD> ;
    	<TD>'+allt(all_faults.reporter)+'</TD><TD>'+ ;
    	dtoc(ttod(all_faults.datein))+'</TD><TD>'+allt(all_faults.section)+'</TD></TR>'
    	endscan
		M.ListTxt=M.ListTxt+"</TABLE>"
else
		M.ListTxt = "No faults!"
endif
select user from users order by user into cursor all_users
if reccount()>0
	M.user='<SELECT NAME="quser" SIZE="1">'
*	if allt(all_users.user)=m.cook
*		M.user=M.user+'<OPTION VALUE="All">All'
*	else
*		M.user=M.user+'<OPTION SELECTED VALUE="All">All'
*	endif
	skip
	scan rest
	if allt(all_users.user)=m.cook
		M.user=M.user+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.user=M.user+'</SELECT>'
else
	M.user="No users"
endif
M.state='<SELECT NAME="status" SIZE="1"><OPTION SELECTED VALUE="Open">Open<OPTION VALUE="Solved">Solved ;
<OPTION VALUE="Hold">Hold<OPTION VALUE="Cancelled">Cancelled<OPTION VALUE="All">All'
M.detail='<SELECT NAME="detail" SIZE="1"><OPTION SELECTED VALUE="Issue">Issue ;
<OPTION VALUE="Issue Describe">Issue Describe<OPTION VALUE="Solution">Solution</SELECT>'
do iplock
if ipfail="T"
	SELECT form_text FROM html_frm WHERE form_id LIKE 'ipfail' INTO ARRAY FormTxt
	html_out = MergeTxt(M.FormTxt)

else
	SELECT form_text FROM html_frm WHERE form_id LIKE 'flist' INTO ARRAY FormTxt
	html_out = MergeTxt(M.FormTxt)
endif
return

proc unsolved
m.inorder=allt(formfield("order"))
m.stated=allt(formfield("status"))
m.quser=allt(formfield("quser"))
m.qfilter=formfield("qfilter")
m.indetail=allt(formfield("detail"))
m.filter=allt(formfield("filt"))
m.hotpotato=formfield("hotpotato")
if m.inorder="idno"
	m.inorder="idno desc"
endif

M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))

m.hottext="<B>UnSolved Only</B>"


mrep=""
mst=""
* do case
*	case m.quser="All"
*		mrep=""
*	case formfield("ACTION")="Reporter"
*		mrep=" where reporter='"+m.quser+"'"
*	case formfield("ACTION")="Assigned"
*		mrep=" where ass1='"+m.quser+"'"
* endcase

do case
	case m.hotpotato="Assigned2"
		mrep=" where ass2='"+m.quser+"'"
	case m.hotpotato="Assigned"
		mrep=" where ass1='"+m.quser+"'"
	case m.hotpotato="Reporter"
		mrep=" where reporter='"+m.quser+"'"
	case m.hotpotato="Supervisor"
		mrep=" where super='"+m.quser+"'"
	case m.hotpotato="All"
		mrep=""
endcase
if m.stated = "All" or len(allt(m.stated))=0
else
	if len(allt(mrep))=0
		mrep=mrep+" where status='"+m.stated+"'"
	else	
		mrep=mrep+" and status='"+m.stated+"'"
	endif
endif
*if len(allt(mrep))=0
*	mrep=" where ass1="+m.cook+"and status='Open'"
*endif
do case
	case substr(m.inorder,1,4)="idno"
		querystring=mrep+ " order by idno"
	case substr(m.inorder,1,7)="section"
		querystring=mrep+ " order by section,idno"
	case substr(m.inorder,1,3)="cat"
		querystring=mrep+ " order by cat,idno"
	otherwise
		querystring=mrep+ " order by idno"
endcase
do case 
	case m.indetail = "Issue"
	case m.indetail = "Issue Describe"
	case m.indetail = "Solution"
endcase

m.hp='<SELECT NAME="hotpotato" size=1><OPTION VALUE="Assigned">Assigned<OPTION VALUE="Reporter"> ;
Reporter<OPTION VALUE="Assigned2">Assigned2<OPTION VALUE="Supervisor">Supervisor'


select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1, to_ass2,to_super,itype,keyin,keyout,opeaction,incharge,agrees,response,cause,scheduled from fault  ;
where allt(status)="Open" into cursor all_faults &querystring

* querystring
if reccount()>0
   	 	M.ListTxt = '<TABLE rules=on border="2">'
   	 	M.ListTxt = M.ListTxt+'<TD></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B></B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>OPG</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>In</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>InChge</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Response</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Cause</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Action</B></TD></TR>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B><A HREF="' + ;
   	UrlEncode(CGI.ExecutablePath+'/flist@'+CGI.ProgramPath+'fats?order=idno')+ ;
  		'"><B>ID No</B></A></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Issue</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Action</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Charge</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Agrees</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Clear</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Clear</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Sched</B></TD></TR>'

   	 	M.ListTxt = M.ListTxt+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD>'+allt(all_faults.issue)+'</TD> ;
    	<TD>'+allt(all_faults.opeaction)+'</TD><TD>' ;
    	+allt(all_faults.incharge)+'</TD><TD>'+allt(all_faults.agrees)+'</TD><TD>'+ ;
    	allt(all_faults.response)+'</TD><TD>'+ ;
    	allt(all_faults.cause)+'</TD><TD>'+ ;
    	allt(all_faults.scheduled)+'</TD></TR>'
   		skip
   	 	scan rest
	   	 	M.ListTxt = M.ListTxt+'<TD><A HREF="' + ;
	    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
	    	UrlEncode(str(all_faults.idno))+'"><B>' ;
	    	+allt(str(all_faults.idno))+'</A></TD><TD>'+allt(all_faults.issue)+'</TD> ;
	    	<TD>'+allt(all_faults.opeaction)+'</TD><TD>' ;
	    	+allt(all_faults.incharge)+'</TD><TD>'+allt(all_faults.agrees)+'</TD><TD>'+ ;
	    	allt(all_faults.response)+'</TD><TD>'+ ;
	    	allt(all_faults.cause)+'</TD><TD>'+ ;
	    	allt(all_faults.scheduled)+'</TD></TR>'
       	endscan
		M.ListTxt=M.ListTxt+"</TABLE>"
else
		M.ListTxt = "No faults!"
endif
select user from users order by user into cursor all_users
if reccount()>0
	M.user='<SELECT NAME="quser" SIZE="1">'
*	if allt(all_users.user)=m.cook
*		M.user=M.user+'<OPTION VALUE="All">All'
*	else
*		M.user=M.user+'<OPTION SELECTED VALUE="All">All'
*	endif
	skip
	scan rest
	if allt(all_users.user)=m.cook
		M.user=M.user+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.user=M.user+'</SELECT>'
else
	M.user="No users"
endif
M.state='<SELECT NAME="status" SIZE="1"><OPTION SELECTED VALUE="Open">Open<OPTION VALUE="Solved">Solved ;
<OPTION VALUE="Hold">Hold<OPTION VALUE="Cancelled">Cancelled<OPTION VALUE="All">All'
M.detail='<SELECT NAME="detail" SIZE="1"><OPTION SELECTED VALUE="Issue">Issue ;
<OPTION VALUE="Issue Describe">Issue Describe<OPTION VALUE="Solution">Solution</SELECT>'
SELECT form_text FROM html_frm WHERE form_id LIKE 'flist2' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc openissue
m.inorder=allt(formfield("order"))
m.stated=allt(formfield("status"))
m.quser=allt(formfield("quser"))
m.qfilter=formfield("qfilter")
m.indetail=allt(formfield("detail"))
m.filter=allt(formfield("filt"))
m.hotpotato=formfield("hotpotato")
if m.inorder="idno"
	m.inorder="idno desc"
endif

M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))

m.hottext="<B>UnSolved Only</B>"


mrep=""
mst=""
* do case
*	case m.quser="All"
*		mrep=""
*	case formfield("ACTION")="Reporter"
*		mrep=" where reporter='"+m.quser+"'"
*	case formfield("ACTION")="Assigned"
*		mrep=" where ass1='"+m.quser+"'"
* endcase

do case
	case m.hotpotato="Assigned2"
		mrep=" where ass2='"+m.quser+"'"
	case m.hotpotato="Assigned"
		mrep=" where ass1='"+m.quser+"'"
	case m.hotpotato="Reporter"
		mrep=" where reporter='"+m.quser+"'"
	case m.hotpotato="Supervisor"
		mrep=" where super='"+m.quser+"'"
	case m.hotpotato="All"
		mrep=""
endcase
if m.stated = "All" or len(allt(m.stated))=0
else
	if len(allt(mrep))=0
		mrep=mrep+" where status='"+m.stated+"'"
	else	
		mrep=mrep+" and status='"+m.stated+"'"
	endif
endif
*if len(allt(mrep))=0
*	mrep=" where ass1="+m.cook+"and status='Open'"
*endif
do case
	case substr(m.inorder,1,4)="idno"
		querystring=mrep+ " order by idno"
	case substr(m.inorder,1,7)="section"
		querystring=mrep+ " order by section,idno"
	case substr(m.inorder,1,3)="cat"
		querystring=mrep+ " order by cat,idno"
	otherwise
		querystring=mrep+ " order by idno"
endcase
do case 
	case m.indetail = "Issue"
	case m.indetail = "Issue Describe"
	case m.indetail = "Solution"
endcase

m.hp='<SELECT NAME="hotpotato" size=1><OPTION VALUE="Assigned">Assigned<OPTION VALUE="Reporter"> ;
Reporter<OPTION VALUE="Assigned2">Assigned2<OPTION VALUE="Supervisor">Supervisor'


select idno,issue,idescribe, ;
solution,sdescribe,solutionj,sdescribej from fault  ;
where allt(status)="Open" into cursor all_faults &querystring

* querystring
if reccount()>0
   	 	M.ListTxt = '<TABLE rules=on border="2">'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>ID No</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Problem/Issue</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Solution Status J</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Solution Status</B></TD></TR>'

   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-2><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD><FONT SIZE=-2><B>'+allt(all_faults.issue)+'</B><BR>'+ ;
    	allt(all_faults.idescribe)+'</TD><TD><FONT SIZE=-2><B>' ;
    	+allt(all_faults.solutionj)+'</B><BR>'+allt(all_faults.sdescribej)+'</TD><TD><FONT SIZE=-2><B>'+ ;
    	allt(all_faults.solution)+'</B><BR>'+ ;
    	allt(all_faults.sdescribe)+'</TD></TR>'
   		skip
   	 	scan rest
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-2><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD><FONT SIZE=-2><B>'+allt(all_faults.issue)+'</B><BR>'+ ;
    	allt(all_faults.idescribe)+'</TD><TD><FONT SIZE=-2><B>' ;
    	+allt(all_faults.solutionj)+'</B><BR>'+allt(all_faults.sdescribej)+'</TD><TD><FONT SIZE=-2><B>'+ ;
    	allt(all_faults.solution)+'</B><BR>'+ ;
    	allt(all_faults.sdescribe)+'</TD></TR>'
      	endscan
		M.ListTxt=M.ListTxt+"</TABLE>"
else
		M.ListTxt = "No faults!"
endif
select user from users order by user into cursor all_users
if reccount()>0
	M.user='<SELECT NAME="quser" SIZE="1">'
*	if allt(all_users.user)=m.cook
*		M.user=M.user+'<OPTION VALUE="All">All'
*	else
*		M.user=M.user+'<OPTION SELECTED VALUE="All">All'
*	endif
	skip
	scan rest
	if allt(all_users.user)=m.cook
		M.user=M.user+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.user=M.user+'</SELECT>'
else
	M.user="No users"
endif
M.state='<SELECT NAME="status" SIZE="1"><OPTION SELECTED VALUE="Open">Open<OPTION VALUE="Solved">Solved ;
<OPTION VALUE="Hold">Hold<OPTION VALUE="Cancelled">Cancelled<OPTION VALUE="All">All'
M.detail='<SELECT NAME="detail" SIZE="1"><OPTION SELECTED VALUE="Issue">Issue ;
<OPTION VALUE="Issue Describe">Issue Describe<OPTION VALUE="Solution">Solution</SELECT>'
SELECT form_text FROM html_frm WHERE form_id LIKE 'flist2' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return



proc addfat
M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
*M.cook='twin'
set exact on
select number from counter where file="fats" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fats"
insert into fault (idno,datein,agrees,response,cause,scheduled) values (m.number,datetime(),"No","No","No","No")
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,solution,sdescribe,datein,action, ;
priority,status,itype,keyin,log,logdate,opeaction,incharge,agrees,response,cause,scheduled from fault ;
where idno=m.number into cursor f1
m.idno=str(f1.idno)
m.reporter=allt(f1.reporter)
m.repmail=allt(f1.repmail)
*m.section=allt(f1.section)
m.cat=allt(f1.cat)
m.subcat=allt(f1.subcat)
m.issue=allt(f1.issue)
m.idescribe='<TEXTAREA WRAP="physical" NAME="idescribe" rows="5" cols="75">'+allt(f1.idescribe)+'</TEXTAREA>'
m.solution=allt(f1.solution)
m.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="5" cols="75">'+allt(f1.sdescribe)+'</TEXTAREA>'
*m.id="Place description of fault here."
*m.idescribe='<TEXTAREA NAME="idescribe" rows="5" cols="75">'+allt(m.id)+'</TEXTAREA>'
*m.idescribe=f1.idescribe
m.datein=allt(ttoc(f1.datein))
m.action=allt(f1.action)
*m.priority=allt(f1.priority)
M.status='<SELECT NAME="status" SIZE="1"><OPTION VALUE="Open">Open<OPTION SELECTED VALUE="Solved">Solved ;
<OPTION VALUE="Hold">Hold<OPTION VALUE="Cancelled">Cancelled'
*m.itype=allt(f1.itype)
m.keyin=allt(f1.keyin)
m.log=allt(str(f1.log))
m.logdate=dtoc(f1.logdate)

m.opeaction=allt(f1.opeaction)
m.incharge=allt(f1.incharge)

m.agrees=allt(f1.agrees)
** agrees Y/N
m.sagrees='<SELECT NAME="sagrees" SIZE="1">'
m.sagrees=m.sagrees+'<OPTION VALUE="Yes">Yes'
m.sagrees=m.sagrees+'<OPTION SELECTED VALUE="No">No</SELECT>'

m.response1=allt(f1.response)
** response Y/N
m.sresponse='<SELECT NAME="sresponse" SIZE="1">'
m.sresponse=m.sresponse+'<OPTION VALUE="Yes">Yes'
m.sresponse=m.sresponse+'<OPTION SELECTED VALUE="No">No</SELECT>'

m.cause=allt(f1.cause)
** cause Y/N
m.scause='<SELECT NAME="scause" SIZE="1">'
m.scause=m.scause+'<OPTION VALUE="Yes">Yes'
m.scause=m.scause+'<OPTION SELECTED VALUE="No">No</SELECT>'

m.scheduled=allt(f1.scheduled)
** cause Y/N
m.sscheduled='<SELECT NAME="sscheduled" SIZE="1">'
m.sscheduled=m.sscheduled+'<OPTION VALUE="Yes">Yes'
m.sscheduled=m.sscheduled+'<OPTION SELECTED VALUE="No">No</SELECT>'

M.priority = '<SELECT NAME="priority" SIZE="1"><OPTION SELECTED VALUE="Low">Low<OPTION VALUE="Med"> ;
Med<OPTION VALUE="High">High</SELECT>'
M.itype = '<SELECT NAME="itype" SIZE="1"><OPTION SELECTED VALUE="Problem">Problem<OPTION VALUE="Error"> ;
Error<OPTION VALUE="Question">Question<OPTION VALUE="Issue">Issue<OPTION VALUE="Request">Request</SELECT>'
m.users=""
select user from users order by user into cursor all_users
if reccount()>0
	skip
	M.user='<SELECT NAME="reporter" SIZE="1">'
	if allt(all_users.user)=allt(m.cook)
		M.user=M.user+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	skip
	scan rest
	if allt(all_users.user)=allt(m.cook)
		M.user=M.user+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.user=M.user+'</SELECT>'
else
	M.user="No users"
endif
*M.user="No users"
select section,ass1,ass1mail from fcat order by section into cursor all_ass
if reccount()>0
	M.section='<SELECT NAME="section" SIZE="1">'
	M.section=M.section+'<OPTION SELECTED VALUE="'+allt(all_ass.section)+'">'+ ;
	allt(all_ass.section)+" - "+allt(all_ass.ass1)
	skip
	scan rest
	M.section=M.section+'<OPTION VALUE="'+allt(all_ass.section)+'">'+ ;
	allt(all_ass.section)+" - "+allt(all_ass.ass1)
	endscan
	M.section=M.section+'</SELECT>'
else
	M.section="No assigned users"
endif
*M.section="No assigned users"
SELECT form_text FROM html_frm WHERE form_id LIKE 'addfault' INTO ARRAY FormTxt
*SELECT form_text FROM html_frm WHERE form_id LIKE 'stntext' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc saveaddfat
m.idno=formfield("idno")
m.sidno=m.idno
m.reporter=formfield("reporter")
m.assigned=formfield("assigned")
m.repmail=formfield("repmail")
m.section=formfield("section")
m.cat=formfield("cat")
m.subcat=formfield("subcat")
m.issue=formfield("issue")
m.idescribe=formfield("idescribe")
m.solution=formfield("solution")
m.sdescribe=formfield("sdescribe")
m.datein=formfield("datein")
m.priority=formfield("priority")
m.status=formfield("status")
m.itype=formfield("itype")
m.keyin=formfield("keyin")

m.opeaction=formfield("opeaction")
m.incharge=formfield("incharge")
m.agrees=formfield("sagrees")
m.response1=formfield("sresponse")
m.cause=formfield("scause")
m.scheduled=formfield("sscheduled")

select ass1,ass1mail,ass2,ass2mail,super,supermail from fcat ;
into cursor one_ass where section=m.section
m.ass1=allt(one_ass.ass1)
m.ass1mail=allt(one_ass.ass1mail)
m.ass2=allt(one_ass.ass2)
m.ass2mail=allt(one_ass.ass2mail)
m.super=allt(one_ass.super)
m.supermail=allt(one_ass.supermail)
if m.status="Open"
	do case
 	case m.priority="Low"
 		m.to_ass1="T"
 		m.to_ass2="F"
 		m.to_super="F"
		m.a_ass1=date()
		m.a_ass2=date()+3
		m.a_super=date()+6
		m.s_ass1=date()+2
		m.s_ass2=date()+5
		m.s_super=date()+7
 	case m.priority="Med"
 		m.to_ass1="T"
 		m.to_ass2="F"
 		m.to_super="F"
		m.a_ass1=date()
		m.a_ass2=date()+1
		m.a_super=date()+2
		m.s_ass1=date()+1
		m.s_ass2=date()+3
		m.s_super=date()+3
	 case m.priority="Hi"
 		m.to_ass1="T"
 		m.to_ass2="T"
 		m.to_super="T"
		m.a_ass1=date()
		m.a_ass2=date()
		m.a_super=date()
		m.s_ass1=date()+1
		m.s_ass2=date()+1
		m.s_super=date()+1
	endcase
else
 		m.to_ass1="F"
 		m.to_ass2="F"
 		m.to_super="F"
		m.a_ass1=date()
		m.a_ass2=date()
		m.a_super=date()
		m.s_ass1=date()
		m.s_ass2=date()
		m.s_super=date()
		m.dateout=date()
		update fault set dateout=m.dateout where idno=val(m.idno)

endif
update fault set idno=val(m.idno),reporter=m.reporter,repmail=m.repmail,section=m.section, ;
cat=m.cat,subcat=m.subcat,issue=m.issue,idescribe=m.idescribe,solution=m.solution, ;
sdescribe=m.sdescribe,datein=ctot(m.datein), ;
priority=m.priority,status=m.status,itype=m.itype,keyin=m.keyin,ass1=allt(one_ass.ass1), ;
ass1mail=allt(one_ass.ass1mail),ass2=allt(one_ass.ass2), ass2mail=allt(one_ass.ass2mail), ;
super=allt(one_ass.super), supermail=allt(one_ass.supermail), ;
to_ass1=m.to_ass1, to_ass2=m.to_ass2, to_super=m.to_super, ;
a_ass1=m.a_ass1, a_ass2=m.a_ass2, a_super=m.a_super, ;
s_ass1=m.s_ass1, s_ass2=m.s_ass2, s_super=m.s_super, ;
opeaction=m.opeaction,incharge=m.incharge,agrees=m.agrees, ;
response=m.response1,cause=m.cause,scheduled=m.scheduled ;
where idno=val(m.idno)
do f1 with m.sidno

proc addsol
m.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
m.cookie=cgi.cookie
m.idno=formfield("idno")
m.sidno=m.idno
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super from fault ;
where idno=val(m.sidno) into cursor f1
m.issue=f1.issue
m.idescribe=f1.idescribe
m.datein=f1.datein
m.reporter=f1.reporter
m.repmail=f1.repmail
select user from users order by user into cursor all_users
if reccount()>0
	skip
	M.users='<SELECT NAME="users" SIZE="1">'
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	skip
	scan rest
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.users=M.users+'</SELECT>'
else
	M.users="No users"
endif
select number from counter where file="fsol" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fsol"
m.solid=m.number
m.action=""
m.solution=""
insert into fsol (idno,solid,providor) values (val(m.sidno),m.solid,m.reporter)
M.sdescribe='<TEXTAREA WRAP="physical"NAME="sdescribe" rows="15" cols="75">'+""+'</TEXTAREA>'
M.sttype='<SELECT NAME="stype" SIZE="1"><OPTION SELECTED VALUE="Solution">Solution ;
<OPTION VALUE="Possible">Possible<OPTION VALUE="Comment">Comment'
SELECT form_text FROM html_frm WHERE form_id LIKE 'addsol' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return


proc addcomm
m.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
m.cookie=cgi.cookie
m.idno=formfield("idno")
m.sidno=m.idno
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super from fault ;
where idno=val(m.sidno) into cursor f1
m.issue=f1.issue
m.idescribe=f1.idescribe
m.datein=f1.datein
m.reporter=f1.reporter
m.repmail=f1.repmail
select user from users order by user into cursor all_users
if reccount()>0
	skip
	M.users='<SELECT NAME="users" SIZE="1">'
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	skip
	scan rest
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.users=M.users+'</SELECT>'
else
	M.users="No users"
endif
select number from counter where file="fsol" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fsol"
m.solid=m.number
m.action=""
m.solution=""
insert into fsol (idno,solid,providor) values (val(m.sidno),m.solid,m.reporter)
M.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="15" cols="75">'+""+'</TEXTAREA>'
M.sttype='<SELECT NAME="stype" SIZE="1"><OPTION VALUE="Solution">Solution ;
<OPTION VALUE="Possible">Possible<OPTION SELECTED VALUE="Comment">Comment'
SELECT form_text FROM html_frm WHERE form_id LIKE 'addsol' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc addposs
m.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
m.cookie=cgi.cookie
m.idno=formfield("idno")
m.sidno=m.idno
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super from fault ;
where idno=val(m.sidno) into cursor f1
m.issue=f1.issue
m.idescribe=f1.idescribe
m.datein=f1.datein
m.reporter=f1.reporter
m.repmail=f1.repmail
select user from users order by user into cursor all_users
if reccount()>0
	skip
	M.users='<SELECT NAME="users" SIZE="1">'
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	skip
	scan rest
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.users=M.users+'</SELECT>'
else
	M.users="No users"
endif
select number from counter where file="fsol" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fsol"
m.solid=m.number
m.action=""
m.solution=""
insert into fsol (idno,solid,providor) values (val(m.sidno),m.solid,m.reporter)
M.sdescribe='<TEXTAREA WRAP="physical"NAME="sdescribe" rows="15" cols="75">'+""+'</TEXTAREA>'
M.sttype='<SELECT NAME="stype" SIZE="1"><OPTION VALUE="Solution">Solution ;
<OPTION SELECTED VALUE="Possible">Possible<OPTION VALUE="Comment">Comment'
SELECT form_text FROM html_frm WHERE form_id LIKE 'addsol' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc getsol
parameter idno
m.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
m.cookie=cgi.cookie
m.solid=allt(formfield("idno"))
select idno,providor from fsol where solid=val(m.solid) into cursor one_sol
m.sidno=one_sol.idno
m.idno=allt(str(one_sol.idno))
m.providor=allt(one_sol.providor)
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super from fault ;
where idno=m.sidno into cursor f1
m.issue=f1.issue
m.idescribe=f1.idescribe
m.datein=f1.datein
m.reporter=f1.reporter
m.repmail=f1.repmail
select user from users order by user into cursor all_users
if reccount()>0
	M.users='<SELECT NAME="users" SIZE="1">'
	scan
		if allt(m.providor)=allt(all_users.user)
			M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
		else
			M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
		endif
	endscan
	M.users=M.users+'</SELECT>'
else
	M.users="No users"
endif
select idno,solid,providor,action,solution,sdescribe,stype from fsol where solid=val(m.solid) ;
into cursor one_fsol
*m.solid=allt(one_fsol.solid)
m.action=allt(one_fsol.action)
m.solution=(one_fsol.solution)
m.stype=(one_fsol.stype)
M.sdescribe='<TEXTAREA WRAP="physical"NAME="sdescribe" rows="15" cols="75">'+ ;
allt(one_fsol.sdescribe)+'</TEXTAREA>'
m.sttype='<SELECT NAME="stype" SIZE="1">'
do case
	case m.stype="Solution"
		m.sttype=m.sttype+'<OPTION SELECTED VALUE="Solution">Solution'
		m.sttype=m.sttype+'<OPTION VALUE="Possible">Possible'
		m.sttype=m.sttype+'<OPTION VALUE="Comment">Comment'
	case m.stype="Possible"
		m.sttype=m.sttype+'<OPTION VALUE="Solution">Solution'
		m.sttype=m.sttype+'<OPTION SELECTED VALUE="Possible">Possible'
		m.sttype=m.sttype+'<OPTION VALUE="Comment">Comment'
	case m.stype="Comment"
		m.sttype=m.sttype+'<OPTION VALUE="Solution">Solution'
		m.sttype=m.sttype+'<OPTION VALUE="Possible">Possible'
		m.sttype=m.sttype+'<OPTION SELECTED VALUE="Comment">Comment'
endcase
m.sttype=m.sttype+'</SELECT>'
SELECT form_text FROM html_frm WHERE form_id LIKE 'addsol' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return



proc editfat
parameter sidno
m.sidno=allt(formfield("idno"))
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1,to_ass2,to_super,itype,keyin,keyout,log,logdate,issuej,idescribej,actionj,solutionj, ;
sdescribej,opeaction,incharge,agrees,response,cause,scheduled from fault ;
where idno=val(m.sidno) into cursor f1
m.idno=str(f1.idno,4)
m.reporter=allt(f1.reporter)
m.repmail=allt(f1.repmail)
m.sect=allt(f1.section)
m.cat=allt(f1.cat)
m.subcat=allt(f1.subcat)
m.issue=allt(f1.issue)
m.idescribe='<TEXTAREA WRAP="physical" NAME="idescribe" rows="5" cols="75">'+allt(f1.idescribe)+'</TEXTAREA>'
m.datein=allt(ttoc(f1.datein))
m.dateout=allt(ttoc(f1.dateout))
m.action=allt(f1.action)
m.solution=allt(f1.solution)
m.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="5" cols="75">'+f1.sdescribe+'</TEXTAREA>'
m.prior=allt(f1.priority)
m.st=allt(f1.status)
m.sfinal=allt(f1.sfinal)
m.ass1=allt(f1.ass1)
m.ass1mail=allt(f1.ass1mail)
m.ass2=allt(f1.ass2)
m.ass2mail=allt(f1.ass2mail)
m.super=allt(f1.super)
m.supermail=allt(f1.supermail)
m.to_ass1=f1.to_ass1
m.to_ass2=f1.to_ass2
m.to_super=f1.to_super
m.it=allt(f1.itype)
m.keyin=allt(f1.keyin)
m.keyout=allt(f1.keyout)
m.log=allt(str(f1.log))
m.logdate=dtoc(f1.logdate)
m.issuej=allt(f1.issuej)
m.idescribej='<TEXTAREA WRAP="physical" NAME="idescribej" rows="5" cols="75">'+allt(f1.idescribej)+'</TEXTAREA>'
m.actionj=allt(f1.actionj)
m.solutionj=allt(f1.solutionj)
m.sdescribej='<TEXTAREA WRAP="physical" NAME="sdescribej" rows="5" cols="75">'+allt(f1.sdescribej)+'</TEXTAREA>'

m.opeaction=allt(f1.opeaction)
m.incharge=allt(f1.incharge)

m.agrees=allt(f1.agrees)
** agrees Y/N
m.sagrees='<SELECT NAME="sagrees" SIZE="1">'
if m.agrees="Yes"
	m.sagrees=m.sagrees+'<OPTION SELECTED VALUE="Yes">Yes'
	m.sagrees=m.sagrees+'<OPTION VALUE="No">No</SELECT>'
else
	m.sagrees=m.sagrees+'<OPTION VALUE="Yes">Yes'
	m.sagrees=m.sagrees+'<OPTION SELECTED VALUE="No">No</SELECT>'
endif		

m.response1=allt(f1.response)
** response Y/N
m.sresponse='<SELECT NAME="sresponse" SIZE="1">'
if m.response1="Yes"
	m.sresponse=m.sresponse+'<OPTION SELECTED VALUE="Yes">Yes'
	m.sresponse=m.sresponse+'<OPTION VALUE="No">No</SELECT>'
else
	m.sresponse=m.sresponse+'<OPTION VALUE="Yes">Yes'
	m.sresponse=m.sresponse+'<OPTION SELECTED VALUE="No">No</SELECT>'
endif		

m.cause=allt(f1.cause)
** cause Y/N
m.scause='<SELECT NAME="scause" SIZE="1">'
if m.cause="Yes"
	m.scause=m.scause+'<OPTION SELECTED VALUE="Yes">Yes'
	m.scause=m.scause+'<OPTION VALUE="No">No</SELECT>'
else
	m.scause=m.scause+'<OPTION VALUE="Yes">Yes'
	m.scause=m.scause+'<OPTION SELECTED VALUE="No">No</SELECT>'
endif		

m.scheduled=allt(f1.scheduled)
** cause Y/N
m.sscheduled='<SELECT NAME="sscheduled" SIZE="1">'
if m.scheduled="Yes"
	m.sscheduled=m.sscheduled+'<OPTION SELECTED VALUE="Yes">Yes'
	m.sscheduled=m.sscheduled+'<OPTION VALUE="No">No</SELECT>'
else
	m.sscheduled=m.sscheduled+'<OPTION VALUE="Yes">Yes'
	m.sscheduled=m.sscheduled+'<OPTION SELECTED VALUE="No">No</SELECT>'
endif		

M.priority = '<SELECT NAME="priority" SIZE="1">'
	if m.prior="Low"
		M.priority=M.priority+'<OPTION SELECTED VALUE="Low">Low'
	else
		M.priority=M.priority+'<OPTION VALUE="Low">Low'
	endif
	if m.prior="Med"
		M.priority=M.priority+'<OPTION SELECTED VALUE="Med">Med'
	else
		M.priority=M.priority+'<OPTION VALUE="Med">Med'
	endif
	if m.prior="High"
		M.priority=M.priority+'<OPTION SELECTED VALUE="High">High'
	else
		M.priority=M.priority+'<OPTION VALUE="High">High'
	endif
	M.priority=M.priority+'</SELECT>'
M.itype = '<SELECT NAME="itype" SIZE="1">'
	if m.it="Problem"
		M.itype=M.itype+'<OPTION SELECTED VALUE="Problem">Problem'
	else
		M.itype=M.itype+'<OPTION VALUE="Problem">Problem'
	endif
	if m.it="Error"
		M.itype=M.itype+'<OPTION SELECTED VALUE="Error">Error'
	else
		M.itype=M.itype+'<OPTION VALUE="Error">Error'
	endif
	if m.it="Question"
		M.itype=M.itype+'<OPTION SELECTED VALUE="Question">Question'
	else
		M.itype=M.itype+'<OPTION VALUE="Question">Question'
	endif
	if m.it="Issue"
		M.itype=M.itype+'<OPTION SELECTED VALUE="Issue">Issue'
	else
		M.itype=M.itype+'<OPTION VALUE="Issue">Issue'
	endif
	if m.it="Request"
		M.itype=M.itype+'<OPTION SELECTED VALUE="Request">Request'
	else
		M.itype=M.itype+'<OPTION VALUE="Request">Request'
	endif
M.itype = M.itype+'</SELECT>'

M.status='<SELECT NAME="status" SIZE="1">'
	if m.st="Open"
		M.status=M.status+'<OPTION SELECTED VALUE="Open">Open'
	else
		M.status=M.status+'<OPTION VALUE="Open">Open'
	endif
	if m.st="Solved"
		M.status=M.status+'<OPTION SELECTED VALUE="Solved">Solved'
	else
		M.status=M.status+'<OPTION VALUE="Solved">Solved'
	endif
	if m.st="Hold"
		M.status=M.status+'<OPTION SELECTED VALUE="Hold">Hold'
	else
		M.status=M.status+'<OPTION VALUE="Hold">Hold'
	endif
	if m.st="Cancelled"
		M.status=M.status+'<OPTION SELECTED VALUE="Cancelled">Cancelled'
	else
		M.status=M.status+'<OPTION VALUE="Cancelled">Cancelled'
	endif
	M.status=M.status+'</SELECT>'


select idno,providor,pmail,action,solution,stype from fsol where idno=val(m.sidno) into cursor all_sol
if reccount()>0
   	 	M.ListTxt1 = '<TABLE><TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A></TD><TD>'+allt(all_sol.solution)+'</TD><TD>'+ ;
    	allt(all_sol.providor)+'</TD></TR>'
		select idno,solid,link,linktxt from flink into cursor all_link where idno=all_sol.idno
		if reccount()>0
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<B></TD></TR>'
	   		skip
	   	 	scan rest
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<B></TD></TR>'
    		endscan
		endif
		sele all_sol
   		skip
   	 	scan rest
   	 	M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/getsol@'+CGI.ProgramPath+'fats?idno=')+ ;
    	UrlEncode(allt(str(all_sol.idno)))+'"><B>' ;
    	+allt(all_sol.stype)+'</A></TD><TD>'+allt(all_sol.solution)+'</TD><TD>'+ ;
    	allt(all_sol.providor)+'</TD></TR>'
		select idno,solid,link,linktxt from flink into cursor all_link where idno=all_sol.idno
		if reccount()>0
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<B></TD></TR>'
	   		skip
	   	 	scan rest
   	 		M.ListTxt1 = M.ListTxt1+'<TD></TD><TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
    		UrlEncode(allt(str(all_link.link))) ;
    		+'">'+str(all_link.link)+'</A> - '+allt(all_link.linktxt)+'<B></TD></TR>'
    		endscan
		endif
    	endscan
		M.ListTxt1=M.ListTxt1+"</TABLE>"
else
		M.ListTxt1 = "No solutions for this fault!"
endif
select section,ass1,ass1mail from fcat order by section into cursor all_ass
if reccount()>0
	M.section='<SELECT NAME="section" SIZE="1">'
	scan
	if m.sect=allt(all_ass.section)
		M.section=M.section+'<OPTION SELECTED VALUE="'+allt(all_ass.section)+'">'+ ;
		allt(all_ass.section)
	else
		M.section=M.section+'<OPTION VALUE="'+allt(all_ass.section)+'">'+ ;
		allt(all_ass.section)
	endif
	endscan
	M.section=M.section+'</SELECT>'
else
	M.section="No assigned users"
endif


SELECT form_text FROM html_frm WHERE form_id LIKE 'editfat' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return


proc f2
parameter sidno
m.sidno=formfield("sidno")
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,stype,priority,status,sfinal,assigned,assmail,backup,bumail,supervisor,supmail, ;
to_assign, to_bu,to_sup,itype,keyin,keyout from fault ;
where idno=val(m.sidno) into cursor f1
m.idno=str(f1.idno,4)
m.reporter=allt(f1.reporter)
m.repmail=allt(f1.repmail)
m.section=allt(f1.section)
m.cat=allt(f1.cat)
m.subcat=allt(f1.subcat)
m.issue=allt(f1.issue)
m.idescribe=allt(f1.idescribe)
m.datein=allt(ttoc(f1.datein))
m.dateout=allt(ttoc(f1.dateout))
m.action=allt(f1.action)
m.solution=allt(f1.solution)
m.sdescribe=allt(f1.sdescribe)
m.stype=allt(f1.stype)
m.priority=allt(f1.priority)
m.status=allt(f1.status)
m.sfinal=allt(f1.sfinal)
m.assigned=allt(f1.assigned)
m.assmail=allt(f1.assmail)
m.backup=allt(f1.backup)
m.bumail=allt(f1.bumail)
m.supervisor=allt(f1.supervisor)
m.supmail=allt(f1.supmail)
m.to_assign=f1.to_assign
m.to_bu=f1.to_bu
m.to_sup=f1.to_sup
m.itype=allt(f1.itype)
m.keyin=allt(f1.keyin)
m.keyout=allt(f1.keyout)
SELECT form_text FROM html_frm WHERE form_id LIKE 'addsol' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc savesol
m.idno=formfield("idno")
m.solid=formfield("solid")
m.action=formfield("action")
m.solution=formfield("solution")
m.sdescribe=formfield("sdescribe")
m.stype=formfield("stype")
m.users=formfield("users")
*m.keyout=formfield("keyout")
select ass1,ass2,super from fault into cursor one_f1 where idno=val(m.idno)
m.ass1=one_f1.ass1
m.ass2=one_f1.ass2
m.super=one_f1.super
if allt(m.users)=allt(m.ass1) 
	update fault set r_ass1=date() where idno=val(m.idno)
endif
if allt(m.users)=allt(m.ass2)
	update fault set r_ass2=date() where idno=val(m.idno)
endif
if allt(m.users)=allt(m.super)
	update fault set r_super=date() where idno=val(m.idno)
endif
if val(m.solid)>0
	update fsol set action=m.action,solution=m.solution,sdescribe=m.sdescribe, ;
	stype=m.stype,providor=m.users,solout=datetime() where solid=val(m.solid)
endif
if m.stype="Solution"
	update fault set action=m.action, solution=m.solution,sdescribe=m.sdescribe,status="Solved", ;
	dateout=datetime(),to_rep="T",to_ass1="F",to_ass2="F",to_super="F" where idno=val(m.idno)
endif
do f1 with m.idno

proc addlink2
m.idno=formfield("idno")
m.solid=formfield("tsolid")
m.link="0"
m.linktxt=""
select idno,reporter,issue,idescribe from fault into cursor all_links
if reccount()>0
		M.ListTxt1 = "<TABLE cellpadding=2 spacing=2><TH align='left'>IDNo</TH> ;
		<TH align='left'>Reporter</TH><TH align='left'>Issue</TH>"+ ;
		"<TH align='left'>Description</TH></TR>"
		M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/savelink@'+CGI.ProgramPath+'fats?link=')+ ;
    		UrlEncode(allt(str(all_links.idno)))+'&'+'idno='+UrlEncode(m.idno)+ ;
    		'&'+'solid='+UrlEncode(m.solid)+ ;
    		'">'+allt(str(all_links.idno))+'</A></TD><TD>'+allt(all_links.reporter)+'</TD><TD>'+ ;
    		allt(all_links.issue)+'</TD><TD>'+allt(all_links.idescribe)+'</TD></TR>'
	   	skip
	   	scan rest
		M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/savelink@'+CGI.ProgramPath+'fats?link=')+ ;
    		UrlEncode(allt(str(all_links.idno)))+'&'+'idno='+UrlEncode(m.idno)+ ;
    		'&'+'solid='+UrlEncode(m.solid)+ ;
    		'">'+allt(str(all_links.idno))+'</A></TD><TD>'+allt(all_links.reporter)+'</TD><TD>'+ ;
    		allt(all_links.issue)+'</TD><TD>'+allt(all_links.idescribe)+'</TD></TR>'
    	endscan
		M.ListTxt1 = M.ListTxt1+"</TABLE>"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'addlink' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc addlink
m.idno=formfield("idno")
m.solid=formfield("solid")
m.link="0"
m.linktxt=""
select idno,reporter,issue,idescribe from fault into cursor all_links
if reccount()>0
		M.ListTxt1 = "<SELECT NAME='linkno' SIZE=30>"
		M.ListTxt1 = M.ListTxt1+'<OPTION SELECTED VALUE="'+allt(str(all_links.idno))+'">'+ ;
		allt(str(all_links.idno))+" "+allt(all_links.issue)
	   	skip
	   	scan rest
		M.ListTxt1 = M.ListTxt1+'<OPTION SELECTED VALUE="'+allt(str(all_links.idno))+'">'+ ;
		allt(str(all_links.idno))+" "+allt(all_links.issue)
    	endscan
		M.ListTxt1 = M.ListTxt1+"</SELECT>"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'addlink' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return


proc savelink
m.idno=formfield("sidno")
m.oldid=m.idno
m.solid=formfield("solid")
m.link=formfield("linkno")
m.linktxt=formfield("linktxt")
insert into flink (idno,solid,link,linktxt) values (val(m.idno),val(m.solid), ;
val(m.link),m.linktxt)
do f1 with m.oldid
return

proc fcatlist
select section,ass1,ass1mail,ass2,ass2mail,super,supermail from fcat order by section into cursor all_fcat
if reccount()>0
*		M.ListTxt1 = "<TABLE cellpadding=2 spacing=2><TH align='left'>Section</TH> ;
*		<TH align='left'>Assign 1</TH><TH align='left'>Assign 1 Mail</TH> ;
*		<TH align='left'>Assign 2</TH><TH align='left'>Assign 2 Mail</TH>"+ ;
*		"<TH align='left'>Supervisor</TH><TH align='left'>Super Mail</TH></TR>"
		M.ListTxt1 = "<TABLE cellpadding=2 spacing=2><TH align='left'>Section</TH></TR>"
		M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/fcatedit@'+CGI.ProgramPath+'fats?section=')+ ;
    		UrlEncode(allt(all_fcat.section))+'">'+allt(all_fcat.section)+'</A></TD></TR>'
	   	skip
	   	scan rest
   	 	M.ListTxt1 = M.ListTxt1+'<TD><A HREF="' + ;
    		UrlEncode(CGI.ExecutablePath+'/fcatedit@'+CGI.ProgramPath+'fats?section=')+ ;
    		UrlEncode(allt(all_fcat.section))+'">'+allt(all_fcat.section)+'</A></TD></TR>'

    	endscan
		M.ListTxt1 = M.ListTxt1+"</TABLE>"
endif
SELECT form_text FROM html_frm WHERE form_id LIKE 'fcatlist' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fcatedit
parameter section
m.section=allt(formfield("section"))
select section,ass1,ass1mail,ass2,ass2mail,super,supermail from fcat into cursor one_fcat ;
where section=m.section
m.sectionedit=m.section
m.ass1=allt(one_fcat.ass1)
m.ass1mail=allt(one_fcat.ass1mail)
m.ass2=allt(one_fcat.ass2)
m.ass2mail=allt(one_fcat.ass2mail)
m.super=allt(one_fcat.super)
m.supermail=allt(one_fcat.supermail)

select user from users order by user into cursor all_nass1
if reccount()>0
	M.nass1='<SELECT NAME="ass1" SIZE="1">'
	if all_nass1.user=m.ass1
		M.nass1=M.nass1+'<OPTION SELECTED VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	else
		M.nass1=M.nass1+'<OPTION VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	endif
	skip
	scan rest
	if all_nass1.user=m.ass1
		M.nass1=M.nass1+'<OPTION SELECTED VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	else
		M.nass1=M.nass1+'<OPTION VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	endif
	endscan
	M.nass1=M.nass1+'</SELECT>'
else
	M.nass1="No users"
endif
select user from users order by user into cursor all_nass2
if reccount()>0
	M.nass2='<SELECT NAME="ass2" SIZE="1">'
	if all_nass2.user=m.ass2
		M.nass2=M.nass2+'<OPTION SELECTED VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	else
		M.nass2=M.nass2+'<OPTION VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	endif
	skip
	scan rest
	if all_nass2.user=m.ass2
		M.nass2=M.nass2+'<OPTION SELECTED VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	else
		M.nass2=M.nass2+'<OPTION VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	endif
	endscan
	M.nass2=M.nass2+'</SELECT>'
else
	M.nass2="No users"
endif
select user from users order by user into cursor all_nsuper
if reccount()>0
	M.nsuper='<SELECT NAME="super" SIZE="1">'
	if all_nsuper.user=m.super
		M.nsuper=M.nsuper+'<OPTION SELECTED VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	else
		M.nsuper=M.nsuper+'<OPTION VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	endif
	skip
	scan rest
	if all_nsuper.user=m.super
		M.nsuper=M.nsuper+'<OPTION SELECTED VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	else
		M.nsuper=M.nsuper+'<OPTION VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	endif
	endscan
	M.nsuper=M.nsuper+'</SELECT>'
else
	M.nsuper="No users"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'fcatedit' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fcatsave
m.section=formfield("section")
m.sectionedit=formfield("sectionedit")
*m.ass1=formfield("ass1")
*m.ass2=formfield("ass2")
*m.super=formfield("super")
update fcat set section=m.sectionedit where section=m.section
do fcatlist

proc fcatadd
insert into fcat (section) values ("NewSection")
select section,ass1,ass1mail,ass2,ass2mail,super,supermail from fcat into cursor one_fcat ;
where section="NewSection"
m.section=allt(one_fcat.section)
m.sectionedit=m.section
m.ass1=allt(one_fcat.ass1)
m.ass1mail=allt(one_fcat.ass1mail)
m.ass2=allt(one_fcat.ass2)
m.ass2mail=allt(one_fcat.ass2mail)
m.super=allt(one_fcat.super)
m.supermail=allt(one_fcat.supermail)

select user from users order by user into cursor all_nass1
if reccount()>0
	M.nass1='<SELECT NAME="ass1" SIZE="1">'
	if all_nass1.user=m.ass1
		M.nass1=M.nass1+'<OPTION SELECTED VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	else
		M.nass1=M.nass1+'<OPTION VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	endif
	skip
	scan rest
	if all_nass1.user=m.ass1
		M.nass1=M.nass1+'<OPTION SELECTED VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	else
		M.nass1=M.nass1+'<OPTION VALUE="'+allt(all_nass1.user)+'">'+allt(all_nass1.user)
	endif
	endscan
	M.nass1=M.nass1+'</SELECT>'
else
	M.nass1="No users"
endif
select user from users order by user into cursor all_nass2
if reccount()>0
	M.nass2='<SELECT NAME="ass2" SIZE="1">'
	if all_nass2.user=m.ass2
		M.nass2=M.nass2+'<OPTION SELECTED VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	else
		M.nass2=M.nass2+'<OPTION VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	endif
	skip
	scan rest
	if all_nass2.user=m.ass2
		M.nass2=M.nass2+'<OPTION SELECTED VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	else
		M.nass2=M.nass2+'<OPTION VALUE="'+allt(all_nass2.user)+'">'+allt(all_nass2.user)
	endif
	endscan
	M.nass2=M.nass2+'</SELECT>'
else
	M.nass2="No users"
endif
select user from users order by user into cursor all_nsuper
if reccount()>0
	M.nsuper='<SELECT NAME="super" SIZE="1">'
	if all_nsuper.user=m.super
		M.nsuper=M.nsuper+'<OPTION SELECTED VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	else
		M.nsuper=M.nsuper+'<OPTION VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	endif
	skip
	scan rest
	if all_nsuper.user=m.super
		M.nsuper=M.nsuper+'<OPTION SELECTED VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	else
		M.nsuper=M.nsuper+'<OPTION VALUE="'+allt(all_nsuper.user)+'">'+allt(all_nsuper.user)
	endif
	endscan
	M.nsuper=M.nsuper+'</SELECT>'
else
	M.nsuper="No users"
endif

SELECT form_text FROM html_frm WHERE form_id LIKE 'fcatedit' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc addcook
m.names=formfield("quser")
m.quser=m.names
*M.cook=SUBSTR(cgi.cookie, AT('number=', CGI.Cookie)+7)
M.cook=allt(cgi.cookie)
SELECT form_text FROM html_frm WHERE form_id LIKE 'addcook' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc pickname
quser=""
select user from users order by user into cursor all_users
if reccount()>0
	M.user='<SELECT NAME="quser" SIZE="1">'
	M.user=M.user+'<OPTION SELECTED VALUE="All">All'
	skip
	scan rest
	M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endscan
	M.user=M.user+'</SELECT>'
else
	M.user="No users"
endif
SELECT form_text FROM html_frm WHERE form_id LIKE 'pickname' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fsearch
m.qstring=""
m.listtxt=""
m.searchtxt=""
m.searchtxt2=""
mstr=""
m.soptions="<SELECT NAME='soptions' SIZE='1'><OPTION SELECTED VALUE='Both'>Both"
m.soptions=m.soptions+"<OPTION VALUE='Issue'>Issue"
m.soptions=m.soptions+"<OPTION VALUE='Solution'>Solution"
m.doptions="<SELECT NAME='doptions' SIZE='1'>"
m.doptions=m.doptions+"<OPTION VALUE='Word'>Word"
m.doptions=m.doptions+"<OPTION VALUE='String' selected>String"
m.doptions=m.doptions+"</SELECT>"
select section,ass1,ass1mail from fcat order by section into cursor all_ass
M.section=''
if reccount()>0
	M.section='<SELECT NAME="section" SIZE="1"><OPTION value="None">None'
	scan
		M.section=M.section+'<OPTION VALUE="'+allt(all_ass.section)+'">'+ ;
		allt(all_ass.section)
	endscan
	M.section=M.section+'</SELECT>'
endif
do iplock
if ipfail="T"
	SELECT form_text FROM html_frm WHERE form_id LIKE 'ipfail' INTO ARRAY FormTxt
	html_out = MergeTxt(M.FormTxt)

else
	SELECT form_text FROM html_frm WHERE form_id LIKE 'fsearch' INTO ARRAY FormTxt
	html_out = MergeTxt(M.FormTxt)
endif
return

proc dosearch
m.searchtxt=allt(formfield("searchtxt"))
m.searchtxt2=allt(formfield("searchtxt2"))
m.section_in=allt(formfield("section"))
m.ooptions=formfield("soptions")
m.dateoptions=formfield("doptions")
m.soptions="<SELECT NAME='soptions' SIZE='1'>"
mstr=""
if m.dateoptions="Word"
		m.searchtxt=m.searchtxt+" "
		m.searchtxt2=m.searchtxt2+" "
endif
m.doptions="<SELECT NAME='doptions' SIZE='1'>"
if m.dateoptions=="Word"
	m.doptions=m.doptions+"<OPTION SELECTED VALUE='Word'>Word"
else
	m.doptions=m.doptions+"<OPTION VALUE='Word'>Word"
endif
if m.dateoptions=="String"
	m.doptions=m.doptions+"<OPTION SELECTED VALUE='String'>String"
else
	m.doptions=m.doptions+"<OPTION VALUE='String'>String"
endif
m.doptions=m.doptions+"</SELECT>"
if len(allt(m.searchtxt2))>0
	m.searchtype='search with 2'
	if allt(m.section_in)=='None'
		select idno,issue,idescribe,action,solution,sdescribe,datein,section ;
		from fault where (upper(m.searchtxt) $ upper(issue) and upper(m.searchtxt2) $ upper(issue)) or ;
		(upper(m.searchtxt) $ upper(idescribe) and upper(m.searchtxt2) $ upper(idescribe)) or ;
		(upper(m.searchtxt) $ upper(keyin) and upper(m.searchtxt2) $ upper(keyin)) or ;
		(upper(m.searchtxt) $ upper(keyout) and upper(m.searchtxt2) $ upper(keyout)) or ;
		(upper(m.searchtxt) $ upper(solution) and upper(m.searchtxt2) $ upper(solution)) or ;
		(upper(m.searchtxt) $ upper(sdescribe) and upper(m.searchtxt2) $ upper(solution)) order by idno desc into cursor all_fats
	else
		select idno,issue,idescribe,action,solution,sdescribe,datein,section ;
		from fault where allt(section)==m.section_in and ((upper(m.searchtxt) $ upper(issue) and upper(m.searchtxt2) $ upper(issue)) or ;
		(upper(m.searchtxt) $ upper(idescribe) and upper(m.searchtxt2) $ upper(idescribe)) or ;
		(upper(m.searchtxt) $ upper(keyin) and upper(m.searchtxt2) $ upper(keyin)) or ;
		(upper(m.searchtxt) $ upper(keyout) and upper(m.searchtxt2) $ upper(keyout)) or ;
		(upper(m.searchtxt) $ upper(solution) and upper(m.searchtxt2) $ upper(solution)) or ;
		(upper(m.searchtxt) $ upper(sdescribe) and upper(m.searchtxt2) $ upper(solution))) ;
		 order by idno desc into cursor all_fats
	endif
	if reccount()>0
			M.ListTxt="<TABLE border=2 rules=2 cellpadding=2 cellspacing=2><TD>IDNo</TD> ;
			<TD align='center'>Section</TD><TD align='left'>Fault</TD><TD align='left'>Solution</TD></TR>"
	   	 	scan
	   	 		M.ListTxt = M.ListTxt+'<tr><TD><A HREF="' + ;
	    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
	    		UrlEncode(allt(str(all_fats.idno))) ;
	    		+'">'+str(all_fats.idno)+'</A></TD><TD align=left><FONT FACE=Arial, Helvetica Size=2>'+allt(all_fats.section)+'</TD><TD><FONT SIZE=-1><B>Fault:</B> '+allt(all_fats.issue)+ ;
	    		'<BR><FONT SIZE=-1><B>Describe: </B>'+substr(allt(all_fats.idescribe),1,50)+ ;
	    		'<BR><FONT SIZE=-1><B>Date: </B>'+dtoc(all_fats.datein)+'</TD><TD><FONT SIZE=-1><B>Solution:</B> '+ ;
	    		+allt(all_fats.solution)+'<BR><B>Describe:</B> '+substr(allt(all_fats.sdescribe),1,50)+ ;
	    		'<BR><FONT SIZE=-1><B>Action:</B> '+allt(all_fats.action)+ ;
	    		'</TD></TR>'
    		endscan
			M.ListTxt=M.ListTxt+"</TABLE>"
	else
		M.ListTxt="No faults meet this search criteria!"
	endif
else
	if len(allt(m.searchtxt))==0

		m.searchtype='search with 0'
		select idno,issue,idescribe,action,solution,sdescribe,datein,section ;
		from fault where allt(section)==m.section_in order by idno desc into cursor all_fats
		
	else
	
		m.searchtype='search with 1'
		if allt(m.section_in)=='None'
			select idno,issue,idescribe,action,solution,sdescribe,datein,section ;
			from fault where (((val(m.searchtxt) = idno) or ;
			(upper(m.searchtxt) $ upper(issue)) or ;
			(upper(m.searchtxt) $ upper(idescribe))) or ;
			((upper(m.searchtxt) $ upper(keyin)) or ;
			(upper(m.searchtxt) $ upper(keyout))) or ;
			((upper(m.searchtxt) $ upper(solution)) or ;
			(upper(m.searchtxt) $ upper(sdescribe))))  order by idno desc into cursor all_fats
		else
			select idno,issue,idescribe,action,solution,sdescribe,datein,section ;
			from fault where (((val(m.searchtxt) = idno) or ;
			(upper(m.searchtxt) $ upper(issue)) or ;
			(upper(m.searchtxt) $ upper(idescribe))) or ;
			((upper(m.searchtxt) $ upper(keyin)) or ;
			(upper(m.searchtxt) $ upper(keyout))) or ;
			((upper(m.searchtxt) $ upper(solution)) or ;
			(upper(m.searchtxt) $ upper(sdescribe)))) and ;
			allt(section)==m.section_in order by idno desc into cursor all_fats
		endif

	endif
	if reccount()>0
			M.ListTxt="<TABLE border=2 rules=2 cellpadding=2 cellspacing=2><TD>IDNo</TD> ;
			<TD align='center'>Section</TD><TD align='left'>Fault</TD><TD align='left'>Solution</TD></TR>"
	   	 	scan
	   	 		M.ListTxt = M.ListTxt+'<tr><TD><A HREF="' + ;
	    		UrlEncode(CGI.ExecutablePath+'/f1@'+CGI.ProgramPath+'fats?sidno=')+ ;
	    		UrlEncode(allt(str(all_fats.idno))) ;
	    		+'">'+str(all_fats.idno)+'</A></TD><td align=center><FONT FACE=Arial, Helvetica Size=2>'+allt(all_fats.section)+'</TD><TD><FONT SIZE=-1><B>Fault:</B> '+allt(all_fats.issue)+ ;
	    		'<BR><FONT SIZE=-1><B>Describe: </B>'+substr(allt(all_fats.idescribe),1,50)+ ;
	    		'<BR><FONT SIZE=-1><B>Date: </B>'+dtoc(all_fats.datein)+'</TD><TD><FONT SIZE=-1><B>Solution:</B> '+ ;
	    		+allt(all_fats.solution)+'<BR><B>Describe:</B> '+substr(allt(all_fats.sdescribe),1,50)+ ;
	    		'<BR><FONT SIZE=-1><B>Action:</B> '+allt(all_fats.action)+ ;
	    		'</TD></TR>'
    		endscan
				M.ListTxt=M.ListTxt+"</TABLE>"
	else
		M.ListTxt="No faults meet this search criteria!"
	endif

endif
select section,ass1,ass1mail from fcat order by section into cursor all_ass
if reccount()>0
	M.section='<SELECT NAME="section" SIZE="1"><OPTION value="None">None'
	scan
		if allt(all_ass.section)==m.section_in
			M.section=M.section+'<OPTION VALUE="'+allt(all_ass.section)+'" selected>'+ ;
			allt(all_ass.section)
		else
			M.section=M.section+'<OPTION VALUE="'+allt(all_ass.section)+'">'+ ;
			allt(all_ass.section)
		endif
		
	endscan
	M.section=M.section+'</SELECT>'
endif

m.qstring="type: "+m.searchtype+" text 1. "+m.searchtxt+' 2: '+m.searchtxt2+", fields = "+m.ooptions+", dates ="+mstr
SELECT form_text FROM html_frm WHERE form_id LIKE 'fsearch' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fstart
M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
do iplock
if ipfail="T"
	SELECT form_text FROM html_frm WHERE form_id LIKE 'ipfail' INTO ARRAY FormTxt
	html_out = MergeTxt(M.FormTxt)

else
	SELECT form_text FROM html_frm WHERE form_id LIKE 'fstart' INTO ARRAY FormTxt
	html_out = MergeTxt(M.FormTxt)
endif
return

proc fusermail
M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
select user,email,mailnew,mailod,mailsum,forward from users order by user into cursor all_users
if reccount()>0
	M.user='<SELECT NAME="fusermail" SIZE="10">'
	skip
	scan rest
	M.user=M.user+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)+ ;
	" "+allt(all_users.email)+" "+allt(all_users.mailnew)+" "+allt(all_users.mailod)+ ;
	" "+allt(all_users.mailsum)+" "+allt(all_users.forward)
	endscan
	M.user=M.user+'</SELECT>'
else
	M.user="No users"
endif
SELECT form_text FROM html_frm WHERE form_id LIKE 'fusermail' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return
	
proc editmail
M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
m.user=formfield("fusermail")
select user,email,mailnew,mailod,mailsum,forward from users into cursor all_users where user=m.user
m.username=all_users.user
m.usermail=all_users.email
m.usernew=all_users.mailnew
m.userod=all_users.mailod
m.usersum=all_users.mailsum
m.forward=all_users.forward
SELECT form_text FROM html_frm WHERE form_id LIKE 'editmail' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc savemail
m.username=formfield("username")
m.usermail=formfield("usermail")
m.mailn=formfield("mailn")
m.mailo=formfield("mailo")
m.mails=formfield("mails")
m.forward=formfield("forward")
*m.mailn="T"
*m.mailo="F"
*m.mails="G"
update users set email=m.usermail,mailnew=m.mailn,mailod=m.mailo,mailsum=m.mails, ;
forward=m.forward where user=m.username
do fstart
return

proc escalate
m.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
m.cookie=cgi.cookie
m.idno=formfield("idno")
m.sidno=m.idno
select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,sdescribe,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1,to_ass2,to_super,itype,keyin,keyout,s_ass1,s_ass2,s_super, ;
a_ass1,a_ass2,a_super,r_ass1,r_ass2,r_super from fault ;
where idno=val(m.sidno) into cursor f1
m.issue=f1.issue
m.idescribe=f1.idescribe
m.datein=f1.datein
m.reporter=f1.reporter
m.repmail=f1.repmail
select user from users order by user into cursor all_users
if reccount()>0
	skip
	M.users='<SELECT NAME="users" SIZE="1">'
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	skip
	scan rest
	if allt(all_users.user)=allt(m.cook)
		M.users=M.users+'<OPTION SELECTED VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	else
		M.users=M.users+'<OPTION VALUE="'+allt(all_users.user)+'">'+allt(all_users.user)
	endif
	endscan
	M.users=M.users+'</SELECT>'
else
	M.users="No users"
endif
select number from counter where file="fsol" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fsol"
m.solid=m.number
m.action=""
m.solution=""
M.sdescribe='<TEXTAREA WRAP="physical" NAME="sdescribe" rows="15" cols="75">'+""+'</TEXTAREA>'
M.stype='<SELECT NAME="stype" SIZE="1"><OPTION SELECTED VALUE="Solution">Solution ;
<OPTION VALUE="Possible">Possible<OPTION VALUE="Comment">Comment'
SELECT form_text FROM html_frm WHERE form_id LIKE 'escalate' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc saveesc
m.idno=formfield("idno")
m.solid=formfield("solid")
m.action=formfield("action")
m.solution=formfield("solution")
m.sdescribe=formfield("sdescribe")
m.stype=formfield("stype")
m.users=formfield("users")
*m.keyout=formfield("keyout")
select ass1,ass2,super from fault into cursor one_f1 where idno=val(m.idno)
m.ass1=one_f1.ass1
m.ass2=one_f1.ass2
m.super=one_f1.super
if allt(m.users)=allt(m.ass1) 
	update fault set r_ass1=date() where idno=val(m.idno)
endif
if allt(m.users)=allt(m.ass2)
	update fault set r_ass2=date() where idno=val(m.idno)
endif
if allt(m.users)=allt(m.super)
	update fault set r_super=date() where idno=val(m.idno)
endif

*create new fault
select number from counter where file="fats" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fats"
insert into fault (idno,datein) values (m.number,datetime())
m.newfault=m.number


* create old solution
insert into fsol (idno,solid,action,solution,sdescribe,stype,providor,solout) values (val(m.idno), ;
val(m.solid),m.action,m.solution,m.sdescribe,m.stype,m.users,datetime())

* close old fault
if m.stype="Solution"
	update fault set action=m.action, solution=m.solution,sdescribe=m.sdescribe,status="Solved", ;
	dateout=date(),to_rep="T",to_ass1="F",to_ass2="F",to_super="F" where idno=val(m.idno)
endif
m.oldfault=m.idno


* create old link
m.idno=m.oldfault
m.solid=m.solid
m.link=m.newfault
m.linktxt="Escalated to "+str(m.newfault)
*
insert into flink (idno,solid,link,linktxt) values (val(m.idno),val(m.solid), ;
m.link,m.linktxt)
*



** create new solution
select number from counter where file="fsol" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fsol"
m.solid=str(m.number)
insert into fsol (idno,solid,action,solution,sdescribe,stype,providor,solout) ;
values (m.newfault,val(m.solid),m.action,m.solution,m.sdescribe,"Comment",m.users,datetime())

* create new link
m.idno=m.newfault
m.solid=m.solid
m.link=m.oldfault
m.linktxt="Escalated from "+m.oldfault
insert into flink (idno,solid,link,linktxt) values (m.idno,val(m.solid), ;
val(m.link),m.linktxt)

do f1 with m.newfault


proc clear_rep
m.idno=formfield("sidno")
update fault set to_rep="F" where idno=val(m.idno)
do f1 with m.idno
return

proc flessons && presentaiton lessons
M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
SELECT form_text FROM html_frm WHERE form_id LIKE 'flessons' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fpresent && presentation
M.cook=allt(SUBSTR(cgi.cookie, AT('user=', CGI.Cookie)+5,36))
SELECT form_text FROM html_frm WHERE form_id LIKE 'fpresent' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fdellist  && delete lists

select idno,reporter,repmail,section,cat,subcat,issue,idescribe,datein,dateout,action, ;
solution,priority,status,sfinal,ass1,ass1mail,ass2,ass2mail,super,supermail, ;
to_ass1, to_ass2,to_super,itype,keyin,keyout from fault  ;
into cursor all_faults order by idno

* querystring
if reccount()>0
   	 	M.ListTxt = '<TABLE>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1>ID No</B></A></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Issue</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>Reporter</B></TD>'
   	 	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1><B>DateIn</B></TD>'

    	M.ListTxt = M.ListTxt+'<TD><FONT SIZE=-1>Section</TD></TR>'
   	 	M.ListTxt = M.ListTxt+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/fdelone@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD>'+allt(all_faults.issue)+'</TD> ;
    	<TD>'+allt(all_faults.reporter)+'</TD><TD>' ;
    	+dtoc(ttod(all_faults.datein))+'</TD><TD>'+allt(all_faults.section)+'</TD></TR>'
   		skip
   	 	scan rest
   	 	M.ListTxt = M.ListTxt+'<TD><A HREF="' + ;
    	UrlEncode(CGI.ExecutablePath+'/fdelone@'+CGI.ProgramPath+'fats?sidno=')+ ;
    	UrlEncode(str(all_faults.idno))+'"><B>' ;
    	+allt(str(all_faults.idno))+'</A></TD><TD>'+allt(all_faults.issue)+'</TD> ;
    	<TD>'+allt(all_faults.reporter)+'</TD><TD>'+ ;
    	dtoc(ttod(all_faults.datein))+'</TD><TD>'+allt(all_faults.section)+'</TD></TR>'
    	endscan
		M.ListTxt=M.ListTxt+"</TABLE>"
else
		M.ListTxt = "No faults!"
endif
SELECT form_text FROM html_frm WHERE form_id LIKE 'fdellist' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc fdelone
m.idno=formfield("sidno")
if val(m.idno)>0
*	delete from fault where idno=val(m.idno)
endif
do flist

proc upfile
m.sidno=allt(formfield("sidno"))
if file("c:\wwwroot\elvis.prg")
*	FileName = "C:\Program Files\Apache Group\Apache2\htdocs\fpix\"+m.sidno+"_{filename}"
*else
	FileName = "C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\fpix\"+m.sidno+"_{filename}"
endif
SELECT form_text FROM html_frm WHERE form_id LIKE 'upfile' INTO ARRAY FormTxt
html_out = MergeTxt(M.FormTxt)
return

proc putfile
private FormTxt
M.idno=allt(formfield("sidno"))
if file("c:\wwwroot\elvis.prg")
*	FileName = "C:\Program Files\Apache Group\Apache2\htdocs\fpix\"+m.idno+"_"+FormField("UpFile", , 2)
*else
	FileName = "C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\fpix\"+m.idno+"_"+FormField("UpFile", , 2)
endif

success=WriteFile(FileName, FormField("UpFile")) 
select number from counter where file="fpix" into cursor one_numb
m.number=one_numb.number
update counter set number=m.number+1 where file="fpix"
insert into faultpic (idno,fidno,imgname) values (m.number,val(m.idno),FormField("UpFile", , 2))
do f1 with m.idno

proc deleteimg
private FormTxt
m.idno=allt(formfield("sidno"))
m.pixidno=allt(formfield("pixidno"))
if val(m.pixidno)>0 and val(m.idno)>0
	select idno,fidno,imgname from faultpic into cursor one_img where idno=val(m.pixidno)
	delete from faultpic where idno=val(m.pixidno)
	if file("c:\wwwroot\elvis.prg")
		m.filename = "C:\Program Files\Apache Group\Apache2\htdocs\fpix\"+m.idno+"_"+allt(one_img.imgname)
	else
		m.filename = "C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\fpix\"+m.idno+"_"+allt(one_img.imgname)
	endif
	if file(m.filename)
		erase &m.filename
	endif
endif
do f1 with m.idno
