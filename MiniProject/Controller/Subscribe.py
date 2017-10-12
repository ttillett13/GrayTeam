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


class Subscribe(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()


            form_data = cgi.FieldStorage()
            requests = form_data.getlist("subscribe")
            stream_name = self.request.get('stream_name')
            status = self.request.get('stream_name')

            #stream = "dummy"
            for key_str in requests:
                key = ndb.Key(urlsafe=key_str)
                stream = key.get
                if not key in current_user.streams_subscribed:
                    current_user.streams_subscribed.append(key)
                    current_user.put()
                    time.sleep(.1)
                self.redirect('/ViewSingleStream?stream_name=' + stream_name + ";status=" + status)


            #self.redirect('/ManageStream')


