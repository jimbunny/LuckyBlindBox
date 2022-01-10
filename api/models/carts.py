#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from sqlalchemy import and_
from flask import current_app
from . import db
from .base import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
import time


class CartsModel(db.Model, BaseModel):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    no = db.Column(db.String(50), nullable=False)

    updateTime = db.Column(db.Integer, default=int(time.time()))

    def __init__(self, email, no):
        self.no = no
        self.email = email

    def __str__(self):
        return "Carts(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def get_id(self):
        return db.session.query(func.max(self.id)).all()

    def get(self, _id):
        return self.query.filter_by(id=_id).first()

    def add(self, product):
        db.session.add(product)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, no):
        self.query.filter(self.no == no).delete(synchronize_session=False)
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        current_app.logger.info(e)
        return reason
