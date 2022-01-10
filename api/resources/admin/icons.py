#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/19 3:25 下午
# software: PyCharm
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
import json, os


class ColorfulIconResource(Resource):
    """
    router list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        """
        图标信息
        :return: json
        """
        data = [
          "biohazard",
          "binoculars",
          "bookmark",
          "briefcase",
          "calculator",
          "calendar",
          "camera",
          "clock",
          "comments",
          "copyright",
          "database",
          "donate",
          "downloads",
          "film",
          "folder",
          "globe",
          "headset",
          "home",
          "info",
          "key",
          "link",
          "lock",
          "music",
          "phone",
          "plus",
          "redo",
          "ruler",
          "search",
          "share",
          "sms",
          "trademark",
          "undo",
          "upload",
          "voicemail",
        ]
        self.parser.add_argument("title", type=str, location="json",
                                 help='Please input title')
        args = self.parser.parse_args()
        data2 = []
        if args.title:
          for item in data:
            if args.title in item:
              data2.append(item)
        else:
          data2 = data
        result = {"totalCount": len(data), "data": data2}
        return pretty_result(code.OK, data=result)
