import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'g3498hg4578gh4578h3f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'seattlerank.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/seattlerank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # prevent annoying debug thing from breaking links
db = SQLAlchemy(app)

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"  # tells flask where to redirect if you try to access a restricted page
login_manager.init_app(app)

# Load debug toolbar
#toolbar = DebugToolbarExtension(app)

# make timestamps look pretty
moment = Moment(app)

import models
import views


import math

millnames = ['',' K',' M',' B',' T']


def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

app.jinja_env.filters['millify'] = millify
