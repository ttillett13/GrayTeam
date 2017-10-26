import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import jinja2
import webapp2
import time
import random

from Config import *
from Model.Stream import Stream
from Model.Stream import Picture
from Model.Stream import User
from Controller.Common import authenticate
import json
from Controller.Common import json_serial


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
        if auth[0]:
            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
            }
            current_user = User.query(User.username == auth[0]._User__email).get()
            template_values = dict(template_values.items() + self.build_template(current_user, self.request, 3).items())


            template = JINJA_ENVIRONMENT.get_template('/Pages/ViewStream.html')
            self.response.write(template.render(template_values))

    @staticmethod
    def build_template(current_user, request, page_size):
        stream_name = request.get('stream_name')
        status = request.get('status')
        page = request.get('page')

        # TODO: For some reason stream = Stream.query(Stream.name == stream_name).get() does not work... fix it later
        for i in Stream.query().fetch():
            if i.name == stream_name:
                stream = i

        time = datetime.datetime.time(datetime.datetime.now())
        stream.view_times.append(time)
        stream.times_viewed = stream.times_viewed + 1
        stream.put()

        pics = []
        if stream.pictures:
            if not page:
                page = len(stream.pictures)
            page = int(page)
            if page == 0:
                page = len(stream.pictures)

            iter = 0
            for i in reversed(range(page - page_size, page)):
                if iter < len(stream.pictures):
                    pic_temp = stream.pictures[i].get()
                    pics.append((pic_temp.name, images.get_serving_url(pic_temp.image, secure_url=False)))
                iter += 1
        else:
            page = 0

        template_values = {
            'stream': stream,
            'pics': pics,
            'status': status,
            'page': page,
            'stream_name': stream.name
        }

        return template_values

    def post(self):
        auth = authenticate(self)
        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()
            template_values = dict(self.build_post_template(current_user, self.request).items())
            stream_name = template_values.get("name")
            status = template_values.get("status")
            page = template_values.get("page")
            self.redirect('/ViewSingleStream?stream_name=' + stream_name + ";status=" + status + ";page=" + str(page))  # [END ViewStream]

    @staticmethod
    def build_post_template(current_user, request):
        stream_name = request.get('stream_name')
        picture_name = request.get('name')
        picture = request.get('file')
        comments = request.get('comments')
        decrementPage = request.get('decrementPage')
        standardPage = request.get('page')
        latitude = request.get('latitude')
        if not latitude:
            latitude = random.uniform(-90, 90)
        else:
            latitude = int(latitude)

        longitude = request.get('longitude')
        if not longitude:
            longitude = random.uniform(-180, 180)
        else:
            longitude = int(longitude)

        status = "success"

        if decrementPage:
            page = int(decrementPage) - 1
        else:
            page = int(standardPage) + 1

        if page < 0:
            page = 0

        dt = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        # Check to see if image name already exists
        if picture_name and not Picture.query(
                        Picture.name == stream_name + "_" + str(picture_name) + "_" + dt).fetch():
            for i in Stream.query().fetch():
                if i.name == stream_name:
                    stream = i

            filename = '/{}/Pictures'.format(BUCKET_NAME) + "/" + stream_name + "_" + str(picture_name) + "_" + dt

            with cloudstorage.open(filename, 'w', content_type='image/jpeg') as filehandle:
                filehandle.write(str(picture))

            blobstore_filename = '/gs{}'.format(filename)
            blob_key = blobstore.create_gs_key(blobstore_filename)

            new_picture = Picture(name=stream_name + "_" + str(picture_name) + "_" + dt,
                                  image=blob_key, comments=comments,
                                  lat=latitude, lon=longitude,
                                  date_uploaded=datetime.datetime.today()).put()

            # Update Stream
            stream.pictures.append(new_picture)
            stream.picture_count += 1
            stream.last_new_picture = datetime.datetime.now()
            stream.put()
            time.sleep(1)
        elif not decrementPage:
            status = "fail"

        template_values = {
            'name': stream_name,
            'status': status,
            'page': page,
            'pic': ""
        }

        return template_values



class ViewStreamAPI(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'application/json'
        # self.response.out.write(json.dumps(ViewStream.build_template("test@example.com", self.request), default=json_serial))

        self.response.headers['Content-Type'] = 'application/json'
        json_data = ViewStream.build_template("test@example.com", self.request, 16)

        new_json = []
        for item in json_data['pics']:
            item_dict = {"name": json_data['stream_name'],
                            "pic": item[1],
                            "status": json_data['status'],
                            "page": json_data['page']}
            new_json.append(item_dict)
        self.response.out.write(json.dumps(new_json, default=json_serial))

    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.headers['Content-Type'] = 'application/json'
        json_data = dict(ViewStream.build_post_template("test@example.com", self.request))
        new_json = []
        new_json.append(json_data)
        self.response.out.write(json.dumps(new_json, default=json_serial))

