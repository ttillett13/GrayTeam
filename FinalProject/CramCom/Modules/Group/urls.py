from django.conf.urls import url

from CramCom.Modules.Group import views

urlpatterns = [
    url(r'^StudyGroups', views.study_groups, name='StudyGroups'),
    url(r'^archived_groups', views.archived_groups, name='ArchivedGroups'),
    url(r'^archive_group', views.archive_group, name='ArchiveGroup'),
    url(r'^create_study_group', views.create_study_group, name='StudyGroupsForm'),
    url(r'^subscribe/$', views.subscribe, name='StudyGroupsForm'),
    url(r'^invite_members/$', views.invite_members, name='InviteMembers'),
    url(r'^create_study_session/$', views.create_study_session, name='CreateSession'),
    url(r'^update_study_group/$', views.update_study_group, name='UpdateStudyGroup'),
    url(r'^get_active_sessions/$', views.get_active_sessions, name='get_active_sessions'),
    url(r'^Sessions/addLink/$', views.add_link, name='add_link'),
    url(r'^Sessions/getLinks/$', views.get_links, name='get_links'),
    url(r'^Sessions/$', views.sessions, name='Sessions'),
]
