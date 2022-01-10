#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from flask import g
from models.packages import PackagesModel
# from models.carts import CartsModel
# from models.mallUsers import MallUsersModel
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
from models.logs import LogsModel
from werkzeug.datastructures import FileStorage
from config import setting
from models.products import ProductsModel
import datetime

import os
filePath = r'./downloads/package/'
if not os.path.exists(filePath):
    os.makedirs(filePath)


class PackageResource(Resource):
    """
    package resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    # @login_required
    def get(self):
        """
        get package info list
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("name", type=str, required=True, location="args", help='name is required')
        self.parser.add_argument("_type", type=str, required=True, location="args", help='_type is required')
        args = self.parser.parse_args()
        package_list = PackagesModel.paginate(PackagesModel, args.pageNo, args.pageSize, name=args.name,
                                              _type=args._type)
        items = []
        package_lists = package_list.items
        for package in package_lists:
            coverFileList = []
            coverImages = package.cover_img.split(",")
            for i in coverImages:
                coverUrl = setting.domain + "/api/v1/admin/image/get?type=package&dir=cover&id=" + i
                coverFileList.append({"name": i, "url": coverUrl})
            package.cover_img = coverFileList
            detailFileList = []
            detailImages = package.detail_img.split(",")
            for i in detailImages:
                detailUrl = setting.domain + "/api/v1/admin/image/get?type=package&dir=detail&id=" + i
                detailFileList.append({"name": i, "url": detailUrl})
            package.detail_img = detailFileList
            items.append(package)
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': package_list.total,
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='get package info successful！')

    @login_required
    def post(self):
        self.parser.add_argument("name", type=str, required=True, location="form", help='name is required')
        self.parser.add_argument("no", type=str, required=True, location="form", help='no is required')
        self.parser.add_argument("type", type=str, required=True, location="form", help='type is required')
        self.parser.add_argument("gender", type=str, required=True, location="form", help='gender is required')
        self.parser.add_argument("size", type=str, required=True, location="form", help='size is required')
        self.parser.add_argument("age", type=str, required=True, location="form", help='age is required')
        self.parser.add_argument("Pclass", type=str, required=True, location="form", help='Pclass is required')
        self.parser.add_argument("count", type=str, required=True, location="form", help='count is required')
        # self.parser.add_argument("price", type=int, required=True, location="form", help='price is required')
        # self.parser.add_argument("total", type=int, required=True, location="form", help='total is required')
        self.parser.add_argument("point", type=int, required=True, location="form", help='point is required')
        self.parser.add_argument("picture", type=FileStorage, required=True, location='files', action='append',
                                 help='picture is required')
        self.parser.add_argument("description", type=FileStorage, required=True, location='files', action='append',
                                 help='description is required')
        self.parser.add_argument("remark", type=str, location="form", help='remark is required')
        self.parser.add_argument("updateUser", type=str, required=True, location="form", help='updateUser is required')
        self.parser.add_argument("removeList", type=str, required=True, location="form", help='removelist is required')
        self.parser.add_argument("removeList2", type=str, required=True, location="form", help='removelist2 is required')
        args = self.parser.parse_args()
        packageInfo = PackageModel.query.filter_by(name=args.name).all()
        if packageInfo:
            return pretty_result(code.ERROR, msg='该套餐名称管理已经被添加！')
        removeList = args.removeList.split(",")
        pictureList = ''
        for item in args.picture:
            if item.filename in removeList:
                continue
            new_fname = filePath + str(item.filename) + '.png'
            item.save(new_fname)
            pictureList = pictureList + str(item.filename) + ","
        pictureList = pictureList[:-1]

        removeList2 = args.removeList2.split(",")
        pictureList2 = ''
        for item in args.description:
            if item.filename in removeList2:
                continue
            new_fname = filePath + str(item.filename) + '.png'
            item.save(new_fname)
            pictureList2 = pictureList2 + str(item.filename) + ","
        pictureList2 = pictureList2[:-1]

        Package = PackageModel(name=args.name, no=args.no, gender=args.gender, size=args.size, age=args.age,
                               Pclass=args.Pclass, count=args.count, type=args.type, description=pictureList2,
                                point=args.point, picture=pictureList, remark=args.remark, updateUser=args.updateUser)
        PackageModel.add(PackageModel, Package)
        if Package.id:
            content = str({"name": args.name, "gender": args.gender,"no":args.no, "size": args.size, "age": args.age,
                           "Pclass": args.Pclass, "count":args.count, "type": args.type, "description": pictureList2,
                           "remark": args.remark, "point": args.point, "picture":pictureList,"updateUser": args.updateUser})
            log = LogsModel(username=args.updateUser, model="package", action="add", content=content)
            LogsModel.add(LogsModel, log)
            return pretty_result(code.OK, msg='套餐管理信息添加成功！')
        else:
            return pretty_result(code.ERROR, msg='套餐管理信息添加失败！')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="form", help='id is required')
        self.parser.add_argument("no", type=str, required=True, location="form", help='no is required')
        self.parser.add_argument("name", type=str, required=True, location="form", help='name is required')
        self.parser.add_argument("type", type=str, required=True, location="form", help='type is required')
        self.parser.add_argument("gender", type=str, required=True, location="form", help='gender is required')
        self.parser.add_argument("size", type=str, required=True, location="form", help='size is required')
        self.parser.add_argument("age", type=str, required=True, location="form", help='age is required')
        self.parser.add_argument("Pclass", type=str, required=True, location="form", help='Pclass is required')
        self.parser.add_argument("count", type=str, required=True, location="form", help='count is required')
        # self.parser.add_argument("price", type=int, required=True, location="form", help='price is required')
        # self.parser.add_argument("total", type=int, required=True, location="form", help='total is required')
        self.parser.add_argument("picture", type=FileStorage, location='files', action='append',
                                 help='picture is file')
        self.parser.add_argument("description", type=FileStorage, location='files', action='append',
                                 help='description is file')
        self.parser.add_argument("point", type=int, required=True, location="form", help='point is required')
        self.parser.add_argument("remark", type=str, location="form", help='remark is required')
        self.parser.add_argument("updateUser", type=str, required=True, location="form", help='updateUser is required')
        self.parser.add_argument("removeList", type=str, required=True, location="form", help='removelist is required')
        self.parser.add_argument("removeList2", type=str, required=True, location="form", help='removelist2 is required')
        args = self.parser.parse_args()
        packageInfo = PackageModel.query.filter_by(name=args.name).all()
        for item in packageInfo:
            if item.id != args.id:
                return pretty_result(code.ERROR, msg='该套餐管理已经被添加！')
        packageInfo = PackageModel.query.filter_by(id=args.id).first()
        packagePictureList = packageInfo.picture.split(",")
        removeList = args.removeList.split(",")
        pictureList = ''
        for j in removeList:
            if j in packagePictureList:
                packagePictureList.remove(j)
                old_fname = filePath + str(j) + '.png'
                if os.path.exists(old_fname):
                    os.remove(old_fname)
                else:
                    print(str(j) + " the file does not exist")
        if args.picture:
            for item in args.picture:
                if item.filename in removeList:
                    continue
                new_fname = filePath + str(item.filename) + '.png'
                item.save(new_fname)
                packagePictureList.append(str(item.filename))
        pictureList = ','.join(packagePictureList)

        packagePictureList2 = packageInfo.description.split(",")
        removeList2 = args.removeList2.split(",")
        pictureList2 = ''
        for j in removeList2:
            if j in packagePictureList2:
                packagePictureList2.remove(j)
                old_fname = filePath + str(j) + '.png'
                if os.path.exists(old_fname):
                    os.remove(old_fname)
                else:
                    print(str(j) + " the file does not exist")
        if args.description:
            for item in args.description:
                if item.filename in removeList2:
                    continue
                new_fname = filePath + str(item.filename) + '.png'
                item.save(new_fname)
                packagePictureList2.append(str(item.filename))
        pictureList2 = ','.join(packagePictureList2)

        packageInfo.id = args.id
        packageInfo.no = args.no
        packageInfo.name = args.name
        packageInfo.type = args.type
        packageInfo.gender = args.gender
        packageInfo.size = args.size
        packageInfo.age = args.age
        packageInfo.Pclass = args.Pclass
        # packageInfo.price = args.price
        # packageInfo.total = args.total
        packageInfo.point = args.point
        packageInfo.picture = pictureList
        packageInfo.description = pictureList2
        packageInfo.remark = args.remark
        packageInfo.updateUser = args.updateUser
        PackageModel.update(packageInfo)
        content = str({"name": args.name, "no":args.no, "type": args.type, "gender": args.gender,
                       "size": args.size, "age": args.age, "Pclass": args.Pclass,
                       "point": args.point,"picture": pictureList, "description": pictureList2, "remark": args.remark,
                       "updateUser": args.updateUser})
        log = LogsModel(username=args.updateUser, model="package", action="edit", content=content)
        LogsModel.add(LogsModel, log)
        return pretty_result(code.OK, msg='套餐管理信息更新成功！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        self.parser.add_argument("updateUser", type=str, required=True, location="json", help='updateUser is required')
        self.parser.add_argument("content", type=list, required=True, location="json", help='content is required')
        args = self.parser.parse_args()
        PackageModel.delete(PackageModel, args.ids)
        for item in args.ids:
            packageInfo = PackageModel.query.filter_by(id=item).first()
            packagePictureList = packageInfo.picture.split(",")
            for j in packagePictureList:
                old_fname = filePath + str(j) + '.png'
                if os.path.exists(old_fname):
                    os.remove(old_fname)
                else:
                    print(str(j) + " the file does not exist")

            packagePictureList2 = packageInfo.description.split(",")
            for j in packagePictureList2:
                old_fname = filePath + str(j) + '.png'
                if os.path.exists(old_fname):
                    os.remove(old_fname)
                else:
                    print(str(j) + " the file does not exist")

        content = str(args.content)
        if len(str(args.content)) > 500:
            content = str(args.ids)
        log = LogsModel(username=args.updateUser, model="package", action="delete", content=content)
        LogsModel.add(LogsModel, log)
        return pretty_result(code.OK, msg='套餐管理信息删除成功！')


class PackageNameResource(Resource):
    """
    package name资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        名字是否存在判断
        :return: json
        """
        self.parser.add_argument("name", type=str, required=True, location="args",
                                 help='name is required')
        args = self.parser.parse_args()
        packageInfo = PackageModel.query.filter_by(name=args.name).all()
        if packageInfo:
            return pretty_result(code.OK, data=False, msg='该套餐管理名称已经被添加！')
        return pretty_result(code.OK, data=True, msg='该套餐管理名称不存在！')


class PackageDetailResource(Resource):
    """
    package detail资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """
        套餐细节信息
        :return: json
        """
        self.parser.add_argument("no", type=str, required=True, location="args",
                                 help='no is required')
        args = self.parser.parse_args()
        package_list = PackageModel.query.filter_by(no=args.no).all()
        items = []
        for package in package_list:
            fileList = []
            fileList2 = []
            url = setting.domain + "/api/v1/pictureManagement/get?type=package&id=" + package.picture
            fileList.append({"name": package.picture, "url": url})
            description = package.description.split(",")
            for i in description:
                url2 = setting.domain + "/api/v1/pictureManagement/get?type=package&id=" + i
                fileList2.append({"name": i, "url": url2})
            items.append(
                {
                    'id': package.id,
                    'no': package.no,
                    'name': package.name,
                    'type': package.type,
                    'gender': package.gender,
                    'size': package.size,
                    'age': package.age,
                    'Pclass': package.Pclass,
                    'count': package.count,
                    # 'price': package.price,
                    # 'total': package.total,
                    'point': package.point,
                    'picture': fileList,
                    'description': fileList2,
                    'remark': package.remark,
                    'updateUser': package.updateUser,
                    'updateTime': package.update_time.strftime("%m/%d/%Y %H:%M:%S")
                }
            )
        if items:
            return pretty_result(code.OK, data=items, msg='Get package detail successful！')
        else:
            return pretty_result(code.ERROR, data=[], msg='The package id is exit！')


class PackageIDResource(Resource):
    """
    packages management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取包裹列表信息
        :return: json
        """
        self.parser.add_argument("type", type=str, required=True, location="args", help='ids is required')
        args = self.parser.parse_args()
        id = PackageModel.get_id(PackageModel)
        no = ""
        if not id[0][0]:
            no = args.type + "%04d" % 1
        else:
            no = args.type + "%04d" % (id[0][0] + 1)
        return pretty_result(code.OK, data=no, msg='获取套餐No信息成功！')


class PackageAwardResource(Resource):
    """
    package detail资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        """
        抽奖信息
        :return: json
        """
        self.parser.add_argument("gender", type=str, required=True, location="json",
                                 help='gender is required')
        self.parser.add_argument("size", type=str, required=True, location="json",
                                 help='size is required')
        self.parser.add_argument("age", type=str, required=True, location="json",
                                 help='age is required')
        self.parser.add_argument("Pclass", type=str, required=True, location="json",
                                 help='Pclass is required')
        self.parser.add_argument("count", type=int, required=True, location="json",
                                 help='count is required')
        self.parser.add_argument("point", type=int, required=True, location="json",
                                 help='point is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        products = ProductsModel.filter_by_gender_size_age_Pclass(ProductsModel, args.gender, args.size, args.age, args.Pclass)
        i = 0
        showData = []
        data=[]
        for item in products:
            print(item)
            if i >= args.count:
                break
            if item.status == "unsold":
                i = i + 1
                showData.append(item)
        if i < args.count:
            for item in products:
                if i >= args.count:
                    break
                if item.status == "online":
                    if (datetime.datetime.now() - item.update_time).total_seconds() > setting.countDown:
                        i = i + 1
                        showData.append(item)
        if i < args.count:
            return pretty_result(code.ERROR, data=[], msg='Get award info failed, Product not enough！')
        else:
            for j in showData:
                # 更新次数和状态
                productsInfo = ProductsModel.query.filter_by(id=j.id).first()
                productsInfo.status = 'online'
                productsInfo.showTimes = productsInfo.showTimes + 1
                ProductsModel.update(productsInfo)
                url = ''
                pictures = productsInfo.picture.split(",")
                for i in pictures:
                    url = setting.domain + "/api/v1/pictureManagement/get?type=product&id=" + i
                    break
                data.append(
                    {
                        'id': productsInfo.id,
                        'no': productsInfo.no,
                        'position': productsInfo.position,
                        'picture': url,
                        'gender': productsInfo.gender,
                        'size': productsInfo.size,
                        'age': productsInfo.age,
                        'Pclass': productsInfo.Pclass,
                        'type': productsInfo.type,
                        'status': productsInfo.status,
                        'inPrice': productsInfo.inPrice,
                        'outPrice': productsInfo.outPrice,
                        'price': productsInfo.price,
                        'level': productsInfo.level,
                        'showTimes': productsInfo.showTimes,
                        'remark': productsInfo.remark,
                        'updateUser': productsInfo.updateUser,
                        'updateTime': productsInfo.update_time.strftime("%m/%d/%Y %H:%M:%S")
                    }
                )
                Cart = CartsModel(email=args.email, no=productsInfo.no)
                CartsModel.add(CartsModel, Cart)
            mallUserInfo = MallUsersModel.query.filter_by(email=args.email).first()
            mallUserInfo.point = mallUserInfo.point - args.point
            MallUsersModel.update(mallUserInfo)
            return pretty_result(code.OK, data=data, msg='Get award info successful！')