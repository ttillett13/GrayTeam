from Config import *
from Controller.CreateStream import CreateStream
from Controller.Error import Error
from Controller.ManageStream import ManageStream
from Controller.SearchStream import AutoComplete, AutoCompleteCreation, SearchStream
from Controller.Delete import Delete
from Controller.TrendingStreams import TrendingStreams, TrendingReport
from Controller.Subscribe import Subscribe
from Controller.Unsubscribe import Unsubscribe
from Controller.ViewStream import ViewStream
from Controller.ViewAllStream import ViewAllStream
from Controller.ViewAllStream import ViewAllStreamsAPI
from Controller.GeoView import GeoView
from Controller.ViewStream import ViewStreamAPI
#from Controller.TrendingStreams import TrendingAPI
from Controller.SearchStream import SearchStreamAPI
#from Controller.NearbyStream import NearbyStreamAPI
from Controller.ManageStream import ManageStreamAPI
from Controller.GeoView import GeoViewAPI


import webapp2
from Controller.Common import authenticate

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url(self.request.uri))

# [START app]
app = webapp2.WSGIApplication([
    ('/', ManageStream),
    ('/AutoComplete', AutoComplete),
    ('/AutoCompleteCreation', AutoCompleteCreation),
    ('/CreateStream', CreateStream),
    ('/Delete', Delete),
    ('/Error', Error),
    ('/ManageStream', ManageStream),
    ('/SearchStream', SearchStream),
    ('/signin', SignInHandler),
    ('/TrendingStreams', TrendingStreams),
    ('/Subscribe', Subscribe),
    ('/Trending/Report', TrendingReport),
    ('/Unsubscribe', Unsubscribe),
    ('/ViewSingleStream', ViewStream),
    ('/ViewAllStream', ViewAllStream),
    ('/GeoView', GeoView),
    ('/ViewAllStream/api', ViewAllStreamsAPI),
    ('/ViewSingleStream/api', ViewStreamAPI),
    #('/Trending/api', TrendingAPI),
    ('/SearchStream/api', SearchStreamAPI),
    #('/NearbyStream/api', NearbyStreamAPI),
    ('/ManageStream/api', ManageStreamAPI),
    ('/GeoView/api', GeoViewAPI),
], debug=True)
# [END app]
