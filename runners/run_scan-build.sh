#!/bin/bash

#----------------------------------------
#author:  Rohan Krishnamurthy, 
#rohan.krishnamurthy@dlr.de
#German Aerospace Center
#Year 2020
#----------------------------------------

LOGFILE=scan-build-results.log

if [ -f $LOGFILE ]
then
	rm $LOGFILE
fi

scan-build make individuals -j4 2> $LOGFILE
