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

from flask import jsonify, request, current_app, g
from models.advices import AdvicesModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from sqlalchemy.exc import SQLAlchemyError
from common.decorators import login_required


class AdvicesResource(Resource):
    """
    advices management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取建议列表信息
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("email", type=str, location="args", help='email')

        args = self.parser.parse_args()
        advice_list = AdvicesModel.paginate(AdvicesModel, args.pageNo, args.pageSize)
        items = []
        totalCount = advice_list.total
        advice_list = advice_list.items
        if args.email:
            advice_list = AdvicesModel.filter_by_email(AdvicesModel, args.email)
            totalCount = len(advice_list)
        for advice in advice_list:
            items.append(
                {
                    'id': advice.id,
                    'email': advice.email,
                    'username': advice.username,
                    'advice': advice.advice,
                    'create_time': advice.create_time,
                }
            )
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='反馈建议信息获取成功！')

    @login_required
    def post(self):
        """
        创建反馈意见
        :return: json
        """
        self.parser.add_argument("username", type=str, required=True, location="json", help='username is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("advice", type=str, required=True, location="json",
                                 help='advice is required')
        args = self.parser.parse_args()
        advice = AdvicesModel(username=args.username, email=args.email, advice=args.advice)
        AdvicesModel.add(AdvicesModel, advice)
        return pretty_result(code.OK, msg='意见反馈成功！')

