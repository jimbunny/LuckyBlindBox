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


class BalancesModel(db.Model, BaseModel):
    __tablename__ = 'balances'
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(25), nullable=True)
    type = db.Column(db.String(25), nullable=True)
    date = db.Column(db.String(25), nullable=True)
    picture = db.Column(db.String(25), nullable=True)
    status = db.Column(db.String(25), nullable=False)
    reason = db.Column(db.String(250), nullable=False)
    remark = db.Column(db.String(500), nullable=False)

    def __init__(self, email, balance, type, date, picture, status="pending", reason="", remark=""):
        self.email = email
        self.balance = balance
        self.type = type
        self.date = date
        self.picture = picture
        self.remark = remark
        self.status = status
        self.reason = reason

    def __str__(self):
        return "Balances(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_email(self, email):
        return self.query.filter(self.email.like("%" + email + "%")).all()

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
