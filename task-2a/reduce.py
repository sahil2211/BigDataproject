#!/usr/bin/python

import sys

current_key = None
total_revenue = 0
t_max = ''
t_min = ''
t_avg = ''
weather_type = ''
depth = ''
waterl = ''
snowfall = ''
precip_total = ''
avg_speed = ''

for line in sys.stdin:
	line = line.strip()
	key, value = line.split('\t')
	values = value.split(',')
	total_amount = 0
	
	try:
                if(len(values) == 1):
                        total_amount = float(value)
	except ValueError:
		continue
	
	if (key == current_key):
                if(len(values) == 1):
                        total_revenue += total_amount
                elif(len(values) == 9):
                        t_max = values[0]
                        t_min = values[1]
                        t_avg = values[2]
                        weather_type = values[3]
                        depth = values[4]
                        waterl = values[5]
                        snowfall = values[6]
                        precip_total = values[7]
                        avg_speed = values[8]
	else:
                if(current_key):
                         print(("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s") % (current_key, total_revenue, t_max, t_min, t_avg, weather_type, depth, waterl, snowfall, precip_total, avg_speed))
                current_key = key
                total_revenue = total_amount
                if(len(values) == 9):
                        t_max = values[0]
                        t_min = values[1]
                        t_avg = values[2]
                        weather_type = values[3]
                        depth = values[4]
                        waterl = values[5]
                        snowfall = values[6]
                        precip_total = values[7]
                        avg_speed = values[8]

print(("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s") % (current_key, total_revenue, t_max, t_min, t_avg, weather_type, depth, waterl, snowfall, precip_total, avg_speed))
