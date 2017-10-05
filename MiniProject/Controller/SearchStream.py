import os
import urllib

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import json
import webapp2

from Config import *

from Model.Stream import Stream
from Controller.Common import authenticate
from Model.Stream import User

class SearchStream(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()
        else:
            current_user = None

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
        }

        template = JINJA_ENVIRONMENT.get_template('/Pages/SearchStream.html')
        self.response.write(template.render(template_values))

    def post(self):
        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()
        else:
            current_user = None

        index = search.Index(INDEX_NAME)
        streams_found = index.search("Tiffany")

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
            'streams_found': streams_found,
        }

        template = JINJA_ENVIRONMENT.get_template('/Pages/SearchStream.html')
        self.response.write(template.render(template_values))

        # { %
        # for stream in streams_found %}
        # < tr > {{stream.field("stream_name").value}} < / tr >
        # < br >
        # { % endfor %}
