import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *
from Model.Stream import Stream
from Model.Stream import Picture
from Model.Stream import User
from Controller.Common import authenticate


import datetime
import cloudstorage
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images


class ViewAllStream(webapp2.RequestHandler):
    def get(self):
        auth = authenticate(self)

        raw_streams = Stream.query().fetch()

        streams = []
        if raw_streams:
            for stream in raw_streams:
                if stream.pictures:
                    cover_image = stream.pictures[0].get()
                    streams.append((stream.name,
                                    images.get_serving_url(cover_image.image, secure_url=False),
                                    stream.url + ";status=success",
                                    stream.creation_time))

        streams = sorted(streams, key=lambda x: str(x[3]))
        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
            'streams': streams
        }
        template = JINJA_ENVIRONMENT.get_template('/Pages/ViewAllStream.html')
        self.response.write(template.render(template_values))


