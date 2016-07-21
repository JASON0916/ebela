#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from flask import Blueprint

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')