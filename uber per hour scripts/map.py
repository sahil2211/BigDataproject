#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time
from datetime import datetime
lookup = {'216': ['Queens'], '217': ['Brooklyn'], '214': ['Staten Island'], '215': ['Queens'], '212': ['Bronx'], '213': ['Bronx'], '210': ['Brooklyn'], '211': ['Manhattan'], '165': ['Brooklyn'], '264': ['Unknown'], '265': ['Unknown'], '218': ['Queens'], '219': ['Queens'], '133': ['Brooklyn'], '132': ['Queens'], '131': ['Queens'], '130': ['Queens'], '137': ['Manhattan'], '136': ['Bronx'], '135': ['Queens'], '134': ['Queens'], '139': ['Queens'], '138': ['Queens'], '166': ['Manhattan'], '24': ['Manhattan'], '25': ['Brooklyn'], '26': ['Brooklyn'], '27': ['Queens'], '20': ['Bronx'], '21': ['Brooklyn'], '22': ['Brooklyn'], '23': ['Staten Island'], '160': ['Queens'], '28': ['Queens'], '29': ['Brooklyn'], '161': ['Manhattan'], '4': ['Manhattan'], '8': ['Queens'], '163': ['Manhattan'], '119': ['Bronx'], '258': ['Queens'], '120': ['Manhattan'], '121': ['Queens'], '122': ['Queens'], '123': ['Brooklyn'], '124': ['Queens'], '125': ['Manhattan'], '126': ['Bronx'], '127': ['Manhattan'], '128': ['Manhattan'], '129': ['Queens'], '167': ['Bronx'], '118': ['Staten Island'], '59': ['Bronx'], '58': ['Bronx'], '55': ['Brooklyn'], '54': ['Brooklyn'], '57': ['Queens'], '56': ['Queens'], '51': ['Bronx'], '50': ['Manhattan'], '53': ['Queens'], '52': ['Brooklyn'], '259': ['Bronx'], '164': ['Manhattan'], '201': ['Queens'], '199': ['Bronx'], '179': ['Queens'], '200': ['Bronx'], '195': ['Brooklyn'], '194': ['Manhattan'], '197': ['Queens'], '178': ['Brooklyn'], '191': ['Queens'], '190': ['Brooklyn'], '193': ['Queens'], '192': ['Queens'], '115': ['Staten Island'], '114': ['Manhattan'], '88': ['Manhattan'], '89': ['Brooklyn'], '111': ['Brooklyn'], '110': ['Staten Island'], '113': ['Manhattan'], '112': ['Brooklyn'], '82': ['Queens'], '83': ['Queens'], '80': ['Brooklyn'], '81': ['Bronx'], '86': ['Queens'], '87': ['Manhattan'], '84': ['Staten Island'], '85': ['Brooklyn'], '251': ['Staten Island'], '198': ['Queens'], '256': ['Brooklyn'], '206': ['Staten Island'], '226': ['Queens'], '257': ['Brooklyn'], '3': ['Bronx'], '177': ['Brooklyn'], '254': ['Bronx'], '7': ['Queens'], '247': ['Bronx'], '255': ['Brooklyn'], '225': ['Brooklyn'], '245': ['Staten Island'], '244': ['Manhattan'], '108': ['Brooklyn'], '109': ['Staten Island'], '241': ['Bronx'], '240': ['Bronx'], '243': ['Manhattan'], '242': ['Bronx'], '102': ['Queens'], '103': ['Manhattan'], '100': ['Manhattan'], '101': ['Queens'], '106': ['Brooklyn'], '107': ['Manhattan'], '104': ['Manhattan'], '105': ['Manhattan'], '39': ['Brooklyn'], '38': ['Queens'], '33': ['Brooklyn'], '32': ['Bronx'], '31': ['Bronx'], '30': ['Queens'], '37': ['Brooklyn'], '36': ['Brooklyn'], '35': ['Brooklyn'], '34': ['Brooklyn'], '246': ['Manhattan'], '73': ['Queens'], '252': ['Queens'], '205': ['Queens'], '223': ['Queens'], '176': ['Staten Island'], '60': ['Bronx'], '61': ['Brooklyn'], '62': ['Brooklyn'], '63': ['Brooklyn'], '64': ['Queens'], '65': ['Brooklyn'], '66': ['Brooklyn'], '67': ['Brooklyn'], '68': ['Manhattan'], '69': ['Bronx'], '175': ['Queens'], '174': ['Bronx'], '173': ['Queens'], '172': ['Staten Island'], '171': ['Queens'], '170': ['Manhattan'], '203': ['Queens'], '222': ['Brooklyn'], '181': ['Brooklyn'], '253': ['Queens'], '248': ['Bronx'], '182': ['Bronx'], '183': ['Bronx'], '180': ['Queens'], '2': ['Queens'], '162': ['Manhattan'], '187': ['Staten Island'], '184': ['Bronx'], '6': ['Staten Island'], '220': ['Bronx'], '186': ['Manhattan'], '188': ['Brooklyn'], '189': ['Brooklyn'], '202': ['Manhattan'], '196': ['Queens'], '221': ['Staten Island'], '185': ['Bronx'], '99': ['Staten Island'], '98': ['Queens'], '168': ['Bronx'], '169': ['Bronx'], '229': ['Manhattan'], '228': ['Brooklyn'], '91': ['Brooklyn'], '90': ['Manhattan'], '93': ['Queens'], '92': ['Queens'], '95': ['Queens'], '94': ['Bronx'], '97': ['Brooklyn'], '96': ['Queens'], '11': ['Brooklyn'], '10': ['Queens'], '13': ['Manhattan'], '12': ['Manhattan'], '15': ['Queens'], '14': ['Brooklyn'], '17': ['Brooklyn'], '16': ['Queens'], '19': ['Queens'], '18': ['Bronx'], '117': ['Queens'], '250': ['Bronx'], '116': ['Manhattan'], '204': ['Staten Island'], '151': ['Manhattan'], '150': ['Brooklyn'], '153': ['Manhattan'], '152': ['Manhattan'], '155': ['Brooklyn'], '154': ['Brooklyn'], '157': ['Queens'], '156': ['Staten Island'], '159': ['Bronx'], '158': ['Manhattan'], '234': ['Manhattan'], '238': ['Manhattan'], '239': ['Manhattan'], '207': ['Queens'], '235': ['Bronx'], '236': ['Manhattan'], '237': ['Manhattan'], '230': ['Manhattan'], '231': ['Manhattan'], '232': ['Manhattan'], '233': ['Manhattan'], '224': ['Manhattan'], '48': ['Manhattan'], '49': ['Brooklyn'], '46': ['Bronx'], '47': ['Bronx'], '44': ['Staten Island'], '45': ['Manhattan'], '42': ['Manhattan'], '43': ['Manhattan'], '40': ['Brooklyn'], '41': ['Manhattan'], '1': ['EWR'], '5': ['Staten Island'], '9': ['Queens'], '146': ['Queens'], '147': ['Bronx'], '144': ['Manhattan'], '145': ['Queens'], '142': ['Manhattan'], '143': ['Manhattan'], '140': ['Manhattan'], '141': ['Manhattan'], '209': ['Manhattan'], '208': ['Bronx'], '148': ['Manhattan'], '149': ['Brooklyn'], '77': ['Brooklyn'], '76': ['Brooklyn'], '75': ['Manhattan'], '74': ['Manhattan'], 'LocationID': ['Borough'], '72': ['Brooklyn'], '71': ['Brooklyn'], '70': ['Queens'], '79': ['Manhattan'], '78': ['Bronx'], '263': ['Manhattan'], '249': ['Manhattan'], '262': ['Manhattan'], '227': ['Brooklyn'], '261': ['Manhattan'], '260': ['Queens']}
weekend=set([4,5,6])
class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Polygon:
	def __init__(self,points):
		self.points = points
		self.nvert = len(points)
		global globalmaxx
		global globalminx
		global globalminy
		global globalmaxy
		minx = maxx = points[0].x
		miny = maxy = points[0].y
		for i in range(1,self.nvert):
			minx = min(minx,points[i].x)
			miny = min(miny,points[i].y)
			maxx = max(maxx,points[i].x)
			maxy = max(maxy,points[i].y)
		globalminx = minx
		globalminy=miny
		globalmaxx=maxx
		globalmaxy=maxy
		self.bound = (minx,miny,maxx,maxy)


	def contains(self,pt):
		firstX = self.points[0].x
		firstY = self.points[0].y
		testx = pt.x
		testy = pt.y
		c = False
		j = 0
		i = 1
		nvert = self.nvert
		while (i < nvert) :
			vi = self.points[i]
			vj = self.points[j]

			if(((vi.y > testy) != (vj.y > testy)) and (testx < (vj.x - vi.x) * (testy - vi.y) / (vj.y - vi.y) + vi.x)):
				c = not(c)

			if(vi.x == firstX and vi.y == firstY):
				i = i + 1
				if (i < nvert):
					vi = self.points[i];
					firstX = vi.x;
					firstY = vi.y;
			j = i
			i = i + 1
		return c

	def bounds(self):
		return self.bound
