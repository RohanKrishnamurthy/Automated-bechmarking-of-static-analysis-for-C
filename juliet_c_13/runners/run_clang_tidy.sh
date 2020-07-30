#!/bin/bash

LOGFILE=clang-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

for i in $(find testcases -type f -iregex ".*CWE.*[0-9]+\.c" \! -name "*w32*"); do
	echo "processing $i"
	cd ~/sastevaluation/C
	clang-tidy-4.0 -extra-arg="-I./testcasesupport/" -checks=-*,clang-analyzer-*,cert-* $i 1>> $LOGFILE
done
