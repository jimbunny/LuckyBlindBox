#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from flask import jsonify, request, current_app, g
from models.mallUsers import MallUsersModel
from models.balances import BalancesModel
from models.points import PointsModel
from models.address import AddressModel
from models.addressConfig import AddressConfigModel
from models.inviters import InvitersModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from common.RSA import getRSAtext
from common.decorators import login_required
from config import setting
from werkzeug.datastructures import FileStorage
import os
import time
filePath = r'./downloads/balance/'
if not os.path.exists(filePath):
    os.makedirs(filePath)


class MallUserResource(Resource):
    """
    users list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取用户信息
        :return: json
        """
        user = MallUsersModel.get(MallUsersModel, g.user_id)
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'description': user.description,
            'avatar': user.avatar,
            'point': user.point,
            'balance': user.balance,
            'coupon': len(user.coupon.split(",")),
            'confirmed': user.confirmed,
            'login_time': user.login_time
        }
        return pretty_result(code.OK, data=returnUser, msg='get user info successful')

    @login_required
    def post(self):
        user = MallUsersModel.get(MallUsersModel, g.user_id)
        coupon = 0
        if user.coupon:
            coupon = user.coupon.split(",")
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'description': user.description,
            'avatar': user.avatar,
            'point': user.point,
            'balance': user.balance,
            'coupon': len(user.coupon.split(",")),
            'confirmed': user.confirmed,
            'login_time': user.login_time
        }
        return pretty_result(code.OK, data=returnUser, msg='get user info successful')

    @login_required
    def put(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("password", type=password_len, location="json", trim=True)
        self.parser.add_argument("description", type=str, location="json", help='description is required')
        args = self.parser.parse_args()
        userEmailInfo = MallUsersModel.query.filter_by(email=args.email).all()
        if userEmailInfo:
            userInfo = MallUsersModel.query.filter_by(email=args.email).first()
            userInfo.description = args.description
            if args.password:
                userInfo.password = MallUsersModel.set_password(MallUsersModel, getRSAtext(args.password))
            MallUsersModel.update(userInfo)
            return pretty_result(code.OK, msg='User info update successful！')
        else:
            return pretty_result(code.ERROR, msg='User info update failed！')


class InvitersResource(Resource):
    """
    inviters list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        """
        邀请表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        inviter = InvitersModel.query.filter_by(invite=args.email).all()
        data = []
        if inviter:
            for item in inviter:
                data.append({
                    'id': item.id,
                    'invite': item.invite,
                    'invited': item.invited,
                    'point': setting.Inviter_Point,
                    'register_on': item.update_time.strftime("%m/%d/%Y"),
                })
        return pretty_result(code.OK, data=data, msg='get inviter info successful！')


class BalanceResource(Resource):
    """
    balances list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        充值表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",help='email format is incorrect')
        self.parser.add_argument("pageNo", type=int, required=True, location="args", help='pageNo format is incorrect')
        self.parser.add_argument("pageSize", type=int, required=True, location="args",help='pageSize format is incorrect')
        args = self.parser.parse_args()
        Balances = BalancesModel.query.filter_by(email=args.email).all()
        totalCount = len(Balances)
        result = []
        if Balances:
            for item in Balances:
                url = setting.domain + "/api/v1/pictureManagement/get?type=balance&id=" + item.picture
                result.append({
                    'id': item.id,
                    'email': item.email,
                    'date': item.date,
                    'type': item.type,
                    'balance': item.balance,
                    'remark': item.remark,
                    'status': item.status,
                    'picture': url,
                    'reason': item.reason
                })
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': result
        }
        return pretty_result(code.OK, data=data, msg='Get balance successful')

    @login_required
    def post(self):
        """
        充值表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="form",
                                 help='email format is incorrect')
        self.parser.add_argument("balance", type=int, location="form", required=True, help='balance is required')
        self.parser.add_argument("type", type=str, location="form", required=True, help='type is required')
        self.parser.add_argument("date", type=str, location="form", required=True, help='date is required')
        self.parser.add_argument("remark", type=str, location="form", help='remark is required')
        self.parser.add_argument("picture", type=FileStorage, required=True, location='files', action='append',
                                 help='picture is required')
        args = self.parser.parse_args()
        file_name = ""
        for item in args.picture:
            file_name = str(int(time.time()))
            new_fname = filePath + file_name + '.png'
            item.save(new_fname)
        Balances = BalancesModel( email=args.email, type=args.type, date=args.date,
                               balance=args.balance, picture=file_name, remark=args.remark)
        BalancesModel.add(BalancesModel, Balances)
        if Balances.id:
            userInfo = MallUsersModel.query.filter_by(email=args.email).first()
            userInfo.balance = userInfo.balance + args.balance
            MallUsersModel.update(userInfo)
            return pretty_result(code.OK, msg='Add balance successful!')
        else:
            return pretty_result(code.ERROR, msg='Add balance failed')


