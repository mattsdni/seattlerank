from flask import render_template, url_for, request, redirect, flash, abort

from . import app
from models import Company


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', companies=Company.top(100), title='Seattle Rank')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
