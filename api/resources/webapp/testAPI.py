#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/29 下午2:00
# software: PyCharm
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common import code, pretty_result


class TestResource(Resource):
    """
    test list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """
        获取用户信息
        :return: json
        """
        return pretty_result(code.OK)