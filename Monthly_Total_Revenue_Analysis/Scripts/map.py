#!/usr/bin/python
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip().split(',')
    if line[0] == 'VendorID' or line[0] == 'WBAN':
        continue
    if len(line) == 19:
        tpep_pickup_datetime = line[1]
        year_month_day = datetime.strptime(tpep_pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
        total_amount = line[18]
        print(("%s\t%s,y") % (year_month_day, total_amount))
    elif len(line) == 21 or len(line) == 23:
        lpep_pickup_datetime = line[1]
        year_month_day = datetime.strptime(lpep_pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
        total_amount = line[18]
        print(("%s\t%s,g") % (year_month_day, total_amount))
