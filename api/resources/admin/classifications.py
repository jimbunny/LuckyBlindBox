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

from models.classifications import ClassificationModel
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
import json, os


class ClassificationResource(Resource):
    """
    classification resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        get classification info list
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("name", type=str, location="args", help='name is required')

        args = self.parser.parse_args()
        classification_list = ClassificationModel.paginate(ClassificationModel, args.pageNo, args.pageSize, name=args.name)
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': classification_list.total,
            'items': classification_list.items
        }
        return pretty_result(code.OK, data=data, msg='get classification info successful！')

    @login_required
    def post(self):
        """
        create permission info
        :return: json
        """
        self.parser.add_argument("name", type=str, required=True, location="json", help='name is required')
        self.parser.add_argument("rank", type=int, required=True, location="json", help='rank is required')
        args = self.parser.parse_args()
        classificationInfo = ClassificationModel.is_name(ClassificationModel,name=args.name)
        if classificationInfo:
            return pretty_result(code.ERROR, msg='the classification name is exit！')
        classification = ClassificationModel()
        classification.name = args.name
        classification.rank = args.rank
        ClassificationModel.add(ClassificationModel, classification)
        if classification.id:
            return pretty_result(code.OK, msg='add classification info successful!')
        else:
            return pretty_result(code.ERROR, msg='add classification info failed!')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("name", type=str, required=True, location="json", help='name is required')
        self.parser.add_argument("rank", type=int, required=True, location="json", help='rank is required')
        args = self.parser.parse_args()
        classification = ClassificationModel.get(ClassificationModel, _id=args.id)
        classification.name = args.name
        classification.rank = args.rank
        ClassificationModel.update(classification)
        return pretty_result(code.OK, msg='update classification info successful！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        args = self.parser.parse_args()
        ClassificationModel.delete(ClassificationModel, args.ids)
        return pretty_result(code.OK, msg='delete classification info successful!')


class ClassificationNameResource(Resource):
    """
    name resource class
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def post(self):
        """
        check classification code is exit
        :return: json
        """
        self.parser.add_argument("name", type=str, required=True, location="json", help='name is required')
        self.parser.add_argument("status", type=str, required=True, location="json", help='status is required')
        self.parser.add_argument("id", type=int, location="json", help='id is required')
        args = self.parser.parse_args()
        classificationInfo = ClassificationModel.query.filter_by(name=args.name).first()
        if not classificationInfo:
            return pretty_result(code.OK, data={"status": False}, msg="successful!")
        else:
            if args.status == 'add':
                return pretty_result(code.OK, data={"status": True}, msg="classification name is exit!")
            else:
                if classificationInfo.id == args.id:
                    return pretty_result(code.OK, data={"status": False}, msg="successful!")
                else:
                    return pretty_result(code.OK, data={"status": True}, msg="classification name is exit!")
