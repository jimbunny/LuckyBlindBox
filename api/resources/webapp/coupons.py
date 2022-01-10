#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/21 9:22 下午
# software: PyCharm

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from flask import jsonify, request, current_app, g
from models.adminRoles import RolesModel
from models.coupons import CouponsModel
from models.mallUsers import MallUsersModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from sqlalchemy.exc import SQLAlchemyError
from common.decorators import login_required
import time


class CouponsResource(Resource):
    """
    roles management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取权限列表信息
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        # coupon_list = CouponsModel.paginate(RolesModel, args.pageNo, args.pageSize)
        # items = []
        # totalCount = coupon_list.total
        # coupon_list = coupon_list.items
        # if args.email:
        userInfo = MallUsersModel.query.filter_by(email=args.email).first()
        items=[]
        for item in userInfo.coupon.split(","):
            if item:
                coupon = CouponsModel.query.filter_by(id=item).first()
                if coupon.endTime > int(time.time()):
                    items.append(
                        {
                            'id': coupon.id,
                            'couponName': coupon.couponName,
                            'startTime': coupon.startTime,
                            'endTime': coupon.endTime,
                            'couponType': coupon.couponType,
                            'couponCondition': coupon.couponCondition,
                            'discountCondition': coupon.discountCondition,
                            'description': coupon.description,
                            'couponStatus': coupon.couponStatus,
                            'couponKey': coupon.couponKey,
                        }
                    )
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': len(items),
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='优惠券信息获取成功！')

    # @login_required
    def post(self):
        """
        创建权限
        :return: json
        """
        # self.parser.add_argument("couponName", type=str, required=True, location="json", help='couponName is required')
        # self.parser.add_argument("startTime", type=str, required=True, location="json", help='startTime is required')
        # self.parser.add_argument("endTime", type=str, required=True, location="json", help='endTime is required')
        # self.parser.add_argument("couponType", type=str, required=True, location="json", help='couponType is required')
        # self.parser.add_argument("couponCondition", type=str, required=True, location="json", help='couponCondition is required')
        # self.parser.add_argument("discountType", type=str, required=True, location="json", help='discountType is required')
        # self.parser.add_argument("discountCondition", type=str, required=True, location="json",
        #                          help='discountCondition is required')
        # self.parser.add_argument("description", type=str, required=True, location="json",help='description is required')
        # self.parser.add_argument("couponStatus", type=str, required=True, location="json",help='couponStatus is required')
        # self.parser.add_argument("couponKey", type=str, required=True, location="json", help='couponKey is required')
        args = self.parser.parse_args()
        args.couponName = 'test5'
        couponsInfo = CouponsModel.query.filter_by(couponName=args.couponName).all()
        # couponName = db.Column(db.String(50), nullable=False)
        # startTime = db.Column(db.Integer, default=int(time.time()), nullable=True)
        # endTime = db.Column(db.Integer, default=int(time.time()), nullable=True)
        # couponCount = db.Column(db.Integer, nullable=True)  # 兑换次数
        # couponType = db.Column(db.String(50), nullable=False)  # 优惠类型 有门槛 无门槛
        # couponCondition = db.Column(db.Integer, nullable=True)  # 优惠条件 高于该价格可以使用
        # discountType = db.Column(db.String(50), nullable=False)  # 折扣类型 优惠价格，折扣比例
        # discountCondition = db.Column(db.Integer, nullable=True)  # 优惠面值 折扣比例
        # description = db.Column(db.String(50), nullable=False)
        # couponStatus = db.Column(db.String(50), nullable=False)  # 全部可用 ，兑换码
        # couponKey = db.Column(db.String(50), nullable=False)  # 兑换码
        dt = "2016-05-05 20:28:54"
        dt2 = "2022-05-05 20:28:54"
        args.startTime = int(time.time())
        args.endTime = int(time.time())
        args.couponType = 1  # 无门槛
        args.couponCondition = 10
        args.discountType = 2 # 价格
        args.discountCondition = 8.8
        args.description = "test3"
        args.couponStatus = 1  # 兑换码
        args.couponKey= ""
        if couponsInfo:
            return pretty_result(code.ERROR, msg='该优惠券名字被添加！')
        coupon = CouponsModel(couponName=args.couponName, startTime=args.startTime, endTime=args.endTime,
                            couponType=args.couponType, couponCondition=args.couponCondition, discountType=args.discountType,
                            discountCondition=args.discountCondition, description=args.description, couponStatus=args.couponStatus, couponKey=args.couponKey)
        CouponsModel.add(CouponsModel, coupon)
        if args.discountType == 2:
            usersInfo = MallUsersModel.query.all()
            for item in usersInfo:
                if item.coupon:
                    item.coupon = item.coupon + "," + str(coupon.id)
                else:
                    item.coupon = str(coupon.id)
                MallUsersModel.update(item)
        if coupon.id:
            returnUser = {
                'id': coupon.id,
            }
            return pretty_result(code.OK, data=returnUser, msg='优惠券添加成功')
        else:
            return pretty_result(code.ERROR, data='', msg='优惠券添加失败')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("couponName", type=str, required=True, location="json", help='couponName is required')
        self.parser.add_argument("startTime", type=str, required=True, location="json", help='startTime is required')
        self.parser.add_argument("endTime", type=str, required=True, location="json", help='endTime is required')
        self.parser.add_argument("couponType", type=str, required=True, location="json", help='couponType is required')
        self.parser.add_argument("couponCondition", type=str, required=True, location="json",
                                 help='couponCondition is required')
        self.parser.add_argument("discountType", type=str, required=True, location="json",
                                 help='discountType is required')
        self.parser.add_argument("discountCondition", type=str, required=True, location="json",
                                 help='discountCondition is required')
        self.parser.add_argument("description", type=str, required=True, location="json",
                                 help='description is required')
        self.parser.add_argument("couponStatus", type=str, required=True, location="json",
                                 help='couponStatus is required')
        self.parser.add_argument("couponKey", type=str, required=True, location="json", help='couponKey is required')
        args = self.parser.parse_args()
        couponInfo = CouponsModel.query.filter_by(id=args.id).first()
        couponInfo.couponName = args.couponName
        couponInfo.startTime = args.startTime
        couponInfo.endTime = args.endTime
        couponInfo.couponType = args.couponType
        couponInfo.couponCondition = args.couponCondition
        couponInfo.discountType = args.discountType
        couponInfo.discountCondition = args.discountCondition
        couponInfo.description = args.description
        couponInfo.couponStatus = args.couponStatus
        couponInfo.couponKey = args.couponKey
        CouponsModel.update(couponInfo)
        return pretty_result(code.OK, msg='优惠券信息更新成功！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        args = self.parser.parse_args()
        CouponsModel.delete(CouponsModel, args.ids)
        return pretty_result(code.OK, msg='优惠券信息删除成功！')


class ExchangeResource(Resource):
    """
    roles management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取权限列表信息
        :return: json
        """
        self.parser.add_argument("totalPrice", type=int, required=True, location="args",
                                 help='totalPrice is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        userInfo = MallUsersModel.query.filter_by(email=args.email).first()
        coupons = []
        disabledCoupons = []
        for item in userInfo.coupon.split(","):
            if item:
                coupon = CouponsModel.query.filter_by(id=item).first()
                if coupon.endTime > int(time.time()):
                    if coupon.couponType == 1 and args.totalPrice < coupon.couponCondition:
                        disabledCoupons.append(
                            {
                                'id': coupon.id,
                                'name': coupon.couponName,
                                'startAt': coupon.startTime,
                                'endAt': coupon.endTime,
                                'condition': "无门槛\n" if coupon.couponType == 0 else "有门槛\n" + "" if coupon.couponType == 0 else "高于" + coupon.couponCondition + "可以使用",
                                'value': coupon.discountCondition * 100,
                                'reason': "不满足最低价格！",
                                'valueDesc': coupon.discountCondition,
                                "discountType": coupon.discountType,
                                'unitDesc': "泰铢" if coupon.discountType == "1" else "折",
                            }
                        )
                    else:
                        coupons.append(
                            {
                                'id': coupon.id,
                                'name': coupon.couponName,
                                'startAt': coupon.startTime,
                                'endAt': coupon.endTime,
                                'condition': "无门槛\n" if coupon.couponType =="0" else "有门槛\n" + ("" if coupon.couponType=="0" else "高于" + str(coupon.couponCondition) + "可以使用"),
                                'value': coupon.discountCondition * 100,
                                'description': coupon.description,
                                'valueDesc': coupon.discountCondition,
                                "discountType": coupon.discountType,
                                'unitDesc': "泰铢" if coupon.discountType == "1" else "折",
                            }
                        )
        data = {
            'disabledCoupons': disabledCoupons,
            'coupons': coupons
        }
        return pretty_result(code.OK, data=data, msg='优惠券信息获取成功！')

    @login_required
    def post(self):
        """
        创建权限
        :return: json
        """
        self.parser.add_argument("email", type=str, required=True, location="json",help='couponStatus is required')
        self.parser.add_argument("key", type=str, required=True, location="json", help='key is required')
        args = self.parser.parse_args()
        couponsInfo = CouponsModel.query.filter_by(couponKey=str(args.key)).first()
        if not couponsInfo:
            return pretty_result(code.ERROR, msg='该优惠码不正确！')
        userInfo = MallUsersModel.query.filter_by(email=args.email).first()
        if not userInfo.coupon:
            userInfo.coupon = couponsInfo.id
        elif str(couponsInfo.id) in userInfo.coupon.split(","):
            return pretty_result(code.ERROR, msg='您已经兑换过！')
        else:
            userInfo.coupon = userInfo.coupon + "," + str(couponsInfo.id)
        MallUsersModel.update(userInfo)
        return pretty_result(code.OK, msg='优惠券兑换成功')
