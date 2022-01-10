#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from models.products import ProductsModel
from models.logs import LogsModel
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
from werkzeug.datastructures import FileStorage
from flask_restful import Resource
from config import setting
from common.utils import coverFilePath, detailFilePath, descriptionFilePath
import datetime
import os


class ProductResource(Resource):
    """
    products resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        get product info
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("name", type=str, required=True, location="args", help='name is required')
        self.parser.add_argument("classification", type=str, required=True, location="args",
                                 help='classification is required')
        args = self.parser.parse_args()
        product_list = ProductsModel.paginate(ProductsModel, args.pageNo, args.pageSize, name=args.name,
                                              classification=args.classification)
        items = []
        product_lists = product_list.items
        for product in product_lists:
            coverFileList = []
            coverImages = product.cover_img.split(",")
            for i in coverImages:
                coverUrl = setting.domain + "/api/v1/admin/image/get?type=product&dir=cover&id=" + i
                coverFileList.append({"name": i, "url": coverUrl})
            product.cover_img = coverFileList
            detailFileList = []
            detailImages = product.detail_img.split(",")
            for i in detailImages:
                detailUrl = setting.domain + "/api/v1/admin/image/get?type=product&dir=detail&id=" + i
                detailFileList.append({"name": i, "url": detailUrl})
            product.detail_img = detailFileList
            descriptionFileList = []
            descriptionImages = product.description_img.split(",")
            for i in descriptionImages:
                descriptionUrl = setting.domain + "/api/v1/admin/image/get?type=product&dir=description&id=" + i
                descriptionFileList.append({"name": i, "url": descriptionUrl})
            product.description_img = descriptionFileList
            items.append(product)
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': product_list.total,
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='get product info successful！')

    @login_required
    def post(self):
        self.parser.add_argument("no", type=str, required=True, location="form", help='no is required')
        self.parser.add_argument("name", type=str, required=True, location="form", help='name is required')
        self.parser.add_argument("classification", type=str, required=True, location="form", help='classification is required')
        self.parser.add_argument("cover_img", type=FileStorage, required=True,  location='files',  action='append',
                                 help='cover_img is required')
        self.parser.add_argument("detail_img", type=FileStorage, required=True, location='files', action='append',
                                 help='detail_img is required')
        self.parser.add_argument("description_img", type=FileStorage, required=True, location='files', action='append',
                                 help='description_img is required')
        self.parser.add_argument("position", type=str, required=True, location="form", help='position is required')
        self.parser.add_argument("package_list", type=list, required=True, location="form", help='package_list is required')
        self.parser.add_argument("status", type=bool, required=True, location="form", help='status is required')
        self.parser.add_argument("in_price", type=int, required=True, location="form", help='inPrice is required')
        self.parser.add_argument("out_price", type=int, required=True, location="form", help='outPrice is required')
        self.parser.add_argument("count", type=int, required=True, location="form", help='count is required')
        self.parser.add_argument("level", type=int, required=True, location="form", help='level is required')
        self.parser.add_argument("rank", type=int, required=True, location="form", help='rank is required')
        self.parser.add_argument("remark", type=str, location="form", help='remark is not required')
        self.parser.add_argument("update_user", type=str, required=True, location="form", help='update_user is required')
        # self.parser.add_argument("removeList", type=str, required=True, location="form", help='removelist is required')
        args = self.parser.parse_args()
        productNoInfo = ProductsModel.query.filter_by(no=args.no).all()
        if productNoInfo:
            return pretty_result(code.ERROR, msg='该商品已经被录入！')
        removeList = args.removeList.split(",")
        pictureList = ''
        for item in args.picture:
            if item.filename in removeList:
                continue
            new_fname = filePath + str(item.filename) + '.png'
            item.save(new_fname)
            pictureList = pictureList + str(item.filename) + ","
        pictureList = pictureList[:-1]
        product = ProductsModel(no=args.no, position=args.position,picture=pictureList, gender=args.gender,
                                size=args.size, age=args.age, Pclass=args.Pclass, type=args.type, name=args.name, description=args.description,
                                status=args.status, inPrice=args.inPrice,outPrice=args.outPrice, price=args.price,
                                level=args.level, remark=args.remark,showTimes=args.showTimes, updateUser=args.updateUser)
        ProductsModel.add(ProductsModel, product)
        if product.id:
            content = str({"no":args.no,"name":args.name,"description":args.description, "position":args.position,"picture":pictureList, "gender":args.gender,
                                "size":args.size, "age":args.age, "Pclass":args.Pclass, "type":args.type,
                                "status":args.status, "inPrice":args.inPrice,"outPrice":args.outPrice, "price":args.price,
                                "level":args.level, "remark":args.remark, "showTimes":args.showTimes, "updateUser":args.updateUser})
            log = LogsModel(username=args.updateUser, model="product", action="add", content=content)
            LogsModel.add(LogsModel, log)
            return pretty_result(code.OK, msg='商品信息创建成功！')
        else:
            return pretty_result(code.Error, msg='商品信息创建失败！')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="form", help='id is required')
        self.parser.add_argument("no", type=str, required=True, location="form", help='no is required')
        self.parser.add_argument("name", type=str, required=True, location="form", help='name is required')
        self.parser.add_argument("description", type=str, required=True, location="form",
                                 help='description is required')
        self.parser.add_argument("position", type=str, required=True, location="form", help='position is required')
        self.parser.add_argument("picture", type=FileStorage, location='files', action='append',
                                 help='picture is file')
        self.parser.add_argument("gender", type=str, required=True, location="form", help='gender is required')
        self.parser.add_argument("size", type=str, required=True, location="form", help='size is required')
        self.parser.add_argument("age", type=str, required=True, location="form", help='age is required')
        self.parser.add_argument("Pclass", type=str, required=True, location="form", help='Pclass is required')
        self.parser.add_argument("type", type=str, required=True, location="form", help='type is required')
        self.parser.add_argument("status", type=str, required=True, location="form", help='status is required')
        self.parser.add_argument("inPrice", type=str, required=True, location="form", help='inprice is required')
        self.parser.add_argument("outPrice", type=str, required=True, location="form", help='outprice is required')
        self.parser.add_argument("price", type=int, required=True, location="form", help='price is required')
        self.parser.add_argument("level", type=int, required=True, location="form", help='level is required')
        self.parser.add_argument("showTimes", type=str, required=True, location="form", help='showTimes is required')
        self.parser.add_argument("remark", type=str, location="form", help='remark is not required')
        self.parser.add_argument("updateUser", type=str, required=True, location="form", help='updateUser is required')
        self.parser.add_argument("removeList", type=str, required=True, location="form", help='removelist is required')
        args = self.parser.parse_args()
        productNoInfo = ProductsModel.query.filter_by(no=args.no).all()
        for item in productNoInfo:
            if item.id != args.id:
                return pretty_result(code.ERROR, msg='该商品编号已存在，不可以编辑！')
        productInfo = ProductsModel.query.filter_by(no=args.no).first()
        productPictureList = productInfo.picture.split(",")
        removeList = args.removeList.split(",")
        pictureList = ''
        for j in removeList:
            if j in productPictureList:
                productPictureList.remove(j)
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
                productPictureList.append(str(item.filename))
        pictureList = ','.join(productPictureList)
        productInfo.no = args.no
        productInfo.name = args.name
        productInfo.description = args.description
        productInfo.position = args.position
        productInfo.picture = pictureList
        productInfo.gender = args.gender
        productInfo.size = args.size
        productInfo.age = args.age
        productInfo.Pclass = args.Pclass
        productInfo.type = args.type
        productInfo.status = args.status
        productInfo.inPrice = args.inPrice
        productInfo.outPrice = args.outPrice
        productInfo.price = args.price
        productInfo.level = args.level
        productInfo.showTimes = args.showTimes
        productInfo.remark = args.remark
        productInfo.updateUser = args.updateUser
        ProductsModel.update(productInfo)
        content = str({"no": args.no,"name":args.name,"description":args.description, "position": args.position, "picture": pictureList, "gender": args.gender,
                       "size": args.size, "age": args.age, "Pclass": args.Pclass, "type": args.type,
                       "status": args.status, "inPrice": args.inPrice, "outPrice": args.outPrice,
                       "price": args.price,"level": args.level,"remark": args.remark,
                       "showTimes": args.showTimes, "updateUser": args.updateUser})
        log = LogsModel(username=args.updateUser, model="product", action="edit", content=content)
        LogsModel.add(LogsModel, log)
        return pretty_result(code.OK, msg='商品信息修改成功！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        self.parser.add_argument("updateUser", type=str, required=True, location="json", help='updateUser is required')
        self.parser.add_argument("content", type=list, required=True, location="json", help='content is required')
        args = self.parser.parse_args()
        for item in args.ids:
            productInfo = ProductsModel.query.filter_by(id=item).first()
            productPictureList = productInfo.picture.split(",")
            for j in productPictureList:
                old_fname = filePath + str(j) + '.png'
                if os.path.exists(old_fname):
                    os.remove(old_fname)
                else:
                    print(str(j) + " the file does not exist")

        ProductsModel.delete(ProductsModel, args.ids)
        content = str(args.content)
        if len(str(args.content)) > 500:
            content = str(args.ids)
        log = LogsModel(username=args.updateUser, model="product", action="delete", content=content)
        LogsModel.add(LogsModel, log)
        return pretty_result(code.OK, msg='商品信息删除成功！')


class ProductNoResource(Resource):
    """
    products management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        product no resource class
        :return: json
        """
        args = self.parser.parse_args()
        id = ProductsModel.get_id(ProductsModel)
        no = ""
        if not id[0][0]:
            no =  "%05d" % 1
        else:
            no = "%05d" % (id[0][0] + 1)
        return pretty_result(code.OK, data=no, msg='get product no successful！')


class ProductNameResource(Resource):
    """
    product name resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        """
        check product code is exit
        :return: json
        """
        self.parser.add_argument("name", type=str, required=True, location="json", help='name is required')
        self.parser.add_argument("status", type=str, required=True, location="json", help='status is required')
        self.parser.add_argument("id", type=int, location="json", help='id is required')
        args = self.parser.parse_args()
        productInfo = ProductsModel.query.filter_by(name=args.name).first()
        if not productInfo:
            return pretty_result(code.OK, data={"status": False}, msg="successful!")
        else:
            if args.status == 'add':
                return pretty_result(code.OK, data={"status": True}, msg="product name is exit!")
            else:
                if productInfo.id == args.id:
                    return pretty_result(code.OK, data={"status": False}, msg="successful!")
                else:
                    return pretty_result(code.OK, data={"status": True}, msg="product name is exit!")


class ProductDetailResource(Resource):
    """
    package detail资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        套餐细节信息
        :return: json
        """
        self.parser.add_argument("no", type=str, required=True, location="args",
                                 help='no is required')
        args = self.parser.parse_args()
        product_list = ProductsModel.query.filter_by(no=args.no).all()
        items = []
        for product in product_list:
            fileList = []
            pictures = product.picture.split(",")
            for i in pictures:
                url = setting.domain + "/api/v1/pictureManagement/get?type=product&id=" + i
                fileList.append({"name": i, "url": url})
            countDown = (datetime.datetime.now() - product.update_time).total_seconds()
            items.append(
                {
                    'id': product.id,
                    'no': product.no,
                    'name': product.name,
                    'description': product.description,
                    'position': product.position,
                    'picture': fileList,
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
        if items:
            return pretty_result(code.OK, data=items, msg='Get product detail successful！')
        else:
            return pretty_result(code.ERROR, data=[], msg='The product no is exit！')
