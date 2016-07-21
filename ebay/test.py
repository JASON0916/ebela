#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort, Flask
from ebay import test

app = Flask(__name__)
app.register_blueprint(test.simple_page)
print app.url_map
