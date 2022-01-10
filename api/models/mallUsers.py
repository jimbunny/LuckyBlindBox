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
from config.setting import config
import time

avatarConfig = config.avatar


class MallUsersModel(db.Model, BaseModel):
    __tablename__ = 'mall_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25),  unique=True, nullable=False)
    username = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(25), nullable=True)
    password = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    birthday = db.Column(db.String(10), nullable=True)
    role = db.Column(db.String(10), default='user', nullable=False)
    registered_on = db.Column(db.Integer, default=int(time.time()), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.Integer, nullable=True)
    point = db.Column(db.Integer, default=0, nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)
    facebook = db.Column(db.String(25), default='', nullable=True)
    avatar = db.Column(db.String(100), default=avatarConfig, nullable=False)
    login_time = db.Column(db.Integer, default=int(time.time()))
    coupon = db.Column(db.String(50), nullable=True)

    def __init__(self, username, email, registered_on, password="", phone="", gender="",  birthday="",
                 avatar=avatarConfig, point=0, facebook="", confirmed=False, confirmed_on=0, coupon=""):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.gender = gender
        self.birthday = birthday
        self.registered_on = registered_on
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.facebook = facebook
        self.avatar = avatar
        self.point = point
        self.coupon = coupon

    def __str__(self):
        return "MallUsers(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_username(self, username):
        return self.query.filter(self.username.like("%" + username + "%")).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, ids):
        # self.query.filter_by(id=id).delete()
        self.query.filter(self.id.in_(ids)).delete(synchronize_session=False)
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.info(e)
        return reason
