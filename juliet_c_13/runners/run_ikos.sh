#!/bin/bash

#-----------------------------------------------
#author:  Rohan Krishnamurthy, Christoph Gentsch
#German Aerospace Center
#-----------------------------------------------

LOGFILE=ikos-results.log

if [ -f $LOGFILE ]
then
    rm $LOGFILE
fi

for i in $(find ~/sastevaluation/C/testcases -type f -iregex ".*CWE.*[0-9]+\.c" \! -name "*w32*"); do
    echo "processing $i"
    /usr/lib/llvm-4.0/bin/clang -pthread -c -g -emit-llvm -D_FORTIFY_SOURCE=0 -DINCLUDEMAIN -I./testcasesupport $i -o $i.bc
    ~/sastevaluation/ikos-3.0/bin/ikos -d=var-pack-dbm --format=no --display-summary=no --display-times=no --output-db=$i.db $i.bc
    rm $i.bc
    python3 print_ikos_messages.py $i.db $i >> $LOGFILE
    rm $i.db
done
