from subprocess import call
import os

#Deploy to the instance
call(["gcloud", "app", "deploy", "app.yaml", "index.yaml", "cron.yaml", "-q"])

#Auto open the prod site
call(["gcloud", "app", "browse"])
