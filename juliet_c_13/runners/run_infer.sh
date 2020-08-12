#!/bin/bash

#-----------------------------------------------
#author:  Rohan Krishnamurthy, Christoph Gentsch
#German Aerospace Center
#-----------------------------------------------

LOGFILE=infer-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

for i in $(find ~/sastevaluation/C testcases -type f -iregex ".*CWE.*[0-9]+\.c" \! -name "*w32*"); do
	echo "processing $i"
	FILENAME=$(echo $i|sed -r "s/.*\/(.*\.[c|h])/\1/")
	~/sastevaluation/infer-linux64-v0.17.0/bin/infer run -a checkers -- clang -I./testcasesupport -DINCLUDEMAIN -c $i 2>>$LOGFILE
	rm `echo $FILENAME | sed -r "s/\.c$/.o/"`
done

#clean the file from the color escapes
sed 's/^[\[[0-9]*m//g' $LOGFILE > $LOGFILE

