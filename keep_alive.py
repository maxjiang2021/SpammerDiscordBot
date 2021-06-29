import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from flask import Flask
import flask
from threading import Thread
import os
import sys

app = Flask('SpammerDiscordBot')

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv = "refresh" content = "0; url = https://discord.com/api/oauth2/authorize?client_id=840380077815627796&permissions=8&scope=bot" />
    </head>
    <body>
        <a href="https://discord.com/api/oauth2/authorize?client_id=840380077815627796&permissions=8&scope=bot">Invite bot</a>
    </body>
</html>
"""


def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run,daemon=False)
    t.start()