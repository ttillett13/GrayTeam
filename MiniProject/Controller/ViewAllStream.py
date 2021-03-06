import webapp2

from Config import *
from Model.Stream import Stream
from Model.Stream import User
from Controller.Common import authenticate

from google.appengine.api import images
import json
from Controller.Common import json_serial


class ViewAllStream(webapp2.RequestHandler):
    def get(self):
        auth = authenticate(self)
        if auth[0]:
            template_values = {
                'user': auth[0],
                'url': auth[1],
                'url_linktext': auth[2],
            }
            current_user = User.query(User.username == auth[0]._User__email).get()
            template_values = dict(template_values.items() + self.build_template(current_user, self.request).items())
            template = JINJA_ENVIRONMENT.get_template('/Pages/ViewAllStream.html')
            self.response.write(template.render(template_values))

    @staticmethod
    def build_template(current_user, request):
            raw_streams = Stream.query().fetch()

            streams = []
            if raw_streams:
                for stream in raw_streams:
                    isSet = False
                    if stream.pictures:
                        cover_image = stream.pictures[0].get()
                        stream_to_append = [stream.name,
                                            images.get_serving_url(cover_image.image, secure_url=False),
                                            stream.url,
                                            stream.creation_time]
                        isSet = True
                    if stream.cover_page_url:
                        stream_to_append = [stream.name,
                                            stream.cover_page_url,
                                            stream.url,
                                            stream.creation_time]
                        isSet = True
                    if not isSet:
                        stream_to_append = [stream.name,
                                            "",
                                            stream.url,
                                            stream.creation_time]
                    streams.append(stream_to_append)

            streams = sorted(streams, key=lambda x: str(x[3]))
            template_values = {

                'streams': streams
            }

            return template_values

class ViewAllStreamsAPI(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            json_data = ViewAllStream.build_template("test@example.com", self.request)
            new_json = []
            for item in json_data['streams']:
                item_dict = {"name": item[0],
                            "url": item[1],
                            "path": item[2],
                            "datetime": item[3]}
                new_json.append(item_dict)
            self.response.out.write(json.dumps(new_json, default=json_serial))

class SubscribedStreamsAPI(webapp2.RedirectHandler):
    def get(self):
        user_email = self.request.get('user')
        current_user = User.query(User.email == user_email).get()
        streams_subscribed = [key.get() for key in current_user.streams_subscribed]


        items = []

        for stream in streams_subscribed:
            for picture in stream.pictures:
                item = []
                item.append(stream.name)
                item.append(stream.url)
                picture_temp = picture.get()
                item.append(images.get_serving_url(picture_temp.image, secure_url=False))
                item.append(picture_temp.date_uploaded)
                items.append(item)

        items = sorted(items, key=lambda x: str(x[3]))



        self.response.headers['Content-Type'] = 'application/json'
        new_json = []
        i = 0
        for item in items:
            if i == 16:
                break
            item_dict = {"name": item[0],
                        "url": item[2],
                        "path": item[1],
                        "datetime": item[3]}
            new_json.append(item_dict)
            i += 1
        self.response.out.write(json.dumps(new_json, default=json_serial))