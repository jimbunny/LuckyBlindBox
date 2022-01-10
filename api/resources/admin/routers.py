#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/19 3:25 下午
# software: PyCharm
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
from app import app
import json, os

router_file_path = os.path.join(os.path.dirname(app.instance_path), "config", 'router')


class RouterResource(Resource):
    """
    router list resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        get router info
        :return: json
        """
        self.parser.add_argument("permission", type=str, default='super', location="args", help='permission is json')
        args = self.parser.parse_args()
        filePath = os.path.join(router_file_path, 'router.json')
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        routerFilePath = os.path.join(router_file_path, 'super_router.json')
        with open(routerFilePath, 'r', encoding='utf-8') as load_f2:
            load_dict2 = json.load(load_f2)
        if args.permission == "super":
            return pretty_result(code.OK, data=load_dict2["data"] + load_dict["data"], msg="get router successful!")
        else:
            return pretty_result(code.OK, data=load_dict["data"], msg="get router successful!")

    @login_required
    def put(self):
        """
        update router info
        :return: json
        """
        self.parser.add_argument("router", required=True, type=list, location="json", help='router is list')
        args = self.parser.parse_args()
        data = {
          "code": 200,
          "msg": "success",
          "data": args.router
        }
        filePath = os.path.join(router_file_path, 'router.json')
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        return pretty_result(code.OK, data=args.router, msg="update router successful!")