class PointResource(Resource):
    """
    balances list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        积分表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",
                                 help='email format is incorrect')
        self.parser.add_argument("pageNo", type=int, required=True, location="args", help='pageNo format is incorrect')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize format is incorrect')
        args = self.parser.parse_args()
        Points = PointsModel.query.filter_by(email=args.email).all()
        totalCount = len(Points)
        result=[]
        if Points:
            for item in Points:
                result.append({
                    'id': item.id,
                    'email': item.email,
                    'date': item.date,
                    'type': item.type,
                    'balance': item.balance,
                    'remark': item.remark,
                    'point': item.point,
                })
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': result
        }
        return pretty_result(code.OK, data=data, msg='Get balance successful')

    @login_required
    def post(self):
        """
        充值表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("balance", type=int, location="json", required=True, help='balance is required')
        self.parser.add_argument("point", type=int, location="json", required=True, help='point is required')
        self.parser.add_argument("type", type=str, location="json", required=True, help='type is required')
        self.parser.add_argument("date", type=str, location="json", required=True, help='date is required')
        self.parser.add_argument("remark", type=str, location="json", help='remark is required')
        args = self.parser.parse_args()
        Points = PointsModel( email=args.email, type=args.type, date=args.date,
                               balance=args.balance, point=args.point, remark=args.remark)
        PointsModel.add(PointsModel, Points)
        if Points.id:
            userInfo = MallUsersModel.query.filter_by(email=args.email).first()
            userInfo.balance = userInfo.balance - args.balance
            userInfo.point = userInfo.point + args.point
            MallUsersModel.update(userInfo)
            return pretty_result(code.OK, msg='Add point successful!')
        else:
            return pretty_result(code.ERROR, msg='Add point failed')


