#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/30 上午10:30
# software: PyCharm

import time
import sys

from flask_restful import Api as _Api
from werkzeug.exceptions import HTTPException
from flask.signals import got_request_exception
from werkzeug.datastructures import Headers
from flask_restful.utils import http_status_message
from flask import jsonify, current_app, g, make_response
from app import limiter


class Api(_Api):
    def error_router(self, original_handler, e):
        """ Override original error_router to only handle HTTPExceptions. """
        if self._has_fr_route() and isinstance(e, HTTPException):
            try:
                return self.handle_error(e)
            except Exception as e:
                pass  # Fall through to original handler
        return original_handler(e)

    #  全局错误处理
    def handle_error(self, e):
        """Error handler for the API transforms a raised exception into a Flask
        response, with the appropriate HTTP status code and body.

        :param e: the raised Exception object
        :type e: Exception

        """
        got_request_exception.send(current_app._get_current_object(), exception=e)
        if not isinstance(e, HTTPException) and current_app.propagate_exceptions:
            exc_type, exc_value, tb = sys.exc_info()
            if exc_value is e:
                raise
            else:
                raise e

        headers = Headers()
        if isinstance(e, HTTPException):
            code = e.code
            if not code:
                return e
            default_data = {
                'code': code,
                'message': getattr(e, 'description', http_status_message(code))
            }
            headers = e.get_response().headers
        else:
            code = 500
            default_data = {
                'code': code,
                'message': http_status_message(code),
            }

        # Werkzeug exceptions generate a content-length header which is added
        # to the response in addition to the actual content-length header
        # https://github.com/flask-restful/flask-restful/issues/534
        remove_headers = ('Content-Length',)

        for header in remove_headers:
            headers.pop(header, None)

        data = getattr(e, 'data', default_data)

        if code and code >= 500:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)

        error_cls_name = type(e).__name__
        if error_cls_name in self.errors:
            custom_data = self.errors.get(error_cls_name, {})
            code = custom_data.get('status', 500)
            data.update(custom_data)

        if code == 406 and self.default_mediatype is None:
            # if we are handling NotAcceptable (406), make sure that
            # make_response uses a representation we support as the
            # default mediatype (so that make_response doesn't throw
            # another NotAcceptable error).
            supported_mediatypes = list(self.representations.keys())
            fallback_mediatype = supported_mediatypes[0] if supported_mediatypes else "text/plain"
            resp = self.make_response(
                data,
                code,
                headers,
                fallback_mediatype = fallback_mediatype
            )
        else:
            resp = self.make_response(data, code, headers)

        if code == 401:
            resp = self.unauthorized(resp)

        if code == 429:
            current_limit = g.view_rate_limit  # 可以从g变量获得 限制频率
            p = limiter.limiter.get_window_stats(*current_limit)[0]  # 获得限制到什么时候
            retry_after = int(p - time.time())  # 多少秒之后 限制解除
            ret = {
                'code': code,
                'error': 'excess request limit!',
                'msg': 'current_request:%s, wait %ss to request again' % (current_limit[0], retry_after)
            }
            resp = make_response(jsonify(ret), 429)

        if code == 4101:
            ret = {
                "code": 4101,
                "data": data,
                "msg": "请求参数错误"
            }
            resp = make_response(jsonify(ret), 4101)
        return resp
