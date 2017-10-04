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
from Model.Stream import User

class CreateStream(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
        }

        template = JINJA_ENVIRONMENT.get_template('/Pages/CreateStream.html')
        self.response.write(template.render(template_values))

    def post(self):
        auth = authenticate(self)
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


        current_user = User.query(User.username==auth[0]._User__email).get()
        current_user.streams_owned.append(new_stream._entity_key)
        current_user.streams_subscribed.append(new_stream._entity_key)

        # if not current_user.streams_owned:
        #     current_user.streams_owned = [new_stream._entity_key]
        # else:
        #     current_user.streams_owned.append(new_stream._entity_key)
        #
        # if not current_user.streams_subscribed:
        #     current_user.streams_subscribed = [new_stream._entity_key]
        # else:
        #     current_user.streams_subscribed.append(new_stream._entity_key)

        current_user.put()
        #print current_user.streams_owned
        #Send an invite to subscriber invites


        #query_params = {'guestbook_name': guestbook_name}
        self.redirect('/ManageStream')
