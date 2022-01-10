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


class AddressConfigModel(db.Model, BaseModel):
    __tablename__ = 'addressConfig'
    id = db.Column(db.Integer, primary_key=True)
    provinceName = db.Column(db.String(50), nullable=True)
    cityName = db.Column(db.String(50), nullable=True)
    townName = db.Column(db.String(50), nullable=True)
    postCode = db.Column(db.String(500), nullable=True)

    def __init__(self,provinceName, cityName, townName, postCode):
        self.provinceName = provinceName
        self.cityName = cityName
        self.townName = townName
        self.postCode = postCode

    def __str__(self):
        return "Address Config (id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_city_name(self, cityName):
        return self.query.filter(self.cityName.like("%" + cityName + "%")).all()

    def filter_by_town_name(self, townName):
        return self.query.filter(self.townName.like("%" + townName + "%")).all()

    def filter_by_province_name(self, provinceName):
        return self.query.filter(self.provinceName.like("%" + provinceName + "%")).all()

    def filter_by_post_code(self, postCode):
        return self.query.filter(self.postCode.like("%" + postCode + "%")).all()

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
