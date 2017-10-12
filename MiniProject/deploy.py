from subprocess import call
import os

#gcloud app deploy -v [YOUR_VERSION_ID]
#Deploy to the instance
call(["gcloud", "app", "deploy", "app.yaml", "index.yaml", "cron.yaml", "-q", "-v", "v2"])

#Auto open the prod site
call(["gcloud", "app", "browse"])
