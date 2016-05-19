Sahil Shah
Ajinkya Shukla
Fenil Tailor

 			              
                                                                                                                                                                                                                                                                           
Introduction: We are going to analyze the following questions with the help of this project. 

1)How does Uber and green taxi  arrival impact the  Yellow Taxi in New York?
Progression of rise of uber and green taxi in all 5 boroughs of New York City over the period of April 2014 to  June 2015.
Is there a particular area which is better served with the arrival of Uber and green taxi?
Do people prefer yellow taxi, green taxi and uber during a particular time of the day? Is there a clear favorite in any of the borough on different hours during the day.
2) How does the revenue of yellow taxi and green taxi vary for the year 2014 and is there a correlation between the weather and public holidays on the revenue? Do people prefer yellow taxi, uber or green taxi during extreme weathers.
3) Which are popular nightlife locations in New York city. At what location do people of new york typically hangout between 9 pm and 2 am in both weekends and weekdays.
4. Are there any locations in the city where citibikes are as fast as the yellow taxi both uptown and downtown? 

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

citibike Data:
https://www.citibikenyc.com/system-data

AWS Commands : 
We performed Hadoop streaming in AWS EMR cluster. We used 1 Master and 4 core nodes for ques 1a and ques 1c and 1 master and 7 core nodes for ques 1b and ques 3, 1 Master and 2 core nodes for question 2.

We needed to install rtree, libspatialindex and pyshp across all nodes. We did it by writing a shell script and installing it across all nodes in the bootstrapping stage. 
Example
We will show the implementation commands used for ques 1a here for reference.

* Termination protection: Yes
* Logging: Enabled (remember to input your S3 bucket to store log file)
* Hadoop distribution: Amazon 2.7.2
* Bootstrap action: This is a very important step because the sample scripts 
make use of python rtree library, but Amazon AMI 2.7.2 does not have rtree installed.
Click 'Add bootstrap action' -> Custom action -> Configure and add -> 
Put the following in 'S3 location': s3://safprojectbigdata/rtree.sh
* Don't add any step at this point
* Cluster Auto-terminate: No
Then we add the neighborhoods files that we use in our mapper to the S3 bucket.
neighborhoods: s3://safprojectbigdata/neighborhoods
Finally to generate output csv file
Replace safprojectbigdatawith your bucket name, except in Input
* Mapper: s3://safprojectbigdata/scripts/ques1a/map.py
* Reducer: s3://safprojectbigdata/scripts/ques1a/reduce.py
* Input: s3://safprojectbigdata/input/ques1/
* Output: s3://safprojectbigdata/ques1aoutputfinal
Arguments: -D mapred.reduce.tasks=1 -files s3://safprojectbigdata/scripts/ques1a/map.py,s3://safprojectbigdata/scripts/ques1a/reduce.py,s3://safprojectbigdata/neighborhoods/ZillowNeighborhoods-NY.shp,s3://safprojectbigdata/neighborhoods/ZillowNeighborhoods-NY.prj,s3://safprojectbigdata/neighborhoods/ZillowNeighborhoods-NY.shp.xml,s3://safprojectbigdata/neighborhoods/ZillowNeighborhoods-NY.shx,s3://safprojectbigdata/neighborhoods/ZillowNeighborhoods-NY.dbf -files s3://safprojectbigdata/scripts/ques1a/map.py,s3://safprojectbigdata/scripts/ques1a/reduce.py -mapper map.py 
 
Likewise we did for every questions. For question 2 we did not require any external library and thus skipped the bootstrapping shell script stage of rtree.sh. We used 2 reducers for every tasks. However this can be accomplished using any amount of reducers as the order is not important in the output file. 




