#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import current_app
from sqlalchemy import and_
from . import db
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy import orm, and_
from datetime import datetime


class PackagesModel(BaseModel):
    __tablename__ = 'packages'
    name = db.Column(db.String(25),  unique=True, nullable=False)
    no = db.Column(db.String(50), nullable=False)
    _type = db.Column(db.String(50), nullable=False)
    cover_img = db.Column(db.String(100), nullable=False)
    detail_img = db.Column(db.String(100), nullable=False)
    status = db.Column(db.BOOLEAN, default=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    product_list = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.String(500))
    update_user_id = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.DATETIME(6), default=datetime.now)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'no', 'name', 'cover_img', 'detail_img', '_type', 'price', 'status',
                       'rank', 'price', 'product_list', 'remark', 'update_user_id', 'update_time']

    def __str__(self):
        return "Packages(id='%s')" % self.id

    def paginate(self, page, per_page, name, _type):
        return self.query.filter(
            and_(self.name.like("%" + name + "%"), self._type.like("%" + _type + "%"))) \
            .paginate(page=page, per_page=per_page, error_out=False)

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def get_id(self):
        return db.session.query(func.max(self.id)).all()

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


