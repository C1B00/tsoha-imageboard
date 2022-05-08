from os import getenv
from flask import Flask

UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__, static_url_path="/static")
app.secret_key = getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

import routes