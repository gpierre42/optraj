#!/bin/bash

sumfile=/vagrant/DonneesBDD/sha1sum
salaries=/vagrant/DonneesBDD/salaries.csv

aoption=

if [  -f salaries ]
then
  echo "ERROR: Unknown file: $salaries."
  exit 1
elif [ -f sumfile ]
then
  echo "ERROR: Unknow file: $sumfile."
fi

newsum="`sha1sum $salaries`"

while getopts 'f' OPTION
do
	case $OPTION in
		f)	foption=1
			;;
		?)	printf "Usage: %s [-f]">&2
			exit 2
			;;
	esac
done
shift $((OPTIND - 1))
if [ "$foption" ]
then
	python /vagrant/optraj.istic.univ-rennes1.fr/src/importData/GenerateWorkers.py
else
	if grep -q "$newsum" $sumfile; then
	  echo "$salaries matches"
	else
	  echo "$salaries IS MODIFIED"
	  sha1sum $salaries > $sumfile
	  python /vagrant/optraj.istic.univ-rennes1.fr/src/importData/GenerateWorkers.py
	fi
fi



