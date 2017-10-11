import re
import os
import urllib

from google.appengine.api import images
from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb

import cgi
import jinja2
import json
import webapp2

from Config import *

from Model.Stream import AutocompleteIndex, Stream, User
from Controller.Common import authenticate
from Model.Stream import User
from Model.Stream import Picture
import datetime
from Common import *


class SearchStream(webapp2.RequestHandler):



    def get(self):
        auth = authenticate(self)

        if auth[0]:
            current_user = User.query(User.username == auth[0]._User__email).get()
            pictures = Picture.query().fetch()
            new_pictures = []
            for picture in pictures:
                new_pictures.append({'image': images.get_serving_url(picture.image, secure_url=False),
                                     'lat': picture.lat, 'lon': picture.lon,
                                     'date_uploaded': picture.date_uploaded.strftime('%Y.%m.%d')})


            index = search.Index(INDEX_NAME)
            form_data = cgi.FieldStorage()
            query_string = form_data.getlist("search")

            today = datetime.date.today()

            if len(query_string) == 0:
                template_values = {
                    'user': auth[0],
                    'url': auth[1],
                    'url_linktext': auth[2],
                    # 'num_found': len(streams_found.results),
                    'num_found': 0,
                    'streams_found': [],
                    'pictures': new_pictures,
                    'cur_date': today.strftime('%Y.%m.%d'),
                    'prev_date': add_years(today, -1).strftime('%Y.%m.%d')
                }

            else:
                query_options = search.QueryOptions(limit=5)
                query = search.Query(query_string=query_string[0], options=query_options)
                streams_found = index.search(query)
                num_found = len(streams_found.results)

                for stream in streams_found.results:
                    if not stream.field('cover_image').value:
                        #key_str = stream.doc_id.value
                        #key = ndb.Key(urlsafe=key_str)
                        #stream_obj = key.get
                        #current_user = User.query(User.username == auth[0]._User__email).get()

                        stream_obj = Stream.query(Stream.name == stream.field('stream_name').value).get()
                        if stream_obj:
                            if stream_obj.pictures:
                                cover_image = images.get_serving_url(stream_obj.pictures[0].get().image,
                                                                     secure_url=False)
                                d = search.Document(
                                    doc_id=stream.doc_id,
                                    fields=[search.TextField(name="stream_name", value=stream_obj.name),
                                        search.TextField(name="cover_image", value=cover_image),
                                        search.TextField(name="url", value=stream_obj.url),
                                        search.TextField(name="tag", value=stream.field('tag').value)],
                                    language="en")
                                search.Index(name=INDEX_NAME).put(d)

                streams_found = index.search(query)

                template_values = {
                    'user': auth[0],
                    'url': auth[1],
                    'url_linktext': auth[2],
                    'num_found': num_found,
                    'streams_found': enumerate(streams_found),
                    'pictures': pictures
                    #'num_found' : len(query),
                    #enumerate = enumerate,
                }

            template = JINJA_ENVIRONMENT.get_template('/Pages/SearchStream.html')
            self.response.write(template.render(template_values))

class AutoComplete(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        if auth[0]:
            index = AutocompleteIndex.query(AutocompleteIndex.name == AUTOCOMPLETE_INDEX).get()
            if index is None:
                data = []
            else:
                data = index.values

            data = json.dumps(data)
            self.response.out.write(data)


class AutoCompleteCreation(webapp2.RequestHandler):

    def get(self):
        streams = Stream.query()

        list = []
        for stream in streams:
            name_list = stream.name.split(" ")
            for name in name_list:
                name = name.lower()
                if not name in list:
                    list.append(name)
            for tag in stream.tags:
                #new_tag = tag[1:] # maybe I should leave the hashtag there?
                tag = tag.lower()
                if not tag in list:
                    list.append(tag)


        index = AutocompleteIndex.query(AutocompleteIndex.name == AUTOCOMPLETE_INDEX).get()
        if index:
            index.values = list
        else:
            index = AutocompleteIndex(name=AUTOCOMPLETE_INDEX, values=list)
        index.put()

        self.redirect('/SearchStream')
