import re
import os
import urllib

from google.appengine.api import images
from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb

import cgi
import jinja2
import json
import webapp2

from Config import *
import json
from Controller.Common import json_serial

from Model.Stream import AutocompleteIndex, Stream, User
from Controller.Common import authenticate
from Model.Stream import User
from Model.Stream import Picture
import datetime
from Common import *


class GeoView(webapp2.RequestHandler):
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



            template = JINJA_ENVIRONMENT.get_template('/Pages/GeoView.html')
            self.response.write(template.render(template_values))

    @staticmethod
    def build_template(current_user, request):
        stream_name = request.get('stream_name')
        # pictures = Picture.query().fetch()
        stream = Stream.query(Stream.name == stream_name).get()
        new_pictures = []
        for picture in stream.pictures:
            pic_temp = picture.get()
            new_pictures.append({'image': images.get_serving_url(pic_temp.image, secure_url=False),
                                 'lat': pic_temp.lat, 'lon': pic_temp.lon,
                                 'date_uploaded': pic_temp.date_uploaded.strftime('%Y.%m.%d')})

        form_data = cgi.FieldStorage()

        today = date.today()

        template_values = {
            'pictures': new_pictures,
            'cur_date': today.strftime('%Y.%m.%d'),
            'prev_date': add_years(today, -1).strftime('%Y.%m.%d')
        }
        return template_values

class GeoViewAPI(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(GeoView.build_template("test@example.com", self.request), default=json_serial))