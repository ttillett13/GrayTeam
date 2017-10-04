from Config import *
from Controller.CreateStream import CreateStream
from Controller.Error import Error
from Controller.ManageStream import ManageStream
from Controller.Common import authenticate

class MainPage(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)

        template_values = {
            'user': auth[0],
            'url': auth[1],
            'url_linktext': auth[2],
        }

        template = JINJA_ENVIRONMENT.get_template('/Pages/ManageStream.html')
        self.response.write(template.render(template_values))

                # guestbook_name = self.request.get('guestbook_name',
        #                                   DEFAULT_GUESTBOOK_NAME)
        # greetings_query = Greeting.query(
        #     ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        # greetings = greetings_query.fetch(10)
        #
        # user = users.get_current_user()
        # if user:
        #     url = users.create_logout_url(self.request.uri)
        #     url_linktext = 'Logout'
        # else:
        #     url = users.create_login_url(self.request.uri)
        #     url_linktext = 'Login'
        #
        # template_values = {
        #     'user': user,
        #     'greetings': greetings,
        #     'guestbook_name': urllib.quote_plus(guestbook_name),
        #     'url': url,
        #     'url_linktext': url_linktext,
        # }


# [END main_page]


# [START guestbook]
# class Guestbook(webapp2.RequestHandler):
#
#     def post(self):
#         # We set the same parent key on the 'Greeting' to ensure each
#         # Greeting is in the same entity group. Queries across the
#         # single entity group will be consistent. However, the write
#         # rate to a single entity group should be limited to
#         # ~1/second.
#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         greeting = Greeting(parent=guestbook_key(guestbook_name))
#
#         if users.get_current_user():
#             greeting.author = Author(
#                     identity=users.get_current_user().user_id(),
#                     email=users.get_current_user().email())
#
#         greeting.content = self.request.get('content')
#         greeting.put()
#
#         test = Picture(name="test", filepath="test.txt")
#         # test.content = self.request.get('content')
#         test.put()
#
#         query_params = {'guestbook_name': guestbook_name}
#         self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url(self.request.uri))

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/error', Error),
    ('/CreateStream', CreateStream),
    ('/ManageStream', ManageStream),
    ('/signin', SignInHandler)
], debug=True)
# [END app]
