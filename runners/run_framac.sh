#!/bin/bash

#-----------------------------------------------
#author:  Rohan Krishnamurthy, Christoph Gentsch
#German Aerospace Center
#-----------------------------------------------

LOGFILE=framac-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

for i in $(find ~/sastevaluation/C/testcases -type f -iregex ".*CWE.*[0-9]+\.c" \! -name "*w32*"); do
	echo "processing $i"
	FILENAME=$(echo $i|sed -r "s/.*\/(.*\.[c|h])/\1/")
	frama-c -quiet -val -cpp-extra-args="-DINCLUDEMAIN -I./testcasesupport" $i >> $LOGFILE
done
