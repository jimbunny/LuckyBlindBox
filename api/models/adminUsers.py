#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from . import db
from .base import BaseModel, MixinJSONSerializer
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from datetime import datetime


class AdminUsersModel(BaseModel):
    __tablename__ = 'admin_users'
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password = db.Column(db.String(250), nullable=False)
    permission = db.Column(db.String(50), default='guest', nullable=False)
    avatar = db.Column(db.String(250), default=app.config.get('avatar',
            'https://i.gtimg.cn/club/item/face/img/2/15922_100.gif'), nullable=False)
    login_time = db.Column(db.DATETIME(6), default=datetime.now, nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'email', 'username', 'permission', 'avatar', 'login_time']

    def __str__(self):
        return "Admin Users(id='%s')" % self.id

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def is_email(self, email):
        query = self.query.filter(self.email == email)
        # Below will return True or False
        at_least_one_email_exists = db.session.query(query.exists()).scalar()
        return at_least_one_email_exists

    def is_username(self, username):
        query = self.query.filter(self.username == username)
        # Below will return True or False
        at_least_one_user_exists = db.session.query(query.exists()).scalar()
        return at_least_one_user_exists

    def check_password(self,  password):
        if not self._password:
            return False
        return check_password_hash(self._password, password)

    def paginate(self, page, per_page, not_permission):
        return self.query.filter(self.permission != not_permission).paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_username(self, username):
        return self.query.filter(self.username.like("%" + username + "%")).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, user):
        with db.auto_commit():
            return db.session.add(user)

    def update(self):
        with db.auto_commit():
            return

    def delete(self, ids):
        self.query.filter(self.id.in_(ids)).delete(synchronize_session=False)
        with db.auto_commit():
            return
