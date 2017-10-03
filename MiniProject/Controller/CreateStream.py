import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *

# [START error]
class CreateStream(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/Pages/CreateStream.html')
        self.response.write(template.render())

    # def post(self):
    #     # We set the same parent key on the 'Greeting' to ensure each
    #     # Greeting is in the same entity group. Queries across the
    #     # single entity group will be consistent. However, the write
    #     # rate to a single entity group should be limited to
    #     # ~1/second.
    #     guestbook_name = self.request.get('guestbook_name',
    #                                       DEFAULT_GUESTBOOK_NAME)
    #     greeting = Greeting(parent=guestbook_key(guestbook_name))
    #
    #     if users.get_current_user():
    #         greeting.author = Author(
    #             identity=users.get_current_user().user_id(),
    #             email=users.get_current_user().email())
    #
    #     greeting.content = self.request.get('content')
    #     greeting.put()
    #
    #     query_params = {'guestbook_name': guestbook_name}
    #     self.redirect('/?' + urllib.urlencode(query_params))
# [END error]