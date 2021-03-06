#!/usr/bin/env python
from Config import *
import datetime
from google.appengine.ext import ndb

# [START Picture]
class Picture(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    image = ndb.BlobProperty(indexed=False)
    comments = ndb.TextProperty(indexed=False)
    lat = ndb.FloatProperty(indexed=False)
    lon = ndb.FloatProperty(indexed=False)
    date_uploaded = ndb.DateTimeProperty(indexed=False)

# [START Model]
class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    streams_owned = ndb.KeyProperty(kind='Stream', repeated=True)
    streams_subscribed = ndb.KeyProperty(kind='Stream', repeated=True)
    email = ndb.StringProperty(indexed=True)
    report_sending=ndb.StringProperty(indexed=True)

# [START Model]
class Stream(ndb.Model):
    """Sub model for representing an author."""
    name = ndb.StringProperty(indexed=True)
    times_viewed = ndb.IntegerProperty(indexed=False, default=0)
    view_times = ndb.TimeProperty(repeated=True)
    #cover_picture = ndb.StringProperty(kind='Picture')
    tags = ndb.StringProperty(repeated=True)
    last_new_picture = ndb.DateProperty(indexed=False)
    pictures = ndb.KeyProperty(kind='Picture', repeated=True)
    picture_count = ndb.IntegerProperty(indexed=False)
    url = ndb.StringProperty(indexed=False)
    creation_time = ndb.DateTimeProperty(indexed=False)
    cover_page_url = ndb.StringProperty(indexed=False)
    distance = ndb.FloatProperty(indexed=False, default=0.0)

class TrendReport(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    html = ndb.StringProperty(indexed=False)

class AutocompleteIndex(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    values = ndb.StringProperty(repeated=True)



