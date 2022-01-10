#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/29 上午11:43
# software: PyCharm

from werkzeug.exceptions import HTTPException
from common.code import OK


class Success(HTTPException):
    code = OK
    msg = 'ok'
    error_code = 0


class DeleteSuccess(HTTPException):
    code = OK
    msg = 'delete ok'
    error_code = 1


class UpdateSuccess(HTTPException):
    code = OK
    msg = 'update ok'
    error_code = 2


class AddSuccess(HTTPException):
    code = OK
    msg = 'add ok'
    error_code = 3


class GetSuccess(HTTPException):
    code = OK
    msg = 'get ok'
    error_code = 4


class ServerError(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake(*￣︶￣)!'
    error_code = 999


class ParameterException(HTTPException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(HTTPException):
    code = 404
    msg = 'the resource are not found'
    error_code = 1001


class AuthFailed(HTTPException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class Forbidden(HTTPException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


class DBError(HTTPException):
    code = 500
    error_code = 998
    msg = 'sql exec error'
