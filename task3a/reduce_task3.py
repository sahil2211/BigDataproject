#!/usr/bin/env python

import sys

curr_latitude=None
curr_longtitude=None
curr_sum=0

for line in sys.stdin:
	line=line.strip()
	key,value=line.split("\t",1)
	longitude,latitude=key.split(",",1)
	
	try:
		value=int(value)
	except ValueError:
		continue
	
	if longitude==curr_latitude and latitude=curr_latitude:
		curr_sum+=value
	else:
		if curr_latitude and curr_longtitude:
			print "%f,%f,%d" % (float(curr_longtitude),float(curr_latitude),curr_sum)
			curr_sum=value
			curr_longtitude=longitude
			curr_latitude=latitude
print "%f,%f,%d" % (float(curr_longtitude),float(curr_latitude),curr_sum)