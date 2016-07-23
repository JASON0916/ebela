#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import os
import re
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
URL_PATTERN = re.compile('sch\/(?P<section>\S*)\/(?P<section_id>\d*)\/i\.html\S*LH_LocatedIn\=(?P<location_code>\d*)')


@SPIDER_API.route('/settings', methods=['POST'])
@use_args({
    'url': fields.Str(required=True)
})
def add_spider_param(args):
    url = args.get('url')
    [section, section_id, location_code] = URL_PATTERN.findall(url)[0]
    try:
        data = yaml.load(open(YAML_PATH, 'rb'))
        data['location'].append(int(location_code)),
        data['section'].append([section, int(section_id)])
        yaml.safe_dump(data, open(YAML_PATH, 'wb'))
        return Response(ujson.dumps({'SUCCESS': True}))
    except Exception as exc:
        LOGGER.exception(exc)
        abort(500)


@SPIDER_API.route('/run', methods=['GET'])
def run_spider():
    os.system('scrapy runspider {}'.format(SPIDER_SCRIPT))
    return Response(ujson.dumps({'SUCCESS': True}))
