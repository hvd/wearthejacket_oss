import redis

class redis_service:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.conn = redis.Redis(connection_pool=self.pool)
        self.ip_to_loc_hash_prefix = 'ip_to_location:'
        self.loc_to_temp_prefix = 'loc_to_temp:'

    '''Set location to temperature mapping, This is a redis key of form ip_to_location:<location> temperature'''
    def set_loc_to_temp_with_expiration(self,location,temp,expire=180):
        #We cache values for 20 minutes
        loc_to_temp_key = self.loc_to_temp_prefix  + location
        self.conn.setex(loc_to_temp_key,temp,expire)

    '''We maintain the list of ips that we geo-located to avoid making api calls for them,
       The incoming location is a dictionary containing location, latitude and longitude.
       We store this as a redis hash ip_to_location:<location> latitude:val longitude:val location:val '''
    def set_ip_to_location_and_coordinates(self,ip,location):
        key = self.ip_to_loc_hash_prefix  + ip
        response = self.conn.hmset(key,location)

    '''Get the temperature based on location key 'loc_to_temp:<location>'''
    def get_temp_from_loc(self,loc):
        key = self.loc_to_temp_prefix + loc
        temp_str = self.conn.get(key)
        if temp_str is not None:
            temp = float(temp_str)
            return temp
        else:
            return None
    
    '''Returns a list of location,latitude and longitude in order requested phew! That is also the expected behavior as per redis documentation.'''
    def get_location_and_coordinates_from_ip(self,ip):
        key = self.ip_to_loc_hash_prefix + ip
        val =  self.conn.hmget(key,'location','latitude','longitude')
        if not any(val):
            return None
        else:
            return val

    def get_location_from_ip(self,ip):
        key = self.ip_to_loc_hash_prefix + ip
        return self.conn.hget(key,'location') 
