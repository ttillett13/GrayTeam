import os
import urllib

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb

import cgi
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

        index = search.Index(INDEX_NAME)
        form_data = cgi.FieldStorage()
        query = form_data.getlist("search")

        if len(query) == 0:
            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
                # 'num_found': len(streams_found.results),
                'num_found': 0,
                'streams_found': []
            }

        else:
            streams_found = index.search(query[0])

            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
                'num_found': len(streams_found.results),
                'streams_found': enumerate(streams_found)
                #'num_found' : len(query),
                #enumerate = enumerate,
            }

        template = JINJA_ENVIRONMENT.get_template('/Pages/SearchStream.html')
        self.response.write(template.render(template_values))

        # { %
        # for stream in streams_found %}
        # < tr > {{stream.field("stream_name").value}} < / tr >
        # < br >
        # { % endfor %}
