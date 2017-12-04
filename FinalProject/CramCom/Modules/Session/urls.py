from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^moveUp', views.move_up, name='move_up'),
    url(r'^moveDown', views.move_down, name='move_down'),
    url(r'^iKnow', views.i_know, name='i_know'),
    url(r'^complete', views.complete, name='complete'),
    url(r'^newSubject', views.new_subject, name='new_subject'),
    url(r'^postComment', views.post_comment, name='post_comment'),
    url(r'^getTags', views.get_tags, name='get_tags'),
    url(r'^update_study_session', views.update_study_session, name='get_subjects'),
    url(r'^getSubjects', views.get_subjects, name='get_subjects'),
    url(r'^Session', views.session, name='session'),
    url(r'^$', views.session, name='index'),
]
