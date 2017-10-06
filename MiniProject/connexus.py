from Config import *
from Controller.CreateStream import CreateStream
from Controller.Error import Error
from Controller.ManageStream import ManageStream
from Controller.SearchStream import SearchStream
from Controller.Delete import Delete
from Controller.TrendingStreams import TrendingStreams
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
    ('/CreateStream', CreateStream),
    ('/Delete', Delete),
    ('/error', Error),
    ('/ManageStream', ManageStream),
    ('/SearchStream', SearchStream),
    ('/signin', SignInHandler),
    ('/Trending', TrendingStreams),
    ('/Unsubscribe', Unsubscribe),
    ('/ViewSingleStream', ViewStream),
    ('/ViewAllStream', ViewAllStream)
], debug=True)
# [END app]
