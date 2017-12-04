from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.conf import settings
import datetime

def random_string():
    return get_random_string(length=50)

##############################################################################################################
#
#
##############################################################################################################
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, default="", null=True)
    avatar = models.ImageField(default="", null=True)
    phone_number = models.CharField(max_length=12, default="")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# class LoggedInUser(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name='logged_in_user')


##############################################################################################################
#
#
##############################################################################################################
class Session(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey("CramCom.Group", default=-1)
    session_name = models.CharField(max_length=100)
    date_meeting = models.DateTimeField()
    link = models.URLField()
    description = models.TextField(default="")
    index = models.IntegerField(default=0)
    token = models.CharField(max_length=50, default=random_string)
    session_duration = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey("CramCom.Session", default=-1, null=True)
    order = models.IntegerField()
    filtered_order = models.IntegerField(null=True)
    title = models.TextField(default="")
    content = models.TextField(default="")
    #comments = models.ForeignKey("CramCom.Comment", default=-1)
    owner = models.ForeignKey(User, related_name="owner")
    #who_understands = models.ForeignKey(User, related_name="who_understands", null=True)
    who_understands = models.ManyToManyField(User, related_name="who_understands")
    date_created = models.DateTimeField()
    resolved = models.BooleanField(default=False)
    tags = ArrayField(
        models.TextField(null=True), null=True  #This will be a JSON of tags
    )
    progress_width = models.TextField(default="")
    index = models.IntegerField(default=0)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(default=0)
    subject = models.ForeignKey("CramCom.Subject", default=-1, null=True)
    commenter = models.ForeignKey(User)
    content = models.TextField(default="")
    date_created = models.DateTimeField()

class Group(models.Model):
    owner = models.ForeignKey(to=User, related_name="group_owner")
    subscribed = models.ManyToManyField(User, related_name="users_subscribed")
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    description = models.TextField(null=True)
    token = models.CharField(max_length=50 ,default=random_string)


class Link(models.Model):
    id = models.AutoField(primary_key=True)
    expiration_date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.TextField()
    display_text = models.CharField(max_length=100)
    link = models.URLField()
    group = models.ForeignKey('CramCom.Group', related_name="Group_link")



