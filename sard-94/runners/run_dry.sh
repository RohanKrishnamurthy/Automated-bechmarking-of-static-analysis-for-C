#!/bin/bash

export CLANG_LIBRARY_PATH="/usr/lib/llvm-4.0/lib"
export C_INCLUDE_PATH="/usr/include:/usr/lib/gcc/x86_64-linux-gnu/7/include:/usr/lib/gcc/x86_64-linux-gnu/7/include-fixed"

LOGFILE=dry-results.log

if [ -f $LOGFILE ]
then
    rm $LOGFILE
fi

for i in $(find $1/epan $1/plugins $1/wiretap -type f -name *.c); do
    FILE=${i#$1/} #get filename without base dir
    echo "processing $FILE"
    /usr/lib/llvm-4.0/bin/clang -c -g -emit-llvm $(./get_includes.py $1 $FILE) $1/$FILE -o $i.bc

    for entry in $(./entry_functions.py $1 $FILE); do
        echo "[[[ checking $entry ]]]"
        echo "$FILE->$entry" >> $LOGFILE
    done
done
