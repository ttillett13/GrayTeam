from google.appengine.api import users

def authenticate(page):
    user = users.get_current_user()
    if user:
        url = users.create_logout_url(page.request.uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(page.request.uri)
        url_linktext = 'Login'

    return (user, url, url_linktext)