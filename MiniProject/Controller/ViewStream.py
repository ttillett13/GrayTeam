import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *

# [START ViewStream]
class ViewStream(webapp2.RequestHandler):

    def get(self):
        # get stream id from somewhere
        # look up stream with that id from database
        # stream.get()?
        # create json output with the data
        # dump the json into the template html
        template = JINJA_ENVIRONMENT.get_template('/Pages/ViewStream.html')
        self.response.write(template.render())

    def post(self):
        # get stream id from the form
        stream_id = self.request.get('stream_id')
        # get stream object from database...how?
        # create json with stream data

        # dump stream into json
        stream = "stuff"


# [END ViewStream]