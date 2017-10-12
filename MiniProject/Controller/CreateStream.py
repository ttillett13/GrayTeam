import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import search

import jinja2
import webapp2
import datetime
import re
import time
from Config import *
import json

from Model.Stream import Stream
from Controller.Common import authenticate
from Model.Stream import User
import sendgrid
from sendgrid.helpers.mail import *

class CreateStream(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        if auth[0]:
            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
            }

            template = JINJA_ENVIRONMENT.get_template('/Pages/CreateStream.html')
            self.response.write(template.render(template_values))

    def post(self):
        auth = authenticate(self)
        if auth[0]:

            stream_name = self.request.get('streamName')
            tag_stream = str(self.request.get('tagStream'))
            cover_image_url = str(self.request.get('coverImageUrl'))

            tag_stream_list = []
            if tag_stream:
                tag_stream_list = re.split(',\s*', tag_stream)
                # check if tags are valid
                for tag in tag_stream_list:
                    if not re.match("^#\w+$", tag) or " " in tag:
                        self.redirect('/Error')
                        return

            # check if stream name is valid
            old_stream = Stream.query(Stream.name == stream_name).get()
            if old_stream:
                self.redirect('/Error')
                return

            #Make the Stream
            new_stream = Stream(name=stream_name, times_viewed=0, view_times=[],
                                tags=tag_stream_list, picture_count=0, url="/ViewSingleStream?stream_name=" + stream_name,
                                creation_time=datetime.datetime.now())
            if cover_image_url:
                new_stream.cover_page_url = cover_image_url
            new_stream.put()

            current_user = User.query(User.username==auth[0]._User__email).get()
            current_user.streams_owned.append(new_stream._entity_key)
            current_user.put()
            #We actually have to wait for the transaction to take place... smh
            #Actual solution can be found https://stackoverflow.com/questions/15460926/google-app-engine-ndb-put-and-then-query-there-is-always-one-less-item
            # TODO: lets fix this later
            time.sleep(.1)
            subscribers = str(self.request.get('subscriber'))
            subscribers = subscribers.split(",")

            sg = sendgrid.SendGridAPIClient(
                apikey="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")
            from_email = Email("jomish2323@gmail.com")

            for subscriber in subscribers:
                user = User.query(User.username==subscriber).get()
                if not user is None:
                    user.streams_subscribed.append(new_stream._entity_key)
                    user.put()

                    # Send an email
                    to_email = Email(user.email)
                    subject = "You've been subscribed!"
                    content = Content("text/plain", str(self.request.get('subscriberMessage')))
                    mail = Mail(from_email, subject, to_email, content)
                    response = sg.client.mail.send.post(request_body=mail.get())

            # need to also make a search api document
            d = search.Document(
                doc_id=new_stream.key.urlsafe(),
                fields=[search.TextField(name="stream_name", value=stream_name),
                        search.TextField(name="cover_image", value=cover_image_url),
                        search.TextField(name="url", value=new_stream.url),
                        search.TextField(name="tag", value=tag_stream.replace(",", " ").replace("#", ""))],
                language="en")
            try:
                search.Index(name=INDEX_NAME).put(d)
            except search.Error:
                self.redirect('/Error')

            self.redirect('/ManageStream')
