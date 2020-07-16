#!/bin/bash

LOGFILE=cppcheck-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

cppcheck -DHAVE_CONFIG_H -DINET6 -DG_DISABLE_DEPRECATED -DG_DISABLE_SINGLE_INCLUDES -DGTK_DISABLE_DEPRECATED -DGTK_DISABLE_SINGLE_INCLUDES -D"_U_=__attribute__((unused))" -j 3 -q --platform=unix64 $1/epan $1/plugins $1/wiretap 2>> $LOGFILE

