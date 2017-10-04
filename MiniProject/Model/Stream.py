#!/usr/bin/env python
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

# [START Model]
class Stream(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(indexed=False)
    times_viewed = ndb.IntegerProperty(indexed=False, default=0)
    #cover_picture = ndb.StringProperty(kind='Picture')
    cover_image_url = ndb.StringProperty(indexed=False)
    tags = ndb.StringProperty(repeated=True)
