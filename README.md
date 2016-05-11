Fenil  Tailor (N18730085) 
Sahil Shah
Ajinkya Avinash Shukla (N17644394)
 			                 	Project Proposal Outline
                                                                                                                                                                                                                                                                           
Introduction: We are going to analyze the following questions with the help of this project. 

1)How does Uber and green taxi  arrival impact the  Yellow Taxi in New York?
Progression of rise of uber and green taxi in all 5 boroughs of New York City over the period of April 2014 to  June 2015.
Is there a particular area which is better served with the arrival of Uber and green taxi?
Do people prefer yellow taxi, green taxi and uber during a particular time of the day? Is there a clear favorite in any of the borough on different hours during the day.
2) How does the revenue of yellow taxi and green taxi vary for the year 2014 and is there a correlation between the weather and public holidays on the revenue? Do people prefer yellow taxi, uber or green taxi during extreme weathers.
3) Which are popular nightlife locations in New York city. At what location do people of new york typically hangout between 9 pm and 2 am in both weekends and weekdays.

    	Technologies used: Hadoop Streaming with Python
	Visualization: R, QGIS . 


 
Data Set Links: 

Taxi data (yellow and green)
- http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

Taxi data 2010-2013
- https://uofi.app.box.com/NYCtaxidata

Uber Data
- https://github.com/fivethirtyeight/uber-tlc-foil-response

Weather Data
http://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets



Understanding The Data
	
For Uber We only have the data between April 2014 to September 2014 and January 2015 to  June 2015. We only have access to pickup date and pickup location.  
We employed the following methods to clean the data.
1)Cleaning the data:If there are any null values or outliers there,we first try to analyze and clean the data  using of various techniques(ignoring null values, replacing it with approximate values)   
2)Data transformation: Transform the PickUpDate, PickUpTime,DropOffDate,DropOffTime 
into DateTime EST format so that we’ll be able to take that format for analysis.
3)Data Reduction: All the data attributes which we think will not helpful to our analysis ,we will eliminate giving way only to the useful data for further analysis.
4)For some coordinates in spatial data we were getting boroughs as ‘Unknown’ so we neglected those coordinates.


Implementation Algorithm:

Question One
Issues:
In uber data the date Format is “mm/dd/yyyy” and  the date format in Taxi data is in “yyyy-mm-dd”.  This can be resolved in our respective mapper code by using strftime method in Python.
For the year 2015 data we are not provided with the latitude and longitude of pickup location. We are only provided with the location ids. We are given corresponding zones and boroughs for that locationid.
In the Yellow and Green Taxi data we have some Outliers that lie outside NYC  some are 0,0 coordinates .We are trying to deal with that tuple either by removing it from our consideration or by just putting approximate value by seeing the PickUp Location and DropOff Location. 
One major issue we encountered for question 1 and question3 was how do we determine the borough from a given latitude and longitude. We planned to use geopy module which is python’s geocoding modules. But we decided against that as it took a lot of time to execute. We decided to use rtree indexing on zillowshapefile to identify the boroughs. This approach reduced the execution and query time significantly. Although we did use geopy module for generating corresponding latitude longitude pair from out lookup table.
In the shapefile record the LGA and JFK zone was missing so we used polygon contains method of the spatial lab to solve that problem. We verified the boundary given in the lab and it turned out to be correct.
Algorithms:
1a)  We first import datetime module of python. With the help of date time we extract the year and month from the datetime string. 
Mapper
For every record in uber,green taxi and yellow taxi file we take our key as Pickup month, Borough,tag. The tag can either be ‘y’, ‘g’ or ‘u’ for yellow taxi, green taxi or uber respectively. And our value will be 1. We employed rtree indexing on the shapefile to get respective borough by indexing pickup geolocation to RTree of New York shapefile. We queried the index with the help of the pickup  longitude and latitude.

Reducer.
We simply counted the amount of keys in our reducer side.  So our output will be pickup_month,borough,tag,count.  The tag identifies whether it is yellow or green taxi or uber and count is the amount of trips for that particular taxi in a particular borough for a particular month.


1b)
Mapper:
For this we faced a couple of issues. 
We wanted to see the distribution of uber, green taxi and yellow taxi on NYC map. But the precision level of longitudes and latitudes varied across the 3 datasets. We decided to use the precision level of upto 3 decimal places across all the datasets. This allowed us to approximate some coordinates.
The other issue that we faced was for the uber Jan-June 2015 data we were not given the pickup longitude and latitudes. We were given location ids and a lookup table to find out the zone and boroughs of respective location id. We decided to use geopy module of python to generate the longitude latitude pair from zone and boroughs. This is ill advised if the data set is too large but our lookup table had only 265 rows so we could complete finding longitude latitude pair in a reasonable amount of time. We generated 2 hash tables from lookup table one to determine the borough from the location id and other to determine the longitude latitude pair from location id. We stored the hash tables in our mapper file.
Algorithm:
Mapper
For each record we found the borough from rtree indexing of shapefile. We extracted the pickup month from pickup_datetime field. For every record we output pickup_month,borough,pickup_longitude,Pickup_latitude,tag as key and 1 as value.

Reducer
We simply add the values of each keys. As a result we get the count of pickups from a particular location for each month.
ques1c)
This was pretty much same as ques1a but instead of extracting the month we extracted the hour from the datetime. We also used the datetime module to determine if a given date is a weekday or a weekend. 
For mapper we emit (pickup_hour,Borough,tag,’weekday’ or ‘weekend’) as key and 1 as value
For reducer we count the keys.
Ques2)
2a)
Mapper 
If the input record is from green taxi or yellow taxi data set we emit the key as date and value as total_amount,tag where tag is either g or y. 
If the input record is from weather dataset then our key is date and our value is the remaining attributes other than date. 
Reducer
There will always be exactly one value for each key in the weather dataset. We store that value in a variable. We  add all the amounts in the reducer side for each key and tag and emit the key as the date and yellow taxi revenue along with green taxi revenue followed by the remaining attributes of weather data as the value.
2b)
Mapper
This is similar as 2a but we add the uber data as input also. Here if the input record is from uber, yellow taxi or green taxi we emit date as key and 1 as value followed by the tag. Rest of the code for weather data is same as 2a.
 Reducer
We separate the tags and the value for the taxi data and add all the ones for respective tags and emit the key as the date and the count of yellow taxi, green taxi,uber followed by all the fields of the weather data set as value.

Ques 3
We assumed the hours of 9pm-2am account for nightlife in NYC
Mapper 
In order to find out true nightlife zones we filtered out locations corresponding to both airports.
Here we extracted the pickup hour from dropoff datetime. We also extract the dropoff date from dropoff datetime in order to determine whether the date is a weekend or a weekday.
If the dropoff hour lies between 9 pm to 2 am we emit dropoff_hour,Borough,dropoff_longitude,dropoff_latitude,tag,weekend or weekday as key and 1 as value

Reducer
We simply count the number of keys at the reducer side.




