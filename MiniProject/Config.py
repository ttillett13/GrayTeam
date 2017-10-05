import os
import jinja2
from google.appengine.api import app_identity

BUCKET_NAME = os.environ.get('BUCKET_NAME',
                               app_identity.get_default_gcs_bucket_name())

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
INDEX_NAME = "default_index"
# [END imports]