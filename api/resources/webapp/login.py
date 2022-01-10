#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/9 10:41 上午
# software: PyCharm

from flask import render_template, redirect, url_for, g
from models.mallUsers import MallUsersModel
from models.inviters import InvitersModel
from .auths import AuthorizationResource
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from common.decorators import login_required
from common.token import generate_confirmation_token, confirm_token
from common.email import send_email
import time, json
import requests
from common.RSA import getRSAtext
from config import setting
import uuid, base64


class MallRegisterResource(Resource):
    """
    Mall用户注册
    """

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        """
        用户注册
        :return: json
        """
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'), required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("username", type=str, required=True, location="json",
                                 help='username is required or format is incorrect')
        self.parser.add_argument("inviterId", type=str, location="json",
                                 help='inviterId is required or format is incorrect')

        # self.parser.add_argument("phone", type=inputs.regex(r'((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))'), required=True, location="json",
        #                          help='phone is required or format is incorrect')
        # self.parser.add_argument("gender", type=str, required=True, location="json",
        #                          help='gender is required or format is incorrect')
        # self.parser.add_argument("birth", type=str, required=True, location="json",
        #                          help='birth is required or format is incorrect')
        self.parser.add_argument("password", type=password_len, required=True, location="json", trim=True, help='password is required or format is incorrect')
        args = self.parser.parse_args()
        MallUserEmailInfo = MallUsersModel.query.filter_by(email=args.email).all()
        for item in MallUserEmailInfo:
            if item.id != args.id:
                return pretty_result(code.ERROR, msg='The email is exit！')
        # mallUser = MallUsersModel(email=args.email, username=args.username, password=MallUsersModel.set_password(MallUsersModel,  getRSAtext(args.password)),
        #                           registered_on=int(time.time()),phone=args.phone.replace('-', ''), gender=args.gender,birthday=args.birth)
        mallUser = MallUsersModel(email=args.email, username=args.username,
                                  password=MallUsersModel.set_password(MallUsersModel, getRSAtext(args.password)),
                                  registered_on=int(time.time()))
        MallUsersModel.add(MallUsersModel, mallUser)
        token = generate_confirmation_token(args.email)
        confirm_url = setting.domain + "/api/v1/mall/confirm?token=" + token
        html = '''
        <p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>
        <p><a href=''' + confirm_url + '''>''' + confirm_url + '''</a></p>
        <br>
        <p>Cheers!</p>'''
        subject = "Please confirm your email"
        send_email(args.email, subject, html)
        if args.inviterId != 'undefined':
            try:
                inviteEmail = base64.b64decode(args.inviterId)
                inviter = InvitersModel(invite=inviteEmail, invited=args.email)
                InvitersModel.add(InvitersModel, inviter)
                userInfo = InvitersModel.query.filter_by(email=inviteEmail).first()
                userInfo.point = setting.Inviter_Point
                InvitersModel.update(userInfo)
            except Exception as e:
                return pretty_result(code.OK,  msg='inviterId is not correct')
        if mallUser.id:
            returnUser = {
                'id': mallUser.id,
                'username': mallUser.username,
                'email': mallUser.email,
                'phone': mallUser.phone,
                'gender': mallUser.gender,
                'birth': mallUser.birthday,
                'confirmed': mallUser.confirmed,
                'login_time': mallUser.login_time
            }
            return pretty_result(code.OK, data=returnUser, msg='User register successful')
        else:
            return pretty_result(code.ERROR, msg='User register failed')


class MallLoginResource(Resource):
    """
    用户登陆
    """

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        """
        用户登陆
        :return: json
        """
        self.parser.add_argument("username", type=str, required=True, location="json",
                                 help='userName is required')
        self.parser.add_argument("password", type=password_len, required=True, location="json", trim=True)
        args = self.parser.parse_args()
        return AuthorizationResource.post(AuthorizationResource, args.username, getRSAtext(args.password), type="user")


class MallLogoutResource(Resource):
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


class CheckUsernameResource(Resource):
    """
    用户名字检查
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        '''
        检查用户名是否存在
        '''
        self.parser.add_argument("username", type=str, required=True, location="args",
                                 help='username is required or format is incorrect')
        args = self.parser.parse_args()
        userNameInfo = MallUsersModel.query.filter_by(username=args.username).all()
        if userNameInfo:
            return pretty_result(code.ERROR, msg='Username is exited')
        else:
            return pretty_result(code.OK, msg='Username check successful！')


class CheckEmailResource(Resource):
    """
    用户邮箱检查
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        '''
        检查用户名是否存在
        '''
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="args",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        userEmailInfo = MallUsersModel.query.filter_by(email=args.email).all()
        if userEmailInfo:
            return pretty_result(code.ERROR, msg='Email is exited')
        else:
            return pretty_result(code.OK, msg='Email check successful！')


class CheckPhoneResource(Resource):
    """
    用户电话号码检查
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        '''
        检查用户名是否存在
        '''
        self.parser.add_argument("phone", type=inputs.regex(
            r'((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))'), required=True,
                                 location="args",
                                 help='phone is required or format is incorrect')
        args = self.parser.parse_args()
        userEmailInfo = MallUsersModel.query.filter_by(phone=args.phone.replace('-', '')).all()
        if userEmailInfo:
            return pretty_result(code.ERROR, msg='Phone is exited')
        else:
            return pretty_result(code.OK, msg='Phone check successful！')


class ConfirmEmailResource(Resource):
    """
    电子邮件确认检查
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        '''
        电子邮件确认
        '''

        self.parser.add_argument("token", type=str, location="args", required=True)
        args = self.parser.parse_args()
        try:
            email = confirm_token(args.token)
        except:
            # flash('The confirmation link is invalid or has expired.', 'danger')
            return pretty_result(code.ERROR, msg='The confirmation link is invalid or has expired.')
        mallUser = MallUsersModel.query.filter_by(email=email).first_or_404()
        if mallUser.confirmed:
            # flash('Account already confirmed. Please login.', 'success')
            return pretty_result(code.OK, msg='Account already confirmed. Please login.')
        else:
            mallUser.confirmed = True
        mallUser.confirmed_on = int(time.time())
        MallUsersModel.update(mallUser)
        # flash('You have confirmed your account. Thanks!', 'success')
        return pretty_result(code.ERROR, msg='You have confirmed your account. Thanks!. Please login.')
        # return redirect(url_for('main.home'))


class ResendResource(Resource):
    """
    发送确认邮件
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        token = generate_confirmation_token(args.email)
        confirm_url = setting.domain + "/api/v1/mall/confirm?token=" + token
        html = '''
                <p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>
                <p><a href=''' + confirm_url + '''>''' + confirm_url + '''</a></p>
                <br>
                <p>Cheers!</p>'''
        subject = "Please confirm your email"
        send_email(args.email, subject, html)
        return pretty_result(code.OK, msg='Account already confirmed. Please login.')


class ValidFBResource(Resource):
    """
    验证FB登陆
    """

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        self.parser.add_argument("accessToken", type=str,required=True, location="json",help='accessToken format is incorrect')
        self.parser.add_argument("userID", type=str, required=True, location="json",
                                 help='userID format is incorrect')
        self.parser.add_argument("inviterId", type=str, location="json",
                                 help='inviterId format is incorrect')
        args = self.parser.parse_args()
        url = "https://graph.facebook.com/debug_token?access_token=" + setting.APP_ID + "%7C" + setting.APP_Secret + "&input_token=" + args.accessToken
        result = requests.get(url)
        result = json.loads(result.content)
        if result.get("data").get("is_valid"):
            url = "https://graph.facebook.com/" + args.userID + "?fields=name,email,gender,hometown&access_token=" + args.accessToken
            result = requests.get(url)
            result = json.loads(result.content)
            MallUserEmailInfo = MallUsersModel.query.filter_by(email=result.get("email")).all()
            if not MallUserEmailInfo:
                avatar = 'https://graph.facebook.com/' + args.userID + '/picture'
                mallUser = MallUsersModel(email=result.get("email"), username=result.get("name").replace(' ', ''),
                                          facebook=args.userID, avatar=avatar, point=setting.Inviter_Point, registered_on=int(time.time()))
                MallUsersModel.add(MallUsersModel, mallUser)
                if args.inviterId:
                    inviteEmail = base64.b64decode(args.inviterId)
                    inviter = InvitersModel(invite=inviteEmail, invited=result.get("email"))
                    InvitersModel.add(InvitersModel, inviter)
                    userInfo = InvitersModel.query.filter_by(email=inviteEmail).first()
                    userInfo.point = setting.Inviter_Point
                    InvitersModel.update(userInfo)
                # if not user.id:
                #     return pretty_result(code.ERROR, msg='Login fail by Facebook.')
            return AuthorizationResource.post(AuthorizationResource, username=args.userID, type="fb")
            # return pretty_result(code.OK, data=result, msg='Facebook login successful.')
        else:
            return pretty_result(code.ERROR, msg='Facebook is not valid.')


class ForgetPasswordResource(Resource):
    """
    发送确认邮件
    """

    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        args = self.parser.parse_args()
        password = uuid.uuid4().hex[:8]
        mallUserInfo = MallUsersModel.query.filter_by(email=args.email).first()
        mallUserInfo.password = MallUsersModel.set_password(MallUsersModel, password)
        MallUsersModel.update(mallUserInfo)
        html = '''
                <p>Welcome! Please keep your password:</p>
                <p>''' + password + '''</p>
                <br>
                <p>Cheers!</p>'''
        subject = "Your Password"
        send_email(args.email, subject, html)
        return pretty_result(code.OK, msg='Please login again.')


class IsLoginResource(Resource):
    """
    发送确认邮件
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        if g.user_id:
            mallUserInfo = MallUsersModel.query.filter_by(id=g.user_id).first()
            return pretty_result(code.OK, data={"email": mallUserInfo.email}, msg='Login successful.')
        else:
            return pretty_result(code.ERROR, msg='Not Login.')