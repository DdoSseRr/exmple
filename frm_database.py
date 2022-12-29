from enum import unique

import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, \
    INT, TEXT, DATETIME, func, BOOLEAN, ForeignKey, BLOB, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship, backref
import logging

engine = create_engine("sqlite://///home/devil/PycharmProjects/urlshortener/FRM/customers.db?check_same_thread=False")

Base = declarative_base(engine)
Session = sessionmaker()
Session.configure(bind=engine)

logger = logging.getLogger(__name__)


class Admins(Base):
    __tablename__ = 'admins'
    admin_id = Column(INT, primary_key=True, nullable=False)
    user_id = Column(INT, unique=True, nullable=False)



    def __repr__(self):
        return "<Admins: admin_id='%s' user_id='%s'>" % (
            self.admin_id,
            self.user_id)


class Users(Base):
    __tablename__ = 'users'
    id = Column(INT, primary_key=True, nullable=False)
    user_id = Column(INT, unique=True, nullable=False)
    authorized = Column(BOOLEAN, nullable=False, server_default="0")
    username = Column(TEXT)
    firstname = Column(TEXT)
    user_balance = Column(TEXT, nullable=False, server_default='0')
    ban_id = Column(INT, nullable=False, server_default='0')
    order_id = Column(INT, ForeignKey('order.id'))
    orders = relationship("Order", secondary="order_product")



    def __repr__(self):
        return "<Users: id='%s' user_id='%s' username='%s' firstname='%s' city='%s'" \
               "dist='%s' product='%s' product_weight='%s' product_price='%s' user_balance='%s' " \
               "bill_id='%s' bill_date='%s' bill_checked='%s' ban_id='%s'>" % \
            (self.id,self.user_id,self.username,self.firstname,self.city,
             self.dist,self.product_code,self.product_weight,self.product_price,
             self.user_balance,self.bill_id,self.bill_date,self.bill_checked,self.ban_id)


class Order(Base):
    __tablename__ = 'order'
    id = Column(INT, primary_key=True, nullable=False)
    city_district = Column(TEXT, nullable=False)
    price_total = Column(INT, nullable=False)
    order_date = Column(DATETIME, server_default=func.now())
    requisites = Column(INT, ForeignKey('qiwi.id'))
    payment_method = Column(TEXT)
    bill_id = Column(TEXT)
    bill_checked = Column(INT, nullable=False, server_default='0')


    def __repr__(self):
        return "<Order: id='%s' user_id='%s' city_district='%s' price_total='%s' order_date='%s' " \
               "requisites='%s' payment_method='%s' bill_id='%s' bill_checked='%s'>" % \
            (self.id,self.user_id,self.city_district,self.price_total,self.order_date,
             self.requisites,self.payment_method,self.bill_id,self.bill_checked)


class Products(Base):
    """id = (INT, primary_key=True, unique=True, nullable=False)
        name  =   (TEXT, unique=True, nullable=False)
        code_name  =      (TEXT, unique=True, nullable=False)
        price  =      (INT, nullable=False)
        description  =    (TEXT, nullable=False)
        photo  =      (BLOB, nullable=False)
        category  =  (INT, ForeignKey('categories.id'), nullable=False)
        orders  =  relationship  =   ('Order', secondary='order_products')
    """
    __tablename__ = 'products'
    id = Column(INT, primary_key=True, unique=True, nullable=False)
    name = Column(TEXT, nullable=False)
    code_name = Column(TEXT, unique=True, nullable=False)
    price = Column(INT, nullable=False)
    description = Column(TEXT, nullable=False)
    photo = Column(BLOB, nullable=False)
    category = Column(INT, ForeignKey('categories.id'), nullable=False)
    orders = relationship('OrderProduct', back_populates='products')


    def __repr__(self):
        return "<Products: id='%s' name='%s' price='%s' description='%s' category='%s' " \
               "image='%s' status='%s' last_time='%s' last_balance='%s'>" \
            % (self.id,self.name,self.price,self.description,self.category,
               self.image,self.status,self.last_time,self.last_balance)


class OrderProduct(Base):
    __tablename__ = 'order_product'
    __table_args__ = (PrimaryKeyConstraint('order_id', 'product_id'),)
    order_id = Column(INT, ForeignKey('order.id'))
    product_id = Column(INT, ForeignKey('products.id'))
    order = relationship("Order", back_populates="product")
    product = relationship("Products", back_populates="order")




class Categories(Base):
    __tablename__ = 'categories'
    id = Column(INT, primary_key=True, unique=True, nullable=False)
    name = Column(TEXT, unique=True, nullable=False)
    description = Column(TEXT, nullable=False)
    



class Configs(Base):
    __tablename__ = 'configs'
    id = Column(INT, primary_key=True, unique=True)
    bitcoin = Column(TEXT)
    operator_link = Column(TEXT)
    chat_link = Column(TEXT)
    channel_link = Column(TEXT)
    site_link = Column(TEXT)
    work_link = Column(TEXT)
    hydra_link = Column(TEXT)

    def __repr__(self):
        return "<Configs: id='%s'" \
               "bitcoin='%s' operator_link='%s' chat_link='%s' channel_link='%s' site_link='%s' " \
               "work_link='%s' hydra_link='%s' >" % (self.id,self.bitcoin,self.operator_link,self.chat_link,
                                                     self.channel_link,self.site_link,self.work_link,
                                                     self.hydra_link)


class Qiwi(Base):
    __tablename__ = 'qiwi'
    id = Column(INT, primary_key=True, unique=True, nullable=False)
    qiwi_card = Column(INT, unique=True, nullable=False)
    qiwi_phone = Column(TEXT, unique=True)
    wallet_api = Column(TEXT, nullable=False)
    p2p_private = Column(TEXT)
    ban = Column(INT, nullable=False, server_default='0')  # 0 - Alive #1 - BAN #3 - restriction limit
    last_time = Column(DATETIME, onupdate=func.now())
    last_balance = Column(BOOLEAN)


    def __repr__(self):
        return "<Qiwi: id='%s' qiwi_card='%s' qiwi_phone='%s' wallet_api='%s' p2p_private='%s' " \
               "ban='%s'  last_time='%s' last_balance='%s'>" % (
            self.id,
            self.qiwi_card,
            self.qiwi_phone,
            self.wallet_api,
            self.p2p_private,
            self.ban,
            self.last_time,
            self.last_balance
        )


class Ofshore(Base):
    __tablename__ = 'ofshore'
    id = Column(INT, primary_key=True, unique=True, nullable=False)
    qiwi_card = Column(INT)
    qiwi_phone = Column(TEXT, unique=True)
    wallet_api = Column(TEXT, nullable=False)
    p2p_private = Column(TEXT)
    ban = Column(INT, nullable=False, server_default='0')
    last_time = Column(DATETIME, onupdate=func.now())
    last_balance = Column(TEXT)

    def __repr__(self):
        return "<OFSHORE: id='%s' qiwi_card='%s' qiwi_phone='%s' wallet_api='%s' p2p_private='%s' " \
               "ban='%s' last_time='%s' last_balance='%s'>" % (self.id,self.qiwi_card,self.qiwi_phone,
                                                               self.wallet_api,self.p2p_private,self.ban,
                                                               self.last_time,self.last_balance)









#Base.metadata.create_all(engine)









