#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from flask import jsonify, request, current_app, g
from models.logs import LogsModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from sqlalchemy.exc import SQLAlchemyError
from common.decorators import login_required


class LogResource(Resource):
    """
    log management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取用户列表信息
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("username", type=str, required=True, location="args", help='username is required')
        self.parser.add_argument("model", type=str, required=True, location="args", help='model is required')
        self.parser.add_argument("action", type=str, required=True, location="args", help='action is required')
        args = self.parser.parse_args()
        log_list = LogsModel.paginate(LogsModel, args.pageNo, args.pageSize)
        items = []
        totalCount = log_list.total
        log_list = log_list.items
        if args.username:
            log_list = LogsModel.filter_by_username_model_action(LogsModel, args.username, args.model, args.action)
            totalCount = len(log_list)
        for log in log_list:
            items.append(
                {
                    'id': log.id,
                    'username': log.username,
                    'model': log.model,
                    'action': log.action,
                    'content': log.content,
                    'updateTime': log.update_time.strftime("%m/%d/%Y %H:%M:%S")
                }
            )
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='日志信息获取成功！')
