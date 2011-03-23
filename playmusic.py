#!/usr/bin/env python
#This program is used to play song by mplayer
#it needs a list, the directory of list is '~/.musicmanager/musiclist'

#CreatedDate: 2010-07-07	Author: xudifsd

#2010-07-08 Notice this modify , program can play without list.
#2010-07-09 Notice this modify , it can add comment(which line starts with #) in list file.
#2010-09-24 this modify make use of argumentsParse , and it can use -n argument to play music in Music's subdir.

#2010-09-25 IMPORTANT UPDATE ! This modify use pyglet and Avbin to play instead of call mplayer	!!!!!
#2010-09-27 IMPORTANT UPDATE ! This modify change player , pyglet I don't know how to use it , but I clean the output of mplayer by use os.system(">&-").

#2010-10-23 this modify is to adapt to python3
#2010-10-30 this modify is make it possible to remove some song from listfile while playing

#2011-01-06 IMPORTANT UPDATE ! This modify divide a big program into many small parts and use .musicmanager/musiclist to store list file , and make it classlized

#2011-03-23 Make the process of playmusic a self name instead of python

import os
import sys
import random
from argumentsParse import argumentsParse	#create by myself

class MusicManager:
	def __init__(self,listname=None,debug=False):	#listname is just a name , not a path!!!
		import dl
		libc = dl.open('/lib/libc.so.6')
		libc.call('prctl',15,'musicmanager',0,0,0)	#set process name to 'musicmanager'
		self.USER_HOME=os.environ['HOME']
		self.MUSIC_HOME=os.path.join(self.USER_HOME,'Music')
		self.PROGRAM_HOME=os.path.join(self.USER_HOME,'.musicmanager')
		self.LIST_HOME=os.path.join(self.PROGRAM_HOME,'musiclist')

		if os.path.isdir(self.PROGRAM_HOME) == False:	#no ~/.musicmanager
			os.makedirs(self.PROGRAM_HOME)
			os.makedirs(self.LIST_HOME)	#list is in there

		if debug:
			print('USER_HOME='+self.USER_HOME)
			print('MUSIC_HOME='+self.MUSIC_HOME)
			print('PROGRAM_HOME='+self.PROGRAM_HOME)
			print('LIST_HOME='+self.LIST_HOME)

	def setPlayList(self,listname=None):
		self.__LISTNAME=listname
		self.__playlist=self.getPlayList(listname)

	def __getFile(self,directory):	#this is only be called by self.getPlayList , directory should be the absolute path
		files=[os.path.join(directory,i) for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i))]
		dirs=[os.path.join(directory,i) for i in os.listdir(directory) if os.path.isdir(os.path.join(directory,i))]
		for dir in dirs:
			files+=self.__getFile(dir)
		return files

	def getPlayList(self,listname=None,debug=False):	#listname is just a name , not a path!!!
		if listname == None:	#need not playlist
			playlist=self.__getFile(self.MUSIC_HOME)
		else:
			try:
				f=open(os.path.join(self.LIST_HOME,listname))
			except:
				sys.stderr.write('Please input legal playlist filename\n')
				sys.exit(2)
			else:
				txt=f.read()
				f.close()
				playlist=txt.split('\n')
				playlist=[song for song in playlist if not song.startswith('#')]	#this makes it legal to add comment in playlist file
				playlist=[song for song in playlist if song]	#in case there are blank line
				del txt
		if debug:
			print('playlist[0]='+playlist[0])
		return playlist

	def play(self,song):	#song should be the absolute path
		print('Playing '+song.split('/')[-1])
		state=os.system('mplayer "'+song+'" 1>&- 2>&-')
		return state

	def randomPlay(self):
		while True:
			song=self.__playlist[random.randint(0,len(self.__playlist)-1)]	#random select song to play
			state=self.play(song)
			if state==2:	#play is interrupt by <CTRL + C>
				self.__playlist.remove(song)	#user use <CTRL + C> delete song from list
				if self.__LISTNAME:	#if user use list to play music
					try:
						f=open(os.path.join(self.LIST_HOME,self.__LISTNAME),'w')	#remove song from original list file
						f.write('\n'.join(self.__playlist))
					except IOError:
						sys.stderr.write("Some problem caused while write list to list file\n")
					finally:
						f.close()
				else:	#user did not use list
					try:
						f=open(os.path.join(self.LIST_HOME,'tmp.list'),'w')
						f.write('\n'.join(self.__playlist))
					except IOError:
						sys.stderr.write("Some problem caused while write list to tmp.list\n")
					finally:
						f.close()

if __name__=='__main__':
	ERRORMESSAGE='''
Argument:
--nolist or -n			Directly play music in ~/Music.
--list or -l		List all list that in ~/.musicmanager/musiclist
path_of_listname	Play music in list.
'''
	playinstance = MusicManager()

#parse arguments
	if len(sys.argv)==2:	#this version can only accept 1 arguments
		arguments=argumentsParse(sys.argv[1:])

		if len(arguments[0]) == 1:	#if argument starts with '--' , this mean user use long argument
			argument=arguments[0][0][2:]

			if argument=='nolist':	#if user neednot list
				playinstance.setPlayList(None)
			elif argument=='list':	#user need to know the name of all list
				list=os.listdir(playinstance.LIST_HOME)
				print('\n'.join(list))
				sys.exit(0)
			else:
				sys.stderr.write(ERRORMESSAGE)
				sys.exit(2)

		elif len(arguments[1])==1:	#if argumen start with '-' , this mean user use short argument
			argument=arguments[1][0][1:]

			if argument=='n':	#if user need not list
				playinstance.setPlayList(None)
			elif argument=='l':	#user need to know the name of all list
				list=os.listdir(playinstance.LIST_HOME)
				print('\n'.join(list))
				sys.exit(0)
			else:
				sys.stderr.write(ERRORMESSAGE)
				sys.exit(2)

		elif len(arguments[3])==1:	#user make list name as argument
			listname=arguments[3][0]
			playinstance.setPlayList(listname)

	else:	#the amount of arguments that user inputed is not 1
		sys.stderr.write(ERRORMESSAGE)
		sys.exit(2)
#play
	playinstance.randomPlay()

