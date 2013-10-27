import sys
sys.path.append('../rules')
import tornado.ioloop
import tornado.web
from decision_engine import decision_engine
from query_engine import query_engine

class MainHandler(tornado.web.RequestHandler):
    '''This is the entry point to the tornado server.'''
    def get(self):
        remote_ip = self.request.remote_ip
        if remote_ip:
            qe = query_engine()
            pos = qe.get_location_and_coordinates_from_ip(remote_ip)
            if pos:
                location = pos['location']
                if not location:
                    location = 'unknown'
                weather_report = qe.get_weather_report(pos)
                if weather_report:
                    de = decision_engine()
                    decision = de.get_decision(weather_report)
                    if decision is not None:
                        self.write(decision + ' visitor from ' + location +'.')
                        self.write('\n')
                    else:
                        self.write('The weather algorithm has no decision, you are on your own.')
                else:
                    self.write("We couldn't get a weather report for this location, try later")
            else:
                self.write("Apologies, Could not geolocate your machine.")
        else:
            self.write("Hmm you don't seem to have an ip, what goes?.")
        
application = tornado.web.Application([(r"/", MainHandler)])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
