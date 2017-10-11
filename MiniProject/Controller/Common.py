from google.appengine.api import users
from Model.Stream import User
from Config import *
import datetime

def authenticate(page):
    user = users.get_current_user()
    if user:
        url = users.create_logout_url(page.request.uri)
        url_linktext = 'Logout'
        # If user does not exist on site, enroll user
        # TODO: Make this a separate page
        username = user.email.im_self._User__email
        site_users = User.query(User.username == username)
        site_users = site_users.get()
        if not site_users:

            new_user = User(username=username, email=username, streams_owned=[], streams_subscribed=[], report_sending="EveryDay")
            new_user.put()
    else:
        url = users.create_login_url(page.request.uri)
        url_linktext = 'Login'
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('/Pages/autherror.html')
        page.response.write(template.render(template_values))
        return (None, url, url_linktext)

    return (user, url, url_linktext)


# Got this from https://stackoverflow.com/questions/15741618/add-one-year-in-current-date-python
def add_years(d, years):

    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (datetime.date(d.year + years, 1, 1) - datetime.date(d.year, 1, 1))