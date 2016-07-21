#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-
import ujson
from flask import (Response,
                   abort,
                   Blueprint)
from webargs import fields
from webargs.flaskparser import use_args
from models.EbayProduct import EbayProduct
from flask.logging import getLogger

INFO_API = Blueprint('info', __name__, url_prefix='/api/info')
LOGGER = getLogger(__file__)


@INFO_API.route('/products', methods=['GET'])
@use_args({
    'name': fields.Str(allow_missing=True),
    'seller': fields.Str(allow_missing=True),
    'datetime': fields.Str(required=True)
})
def get_products_info(args):
    try:
        row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        data = map(row2dict, EbayProduct.get(**args))
        return Response(ujson.dumps(data))
    except Exception as exc:
        LOGGER.exception(exc)
        abort(500)


@INFO_API.route('/ping', methods=['GET'])
def ping():
    msg = {
        'SUCCESS': True,
    }
    return Response(ujson.dumps(msg))
