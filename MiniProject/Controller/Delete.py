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

class Delete(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()
        else:
            current_user = None
            self.redirect('/Error')

        form_data = cgi.FieldStorage()
        requests = form_data.getlist("chkDeleteStream")
        for key_str in requests:
            key = ndb.Key(urlsafe=key_str)
            key.delete()
            current_user.streams_owned.remove(key)

        else:
            self.redirect('/Error')
        current_user.put()
        time.sleep(.1)

        self.redirect('/ManageStream')

