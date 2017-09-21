from subprocess import call
import os
import webbrowser

webbrowser.open('http://localhost:8080')

#Deploy to the instance
call(["dev_appserver.py", "./"])


