import sys
sys.path.append('../service')
import urllib2
import ast
from redis_service import redis_service

class query_engine(object):
    def __init__(self):
        self.geo_information = {}
        self.forecast_api_key = '<replace_with_forecat.io_key>'
        self.forecast_api_prefix = 'https://api.forecast.io/forecast/'
        #Reduce the api response size & time for performance
        self.forecast_api_suffix  = '?exclude=minutely,hourly,daily,alerts,flags'
        self.freegeoip_url_prefix = 'http://freegeoip.net/json/'
        self.redis_service = redis_service()

    '''Returns the city,region clubbed under location along with the latitude and longitude'''
    def get_location_and_coordinates_from_ip(self,ip):
        location_and_coordinate_dict = {}
        location_and_coordinate_list = self.redis_service.get_location_and_coordinates_from_ip(ip)
        if location_and_coordinate_list:
            location_and_coordinate_dict['location'] = location_and_coordinate_list[0]
            location_and_coordinate_dict['latitude'] = location_and_coordinate_list[1]
            location_and_coordinate_dict['longitude'] = location_and_coordinate_list[2]
            return location_and_coordinate_dict
        else:
            geo_information = self.get_all_geo_information(ip)
            if  geo_information:    
                location_and_coordinate_dict['latitude'] = geo_information['latitude']
                location_and_coordinate_dict['longitude'] = geo_information['longitude']
                location_and_coordinate_dict['location'] = self.get_location()
                #cache this information, no  need to expire as this does not change
                self.redis_service.set_ip_to_location_and_coordinates(ip,location_and_coordinate_dict)
            return location_and_coordinate_dict

    '''Returns a json representation of the current weather at the given position'''        
    def get_weather_report(self,position={}):
        if position:
            latitude = str(position['latitude'])
            longitude = str(position['longitude'])
            location = str(position['location'])
            temp_cached = self.redis_service.get_temp_from_loc(location)
            weather_info_cached = {'currently':{}}
            if temp_cached:
                weather_info_cached['currently']['apparentTemperature'] = float(temp_cached) 
                return weather_info_cached
            else:
                pos_str = latitude+','+longitude
                request_str = self.forecast_api_prefix + self.forecast_api_key + '/' +pos_str + self.forecast_api_suffix
                req = urllib2.Request(request_str)
                response = urllib2.urlopen(req)
                #api returns a string
                weather_info = response.read()
                if weather_info:
                    weather_info_dict = ast.literal_eval(weather_info)
                    temp = 0.0
                    if weather_info_dict['currently']['apparentTemperature']:
                        temp = weather_info_dict['currently']['apparentTemperature']
                    else:
                        temp = weather_info_dict['currently']['temperature']
                    #set value to cache.
                    self.redis_service.set_loc_to_temp_with_expiration(location,temp)
                    return weather_info_dict
                else:
                    empty_weather_info = {}
                    return empty_weather_info

    '''Return all available geographic information based upon the ip'''
    def get_all_geo_information(self,ip):
        request_str = self.freegeoip_url_prefix + str(ip)
        req = urllib2.Request(request_str)
        response = urllib2.urlopen(req)
        #This api returns a dict in a string format
        geo_information_str = response.read()
        self.geo_information = ast.literal_eval(geo_information_str)
        return self.geo_information

    def get_location(self):
        if self.geo_information:
            loc_str = self.geo_information['city']+', '+self.geo_information['region_name']
            return loc_str 