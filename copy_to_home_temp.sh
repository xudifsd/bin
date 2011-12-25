#!/bin/bash

until [ -z $1 ]; do
	cp $1 $HOME/temp/`basename $1`
	echo copied to ~/temp/`basename $1`
	file ~/temp/`basename $1`
	shift
done
