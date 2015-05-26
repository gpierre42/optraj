#!/bin/bash

if [ $# -lt 1 ]
then
	echo "usage: loaddata.sh filename.sql"
else
	file = $1
	echo $file
	if [ -f file ] && [[ ${file: -4} == ".sql" ]]
	then
		mysql  -uroot -ppassword --local-infile < $file
	else
		echo "$file n'est pas un fichier .sql"
	fi
fi
