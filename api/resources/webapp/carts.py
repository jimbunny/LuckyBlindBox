#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import g
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from app import hash_ids
from models import db
from common import code, pretty_result
from models.carts import CartsModel
from models.products import ProductsModel
from common.decorators import login_required
import datetime
from config import setting


class CartsResource(Resource):
    """
    示例cart list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        cartInfo = CartsModel.query.filter_by(email=args.email).all()
        data=[]
        for item in cartInfo:
            if (datetime.datetime.now() - item.update_time).total_seconds() < setting.countDown:
                data.append(item)
        return pretty_result(code.OK, data={"length": len(data)}, msg="get cart count successful!")

    @login_required
    def post(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        cartInfo = CartsModel.query.filter_by(email=args.email).all()
        data = []
        for item in cartInfo:
            countDown = (datetime.datetime.now() - item.update_time).total_seconds()
            if countDown < setting.countDown:
                product = ProductsModel.query.filter_by(no=item.no).first()
                url = ''
                pictures = product.picture.split(",")
                for i in pictures:
                    url = setting.domain + "/api/v1/pictureManagement/get?type=product&id=" + i
                    break
                data.append(
                    {
                        'id': product.id,
                        'no': product.no,
                        'name': product.name,
                        'description': product.description,
                        'position': product.position,
                        'picture': url,
                        'gender': product.gender,
                        'size': product.size,
                        'age': product.age,
                        'Pclass': product.Pclass,
                        'type': product.type,
                        'status': product.status,
                        'inPrice': product.inPrice,
                        'outPrice': product.outPrice,
                        'price': product.price,
                        'level': product.level,
                        'showTimes': product.showTimes,
                        'remark': product.remark,
                        'time': (setting.countDown - countDown) * 1000,
                        'updateUser': product.updateUser,
                        'updateTime': product.update_time.strftime("%m/%d/%Y %H:%M:%S")
                    }
                )
        return pretty_result(code.OK, data=data, msg="get cart info successful!")

    @login_required
    def put(self):
        self.parser.add_argument("cartItemIds", type=list, location="json", help='cartItemIds format is incorrect')
        args = self.parser.parse_args()
        if args.cartItemIds:
            productInfo = ProductsModel.get_ids(ProductsModel, args.cartItemIds)
            data = []
            for product in productInfo:
                url = ''
                countDown = (datetime.datetime.now() - product.update_time).total_seconds()
                pictures = product.picture.split(",")
                for i in pictures:
                    url = setting.domain + "/api/v1/pictureManagement/get?type=product&id=" + i
                    break
                data.append(
                    {
                        'id': product.id,
                        'no': product.no,
                        'name': product.name,
                        'description': product.description,
                        'position': product.position,
                        'picture': url,
                        'gender': product.gender,
                        'size': product.size,
                        'age': product.age,
                        'Pclass': product.Pclass,
                        'type': product.type,
                        'status': product.status,
                        'inPrice': product.inPrice,
                        'outPrice': product.outPrice,
                        'price': product.price,
                        'level': product.level,
                        'showTimes': product.showTimes,
                        'remark': product.remark,
                        'time': (setting.countDown - countDown) * 1000,
                        'updateUser': product.updateUser,
                        'updateTime': product.update_time.strftime("%m/%d/%Y %H:%M:%S")
                    }
                )
            return pretty_result(code.OK, data=data, msg="get create order info successful!")
        else:
            return pretty_result(code.OK, data=[], msg="get create order info successful!")


    @login_required
    def delete(self):
        self.parser.add_argument("no", type=str, required=True, location="json", help='no is required')
        args = self.parser.parse_args()
        CartsModel.delete(CartsModel, args.no)
        return pretty_result(code.OK, msg='购物车商品信息删除成功！')
