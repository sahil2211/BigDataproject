#!/usr/bin/python
import sys

for line in sys.stdin:
    line_new = line.strip().split(',')
    if line_new[0] == 'co':
        continue
	if len(line_new)==19:
		longitude=line_new[5]
		latitude=line_new[6]
		print "%.4f%.4f\t%s" % (longitude,latitude,1)

	