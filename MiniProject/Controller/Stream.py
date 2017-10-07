#!/usr/bin/env python

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from Controller.Error import Error
from Controller.CreateStream import CreateStream
from Config import *


# [START Picture]
class Picture(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    filepath = ndb.StringProperty(indexed=False)

# [START Model]
class User(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    streams_owned = ndb.KeyProperty(kind='Stream')
    streams_subscribed = ndb.KeyProperty(kind='Stream')
    email = ndb.StringProperty(indexed=False)
    report_sending=ndb.StringProperty(indexed=False)

# [START Model]
class Stream(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(indexed=False)
    pictures = ndb.ListProperty()
    picture_count = ndb.IntegerProperty() # number of pictures in the stream
    times_viewed = ndb.IntegerProperty(indexed=False) # total times viewed for management page
    view_times = ndb.ListProperty() # the actual times, it was viewed to help with trending
    cover_picture = ndb.KeyProperty(kind='Picture')