def findNeighborhood(location, index, neighborhoods):
        
        match = index.intersection((location[0], location[1], location[0], location[1]))
        for a in match:
                if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
                        return a
        return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
        sf = shapefile.Reader(shapeFilename)
        for sr in sf.shapeRecords():
                if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx', 'Richmond' ]: continue
                paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
                bbox = paths[0].get_extents()
                map(bbox.update_from_path, paths[1:])
                index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
                neighborhoods.append((sr.record[2], paths))
        neighborhoods.append(('UNKNOWN', None))

def parseInput():
        
        
        for line in sys.stdin:
                
                
                line = line.strip()
                values = line.split(',')
                if values[0]=='"Date/Time"': continue
                if values[0]=="Dispatching_base_num": continue
                if values[0]=='VendorID':continue
                if values[0]=='vendor_id': continue
                if len(values)>1:
                        yield values

def mapper():
        index = rtree.Index()
        neighborhoods = []
        readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
        poly = Polygon([Point(40.6188,-73.7712),Point(40.6233,-73.7674),Point(40.6248,-73.7681),Point(40.6281,-73.7681),Point(40.6356,-73.7472),Point(40.6422,-73.7468),Point(40.6469,-73.7534),
	Point(40.6460,-73.7544),Point(40.6589,-73.7745),Point(40.6628,-73.7858),Point(40.6634,-73.7891),Point(40.6655,-73.7903),Point(40.6658,-73.8021),Point(40.6632,-73.8146),Point(40.6638,-73.8210),Point(40.6621,-73.8244),Point(40.6546,-73.8248),
	Point(40.6469,-73.8212),Point(40.6302,-73.7848),Point(40.6223,-73.7899),Point(40.6203,-73.7831),Point(40.6274,-73.7782),Point(40.6235,-73.7731),Point(40.6193,-73.7738),Point(40.6188,-73.7712)])

        poly1 = Polygon([Point(40.7662,-73.8888),Point(40.7736,-73.8898),Point(40.7751,-73.8843),Point(40.7808,-73.8852),Point(40.7812,-73.8795),Point(40.7842,-73.8788),Point(40.7827,-73.8751),
	Point(40.7864,-73.8711),Point(40.788,-73.8673),Point(40.7832,-73.868),Point(40.7808,-73.8716),Point(40.773,-73.8534),Point(40.7697,-73.8557),Point(40.7673,-73.8505),Point(40.7645,-73.85),Point(40.7637,-73.8529),
        Point(40.7676,-73.856),Point(40.7659,-73.8594),Point(40.7654,-73.8625),Point(40.7693,-73.8672),Point(40.7714,-73.8732),Point(40.7697,-73.8871),Point(40.7665,-73.8866),Point(40.7662,-73.8888)])    
    # read taxi trip and fare data 
        for values in parseInput():
                pickup_neighborhood=-1        # default as first
                total = -1              # default as first
                
                
                if values[0].isalnum():
                        pickup_datetime = values[1]
                        locationid = values[3]
                        if locationid == '264' or locationid == '265' : continue
                        pickup_time = datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%H')
                        pickup_year = int (datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y'))            
                        pickup_month = int( datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%m'))
                        pickup_date = int (datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%d'))
                        pickup_time = datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S').strftime('%H')
                        dateset = datetime(pickup_year,pickup_month,pickup_date)
                        if dateset.weekday() in weekend:
                                print("%s,%s,u,weekend\t%d" % (pickup_time,lookup[locationid][0],1))
                        else:
                                print("%s,%s,u,weekday\t%d" % (pickup_time,lookup[locationid][0],1))
                

                else: # uber_data
            
                        pickup_location = (float(values[2]), float(values[1]))
                        point1=Point(float('%.5f'%float(values[1])),float('%.5f'%float(values[2])))
                        pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
                        pickup_datetime = values[0]
                        pickup_datetime = pickup_datetime[1:-1]
                        pickup_year = int (datetime.strptime(pickup_datetime, '%m/%d/%Y %H:%M:%S').strftime('%Y'))
                        pickup_month = int (datetime.strptime(pickup_datetime, '%m/%d/%Y %H:%M:%S').strftime('%m'))
                        pickup_date = int (datetime.strptime(pickup_datetime, '%m/%d/%Y %H:%M:%S').strftime('%d'))
                        pickup_time = datetime.strptime(pickup_datetime, '%m/%d/%Y %H:%M:%S').strftime('%H')
                        dateset = datetime(pickup_year,pickup_month,pickup_date)
                        if poly.contains(point1) or poly1.contains(point1):
                                if dateset.weekday() in weekend:
                                        print("%s,Queens,u,weekend\t%d" % (pickup_time,1))
                                else:
                                        print("%s,Queens,u,weekday\t%d" % (pickup_time,1))
                                continue
                        if dateset.weekday() in weekend:
                                if "Manhattan" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Manhattan,u,weekend\t%d" % (pickup_time,1))
                                elif "Bronx" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Bronx,u,weekend\t%d" % (pickup_time,1))
                                elif "Brooklyn" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Brooklyn,u,weekend\t%d" % (pickup_time,1))
                                elif "Queens" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Queens,u,weekend\t%d" % (pickup_time,1))
                                elif "Staten Island" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Staten Island,u,weekend\t%d" % (pickup_time,1))
                        else:
                                if "Manhattan" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Manhattan,u,weekday\t%d" % (pickup_time,1))
                                elif "Bronx" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Bronx,u,weekday\t%d" % (pickup_time,1))
                                elif "Brooklyn" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Brooklyn,u,weekday\t%d" % (pickup_time,1))
                                elif "Queens" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Queens,u,weekday\t%d" % (pickup_time,1))
                                elif "Staten Island" in neighborhoods[pickup_neighborhood][0]:
                                        print ("%s,Staten Island,u,weekday\t%d" % (pickup_time,1))


if __name__=='__main__':
        
        mapper()
