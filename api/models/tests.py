#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import current_app
from . import db
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import orm

import datetime


class TestsModel(BaseModel):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250),  unique=True, nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.datetime.now)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'username', 'login_time']

    def __str__(self):
        return "Tests(id='%s')" % self.id

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
