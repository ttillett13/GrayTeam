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
        else:
            current_user = None
            self.redirect('/Error')

        form_data = cgi.FieldStorage()
        requests = form_data.getlist("subscribe")
        stream = "dummy"
        for key_str in requests:
            key = ndb.Key(urlsafe=key_str)
            stream = key.get
            if not key in current_user.streams_subscribed:
                current_user.streams_subscribed.append(key)
                current_user.put()
                time.sleep(.1)

        self.redirect('/ManageStream')
        #self.redirect(
              #      '/ViewSingleStream?stream_name=' + stream.name + ";status=" + stream.status + ";page=" + str(page))


