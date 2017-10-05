import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Config import *
from Model.Stream import Stream
from Model.Stream import Picture
from Model.Stream import User
from Controller.Common import authenticate
from google import datastore




# [START ViewStream]
class ViewStream(webapp2.RequestHandler):

# Note: use last_new_picture=datetime.datetime.now() to update the date.

    def get(self):
        # get stream id from somewhere
        # look up stream with that id from database
        # stream.get()?
        # create json output with the data
        # dump the json into the template html
        auth = authenticate(self)

        stream_name = self.request.get('stream_name')

        # TODO: For some reason stream = Stream.query(Stream.name == stream_name).get() does not work... fix it later
        for i in Stream.query().fetch():
            if i.name == stream_name:
                stream = i


        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
            'stream': stream,
        }
        template = JINJA_ENVIRONMENT.get_template('/Pages/ViewStream.html')
        self.response.write(template.render(template_values))

    def post(self):
        stream_name = self.request.get('stream_name')
        picture_name = self.request.get('name')
        picture = self.request.get('image')

        print "test"
        for i in Stream.query().fetch():
            if i.name == stream_name:
                stream = i

        test = gcs.upload_file()
        # write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        # gcs_file = gcs.open("test/",
        #                     'w',
        #                     content_type='text/plain',
        #                     options={'x-goog-meta-foo': 'foo',
        #                              'x-goog-meta-bar': 'bar'},
        #                     retry_params=write_retry_params)
        # gcs_file.write('abcde\n')
        # gcs_file.write('f' * 1024 * 4 + '\n')
        # gcs_file.close()

        new_picture = Picture(name=str(picture_name), image=str(picture)).put()

        stream.pictures.append(new_picture)
        stream.put()

        self.redirect('/ViewSingleStream?stream_name=' + stream_name)





        # get stream object from database...how?
        # create json with stream data

        # dump stream into json



# [END ViewStream]

