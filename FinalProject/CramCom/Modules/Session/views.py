import time
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
import json
import re
import datetime
import pytz
from django.utils import timezone
import multiprocessing
from CramCom.Modules.Group.views import send_invite
from CramCom.models import Link
from datetime import date, timedelta
from CramCom.models import Comment, Group, Subject, Session

@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return HttpResponse("Hello")


def move_up(request):
    param_dict = request.POST
    sess_token = param_dict.__getitem__("token")
    my_session = Session.objects.get(token=sess_token)
    subj_id = param_dict.__getitem__("subject")
    tag = param_dict.__getitem__("filter_tag")
    subject = Subject.objects.get(id=subj_id)
    index = subject.filtered_order
    if index > 0:
        new_index = index - 1
        old_subject = Subject.objects.filter(filtered_order=new_index, session=my_session).get()
        old_subject.filtered_order = index
        subject.filtered_order = new_index
        subject.order = old_subject.order
        subject.save()
        while old_subject:
            subject = old_subject
            new_order = subject.order + 1
            old_subject = Subject.objects.filter(order=new_order, session=my_session)
            if old_subject:
                old_subject = old_subject.get()
            subject.order = new_order
            subject.save()

    #return get_subjects(request)
    return redirect('/Session?token=' + sess_token + ";tag=" + tag)


def move_down(request):
    param_dict = request.POST
    sess_token = param_dict.__getitem__("token")
    subj_id = param_dict.__getitem__("subject")
    tag = param_dict.__getitem__("filter_tag")
    subject = Subject.objects.get(id=subj_id)
    my_session = Session.objects.get(token=sess_token)
    max_index = my_session.subject_set.all().exclude(filtered_order=-1).count() -1
    index = subject.filtered_order
    if index < max_index:
        new_index = index + 1
        old_subject = Subject.objects.filter(filtered_order=new_index, session=my_session).get()
        old_subject.filtered_order = index
        subject.filtered_order = new_index
        subject.order = old_subject.order
        subject.save()
        while old_subject:
            subject = old_subject
            new_order = subject.order - 1
            old_subject = Subject.objects.filter(order=new_order, session=my_session)
            if old_subject:
                old_subject = old_subject.get()
            subject.order = new_order
            subject.save()

    #return get_subjects(request)
    return redirect('/Session?token=' + sess_token + ";tag=" + tag)

@login_required
def i_know(request):
    param_dict = request.POST
    sess_token = param_dict.__getitem__("token")
    subj_id = param_dict.__getitem__("subject")
    tag = param_dict.__getitem__("filter_tag")
    checked = param_dict.__contains__("know")
    subject = Subject.objects.get(id=subj_id)
    user = request.user
    my_session = Session.objects.get(token=sess_token)
    group = my_session.group
    num = group.subscribed.count() + 1
    if checked:
        subject.who_understands.add(user.id)
    else:
        subject.who_understands.remove(user.id)

    count = subject.who_understands.count()
    if count >= num:
        subject.resolved = True
    else:
        subject.resolved = False
    progress = count / num * 100
    subject.progress_width=str(progress) + "%"
    subject.save()

    #return get_subjects(request)
    return redirect('/Session?token=' + sess_token + ";tag=" + tag)


@login_required
def complete(request):
    param_dict = request.POST
    sess_token = param_dict.__getitem__("token")
    subj_id = param_dict.__getitem__("subject")
    tag = param_dict.__getitem__("filter_tag")
    checked = param_dict.__contains__("complete")
    subject = Subject.objects.get(id=subj_id)
    user = request.user
    my_session = Session.objects.get(token=sess_token)
    group = my_session.group
    error = False
    if user.id is group.owner.id:
        if checked:
            subject.resolved = True
        else:
            subject.resolved = False
        subject.save()
    else:
        error = True

    #return get_subjects(request)
    return redirect('/Session?token=' + sess_token + ";tag=" + tag + ";error=" + str(error))


@login_required
def new_subject(request):
    param_dict = request.POST
    sess_token = param_dict.__getitem__("token")
    title = param_dict.__getitem__("title")
    tag = param_dict.__getitem__("tags")
    tag = tag.lower()
    tags = tag.split()
    content = param_dict.__getitem__("content")
    curtime = datetime.datetime.now()
    user = request.user
    my_session = Session.objects.get(token=sess_token)
    order_index = my_session.index

    subject = Subject(order=order_index, date_created=curtime, title=title,
                      content=content, tags=tags, progress_width="0%", owner=user, session=my_session)
    subject.save()
    my_session.index = order_index + 1
    my_session.save()
    return redirect('/Session?token=' + sess_token)


@login_required
def post_comment(request):
    param_dict = request.POST
    sess_token = param_dict.__getitem__("token")
    subj_id = param_dict.__getitem__("subject")
    tag = param_dict.__getitem__("filter_tag")
    content = param_dict.__getitem__("comment")
    if len(content) > 0:
        curtime = datetime.datetime.now()
        user = request.user
        subject = Subject.objects.get(id=subj_id)
        order_index = subject.index
        comment = Comment(order=order_index, date_created=curtime, content=content, subject=subject, commenter=user)
        comment.save()
        subject.index = order_index+1
        subject.save()

    #return get_subjects(request)
    return redirect('/Session?token=' + sess_token + ";tag=" + tag)

