#!/bin/bash

LOGFILE=flawfinder-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

for i in $(find $1/epan $1/plugins $1/wiretap -type f -name *.c); do
    FILE=${i#$1/} #get filename without base dir
    echo "processing $FILE"
	flawfinder -D -Q -S $i >> $LOGFILE
done
