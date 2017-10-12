import os
import urllib
import cgi
import cloudstorage
import jinja2
import time
import webapp2
import json

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images


from Config import *

from Model.Stream import Picture
from Model.Stream import User
from Controller.Common import authenticate



class Delete(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()


            form_data = cgi.FieldStorage()
            requests = form_data.getlist("chkDeleteStream")
            index = search.Index(INDEX_NAME)

            for key_str in requests:
                key = ndb.Key(urlsafe=key_str)
                stream = key.get()
                for pic_key in stream.pictures:
                    picture = pic_key.get()
                    picture_name = picture.name
                    #pic_key = Picture.query(Picture.name == picture_name)
                    filename = '/{}/Pictures'.format(BUCKET_NAME) + "/" + picture_name
                    cloudstorage.delete(filename)
                    blob_key = picture.image
                    #image_url = get_serving_url(blob_key, size=450, crop=False, secure_url=True)
                    images.delete_serving_url(blob_key)
                    blobstore.delete(blob_key)
                    pic_key.delete()
                key.delete()
                index.delete(key_str)
                current_user.streams_owned.remove(key)

            else:
                self.redirect('/Error')
            current_user.put()
            time.sleep(.1)

            self.redirect('/ManageStream')

