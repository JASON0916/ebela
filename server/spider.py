#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import os
import yaml
import ujson
from flask import (
    Response,
    abort,
    Blueprint
)
from flask.logging import getLogger
from webargs import fields
from webargs.flaskparser import use_args


SPIDER_API = Blueprint('spider', __name__, url_prefix='/api/spider')
LOGGER = getLogger(__file__)
PROJECT_PATH = '/'.join(os.path.abspath(__file__).split('/')[:-2])
YAML_PATH = os.path.join(PROJECT_PATH, 'spider_target.yaml')
SPIDER_SCRIPT = os.path.join(PROJECT_PATH, 'ebay/spiders/EbaySpider.py')


@SPIDER_API.route('/settings', methods=['POST'])
@use_args({
    'location_code': fields.Int(required=True),
    'section': fields.Str(required=True),
    'section_id': fields.Int(required=True)
})
def add_spider_param(args):
    location_code = args.get('location_code')
    section = args.get('section')
    section_id = args.get('section_id')
    try:
        data = yaml.load(open(YAML_PATH, 'rb'))
        print (data)
        data['location'].append(location_code),
        data['section'].append([section, section_id])
        print (data)
        yaml.safe_dump(data, open(YAML_PATH, 'wb'))
        return Response(ujson.dumps({'SUCCESS': True}))
    except Exception as exc:
        LOGGER.exception(exc)
        abort(500)


@SPIDER_API.route('/run', methods=['GET'])
def run_spider():
    os.system('scrapy runspider {}'.format(SPIDER_SCRIPT))
    return Response(ujson.dumps({'SUCCESS': True}))
