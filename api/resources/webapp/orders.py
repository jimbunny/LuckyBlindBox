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
from common.utils import get_order_code
from common import code, pretty_result
from models.orders import OrdersModel
from models.products import ProductsModel
from models.mallUsers import MallUsersModel
from common.decorators import login_required
import math
import time
from config import setting


class OrdersResource(Resource):
    """
    示例orders list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",
                                 help='email format is incorrect')
        self.parser.add_argument("status", type=str, required=True, location="args",
                                 help='status format is incorrect')
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo format is incorrect')
        self.parser.add_argument("pageSize", type=int, required=True, location="args",
                                 help='pageSize format is incorrect')
        args = self.parser.parse_args()
        if args.status == "all":
            orderInfo = OrdersModel.paginate(OrdersModel, args.pageNo, args.pageSize)
        elif args.status == "noDelivery":
            orderInfo = OrdersModel.paginate_by_status(OrdersModel,'noDelivery', args.pageNo, args.pageSize)
        else:
            orderInfo = OrdersModel.paginate_by_status(OrdersModel,'delivered', args.pageNo, args.pageSize)
        data=[]
        if orderInfo.items:
            for item in orderInfo.items:
                OrderItemVOS = []
                productList = item.productList.split(',')
                for i in productList:
                    productInfo = ProductsModel.query.filter_by(id=i).first()
                    OrderItemVOS.append(productInfo.to_dict())
                data.append({
                    'no': item.no,
                    'totalPrice': item.totalPrice,
                    'username': item.username,
                    'phone': item.phone,
                    'payType': item.payType,
                    'status': item.status,
                    'productList': item.productList,
                    'addressId': item.addressId,
                    'createTime': item.createTime,
                    'OrderItemVOS': OrderItemVOS
                })
        totalCount = len(data)
        result = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': data,
            'totalPage': math.ceil(totalCount/args.pageSize)
        }
        return pretty_result(code.OK, data=result, msg="get order info successful!")

    @login_required
    def post(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("totalPrice", type=int, required=True, location="json", help='totalPrice format is incorrect')
        self.parser.add_argument("username", type=str, required=True, location="json",
                                 help='username format is incorrect')
        self.parser.add_argument("phone", type=str, required=True, location="json",
                                 help='phone format is incorrect')
        self.parser.add_argument("payType", type=str, required=True, location="json",
                                 help='payType format is incorrect')
        self.parser.add_argument("productList", type=list, required=True, location="json",
                                 help='productList format is incorrect')
        self.parser.add_argument("addressId", type=str, required=True, location="json",
                                 help='addressId format is incorrect')
        args = self.parser.parse_args()
        mallUsersInfo = MallUsersModel.query.filter_by(email=args.email).first()
        if mallUsersInfo.balance < args.totalPrice:
            return pretty_result(code.ERROR, msg="create order failed, balance ont enough!")
        else:
            for i in args.productList:
                proudctInfo = ProductsModel.query.filter_by(id=i).first()
                proudctInfo.status = "solded"
                ProductsModel.update(proudctInfo)
            mallUsersInfo.balance = mallUsersInfo.balance - args.totalPrice
            MallUsersModel.update(mallUsersInfo)
        order = OrdersModel(email=args.email,no=get_order_code(), username=args.username, totalPrice=args.totalPrice, phone=args.phone.replace("-", ""),
                                couponPrice=0, payType=args.payType, status="noDelivery", productList=','.join([str(x) for x in args.productList]),
                                addressId=args.addressId)
        OrdersModel.add(OrdersModel, order)
        return pretty_result(code.OK, msg="create order info successful!")

    @login_required
    def put(self):
        self.parser.add_argument("no", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='no format is incorrect')
        self.parser.add_argument("status", type=str, required=True, location="json",
                                 help='status format is incorrect')
        args = self.parser.parse_args()
        orderInfo = OrdersModel.query.filter_by(no=args.no).first()
        orderInfo.status = args.status
        OrdersModel.update(orderInfo)
        return pretty_result(code.OK, msg="update order status info successful!")


class OrdersByNoResource(Resource):
    """
    示例orders list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        self.parser.add_argument("no", type=str, required=True, location="args",
                                 help='no format is incorrect')
        args = self.parser.parse_args()
        orderInfo = OrdersModel.query.filter_by(no=args.no).first()
        OrderItemVOS = []
        productList = orderInfo.productList.split(',')
        for i in productList:
            productInfo = ProductsModel.query.filter_by(id=i).first()
            OrderItemVOS.append(productInfo.to_dict())
        data ={
            'no': orderInfo.no,
            'totalPrice': orderInfo.totalPrice,
            'phone': orderInfo.phone,
            'payType': orderInfo.payType,
            'status': orderInfo.status,
            'productList': orderInfo.productList,
            'addressId': orderInfo.addressId,
            "createTime": orderInfo.createTime,
            'OrderItemVOS': OrderItemVOS
        }
        return pretty_result(code.OK, data=data, msg="get order info successful!")