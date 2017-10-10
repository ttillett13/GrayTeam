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
    ('/ViewAllStream', ViewAllStream)
], debug=True)
# [END app]
