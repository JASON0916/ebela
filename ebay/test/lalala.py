#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from ebay.test import simple_page
from jinja2 import TemplateNotFound
from flask import abort, render_template


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
