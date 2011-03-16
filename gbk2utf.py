#!/usr/bin/python3
#Date:2010-07-05	Author:xudifsd

#2010-09-21	this modify add feature that can assign fromcode and tocode,and default fromcode is gbk,default tocode is utf-8
#2010-09-24 this modify make use of argumentsParse
#2010-10-23 this modify is to adapt to python3

import sys
from argumentsParse import argumentsParse

ERRORMESSAGE='''
Usage :
f= code that you want change from default gbk
t= code that you want change to default utf-8
filename file that you want change
'''

#parse arguments
if len(sys.argv)==1:
	print(ERRORMESSAGE)
else:
	fromcode=tocode=''

	arguments=argumentsParse(sys.argv[1:])

	try:	#default fromcode=gbkt , default tocode=utf-8
		fromcode=arguments[2]['f']
	except KeyError:
		fromcode='gbk'
	try:
		tocode=arguments[2]['t']
	except KeyError:
		tocode='utf-8'

	filenames=arguments[3]

#main
	for filename in filenames:
		#read file
		try:
			file=open(filename,encoding=fromcode)
			txt=file.read()	#in python3 txt is already utf-8
		except IOError:
			print('[warning]\tno file named %s!'%(filename))
			continue
		
		#write file
		try:
			outfile=open(tocode+'_'+filename,'w',encoding=tocode)
			outfile.write(txt)
		except IOError:
			print('[warning]\tcreat out file of %s failure!'%(filename))
			continue
		else:
			print('translate %s successful!'%(filename))
