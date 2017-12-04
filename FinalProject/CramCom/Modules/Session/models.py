# from django.db import models
#
# ##############################################################################################################
# #
# #
# ##############################################################################################################
# class Session(models.Model):
#     id = models.IntegerField(primary_key=True)
#     subjects = models.ForeignKey("Subject")
#     session_name = models.CharField(max_length=100)
#     date_created = models.DateTimeField()
#     link = models.URLField()
#     description = models.TextField()
#
# class Subject(models.Model):
#     id = models.IntegerField(primary_key=True)
#     order = models.IntegerField()
#     content = models.TextField()
#     comments = models.ForeignKey("Comment")
#     owner = models.ForeignKey("CramCom.User")
#     who_understands = models.ForeignKey("CramCom.User")
#     date_created = models.DateTimeField()
#     resolved = models.BooleanField()
#     tags = models.TextField()  #This will be a JSON of tags
#
# class Comment(models.Model):
#     id = models.IntegerField(primary_key=True)
#     commenter = models.ForeignKey("CramCom.User")
#     content = models.TextField()
#     date_created = models.DateTimeField()
#
#
