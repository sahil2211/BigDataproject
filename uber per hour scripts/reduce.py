#!/usr/bin/python
import sys

current_key = None
current_sum = 0

for line in sys.stdin:
    
    key, count = line.strip().split("\t", 1)
    
    try:
        count = int(count)
    except ValueError:
        continue
    
    if key == current_key:
        current_sum += count
    else:
        if current_key:
            print "%s,%d" % (current_key, current_sum)
        current_key = key
        current_sum = count

print "%s,%d" % (current_key, current_sum)
