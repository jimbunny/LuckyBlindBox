#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from . import db
from .base import BaseModel
from sqlalchemy import orm, and_


class ClassificationModel(BaseModel):
    __tablename__ = 'classifications'
    name = db.Column(db.String(50), unique=True,nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'rank', 'create_time']

    def __str__(self):
        return "Types(id='%s')" % self.id

    def paginate(self, page, per_page, name):
        return self.query.filter(self.name.like("%" + name + "%"))\
            .paginate(page=page, per_page=per_page, error_out=False)

    def is_name(self, name):
        query = self.query.filter(self.name == name)
        at_least_one_name_exists = db.session.query(query.exists()).scalar()
        return at_least_one_name_exists

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, role):
        with db.auto_commit():
            return db.session.add(role)

    def update(self):
        with db.auto_commit():
            return

    def delete(self, ids):
        self.query.filter(self.id.in_(ids)).delete(synchronize_session=False)
        with db.auto_commit():
            return

