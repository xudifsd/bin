#!/usr/bin/python3
#Author : xudifsd , CreateDate : 2009-09-24

#THIS FILE IS IMPORT BY MANY PROGRAM IN ~/bin !
#2010-10-23 this modify is to adapt to python3

'''
form of result:
result[0] is arguments that starts with '--'	i.e. --argu
result[1] is arguments that starts with '-'	i.e. -argu
result[2] is arguments that have '=' in it	i.e. a=argu
result[3] is just a normal arguments		i.e. argu
'''

def argumentsParse(rawArguments):
	#ATTENTION:if you make sys.argv as arguments you should remember that sys.argv[0] maybe not argumen you want
	'''This function is used to parse sys.argv , and it will never change arguments , which means '-p' is still '-p'.
Return is a tuple that contain 4 item :
The 1st item is tuple , it contains arguments that starts with"--" ;
The 2nd item is tuple that contains arguments that starts with "-" ; 
The 3rd item is dictionary which key is arguments before "=" , value is arguments after "=" ;
The 4th is tuple , it is normal arguments.'''
	result=[[],[],{},[]]

	result[0]=tuple((i for i in rawArguments if i.startswith('--')))

	result[1]=tuple((i for i in rawArguments if i not in result[0] and i.startswith('-')))

	dicttemp=tuple((i for i in rawArguments if '=' in i))

	for i in dicttemp:
		argument=i.split('=')
		result[2][argument[0]]=argument[1]

	result[3]=tuple((i for i in rawArguments if i not in result[0]+result[1]+dicttemp))	#this contain normal argument

	return tuple(result)

if __name__=='__main__':
	import sys
	print(argumentsParse(sys.argv[1:]))
