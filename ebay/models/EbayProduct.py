#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

import datetime
import logging
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

meta = declarative_base(metaclass=DeclarativeMeta)


class EbayProduct(meta):

    __tablename__ = 'ebay_product'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    picture = Column(String(50))
    create_date = Column(String, nullable=False)
    price = Column(Float)
    price_unit = Column(String(5))
    seller = Column(String(20))
    seller_href = Column(String(50))
    shipping_price = Column(Float)
    shipping_unit = Column(String(5))
    href = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)

    @classmethod
    def add(cls, session, name='', picture='', create_date='',
            price=0, price_unit='', seller='', seller_href='',
            shipping_price=0, shipping_unit='', href=''):
        data = cls(
            name=name,
            picture=picture,
            create_date=create_date,
            price=price,
            price_unit=price_unit,
            seller=seller,
            seller_href=seller_href,
            shipping_price=shipping_price,
            shipping_unit=shipping_unit,
            href=href
        )
        try:
            session.add(data)
            session.commit()
        except SQLAlchemyError as exc:
            logging.error(exc.message)
            session.rollback()