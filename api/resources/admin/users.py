#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from flask import jsonify, request, current_app, g
from models.adminUsers import AdminUsersModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from sqlalchemy.exc import SQLAlchemyError
from common.decorators import login_required


class UserResource(Resource):
    """
    users resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        get user list info
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        args = self.parser.parse_args()
        user_list = AdminUsersModel.paginate(AdminUsersModel, args.pageNo, args.pageSize, not_permission="SuperAdmin")
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': user_list.total,
            'items': user_list.items
        }
        return pretty_result(code.OK, data=data, msg='get user info successful！')

    @login_required
    def post(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("password", type=password_len, location="json", trim=True)
        args = self.parser.parse_args()
        userEmailInfo = AdminUsersModel.is_email(AdminUsersModel, email=args.email)
        if userEmailInfo:
            return pretty_result(code.ERROR, msg='The email is registered！')
        userInfo = AdminUsersModel.get(_id=args.id)
        userInfo.email = args.email
        if args.password:
            userInfo.password = AdminUsersModel.set_password(AdminUsersModel, args.password)
        AdminUsersModel.update(userInfo)
        return pretty_result(code.OK, msg='add user info successful！')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        self.parser.add_argument("password", type=password_len, location="json", trim=True)
        args = self.parser.parse_args()
        userEmailInfo = AdminUsersModel.query.filter_by(email=args.email).first()
        if userEmailInfo and userEmailInfo.id != args.id:
            return pretty_result(code.ERROR, msg='The email is registered！')
        userInfo = AdminUsersModel.get(AdminUsersModel, _id=args.id)
        userInfo.email = args.email
        userInfo.permission = args.permission
        if args.password:
            userInfo.password = args.password
        AdminUsersModel.update(userInfo)
        return pretty_result(code.OK, msg='update user info successful！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        args = self.parser.parse_args()
        AdminUsersModel.delete(AdminUsersModel, args.ids)
        return pretty_result(code.OK, msg='delete user info successful！')
