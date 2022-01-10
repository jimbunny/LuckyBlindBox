#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from . import db
from .base import BaseModel
from sqlalchemy import orm, and_


class AdminRolesModel(BaseModel):
    __tablename__ = 'admin_roles'
    description = db.Column(db.String(50), nullable=False)
    permission = db.Column(db.String(10), default='test', nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'description', 'permission']

    def __str__(self):
        return "Roles(id='%s')" % self.id

    def paginate(self, page, per_page, description, not_permission):
        return self.query.filter(and_(self.permission != not_permission,
                                      self.description.like("%" + description + "%")))\
            .paginate(page=page, per_page=per_page, error_out=False)

    def is_permission(self, permission):
        query = self.query.filter(self.permission == permission)
        at_least_one_permission_exists = db.session.query(query.exists()).scalar()
        return at_least_one_permission_exists

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

