#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import current_app
from sqlalchemy import and_

from . import db
from .base import BaseModel
from sqlalchemy import orm, and_
from datetime import datetime


class LogsModel(BaseModel):
    __tablename__ = 'logs'
    username = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    update_time = db.Column(db.DateTime(6), default=datetime.now)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'username', 'model', 'action', 'content', 'update_time']

    def __str__(self):
        return "Logs(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_username_model_action(self, username, model, action):
        return self.query.filter(and_(
            self.username.like("%" + username + "%"),
            self.model.like("%" + model + "%"),
            self.action.like("%" + action + "%"))).all()

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
