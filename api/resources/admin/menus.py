#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/19 3:25 下午
# software: PyCharm
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
from app import app
import json, os

router_file_path = os.path.join(os.path.dirname(app.instance_path), "config", 'router')


class MenuResource(Resource):
    """
    menu resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    def get_menu_checked_by_permission(self, routeLIst, permission, result):
        if len(routeLIst):
            for item in routeLIst:
                if item.get("children"):
                    self.get_menu_checked_by_permission(item.get("children"), permission, result)
                else:
                    if permission in item.get("meta").get("permissions"):
                        result.append(item.get("name"))
        return result

    def add_menu_permission(self, routeLIst, permission, names):
        if len(routeLIst):
            for item in routeLIst:
                if item.get("name") in names:
                    if permission not in item.get("meta").get("permissions"):
                        item.get("meta").get("permissions").append(permission)
                else:
                    if permission in item.get("meta").get("permissions"):
                        item.get("meta").get("permissions").remove(permission)
                if item.get("children"):
                    self.add_menu_permission(item.get("children"), permission, names)
        return routeLIst

    @login_required
    def get(self):
        """
        get menu checked
        :return: json
        """
        self.parser.add_argument("permission", required=True, type=str, location="args", help='permission is str')
        args = self.parser.parse_args()
        filePath = os.path.join(router_file_path, 'router.json')
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        menuList = self.get_menu_checked_by_permission(load_dict["data"], args.permission, [])
        return pretty_result(code.OK, data=menuList)

    @login_required
    def put(self):
        """
        update menu permission info
        :return: json
        """
        self.parser.add_argument("permission", required=True, type=str, location="json", help='permission is str')
        self.parser.add_argument("names", required=True, type=list, location="json", help='names is list')
        args = self.parser.parse_args()
        filePath = os.path.join(router_file_path, 'router.json')
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        menuList = self.add_menu_permission(load_dict["data"], args.permission, args.names)
        data = {
            "code": 200,
            "msg": "success",
            "data": menuList
        }
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        return pretty_result(code.OK)


