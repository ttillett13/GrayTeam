from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from CramCom.models import Group
from CramCom.models import Session
from CramCom.models import Link
from CramCom.models import Subject
from django.core.mail import send_mail
from datetime import date, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django_gravatar.helpers import get_gravatar_url, has_gravatar, get_gravatar_profile_url, calculate_gravatar_hash
import multiprocessing

import pytz
from CramCom.Modules.Group.meetingInvite import send_invite
import datetime


def send_subscribtion_invite(email_list, group, message, url):
    email_message = ("You have been invited to join " + group +
                    "!\n Click the following link to subscribe this study group:\n" +
                    url + "\n\n" + message)

    send_mail(
        'CramCom - Invitation to join ' + group,
        email_message,
        'sourceiron.confirmation@gmail.com',
        email_list,
        fail_silently=False,)


def get_all_contacts(user):
    groups_subscribed = Group.objects.filter(subscribed=user).all()
    groups_owned = Group.objects.filter(owner=user).all()

    user_list = []

    for group in groups_subscribed:
        group_users = list(group.subscribed.all())
        group_users.append(group.owner)
        for group_user in group_users:
            if group_user not in user_list and group_user != user:
                user_list.append(group_user)

    for group in groups_owned:
        group_users = list(group.subscribed.all())
        group_users.append(group.owner)
        for group_user in group_users:
            if group_user not in user_list and group_user != user:
                user_list.append(group_user)

    return user_list


def get_group_contacts(user, group):
    user_list = []

    group_users = list(group.subscribed.all())
    group_users.append(group.owner)
    for group_user in group_users:
        if group_user not in user_list and group_user != user:
            user_list.append(group_user)

    return user_list


def filter_emails(group, email_list):
    new_email_list = []
    already_member_list = [group.owner.email]
    for member in group.subscribed.all():
        already_member_list.append(member.email)

    for email in email_list:
        if email not in already_member_list:
            new_email_list.append(email)

    return new_email_list


@login_required()
def archive_group(request):
    group = Group.objects.filter(token=request.POST['token']).get()

    group.expiration_date = date.today() - timedelta(1)
    group.save()

    return redirect('/Groups/StudyGroups')


@login_required
def study_groups(request):
    groups_owned = Group.objects.filter(owner_id=request.user.id)
    groups_subscribed = Group.objects.filter(subscribed=request.user.id)

    groups_owned_json = []
    for group in groups_owned:
        if group.owner:
            group_json = {}
            members = ""
            members += group.owner.get_full_name()
            for member in group.subscribed.all():
                members += (", " + member.get_full_name())
            group_json['group_name'] = group.group_name
            group_json['description'] = group.description
            group_json['token'] = group.token
            group_json['date_created'] = group.date_created
            group_json['members'] = members

            if group.expiration_date >= datetime.date.today():
                groups_owned_json.append(group_json)

    groups_subscribed_json = []
    for group in groups_subscribed:
        if group.subscribed:
            group_json = {}
            members = ""
            members += group.owner.get_full_name()
            for member in group.subscribed.all():
                members += (", " + member.get_full_name())
            group_json['group_name'] = group.group_name
            group_json['description'] = group.description
            group_json['token'] = group.token
            group_json['date_created'] = group.date_created
            group_json['members'] = members

            if group.expiration_date >= datetime.date.today():
                groups_subscribed_json.append(group_json)

    groups_owned_json.sort(key=lambda item: item['date_created'], reverse=True)
    groups_subscribed_json.sort(key=lambda item: item['date_created'], reverse=True)

    context = {'groups_owned': groups_owned_json,
               'groups_subscribed': groups_subscribed_json,
               'mode': "active",
               'users': get_all_contacts(request.user)}

    return render(request, 'StudyGroups.html', context)


@login_required
def create_study_group(request):
    if request.POST['expiration_date'] and request.POST['expiration_date']:

        description = request.POST['description']
        group = Group(group_name=request.POST['group_name'],
                      description=description,
                      owner=request.user,
                      expiration_date=request.POST['expiration_date'])
        group.save()

    if request.POST['email_list']:
        p = multiprocessing.Process(target=send_subscribtion_invite, args=(filter_emails(group, request.POST['email_list'].split(',')),
                                                                           group.group_name,
                                                                           request.POST['email_message'],
                                                                           request.build_absolute_uri('/Groups/subscribe') + '/?token=' + group.token))
        p.start()

    return redirect('/Groups/StudyGroups')


