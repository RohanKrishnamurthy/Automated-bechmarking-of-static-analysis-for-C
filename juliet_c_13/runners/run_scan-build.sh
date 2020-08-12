#!/bin/bash

#-----------------------------------------------
#author:  Rohan Krishnamurthy, Christoph Gentsch
#German Aerospace Center
#-----------------------------------------------

LOGFILE=scan-build-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

cd ~/sastevaluation/C
scan-build-4.0 make individuals -j4 2> $LOGFILE
