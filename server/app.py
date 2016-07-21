#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import os
from flask import (Flask,
                   render_template
                   )
from info import INFO_API
from spider import SPIDER_API


def create_app():
    app = Flask(__name__, template_folder='static')
    app.register_blueprint(INFO_API)
    app.register_blueprint(SPIDER_API)
    return app

app = create_app()


@app.route('/', methods=['GET'])
def index():
    # return Response(ujson.dumps({'SUCCESS': True}))
    return render_template(os.path.join('html/index.html'))
app.run(debug=True)
