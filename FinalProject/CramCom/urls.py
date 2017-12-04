from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.contrib.auth.views import password_change, password_change_done
from django.views.generic.base import TemplateView
from solid_i18n.urls import solid_i18n_patterns


from . import views

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

# urlpatterns = [
#     #url(r'^accounts/login/', views.login),
#     url(r'^accounts/', include('allauth.urls')),
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^accounts/profile/$', TemplateView.as_view(template_name='profile.html')),
#
#
#
#     # url(r'^admin/logout/', logout, {'template_name': 'logged_out.html'}),
#     # url(r'^password_change/$', password_change, {'template_name': 'password_change_form.html'}, name='password_change'),
#     # url(r'^password_change/done/$', password_change_done, {'template_name': 'password_change_done.html'},name='password_change_done'),
#     url(r'^Groups/', include('CramCom.Modules.Group.urls')),
#     url(r'^Session/', include('CramCom.Modules.Session.urls')),
#     url(r'^$', views.user_list, name='index'),
#     ]



# urlpatterns = [
#     url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
#         home_files, name='home-files'),
# ]

urlpatterns = []
urlpatterns += solid_i18n_patterns(
    #url(r'^accounts/login/', views.login),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='profile.html')),



    # url(r'^admin/logout/', logout, {'template_name': 'logged_out.html'}),
    # url(r'^password_change/$', password_change, {'template_name': 'password_change_form.html'}, name='password_change'),
    # url(r'^password_change/done/$', password_change_done, {'template_name': 'password_change_done.html'},name='password_change_done'),
    url(r'^Groups/', include('CramCom.Modules.Group.urls')),
    url(r'^Session/', include('CramCom.Modules.Session.urls')),
    url(r'^$', views.user_list, name='index'),
)



admin.site.site_header = 'CramCom Administration'
