#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, Flask
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)

app = Flask(__name__)
app.register_blueprint(simple_page)
print app.url_map
