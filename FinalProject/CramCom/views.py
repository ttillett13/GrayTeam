from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect



User = get_user_model()


# @login_required(login_url='/log_in/')
def user_list(request):
    """
    NOTE: This is fine for demonstration purposes, but this should be
    refactored before we deploy this app to production.
    Imagine how 100,000 users logging in and out of our app would affect
    the performance of this code!
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/Groups/StudyGroups')
    else:
        # users = User.objects.select_related('logged_in_user')
        # for user in users:
        #     user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
        return render(request, 'splash.html', {'users': "test"})
