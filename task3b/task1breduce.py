#!/usr/bin/env python

import sys
import os

curr_latitude=None
curr_longitude=None
curr_sum=0

for line in sys.stdin:
	line=line.strip()
	key,value=line.split("\t",1)
	Dropoff_hr,longitude,latitude=key.split(",",2)
	Dropoff_hr=int(Dropoff_hr)
	try:
		value=int(value)
	except ValueError:
		continue

	if longitude==curr_longitude and latitude==curr_latitude and Dropoff_hr>=00 and Dropoff_hr<=06 :
		curr_sum+=value
	else:
		if curr_latitude and curr_longitude:
			print "%.3f,%.3f,%d" % (float(curr_longitude),float(curr_latitude),curr_sum)
		curr_sum=value
		curr_longitude=longitude
		curr_latitude=latitude
print "%.3f,%.3f,%d" % (float(curr_longitude),float(curr_latitude),curr_sum)
