import webapp2

from Config import *
from Model.Stream import Stream
from Controller.Common import authenticate

from Controller.Common import json_serial
from google.appengine.api import images
import json


class ViewAllStream(webapp2.RequestHandler):
    def get(self):
        auth = authenticate(self)
        if auth[0]:
            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
            }
            template_values = dict(template_values.items() + self.build_template().items())
            template = JINJA_ENVIRONMENT.get_template('/Pages/ViewAllStream.html')
            self.response.write(template.render(template_values))

    @staticmethod
    def build_template():


            raw_streams = Stream.query().fetch()

            streams = []
            if raw_streams:
                for stream in raw_streams:
                    isSet = False
                    if stream.pictures:
                        cover_image = stream.pictures[0].get()
                        stream_to_append = [stream.name,
                                            images.get_serving_url(cover_image.image, secure_url=False),
                                            stream.url,
                                            stream.creation_time]
                        isSet = True
                    if stream.cover_page_url:
                        stream_to_append = [stream.name,
                                            stream.cover_page_url,
                                            stream.url,
                                            stream.creation_time]
                        isSet = True
                    if not isSet:
                        stream_to_append = [stream.name,
                                            "",
                                            stream.url,
                                            stream.creation_time]
                    streams.append(stream_to_append)

            streams = sorted(streams, key=lambda x: str(x[3]))
            template_values = {

                'streams': streams
            }

            return template_values

class ViewAllStreamsAPI(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(ViewAllStream.build_template(), default=json_serial))