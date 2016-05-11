#!/usr/bin/env python

import sys
import csv
import StringIO
from datetime import datetime

for line in sys.stdin:
	dropofftime,dropofflongitude,dropofflatitude = line.strip().split(',',2)
	if dropofflongitude == 'Dropoff_longitude':
        	continue
	Drop_time = datetime.strptime(dropofftime,'%m/%d/%Y %H:%M').strftime('%H')
	dropofflongitude=float(dropofflongitude)
	dropofflatitude=float(dropofflatitude)
	print "%s,%.3f,%.3f\t%d" %(Drop_time,dropofflongitude,dropofflatitude,1) 

	
