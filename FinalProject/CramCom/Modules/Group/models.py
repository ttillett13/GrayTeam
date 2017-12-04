# from django.db import models
#
# ##############################################################################################################
# #
# #
# ##############################################################################################################
# class Group(models.Model):
#     id = models.IntegerField(primary_key=True)
#     session = models.ForeignKey("CramCom.Session")
#     group_name = models.CharField(max_length=100)
#     date_created = models.DateTimeField()
#     links = models.ForeignKey("Link")
#
# class Link(models.Model):
#     id = models.IntegerField(primary_key=True)
#     display_text = models.CharField(max_length=100)
#     link = models.URLField()
#
#
#
