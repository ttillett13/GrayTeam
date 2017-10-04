import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *
import json

from Model.Stream import Stream

class ManageStream(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/Pages/ManageStream.html')
        self.response.write(template.render())


