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

from models.adminRoles import AdminRolesModel
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
from app import app
import json, os

router_file_path = os.path.join(os.path.dirname(app.instance_path), "config", 'router')


class RoleResource(Resource):
    """
    roles resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        get permission info list
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("description", type=str, location="args", help='description is required')

        args = self.parser.parse_args()
        role_list = AdminRolesModel.paginate(AdminRolesModel, args.pageNo, args.pageSize, description=args.description,
                                             not_permission="SuperAdmin")
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': role_list.total,
            'items': role_list.items
        }
        return pretty_result(code.OK, data=data, msg='get permission info successful！')

    @login_required
    def post(self):
        """
        create permission info
        :return: json
        """
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        self.parser.add_argument("description", type=str, required=True, location="json", help='description is required')
        args = self.parser.parse_args()
        rolePermissionInfo = AdminRolesModel.is_permission(AdminRolesModel,permission=args.permission)
        if rolePermissionInfo:
            return pretty_result(code.ERROR, msg='the permission code is exit！')
        role = AdminRolesModel()
        role.description = args.description
        role.permission = args.permission
        AdminRolesModel.add(AdminRolesModel, role)
        if role.id:
            return pretty_result(code.OK, msg='add permission code successful!')
        else:
            return pretty_result(code.ERROR, data='', msg='add permission code failed!')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        self.parser.add_argument("description", type=str, required=True, location="json", help='description is required')
        args = self.parser.parse_args()
        roleInfo = AdminRolesModel.get(AdminRolesModel, _id=args.id)
        roleInfo.description = args.description
        roleInfo.permission = args.permission
        AdminRolesModel.update(roleInfo)
        return pretty_result(code.OK, msg='update permission code successful！')

    def delete_menu_permission(self, routeLIst, permission):
        if len(routeLIst):
            for item in routeLIst:
                if permission in item.get("meta").get("permissions"):
                    item.get("meta").get("permissions").remove(permission)
                if item.get("children"):
                    self.delete_menu_permission(item.get("children"), permission)
        return routeLIst

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        args = self.parser.parse_args()
        filePath = os.path.join(router_file_path, 'router.json')
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        menuList = []
        for _id in args.ids:
            roleInfo = AdminRolesModel.get(AdminRolesModel, _id=_id)
            menuList = self.delete_menu_permission(load_dict["data"], roleInfo.permission)
        data = {
            "code": 200,
            "msg": "success",
            "data": menuList
        }
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        AdminRolesModel.delete(AdminRolesModel, args.ids)
        return pretty_result(code.OK, msg='delete permission code successful!')


class PermissionResource(Resource):
    """
    permissions resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        """
        check permission code is exit
        :return: json
        """
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        args = self.parser.parse_args()
        rolePermissionInfo = AdminRolesModel.is_permission(AdminRolesModel, permission=args.permission)
        if rolePermissionInfo:
            return pretty_result(code.OK, data={"status": True}, msg="permission is exit!")
        else:
            return pretty_result(code.OK, data={"status": False}, msg="successful!")


