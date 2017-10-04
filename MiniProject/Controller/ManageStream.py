import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *
import json

from Model.Stream import Stream
from Controller.Common import authenticate

class ManageStream(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
        }

        if users.get_current_user():
            print(users.get_current_user())
        template = JINJA_ENVIRONMENT.get_template('/Pages/ManageStream.html')
        self.response.write(template.render(template_values))


