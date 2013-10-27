wearthejacket is a weather decision engine which makes a simple decision,
"To wear a jacket or not" based on prevailing conditions at the end users location.

The application is test driven and tests can be run from the tests folder with invocation
python 

The design is pretty modular so components can be used as libraries.
The query_engine is the interface to the external geo-location[freegeoip.net] and weather api.[forecast.io]
Note that you will have to independently obtain a forecast.io api key for the application to work. 
Prerequisite:
python,tornado,redis
pip install tornado
Get redis from http://redis.io/

Usage as server:
Make sure you have a redis instance setup.
cd server
python weather_server.py
You can now receive requests on port 8888.


Usage as library:
from query_engine import query_engine
from decision_engine import decision_engine

qe = query_engine()
#Returns a dictionary of latitude longitude and location.
pos = qe.get_latitude_and_longitude_from_ip(<give_some_valid_ip_here>)

#Fetches the weather report based on the postion dictionary
weather_report = qe.get_weather_report(pos)

de = decision_engine()
#Takes the decision based on the weather report.
de.get_decision(weather_report) 



Feel free to send out any questions at hershvd@gmail.com