# -*- coding: utf-8 -*-

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from settings import FLASK_CONFIG

app = flask.Flask(__name__)
app.config.update(FLASK_CONFIG)
db = SQLAlchemy(app)


@app.route("/")
def index():
    return '1'