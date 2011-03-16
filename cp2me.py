#!/usr/bin/python
#this program help me copy other's video file into my '/home/xudifsd/Videos' silience
#Last modify: 2010-7-8	Author: xudifsd

#2010-10-23 this modify is to adapt to python3

import os
from filesearch import filesearch
import time

def copy(source,target):
	for file in source:
		os.system('cp -n "%s" "%s"'%(file,target))

#test if there are flashdisk

harddisk=('system','program','image','ghost')	#the name of my harddisk
extname=('.avi','.mp4','.wmv','.rmvb','.AVI','.MP4','.WMV','.RMVB')	#the ext name of file

a=filesearch()
while True:
	disk=os.listdir('/media/')
	if disk:
		target=[i for i in disk if i not in harddisk]	#if system mount disk that not my harddisk
		if target:
			for udisk in target:
				a.search('/media/'+udisk+'/',extname)
			copy(a.result,'/home/xudifsd/Videos')
			print('The one copy is completed!')
	print('lazying!')
	time.sleep(10)

