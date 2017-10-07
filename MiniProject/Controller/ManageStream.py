import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import cgi
import jinja2
import time
import webapp2

from Config import *

import json


from Model.Stream import Stream
from Model.Stream import User
from Controller.Common import authenticate

class ManageStream(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)
        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()


            if current_user:
                for key in current_user.streams_subscribed:
                    item = key.get()
                    if item == None:
                        current_user.streams_subscribed.remove(key)
                current_user.put()
                time.sleep(.1)


                streams_owned = [key.get() for key in current_user.streams_owned]
                streams_subscribed = [key.get() for key in current_user.streams_subscribed]

            else:
                streams_owned = []
                streams_subscribed = []


            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
                'streams_owned': streams_owned,
                'streams_subscribed': streams_subscribed
            }

            template = JINJA_ENVIRONMENT.get_template('/Pages/ManageStream.html')
            self.response.write(template.render(template_values))
