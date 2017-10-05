import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import search

import jinja2
import webapp2
import datetime
import time
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

        stream_name = self.request.get('streamName')
        tag_stream = str(self.request.get('tagStream'))
        cover_image_url = str(self.request.get('coverImageUrl'))

        #Split the tags into a list
        tag_stream_list = tag_stream.split(',')


        #Make the Stream
        new_stream = Stream(name=stream_name, cover_image_url=cover_image_url, times_viewed=0,
                            tags=tag_stream_list, picture_count=0, url="/ViewSingleStream?stream_name=" + stream_name)
        new_stream.put()

        current_user = User.query(User.username==auth[0]._User__email).get()
        current_user.streams_owned.append(new_stream._entity_key)
        #current_user.streams_subscribed.append(new_stream._entity_key)
        current_user.put()
        #We actually have to wait for the transaction to take place... smh
        #Actual solution can be found https://stackoverflow.com/questions/15460926/google-app-engine-ndb-put-and-then-query-there-is-always-one-less-item
        # TODO: lets fix this later
        time.sleep(.1)
        subscriber_message = str(self.request.get('subscriberMessage'))
        subscribers = str(self.request.get('subscriber'))
        subscribers = subscribers.split(",")
        for subscriber in subscribers:
            user = User.query(User.username==subscriber).get()
            user.streams_subscribed.append(new_stream._entity_key)
            user.put()
        #print current_user.streams_owned
        #Send an invite to subscriber invites

        # need to also make a search api document
        d = search.Document(
            #doc_id=stream_name,
            fields=[search.TextField(name="stream_name", value=stream_name),
                    search.TextField(name="cover_image", value=cover_image_url)],
            language="en")
        try:
            search.Index(name=INDEX_NAME).put(d)
        except search.Error:
            self.redirect('/Error')

        self.redirect('/ManageStream')
