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


class CouponsModel(db.Model, BaseModel):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    couponName = db.Column(db.String(50), nullable=False)
    startTime = db.Column(db.Integer, default=int(time.time()), nullable=True)
    endTime = db.Column(db.Integer, default=int(time.time()), nullable=True)
    couponCount = db.Column(db.Integer, nullable=True)  # 兑换次数
    couponType = db.Column(db.String(50), nullable=False)  # 优惠类型 有门槛 无门槛
    couponCondition = db.Column(db.Integer, nullable=True)  # 优惠条件 高于该价格可以使用
    discountType = db.Column(db.String(50), nullable=False)  # 折扣类型 优惠价格，折扣比例
    discountCondition = db.Column(db.Integer, nullable=True)  # 优惠面值 折扣比例
    description = db.Column(db.String(50), nullable=False)
    couponStatus = db.Column(db.String(50), nullable=False)  # 全部可用 ，兑换码
    couponKey = db.Column(db.String(50), nullable=False)  # 兑换码

    def __init__(self, couponName, startTime, endTime, couponType, couponCondition, discountType, discountCondition,
                 description, couponStatus, couponKey):
        self.couponName = couponName
        self.startTime = startTime
        self.endTime = endTime
        self.couponType = couponType
        self.couponCondition = couponCondition
        self.discountType = discountType
        self.discountCondition = discountCondition
        self.description = description
        self.couponStatus = couponStatus
        self.couponKey = couponKey

    def __str__(self):
        return "Coupons(id='%s')" % self.id

    def paginate(self, page, per_page):
        return self.query.paginate(page=page, per_page=per_page, error_out=False)

    def filter_by_description(self, description):
        return self.query.filter(self.description.like("%" + description + "%")).all()

    def filter_by_permission(self, permission):
        return self.query.filter(self.permission.like("%" + permission + "%")).all()

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
