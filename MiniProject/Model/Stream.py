#!/usr/bin/env python
from Config import *
from google.appengine.ext import ndb
# [START Picture]
class Picture(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    image = ndb.BlobProperty(indexed=False)
    comments = ndb.TextProperty(indexed=False)

# [START Model]
class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    streams_owned = ndb.KeyProperty(kind='Stream', repeated=True)
    streams_subscribed = ndb.KeyProperty(kind='Stream', repeated=True)
    email = ndb.StringProperty(indexed=True)

# [START Model]
class Stream(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(indexed=True)
    times_viewed = ndb.IntegerProperty(indexed=False, default=0)
    tags = ndb.StringProperty(repeated=True)
    last_new_picture = ndb.DateProperty(indexed=False)
    pictures = ndb.KeyProperty(kind='Picture', repeated=True)
    picture_count = ndb.IntegerProperty(indexed=False)
    url = ndb.StringProperty(indexed=False)
    creation_time = ndb.DateTimeProperty(indexed=False)

