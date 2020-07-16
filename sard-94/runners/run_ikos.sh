#!/bin/bash

LOGFILE=ikos-results.log

export CLANG_LIBRARY_PATH="/usr/lib/llvm-6.0/lib"
export C_INCLUDE_PATH="/usr/include:/usr/lib/gcc/x86_64-linux-gnu/8/include:/usr/lib/gcc/x86_64-linux-gnu/8/include-fixed"

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
        ikos --format=no --display-summary=no --display-times=no --output-db=output.db --entry-points=$entry $i.bc
        ./print_ikos_messages.py output.db $FILE >> $LOGFILE
        rm output.db
    done

    rm $i.bc
done
