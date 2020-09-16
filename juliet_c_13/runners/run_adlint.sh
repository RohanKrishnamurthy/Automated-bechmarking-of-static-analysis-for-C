#!/bin/bash

#-----------------------------------------------
#author:  Rohan Krishnamurthy, Christoph Gentsch
#German Aerospace Center
#-----------------------------------------------

LOGFILE=adlint-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

for i in $(find testcases -type f -iregex ".*CWE.*[0-9]+\.c" \! -name "*w32*"); do
	echo "processing $i"
	FILENAME=$(echo $i|sed -r "s/.*\/(.*\.[c|h])/\1/")
	adlint_sma -t adlint_traits.yml -o . -p 1 $i 2>> $LOGFILE
done
