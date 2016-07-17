# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import (Table, Column, Integer,
                        String, Float, DateTime,
                        MetaData, UniqueConstraint, Index)
from ebay.models import POSTGRE_ENGINE

meta = MetaData()

EbayProduct = Table('ebay_product', meta,
                    Column('id', Integer, autoincrement=True, primary_key=True),
                    Column('name', String(30), nullable=False),
                    Column('picture', String(50)),
                    Column('create_date', String, nullable=False),
                    Column('price', Float),
                    Column('price_unit', String(5)),
                    Column('seller', String(20)),
                    Column('seller_href', String(50)),
                    Column('shipping_price', Float),
                    Column('shipping_unit', String(5)),
                    Column('href', String(50)),
                    Column('created_at', DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now),
                    Index('eb_name', 'name'),
                    Index('eb_create_date', 'create_date'),
                    Index('eb_seller', 'seller', 'seller_href'),
                    UniqueConstraint('name', 'seller')
                    )

meta.drop_all(POSTGRE_ENGINE)
meta.create_all(POSTGRE_ENGINE)
