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


class AddressConfigResource(Resource):
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
        self.parser.add_argument("address", type=str, location="args", help='address format is incorrect')
        self.parser.add_argument("pageNo", type=int, required=True, location="args", help='pageNo format is incorrect')
        self.parser.add_argument("pageSize", type=int, required=True, location="args",
                                 help='pageSize format is incorrect')
        args = self.parser.parse_args()
        items = []
        if args.address:
            address_config_list1 = AddressConfigModel.filter_by_province_name(AddressConfigModel, args.address)
            address_config_list2 = AddressConfigModel.filter_by_city_name(AddressConfigModel, args.address)
            address_config_list3 = AddressConfigModel.filter_by_town_name(AddressConfigModel, args.address)
            address_config_list4 = AddressConfigModel.filter_by_post_code(AddressConfigModel, args.address)
            address_config_list = list(set(address_config_list1 + address_config_list2 + address_config_list3 + address_config_list4))
            totalCount = len(address_config_list)
        else:
            address_config_list = AddressConfigModel.paginate(AddressConfigModel, args.pageNo, args.pageSize)
            totalCount = address_config_list.total
            address_config_list = address_config_list.items
        if address_config_list:
            for item in address_config_list:
                items.append({
                    'id': item.id,
                    'provinceName': item.provinceName,
                    'cityName': item.cityName,
                    'townName': item.townName,
                    'postCode': item.postCode
                })
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='Get address config successful')


class AddressOrderResource(Resource):
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
                                  location="args",required=True,
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        Addresses = AddressModel.query.filter_by(email=args.email).all()
        result = []
        for item in Addresses:
            if item.defaultFlag:
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
        if result:
            return pretty_result(code.OK, data=result[0], msg='Get default address successful')
        else:
            return pretty_result(code.OK, data=False, msg='Get default address is exit!')

    @login_required
    def post(self):
        """
        地址表信息
        :return: json
        """
        self.parser.add_argument("addressId", type=int, location="json",required=True,
                                 help='addressId format is incorrect')
        args = self.parser.parse_args()
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
            return pretty_result(code.OK, data=result[0], msg='Get address by id successful!')
        else:
            return pretty_result(code.ERROR, data=False, msg='Get address by id is not exit!')