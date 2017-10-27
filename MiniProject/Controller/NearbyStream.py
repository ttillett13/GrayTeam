import webapp2

from Config import *
from Model.Stream import Stream
from Model.Stream import User
from Controller.Common import authenticate
#import geopy.distance
from math import radians, sin, cos, acos
from google.appengine.api import images
import json
from Controller.Common import json_serial


class NearbyStream(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)
        if auth[0]:
            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
            }
            current_user = User.query(User.username == auth[0]._User__email).get()
            template_values = dict(template_values.items() + self.build_template(current_user, self.request).items())
            template = JINJA_ENVIRONMENT.get_template('/Pages/ViewAllStream.html')
            self.response.write(template.render(template_values))

    @staticmethod
    def build_template(current_user, request):
            raw_streams = Stream.query().fetch()
            longitude = float(request.get('longitude'))
            latitude = float(request.get('latitude'))

            pictures = []
            if raw_streams:
                for stream in raw_streams:
                    isSet = False
                    short_distance = 0.0
                    if stream.pictures:
                        for item in stream.pictures:
                            picture = item.get()
                            lon = picture.lon
                            lat = picture.lat

                            distance =6371.01 * acos(sin(latitude)*sin(lat) + cos(latitude)*cos(lat)*cos(longitude - lon))
                            distance= distance * 0.621371

                            stream_to_append = [stream.name,
                                                images.get_serving_url(picture.image, secure_url=False),
                                                stream.url,
                                                stream.creation_time,
                                                distance]

                            pictures.append(stream_to_append)

            pictures = sorted(pictures, key=lambda x: x[4])
            template_values = {

                'pictures': pictures
            }

            return template_values


class NearbyStreamAPI(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            json_data = NearbyStream.build_template("test@example.com", self.request)
            new_json = []
            for item in json_data['pictures']:
                item_dict = {"name": item[0],
                            "url": item[1],
                            "path": item[2],
                            "datetime": item[3],
                            "distance":item[4]}
                new_json.append(item_dict)
            self.response.out.write(json.dumps(new_json, default=json_serial))

