#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import datetime
from models import DBSession
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

meta = declarative_base(metaclass=DeclarativeMeta)


class EbayProduct(meta):

    __tablename__ = 'ebay_product'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False, default='')
    picture = Column(String(200), default='')
    create_date = Column(String, default='')
    price = Column(Float, default=0.0)
    price_unit = Column(String(10), default='')
    seller = Column(String(50), default='')
    seller_href = Column(String(200), default='')
    shipping_price = Column(Float, default=0.0)
    shipping_unit = Column(String(10), default='')
    href = Column(String(200), default='')
    created_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    @classmethod
    def get(cls, name='', seller='', date=''):
        query = DBSession().query(cls)
        if name:
            query = query.filter(cls.name == name)
        if seller:
            query = query.filter(cls.seller == seller)
        if date:
            today = datetime.datetime.strptime(date, '%Y-%m-%d')
            yesterday = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            query = query.filter(cls.created_at.between(yesterday, today))
        return query.all()
