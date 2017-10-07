import os
import urllib

from google.appengine.api import search
from google.appengine.api import users
from google.appengine.ext import ndb

import datetime
import jinja2
import webapp2

from Config import *
from Controller.Common import authenticate
from Model.Stream import Stream,User,TrendReport

# [START TrendingStreams]
class TrendingStreams(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)
        if auth[0]:

            # index = search.Index(INDEX_NAME)
            # d = index.get(TREND_REPORT)
            #html_text = d.field("html").value

            report = TrendReport.query(TrendReport.name == TREND_REPORT).get()
            if report is None:
                message = "No report currently generated"
                template_values = {
                    'user': auth[0],
                    'url': auth[1],
                    'url_linktext': auth[2],
                    'html_text': message,
                }

                template = JINJA_ENVIRONMENT.get_template('/Pages/TrendingStreams.html')
                html_text = template.render(template_values)
            else:
                html_text = report.html

            self.response.write(html_text)

# [END TrendingStreams]


# [START TrendingReport]
class TrendingReport(webapp2.RequestHandler):

    def get(self):
        auth = authenticate(self)
        if auth[0]:

            time = datetime.datetime.time(datetime.datetime.now())
            hour = time.hour
            minute = time.minute

            if (hour > 0):
                hour_limit = hour - 1
            else:
                hour_limit = 23
            min_limit = minute

            streams = Stream.query()

            for stream in streams:
                view_times = stream.view_times
                for time in view_times:
                    if time.hour == 0:
                        hour = 24
                    else:
                        hour = time.hour
                    if hour < hour_limit or (time.minute <= min_limit and hour == hour_limit):
                        view_times.remove(time)
                stream.view_times = view_times
                stream.put()

            streams = Stream.query()

            streams = list(filter(lambda x: len(x.view_times) > 0, streams))
            sorted_streams = sorted(streams, key=lambda k: len(k.view_times), reverse=True)
            num = len(sorted_streams)
            title = "Top 3 Trending Streams"
            if num > 3:
                sorted_streams = sorted_streams[:2]
            elif num == 2:
                title = "Top 2 Trending Streams"
            elif num == 1:
                title = "Top Trending Stream"
            elif num == 0:
                title = "No Streams Trending Currently"

            counts = list(map(lambda x: len(list(x.view_times)), sorted_streams))



            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
                'title': title,
                'streams': sorted_streams,
                'counts': counts
            }

            template = JINJA_ENVIRONMENT.get_template('/Pages/TrendingStreams.html')
            render = template.render(template_values)

            report = TrendReport.query(TrendReport.name == TREND_REPORT).get()
            if report:
                report.html = render
            else:
                report = TrendReport(name=TREND_REPORT, html=render)
            report.put()

            # send emails
            # users = User.query()
            #for user in users:
            #       if user wants reports every 5 mins send email
            #       if user wants reports every hour and minute==0 send email
            #       is user wants reports every day and hour==0 and minute==0 send email
            #       else send no email
# [END TrendingReport]
