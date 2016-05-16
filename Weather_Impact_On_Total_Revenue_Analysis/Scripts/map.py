#!/usr/bin/python
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip().split(',')
    if line[0] == 'VendorID' or line[0] == 'WBAN':
        continue
    if len(line) == 19:
        tpep_pickup_datetime = line[1]
        year_month_day = datetime.strptime(tpep_pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        total_amount = line[18]
        print(("%s\t%s,y") % (year_month_day, total_amount))
    elif len(line) == 21 or len(line) == 23:
        lpep_pickup_datetime = line[1]
        year_month_day = datetime.strptime(lpep_pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        total_amount = line[18]
        print(("%s\t%s,g") % (year_month_day, total_amount))
    elif len(line) == 50:
        year_month_day = datetime.strptime(line[1], '%Y%m%d').strftime('%Y-%m-%d')
        t_max = line[2]
        t_min = line[4]
        t_avg = line[6]
        weather_type = line[22]
        depth = line[24]
        water1 = line[26]
        snowfall = line[28]
        precip_total = line[30]
        avg_speed = line[40]
        print(("%s\t%s,%s,%s,%s,%s,%s,%s,%s,%s") % (year_month_day, t_max, t_min, t_avg, weather_type, depth, water1, snowfall, precip_total, avg_speed))
