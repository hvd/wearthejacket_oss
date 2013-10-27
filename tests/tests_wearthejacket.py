import unittest
import sys
sys.path.append('../service')
sys.path.append('../server')
sys.path.append('../rules')
from query_engine import query_engine
from decision_engine import decision_engine
from redis_service import redis_service
import time


class tests_wearthejacket(unittest.TestCase):
    #Assign the self.ip with a valid ip address and have a redis instance running before running the tests.
    def setUp(self):
        self.ip = '<replace_with_some_ip>'
        self.qe = query_engine()
        self.pos = self.qe.get_location_and_coordinates_from_ip(self.ip)
        #print self.pos
        self.de = decision_engine()
        self.redis_service = redis_service()

    #The values are already computed in the setup step from the ip.
    def test_get_coordinates_and_location_from_ip(self):
        length = len(self.pos)
        self.assertEqual(length,3)

    def test_get_weather_report(self):
        weather_report = self.qe.get_weather_report(self.pos)
        self.assertTrue(weather_report)

    #Tests for the decision_engine and the query_engine
    def test_get_decision(self):
        weather_report = self.qe.get_weather_report(self.pos)
        decision = self.de.get_decision(weather_report)
        print decision
        self.assertTrue(decision)


    def test_get_all_geo_information(self):
        geo_info = self.qe.get_all_geo_information(self.ip)
        self.assertTrue(geo_info)
        print geo_info

    def test_get_location(self):
        location = self.pos['location']
        print location
        self.assertTrue(location)

    #Tests for the Redis Service
    def test_set_loc_to_temp_with_expiration(self):
        location = 'loc'
        expiration = 10
        temperature = 100
        self.redis_service.set_loc_to_temp_with_expiration(location,temperature,expiration)
        val = self.redis_service.get_temp_from_loc(location)
        self.assertTrue(val is not None)
        print 'sleeping for 10 seconds to check expiry'
        time.sleep(10)
        val = self.redis_service.get_temp_from_loc(location)
        self.assertTrue(val is None)


    #Tests for uncertainity, TODO
    def test_fetch_weather_report_from_api_when_api_down(self):
        pass

    def test_get_location_from_ip_returns_null(self):
        #accounted for in the server code
        pass

    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()