class AddressResource(Resource):
    """
    address list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        地址表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                  location="args",
                                 help='email format is incorrect')
        self.parser.add_argument("pageNo", type=int, required=True, location="args", help='pageNo format is incorrect')
        self.parser.add_argument("pageSize", type=int, required=True, location="args",
                                 help='pageSize format is incorrect')
        self.parser.add_argument("addressId", type=int, location="args",
                                 help='addressId format is incorrect')
        args = self.parser.parse_args()
        if args.addressId:
            Address = AddressModel.query.filter_by(addressId=args.addressId).all()
            result = []
            if Address:
                for item in Address:
                    result.append({
                        'id': item.id,
                        'email': item.email,
                        'addressId': item.addressId,
                        'username': item.username,
                        'phone': item.phone,
                        'defaultFlag': item.defaultFlag,
                        'provinceName': item.provinceName,
                        'cityName': item.cityName,
                        'townName': item.townName,
                        'postCode': item.postCode,
                        'detailAddress': item.detailAddress,
                    })
            return pretty_result(code.OK, data=result[0], msg='Get address successful')
        Address = AddressModel.query.filter_by(email=args.email).all()
        totalCount = len(Address)
        result = []
        if Address:
            for item in Address:
                result.append({
                    'id': item.id,
                    'email': item.email,
                    'addressId': item.addressId,
                    'username': item.username,
                    'phone': item.phone,
                    'defaultFlag': item.defaultFlag,
                    'provinceName': item.provinceName,
                    'cityName': item.cityName,
                    'townName': item.townName,
                    'postCode': item.postCode,
                    'detailAddress': item.detailAddress,
                })
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': result
        }
        return pretty_result(code.OK, data=data, msg='Get address successful')

    @login_required
    def post(self):
        """
        充值表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("username", type=str, location="json", required=True, help='username is required')
        self.parser.add_argument("phone", type=inputs.regex(
            r'((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))'), required=True,
                                 location="json",help='phone is required or format is incorrect')
        self.parser.add_argument("defaultFlag", type=int, location="json", required=True, help='defaultFlag is required')
        self.parser.add_argument("provinceName", type=str, location="json", required=True, help='provinceName is required')
        self.parser.add_argument("cityName", type=str, location="json", required=True, help='cityName is required')
        self.parser.add_argument("townName", type=str, location="json", required=True, help='townName is required')
        self.parser.add_argument("postCode", type=str, location="json", required=True, help='postCode is required')
        self.parser.add_argument("detailAddress", type=str, location="json", required=True, help='detailAddress is required')
        args = self.parser.parse_args()
        if args.defaultFlag:
            AddressModel.updateStatus(AddressModel, args.email);
        Address = AddressModel( email=args.email, addressId=int(time.time()), username=args.username,
                               phone=args.phone.replace("-",""), defaultFlag=args.defaultFlag, provinceName=args.provinceName,
                                  cityName=args.cityName, townName=args.townName, detailAddress=args.detailAddress, postCode=args.postCode)
        AddressModel.add(AddressModel, Address)
        if Address.id:
            return pretty_result(code.OK, msg='Add address successful!')
        else:
            return pretty_result(code.ERROR, msg='Add address failed')

    @login_required
    def put(self):
        """
        充值表信息
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("username", type=str, location="json", required=True, help='username is required')
        self.parser.add_argument("addressId", type=str, location="json", required=True, help='addressId is required')
        self.parser.add_argument("phone", type=inputs.regex(
            r'((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))'), required=True,
                                 location="json", help='phone is required or format is incorrect')
        self.parser.add_argument("defaultFlag", type=int, location="json", required=True,
                                 help='defaultFlag is required')
        self.parser.add_argument("provinceName", type=str, location="json", required=True,
                                 help='provinceName is required')
        self.parser.add_argument("cityName", type=str, location="json", required=True, help='cityName is required')
        self.parser.add_argument("townName", type=str, location="json", required=True, help='townName is required')
        self.parser.add_argument("detailAddress", type=str, location="json", required=True,
                                 help='detailAddress is required')
        args = self.parser.parse_args()
        Address = AddressModel.query.filter_by(addressId=args.addressId).first()
        if Address.defaultFlag == 0 and args.defaultFlag == 1:
            AddressModel.updateStatus(AddressModel, args.email);
        Address.email = args.email
        Address.username = args.username
        Address.phone = args.phone
        Address.defaultFlag = args.defaultFlag
        Address.provinceName = args.provinceName
        Address.cityName = args.cityName
        Address.townName = args.townName
        Address.detailAddress = args.detailAddress
        AddressModel.update(Address)
        if Address.id:
            return pretty_result(code.OK, msg='Update address successful!')
        else:
            return pretty_result(code.ERROR, msg='Update address failed')

    @login_required
    def delete(self):
        self.parser.add_argument("addressId", type=str, required=True, location="json", help='addressId is required')
        args = self.parser.parse_args()
        AddressModel.delete(AddressModel, [args.addressId])
        return pretty_result(code.OK, msg='Delete address successful!')

