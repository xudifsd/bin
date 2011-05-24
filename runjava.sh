#Author : xudifsd Date : 2010-08-28
#This shell script is used by alias in ~/.bashrc , if you changed this file you should notice this would affect the alias too.


#this shell program is used to make compile java and run java more easy.

javac $1.java 2>javacerror.tmp
error=$(head -n 1 javacerror.tmp)	#every time there would be javacerror.tmp file,so if error $error will not empty.
if [ "$error" ];then	#if $error is not empty.(this means there are error)
	cat javacerror.tmp	#print error message.
	rm javacerror.tmp
else
	java $1
	rm javacerror.tmp 2>/dev/null
fi