@login_required
def subscribe(request):
    user = request.user
    token = request.GET['token']
    group = Group.objects.filter(token=token).get()
    if user != group.owner:
        group.subscribed.add(user)
        return render(request, 'Subscribed.html')
    else:
        return redirect('/Groups/Sessions?token=' + token)


@login_required
def archived_groups(request):
    groups_owned = Group.objects.filter(owner_id=request.user.id)
    groups_subscribed = Group.objects.filter(subscribed=request.user.id)

    groups_owned_json = []
    for group in groups_owned:
        if group.owner:
            group_json = {}
            members = ""
            members += group.owner.get_full_name()  # (group.owner.first_name + " " + group.owner.last_name)
            group_json['group_name'] = group.group_name
            group_json['description'] = group.description
            group_json['token'] = group.token
            group_json['date_created'] = group.date_created
            group_json['members'] = members

            if group.expiration_date < datetime.date.today():
                groups_owned_json.append(group_json)

    groups_subscribed_json = []
    for group in groups_subscribed:
        if group.subscribed:
            group_json = {}
            members = ""
            members += group.owner.get_full_name()  # (group.owner.first_name + " " + group.owner.last_name)
            group_json['group_name'] = group.group_name
            group_json['description'] = group.description
            group_json['token'] = group.token
            group_json['date_created'] = group.date_created
            group_json['members'] = members

            if group.expiration_date < datetime.date.today():
                groups_owned_json.append(group_json)

    groups_owned_json.sort(key=lambda item: item['date_created'], reverse=True)
    groups_subscribed_json.sort(key=lambda item: item['date_created'], reverse=True)

    context = {'groups_owned': groups_owned_json,
               'groups_subscribed': groups_subscribed_json,
               'mode': "archived",
               'users': get_all_contacts(request.user)}

    return render(request, 'StudyGroups.html', context)


@login_required
def invite_members(request):
    token = request.POST['token']
    group = Group.objects.filter(token=token).get()

    p = multiprocessing.Process(target=send_subscribtion_invite,
                                args=(filter_emails(group, request.POST['email_list'].split(',')),
                                      group.group_name,
                                      request.POST['email_message'],
                                      request.build_absolute_uri('/Groups/subscribe') + '/?token=' + group.token))
    p.start()

    context = {'token': token,
               'group_name': group.group_name,
               'expiration_date': group.expiration_date.strftime('%Y-%m-%d'),
               'description': group.description,
               'users': get_group_contacts(request.user, group)}

    #return sessions(request)#render(request, 'Sessions.html', context)
    return redirect('/Groups/Sessions?token=' + token)


@login_required
def update_study_group(request):
    group = Group.objects.filter(token=request.POST['token']).get()
    if request.POST['group_name']:
        group.group_name = request.POST['group_name']
    if request.POST['description']:
        group.description = request.POST['description']
    if request.POST['expiration_date']:
        group.expiration_date = request.POST['expiration_date']
    group.save()

    return redirect('/Groups/Sessions?token=' + request.POST['token'])


@login_required
def sessions(request, token=None):
    if request.method == "GET":
        token = request.GET['token']
    elif request.method == "POST":
        token = request.POST['token']

    current_group = Group.objects.filter(token=token).get()
    sessions = Session.objects.filter(group=current_group)

    active_sessions_json = []
    completed_sessions_json = []
    for session in sessions:
        if session.group:
            session_json = {}
            session_json['session_name'] = session.session_name
            session_json['date_meeting'] = session.date_meeting.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Chicago")).strftime('%m/%d/%Y %I:%M %p')
            session_json['date_meeting_raw'] = session.date_meeting
            session_json['session_token'] = session.token
            session_json['answered_subjects'] = str(Subject.objects.filter(session=session, resolved=True).count())
            session_json['total_subjects'] = str(Subject.objects.filter(session=session).count())
            session_json['date_created'] = session.date_created

            if session_json['answered_subjects'] != session_json['total_subjects'] or session_json['total_subjects'] == "0":
                active_sessions_json.append(session_json)
            else:
                completed_sessions_json.append(session_json)

    links = Link.objects.filter(group=current_group).all()

    links_json = {}
    for link in links:
        links_json['link'] = link.link
        links_json['display_text'] = link.display_text

    #Sort the sessions
    if active_sessions_json:
        active_sessions_json.sort(key=lambda item: item['date_meeting_raw'], reverse=False)
    if completed_sessions_json:
        completed_sessions_json.sort(key=lambda item: item['date_meeting_raw'], reverse=False)

    context = {'token': token,
               'active_sessions': active_sessions_json,
               'completed_sessions': completed_sessions_json,
               'group_name': current_group.group_name,
               'expiration_date': current_group.expiration_date.strftime('%Y-%m-%d'),
               'description': current_group.description,
               'links': links_json,
               'users': get_group_contacts(request.user, current_group)}
    return render(request, 'Sessions.html', context)
    # # template = loader.get_template("")
    # return render_to_response('Sessions.html', context)

