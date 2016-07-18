#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

meta = declarative_base(metaclass=DeclarativeMeta)


class EbayProduct(meta):

    __tablename__ = 'ebay_product'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    picture = Column(String(200))
    create_date = Column(String, nullable=False)
    price = Column(Float)
    price_unit = Column(String(10))
    seller = Column(String(50))
    seller_href = Column(String(200))
    shipping_price = Column(Float)
    shipping_unit = Column(String(10))
    href = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)