def setup():
    curtime = datetime.datetime.now()
    group = Group(group_name="Dummy Group", date_created=curtime, description="some dummy description for dummy group")
    group.save()
    my_session = Session(group=group, session_name="Dummy Session", date_created=curtime,
                      link="dummy link", description="Some dummy description for dummy session")
    my_session.save()

def get_tags(request):
    token = request.GET['token']
    session = Session.objects.get(token=token)

    tags = []
    tags.append("all")

    subjects = session.subject_set.all()
    if subjects:
        for subject in subjects:
            subj_tags = subject.tags
            for tag in subj_tags:
                if tag not in tags:
                    tags.append(tag)


    context = {'tags': tags,
               'token': token,
               'description': session.description}
    return render(request, 'Navigation.html', context)

def get_subjects(request):
    if request.method == 'GET':
        param_dict = request.GET
    elif request.method == 'POST':
        param_dict = request.POST
    token = param_dict.__getitem__('token')
    filter_tag = param_dict.__getitem__('filter_tag')

    my_session = Session.objects.get(token=token)
    subjects = my_session.subject_set.all()

    filtered_subjects = []
    if subjects:
        subjects = sorted(subjects, key=lambda x: x.order)
        filtered_index = 0
        for subject in subjects:
            subj_tags = subject.tags
            found = False
            for tag in subj_tags:
                if tag == filter_tag:
                    found = True
            if filter_tag == "all" or found:
                filtered_subjects.append(subject)
                subject.filtered_order = filtered_index
                filtered_index += 1
            else:
                subject.filtered_order = -1
            subject.save()

    context = {'token': token,
               'filter_tag': filter_tag,
               'subjects': filtered_subjects}
    return render(request, 'Subject.html', context)

@login_required
def update_study_session(request):
    start_date_time = datetime.datetime.strptime(request.POST['study_session_date'], '%m/%d/%Y %I:%M %p')
    #group = Group.objects.filter(token=request.POST['group_token']).get()
    cur_session = Session.objects.filter(token=request.POST['token']).get()
    cur_session.session_name = request.POST['study_session_name']
    cur_session.description = request.POST['study_session_description']
    cur_session.session_duration = float(request.POST['study_session_duration'])
    cur_session.date_meeting = start_date_time
    cur_session.save()

    group = Group.objects.filter(token=request.POST['group_token']).get()
    # Get data for email
    user_list = list(group.subscribed.all())
    user_list.append(group.owner)

    links = list(Link.objects.filter(group=group).all())

    url_link = Link(display_text="Session",
                    link=request.build_absolute_uri('/')[:-1] + "/Session?token=" + cur_session.token)
    links = [url_link] + links

    tz = pytz.timezone("America/Chicago")
    start_date_time = tz.localize(start_date_time)

    p = multiprocessing.Process(target=send_invite, args=(({
        "to": [user.email for user in user_list],
        "subject": "\"" + group.group_name + "\" Study Session: \"" + cur_session.session_name + "\"",
        "location": "Remote Meeting",
        "describe": cur_session.description,
        "startDate": start_date_time.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"),
        "endDate": (start_date_time.astimezone(pytz.utc) + timedelta(hours=cur_session.session_duration)).strftime("%Y%m%dT%H%M%SZ"),
        'group_name': group.group_name,
        "links": links,
        "session_name": cur_session.session_name,
        "token": cur_session.token
    }),))
    p.start()

    # tz = pytz.timezone("America/Chicago")
    # start_date_time = tz.localize(start_date_time)
    #
    # if request.POST['email_list']:
    #     send_subscribtion_invite(filter_emails(group, request.POST['email_list'].split(';')),
    #                              group.group_name,
    #                              request.POST['email_message'],
    #                              request.build_absolute_uri('/Groups/subscribe') + '/?token=' + group.token)


    return redirect('/Session?token=' + request.POST['token'])

@login_required
def session(request):
    if request.method == "GET":
        param_dict = request.GET
    elif request.method == "POST":
        param_dict = request.POST
    # param_dict = request.GET
    #setup()
    sess_token = param_dict.__getitem__("token")
    if param_dict.__contains__("tag"):
        filter_tag = param_dict.__getitem__("tag")
    else:
        filter_tag = "all"
    if param_dict.__contains__("error"):
        error = param_dict.__getitem__("error")
    else:
        error = False
    session = Session.objects.get(token=sess_token)
    group = session.group
    title = group.group_name + ": " + session.session_name

    user = request.user
    users = []
    if user.id is not group.owner.id:
        users.append(group.owner)

    subscribed = group.subscribed.all()
    for subscriber in subscribed:
        if user.id is not subscriber.id:
            users.append(subscriber)

    #time = session.date_meeting.astimezone(pytz.utc)
    # tz = pytz.timezone("America/Chicago")
    # date_meeting = tz.localize(session.date_meeting)

    context = {'group_token': group.token,
               'token': sess_token,
               'title': title,
               'name': session.session_name,
               'filter_tag': filter_tag,
               'description': session.description,
               'user': user,
               'users': users,
               'error': error,
               'duration': session.session_duration,
               'date_meeting': datetime.datetime.strftime(session.date_meeting.astimezone(pytz.timezone("America/Chicago")), '%m/%d/%Y %I:%M %p')
               }
    # start_date_time.astimezone(pytz.utc)

    # session.date_meeting.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ")
    return render(request, 'Session.html', context)


