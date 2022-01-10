#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/29 下午2:00
# software: PyCharm
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.error_code import Success,ServerError
import logging
from app import limiter
from app import rd
from models.tests import TestsModel
from flasgger import swag_from


class TestResource(Resource):
    """
    test list资源类
    """
    # decorators = [limiter.exempt]
    # decorators = [limiter.limit("1/day")]

    def __init__(self):
        self.parser = RequestParser()

    @swag_from('../../docs/swagger/admin/test/test_get.yml', methods=['GET'])
    def get(self):
        """
        Test Method

        swagger_from_file: ../../docs/swagger/test_get.yml

        """
        self.parser.add_argument("username", type=str, required=True, location="args", help='name format is incorrect')
        args = self.parser.parse_args()
        rd.set('username', args.username)
        data = {"username": str(rd.get('username'))}
        logging.error("error info: %s" % "test error")
        # raise InternalServerError()
        # raise Success()
        test = TestsModel()
        test.username = args.username
        TestsModel.add(TestsModel, test)
        if test.id:
            return pretty_result(code.OK, data=data, msg="redis mysql test successful")
        else:
            return pretty_result(code.OK, msg="redis mysql test failed")

    def post(self):
        """
        test
        :return: json
        """
        # return pretty_result(code.OK)
        logging.error("error info: %s" % "test error")
        # raise InternalServerError()
        # raise Success()
        return pretty_result(code.OK)