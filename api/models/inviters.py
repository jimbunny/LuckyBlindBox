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


class InvitersModel(db.Model, BaseModel):
    __tablename__ = 'inviters'
    id = db.Column(db.Integer, primary_key=True)
    invite = db.Column(db.String(25), nullable=False)
    invited = db.Column(db.String(25), nullable=False)
    register_on = db.Column(db.Integer, default=int(time.time()))

    def __init__(self, invite, invited):
        self.invite = invite
        self.invited = invited

    def __str__(self):
        return "Inviters(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_invite(self, invite):
        return self.query.filter(self.invite.like("%" + invite + "%")).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, role):
        db.session.add(role)
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
