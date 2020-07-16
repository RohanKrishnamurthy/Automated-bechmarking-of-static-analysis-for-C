#!/bin/bash

LOGFILE=clang-results.log
export CLANG_LIBRARY_PATH="/usr/lib/llvm-6.0/lib"

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

for i in $(find $1/epan $1/plugins $1/wiretap -type f -name *.c); do
    FILE=${i#$1/} #get filename without base dir
    echo "processing $FILE"
	clang-tidy-6.0 -extra-arg="$(./get_includes.py $1 $FILE)" -checks=-*,clang-analyzer-*,cert-* $i 1>> $LOGFILE
done
