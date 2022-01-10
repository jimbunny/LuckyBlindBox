#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/29 下午9:45
# software: PyCharm
import datetime
import decimal
import uuid
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from common.error_code import ServerError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime.datetime):
            # 格式化时间
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            # 格式化日期
            return o.strftime('%Y-%m-%d')
        if isinstance(o, decimal.Decimal):
            # 格式化高精度数字
            return str(o)
        if isinstance(o, uuid.UUID):
            # 格式化uuid
            return str(o)
        if isinstance(o, bytes):
            # 格式化字节数据
            return o.decode("utf-8")
        # if isinstance(o, (bool, float, int)):
        #     # 返回元数据
        #     return o
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder