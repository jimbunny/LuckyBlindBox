#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/9 10:41 上午
# software: PyCharm

from flask import jsonify, request, current_app, g
from models.adminUsers import AdminUsersModel
from .auths import AuthorizationResource
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from common.decorators import login_required
from sqlalchemy import exists


class RegisterResource(Resource):
    """
    admin user register
    """

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        """
        user register
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json", help='email format is incorrect')
        self.parser.add_argument("username", type=str, required=True, location="json", help='username is required')
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        self.parser.add_argument("password", type=password_len, required=True, location="json", trim=True)
        args = self.parser.parse_args()
        # 判断邮箱是否存在
        adminUserEmailStatus = AdminUsersModel.is_email(AdminUsersModel, email=args.email)
        if adminUserEmailStatus:
            return pretty_result(code.ERROR, msg='The email is registered！')
        # 判断用户名是否存在
        adminUserNameStatus = AdminUsersModel.is_username(AdminUsersModel, username=args.username)
        if adminUserNameStatus:
            return pretty_result(code.ERROR, msg='The username is registered！')
        user = AdminUsersModel()
        user.email = args.email
        user.username = args.username
        user.password = args.password
        user.permission = args.permission
        AdminUsersModel.add(AdminUsersModel, user)
        if user.id:
            return pretty_result(code.OK, data=user, msg='user register successful')
        else:
            return pretty_result(code.ERROR, data='', msg='user register failed')


class LoginResource(Resource):
    """
    user login
    """

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        """
        user login
        :return: json
        """
        self.parser.add_argument("username", type=str, required=True, location="json", help='username is required')
        self.parser.add_argument("password", type=password_len, required=True, location="json", trim=True)
        args = self.parser.parse_args()
        return AuthorizationResource.post(AuthorizationResource, args.username, args.password)


class LogoutResource(Resource):
    """
    用户退出
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        '''
        存在的两个问题
        用户登出
        前端可以直接丢弃当前的 access token，当然，如果再严谨些，后端最好有一个 redis 之类的缓存数据库，如果用户登出，则把对应的 token 加入到缓存中，如果再有请求携带该 token 时，则要先到缓存中查看 token 是否存在，如果存在，那么就要返回该 token 已经是非法的 token 了。
        token 过期续期
        这个问题就可以用到 refresh token 了，当前端根据 access token expire 发现用户的 access token 快要过期时，则使用 refresh token 到后端获取新的 access token，只要保证 refresh token 的过期时间长于 access token 的就可以了。
        '''
        return pretty_result(code.OK, msg='Logout successful！')


class UserResource(Resource):
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
        user = AdminUsersModel.get(AdminUsersModel, g.user_id)
        return pretty_result(code.OK, data=user)
