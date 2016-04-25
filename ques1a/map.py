#!/usr/bin/python
import sys
from datetime import datetime
for line in sys.stdin:

    line = line.strip().split(',')
    if line[0]=='"Date/Time"':
        continue
    if len(line)==17:
        picpup_datetime = line[1]
        pickup_date = datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
    if len(line)==4:
        pickup_datetime = line[0]
        pickup_datetime = pickup_datetime[1:-1]
    
        pickup_date = datetime.strptime(pickup_datetime, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m')
                                                                                       

    print ("%s\t%d" % (pickup_date,1))