@login_required
def get_active_sessions(request):
    token = request.GET['token']

    current_group = Group.objects.filter(token=token).get()
    sessions = Session.objects.filter(group=current_group)

    active_sessions_json = []
    completed_sessions_json = []
    for session in sessions:
        if session.group:
            session_json = {}
            session_json['session_name'] = session.session_name
            session_json['date_meeting'] = session.date_meeting.replace(tzinfo=pytz.utc).astimezone(
                pytz.timezone("America/Chicago")).strftime('%m/%d/%Y %I:%M %p')
            session_json['date_meeting_raw'] = session.date_meeting
            session_json['session_token'] = session.token
            session_json['answered_subjects'] = str(Subject.objects.filter(session=session, resolved=True).count())
            session_json['total_subjects'] = str(Subject.objects.filter(session=session).count())
            session_json['date_created'] = session.date_created

            if session_json['answered_subjects'] != session_json['total_subjects'] or session_json[
                'total_subjects'] == "0":
                active_sessions_json.append(session_json)
            # else:
            #     completed_sessions_json.append(session_json)

    links = Link.objects.filter(group=current_group).all()

    links_json = {}
    for link in links:
        links_json['link'] = link.link
        links_json['display_text'] = link.display_text

    # Sort the sessions
    if active_sessions_json:
        active_sessions_json.sort(key=lambda item: item['date_meeting_raw'], reverse=False)
    if completed_sessions_json:
        completed_sessions_json.sort(key=lambda item: item['date_meeting_raw'], reverse=False)

    context = {'token': token,
               'active_sessions': active_sessions_json}
    return render(request, 'SessionTable.html', context)


def add_link(request):
    token = request.POST['token']

    url = request.POST['url'].replace("https://", '')
    url = url.replace("http://", '')
    current_group = Group.objects.filter(token=token).get()
    new_link = Link(link=url,
                    display_text=request.POST['display_text'],
                    group_id=current_group.id)
    new_link.save()

    links = Link.objects.filter(group_id=current_group.id).all()

    context = {'token': token,
               'links': links}
    return render(request, 'Links.html', context)


@login_required
def get_links(request):
    token = request.GET['token']

    current_group = Group.objects.filter(token=token).get()
    links = Link.objects.filter(group_id=current_group.id).all()

    context = {'links': links,
               'token': token}
    return render(request, 'Links.html', context)


@login_required
def create_study_session(request):
    start_date_time = datetime.datetime.strptime(request.POST['study_session_date'], '%m/%d/%Y %I:%M %p')
    group = Group.objects.filter(token=request.POST['token']).get()
    session = Session(session_name=request.POST['study_session_name'],
                      date_meeting=datetime.datetime.strptime(request.POST['study_session_date'], '%m/%d/%Y %I:%M %p'),
                      group=group,
                      session_duration=float(request.POST['study_session_duration']),
                      description=request.POST['description'])
    datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")

    # Get data for email
    user_list = list(group.subscribed.all())
    user_list.append(group.owner)

    links = list(Link.objects.filter(group=group).all())

    tz = pytz.timezone("America/Chicago")
    start_date_time = tz.localize(start_date_time)

    url_link = Link(display_text="Session", link=request.build_absolute_uri('/')[:-1] + "/Session?token=" + session.token)
    links = [url_link] + links

    p = multiprocessing.Process(target=send_invite, args=(({
        "to": [user.email for user in user_list],
        "subject": "\"" + group.group_name + "\" Study Session: \"" + session.session_name + "\"",
        "location": "Remote Meeting",
        "describe": session.description,
        "startDate": start_date_time.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"),
        "endDate": (start_date_time.astimezone(pytz.utc) + timedelta(hours=session.session_duration)).strftime("%Y%m%dT%H%M%SZ"),
        'group_name': group.group_name,
        "links": links,
        "session_name": session.session_name,
        "token": session.token
    }),))
    p.start()
    session.save()

    return redirect('/Groups/Sessions?token=' + group.token)
