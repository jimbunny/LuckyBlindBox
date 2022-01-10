#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import current_app
from . import db
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import time


class OrdersModel(db.Model, BaseModel):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(25), nullable=True)
    username = db.Column(db.String(25), nullable=True)
    phone = db.Column(db.String(25), nullable=True)
    totalPrice = db.Column(db.Integer, nullable=True)
    couponPrice = db.Column(db.Integer, nullable=True)
    payType = db.Column(db.String(25), nullable=True)
    status = db.Column(db.String(25), nullable=True)
    couponId = db.Column(db.Integer, nullable=True)
    couponCondition = db.Column(db.Integer, nullable=True)
    createTime = db.Column(db.Integer, default=int(time.time()),nullable=True)
    addressId = db.Column(db.Integer, default=int(time.time()), nullable=True)
    productList = db.Column(db.String(50), nullable=True)
    deliveryMethod = db.Column(db.String(50), nullable=True)
    # finalPrice = db.Column(db.Integer, default=0, nullable=True)
    # discountType = db.Column(db.Integer, default=0, nullable=True)
    # discountType = db.Column(db.Integer, default=0, nullable=True)
    # discountCondition = db.Column(db.String(50), nullable=True)
    # wayBillNo = db.Column(db.String(50), nullable=True)
    # deliveryPrice = db.Column(db.Integer, default=0, nullable=True)

    def __init__(self, email, no, username, totalPrice, phone, payType, status, addressId, productList, couponPrice=0, couponId="",couponCondition="",deliveryMethod=""):
        self.email = email
        self.no = no
        self.username = username
        self.totalPrice = totalPrice
        self.phone = phone
        self.payType = payType
        self.status = status
        self.addressId = addressId
        self.productList = productList
        # self.deliveryPrice = deliveryPrice
        self.couponPrice = couponPrice
        self.couponId = couponId
        self.couponCondition = couponCondition
        self.deliveryMethod = deliveryMethod

    def __str__(self):
        return "Orders(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def paginate_by_status(self, status, page, per_page):
        return self.query.filter_by(status=status).paginate(page=page, per_page=per_page, error_out=False)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    # 配合todict一起使用
    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v

    def filter_by_email(self, email):
        return self.query.filter(self.email.like("%" + email + "%")).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, role):
        db.session.add(role)
        return session_commit()

    def update(self):
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.info(e)
        return reason
