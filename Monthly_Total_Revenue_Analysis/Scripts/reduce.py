#!/usr/bin/python

import sys

current_key = None
total_revenue_y = 0
total_revenue_g = 0

for line in sys.stdin:
	line = line.strip()
	key, value = line.split('\t')
	values = value.split(',')
	taxi_type = ''
	if len(values) == 2:
                taxi_type = values[1]
	total_amount_y = 0
	total_amount_g = 0

	try:
                if(len(values) == 2):
                        if taxi_type == "y":
                                total_amount_y = float(values[0])
                        elif taxi_type == "g":
                                total_amount_g = float(values[0])
	except ValueError:
		continue
	
	if (key == current_key):
                if(len(values) == 2):
                        if taxi_type == "y":
                                total_revenue_y += total_amount_y
                        elif taxi_type == "g":
                                total_revenue_g += total_amount_g
	else:
                if(current_key):
                         print(("%s,%s,%s") % (current_key, total_revenue_y, total_revenue_g))
                current_key = key
                total_revenue_y = total_amount_y
                total_revenue_g = total_amount_g

print(("%s,%s,%s") % (current_key, total_revenue_y, total_revenue_g))
