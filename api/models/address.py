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


class AddressModel(db.Model, BaseModel):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    addressId = db.Column(db.Integer, default=int(time.time()), nullable=True)
    email = db.Column(db.String(25), nullable=True)
    username = db.Column(db.String(25), nullable=True)
    phone = db.Column(db.String(25), nullable=True)
    defaultFlag = db.Column(db.Integer, default=0, nullable=True)
    provinceName = db.Column(db.String(50), nullable=True)
    cityName = db.Column(db.String(50), nullable=True)
    townName = db.Column(db.String(50), nullable=True)
    postCode = db.Column(db.String(50), nullable=True)
    detailAddress = db.Column(db.String(500), nullable=False)

    def __init__(self, email, username, phone, provinceName, cityName, townName, detailAddress, postCode, addressId=int(time.time()), defaultFlag=0):
        self.email = email
        self.username = username
        self.phone = phone
        self.provinceName = provinceName
        self.cityName = cityName
        self.townName = townName
        self.detailAddress = detailAddress
        self.defaultFlag = defaultFlag
        self.addressId = addressId
        self.postCode = postCode

    def __str__(self):
        return "Address(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_email(self, email):
        return self.query.filter(self.email.like("%" + email + "%")).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, role):
        db.session.add(role)
        return session_commit()

    def updateStatus(self, email):
        self.query.filter_by(email=email).update({"defaultFlag": 0})
        session_commit()

    def update(self):
        return session_commit()

    def delete(self, addressId):
        # self.query.filter_by(id=id).delete()
        self.query.filter(self.addressId.in_(addressId)).delete(synchronize_session=False)
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.info(e)
        return reason
