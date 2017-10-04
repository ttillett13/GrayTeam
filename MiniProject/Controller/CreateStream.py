import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *
import json

from Model.Stream import Stream

class CreateStream(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/Pages/CreateStream.html')
        self.response.write(template.render())

    def post(self):
        subscriber = str(self.request.get('subscriber'))
        subscriber_message = str(self.request.get('subscriberMessage'))
        stream_name = self.request.get('streamName')
        tag_stream = str(self.request.get('tagStream'))
        cover_image_url = str(self.request.get('coverImageUrl'))

        #Split the tags into a list
        #convert it to a json object
        tag_stream_list = tag_stream.split(',')


        #Make the Stream
        new_stream = Stream(name=stream_name, cover_image_url=cover_image_url,
                            tags=tag_stream_list)
        new_stream.put()

        #Send an invite to subscriber invites


        #query_params = {'guestbook_name': guestbook_name}
        self.redirect('/ManageStream')
