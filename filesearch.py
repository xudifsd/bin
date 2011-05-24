#!/usr/bin/env python
#Last modify: 2010-7-12	Author: xudifsd

#2010-07-08 notice this time i use class instead one function,this can use no global varity! and it will be easy to extend it.
#2010-07-08 notice this time program can search more than one key word in one search(this is only useful when you search extname of file).
#2010-07-31 this modify make program ignore case of word.
#2010-08-12 this modify make program can accept '/home' and '/home/' as path instead of only accept '/home/'.
#2010-09-07 fixed a print bug
#2010-09-24 use argumentsParse to parse argument
#2010-10-23 this modify is to adapt to python3
#2010-10-24 this modify is used os model instead of create it by myself
#2010-10-25 this modify used stderr to show error message

#WARNING: THIS PROGRAM IS IMPORTED BY cp2me.py! IF YOU CHANGED THIS PROGRAM PLEASE ADJUST cp2me.py TOO!

import sys
import os
from argumentsParse import argumentsParse

class filesearch:
	def __init__(self):
		self.result=[]
	def search(self,path,key_words):	#key_words must be tuple
		"""This function helps you find files that have exact word in its name,good luck!
		key_word means the key word you want search,path means the path of directory."""
		try:
			all=os.walk(path,False)	#os.walk() is a generator , the return is a tuple which is (dirpath,dirnames,filenames)
		except:
			pass
		else:
			for item in all:
				filepath=item[0]
				for filename in item[2]:
					for key_word in key_words:	#find all key_word
						if key_word in filename.lower():	#ignore case of word , and only search filename
							self.result.append(os.path.join(filepath,filename))

if __name__=='__main__':

	ERRORMESSAGE='''
Arguments:
k=key_word1,key_word2	the word you want to search(must be lower case!).
p=path			where you want search.'''

#arguments parse
	if len(sys.argv) != 3:
		sys.stderr.write(ERRORMESSAGE+'\n')
	else:
		key_words=[]	#key_words must be list!
		path=''
		arguments=argumentsParse(sys.argv[1:])
		try:
			key_words=arguments[2]['k'].split(',')
			path=arguments[2]['p']
		except KeyError:
			sys.stderr.write(ERRORMESSAGE+'\n')
		else:
			if not os.path.isdir(path):
				sys.stderr.write(path+' is not a directory!\n')
#search
			else:
				a=filesearch()
				a.search(path,key_words)
				print('\n'.join(a.result))
				print('#There are %d file(s) in match.'%len(a.result))
