import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *
from Controller.Common import authenticate

from Model.Stream import User
# [START error]
class TrendingStreams(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
        }

        template = JINJA_ENVIRONMENT.get_template('/Pages/TrendingStreams.html')
        self.response.write(template.render(template_values))

    def post(self):

        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()
        else:
            current_user = None
            self.redirect('/Error')

        email_sending= self.request.get('onetype')
        current_user.report_sending=email_sending
        current_user.put()

        self.redirect('/TrendingStreams')
 # [END error]