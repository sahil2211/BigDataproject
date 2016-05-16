#!/usr/bin/python

import sys

current_key = None
total_count_y = 0
total_count_g = 0
total_count_u = 0 
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
	taxi_type = ''
	if len(values) == 2:
                taxi_type = values[1]
	count_y = 0
	count_g = 0
	count_u = 0

	try:
                if(len(values) == 2):
                        if taxi_type == "y":
                                count_y = int(values[0])
                        elif taxi_type == "g":
                                count_g = int(values[0])
                        else:
                                count_u = int(values[0])
	except ValueError:
		continue
	
	if (key == current_key):
                if(len(values) == 2):
                        if taxi_type == "y":
                                total_count_y += count_y
                        elif taxi_type == "g":
                                total_count_g += count_g
                        else:
                                total_count_u += count_u
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
                         print(("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s") % (current_key, total_count_y, total_count_g,total_count_u,t_max, t_min, t_avg, weather_type, depth, waterl, snowfall, precip_total, avg_speed))
                current_key = key
                total_count_y = count_y
                total_count_g = count_g
                total_count_u = count_u
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

print(("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s") % (current_key, total_count_y, total_count_g,total_count_u,t_max, t_min, t_avg, weather_type, depth, waterl, snowfall, precip_total, avg_speed))
