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


import datetime
import cloudstorage
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

# [START ViewStream]
class ViewStream(webapp2.RequestHandler):
    def get(self):
        auth = authenticate(self)

        stream_name = self.request.get('stream_name')
        status = self.request.get('status')
        page = self.request.get('page')



        # TODO: For some reason stream = Stream.query(Stream.name == stream_name).get() does not work... fix it later
        for i in Stream.query().fetch():
            if i.name == stream_name:
                stream = i

        pics = []
        if stream.pictures:
            if not page:
                page = len(stream.pictures)
            page = int(page)
            if page == 0:
                page = len(stream.pictures)

            iter = 0
            for i in reversed(range(page - 3, page)):
                if iter < len(stream.pictures):
                    pic_temp = stream.pictures[i].get()
                    pics.append((pic_temp.name, images.get_serving_url(pic_temp.image, secure_url=False)))
                iter += 1
        else:
            page = 0

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
            'stream': stream,
            'pics': pics,
            'status': status,
            'page': page,
            'stream_name': stream.name
        }
        template = JINJA_ENVIRONMENT.get_template('/Pages/ViewStream.html')
        self.response.write(template.render(template_values))

    def post(self):
        stream_name = self.request.get('stream_name')
        picture_name = self.request.get('name')
        picture = self.request.get('image')
        comments = self.request.get('comments')
        decrementPage = self.request.get('decrementPage')
        standardPage = self.request.get('page')
        status = "success"

        if decrementPage:
            page = int(decrementPage) - 1
        else:
            page = int(standardPage) + 1

        #Check to see if image name already exists
        if not Picture.query(Picture.name == picture_name).fetch():

            for i in Stream.query().fetch():
                if i.name == stream_name:
                    stream = i

            #Write to gcs
            filename = '/{}/Pictures'.format(BUCKET_NAME) + "/" + picture_name

            with cloudstorage.open(filename, 'w', content_type='image/jpeg' ) as filehandle:
                filehandle.write(str(picture))

            blobstore_filename = '/gs{}'.format(filename)
            blob_key = blobstore.create_gs_key(blobstore_filename)

            #serving_url = images.get_serving_url(blob_key, secure_url=False)


            new_picture = Picture(name=str(picture_name), image=blob_key, comments=comments).put()

            #Update Stream
            stream.pictures.append(new_picture)
            stream.picture_count += 1
            stream.last_new_picture = datetime.datetime.now()
            stream.put()
        elif not decrementPage:
            status = "fail"

        self.redirect('/ViewSingleStream?stream_name=' + stream_name + ";status=" + status + ";page=" + str(page))




# [END ViewStream]

