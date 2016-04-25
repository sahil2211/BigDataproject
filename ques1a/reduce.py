#!/usr/bin/python
import sys

current_date = None
current_sum = 0

for line in sys.stdin:
    
    date, count = line.strip().split("\t", 1)
    
    try:
        count = int(count)
    except ValueError:
        continue
    
    if date == current_date:
        current_sum += count
    else:
        if current_date:
            print "%s\t%d" % (current_date, current_sum)
        current_date = date
        current_sum = count

print "%s\t%d" % (current_date, current_sum)
