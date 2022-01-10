#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

import string
import logging

import flask_restful
from flask import abort, jsonify, request

from hashids import Hashids
from models import db
from common import code, pretty_result
# 添加请求钩子
from common.middlewares import jwt_authentication
from Flask import Flask
from flask import got_request_exception
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_redis import FlaskRedis
from flasgger import Swagger


def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    # sender.logger.exception('Got exception %s: ', exception)
    logging.error('Got exception during processing: %s', exception)


app = Flask(__name__)

rd = FlaskRedis(app)

#  limit限制
# def limit_key_func():
#     return str(flask_request.headers.get("X-Forwarded-For", '127.0.0.1'))

# REDIS_URL = "redis://:password@localhost:6379/0"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config.get("RATELIMIT_STORAGE_URL"),
    headers_enabled=True  # X-RateLimit写入响应头。
)

# route 错误日志
got_request_exception.connect(log_exception, app)

hash_ids = Hashids(salt='hvwptlmj129d5quf', min_length=8, alphabet=string.ascii_lowercase + string.digits)

# 保留flask原生异常处理
handle_exception = app.handle_exception
handle_user_exception = app.handle_user_exception


def _custom_abort(http_status_code, **kwargs):
    """
    自定义abort 400响应数据格式
    """
    if http_status_code == 400:
        message = kwargs.get('message')
        if isinstance(message, dict):
            param, info = list(message.items())[0]
            data = '{}:{}!'.format(param, info)
            return abort(jsonify(pretty_result(code.PARAM_ERROR, data=data)))
        else:
            return abort(jsonify(pretty_result(code.PARAM_ERROR, data=message)))
    return abort(http_status_code)


def _access_control(response):
    """
    解决跨域请求
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,PUT,PATCH,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 86400
    return response


def register_blueprints(app):
    # 注册蓝图
    from routes import api_v1_admin, api_v1_webapp
    app.register_blueprint(api_v1_admin, url_prefix='/api/v1/admin')
    app.register_blueprint(api_v1_webapp, url_prefix='/api/v1/webapp')


def create_app(config):
    """
    创建app
    """
    # 添加配置
    app.config.from_object(config)
    # 解决跨域
    app.after_request(_access_control)
    # 自定义abort 400 响应数据格式
    flask_restful.abort = _custom_abort

    @app.before_request
    def before_request():
        jwt_authentication()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    @limiter.request_filter
    def ip_whitelist():
        if request.remote_addr in app.config.get('blackList', []):
            return False
        return request.remote_addr in app.config.get('whiteList', ['127.0.0.1'])

    # 数据库初始化
    db.init_app(app)
    limiter.init_app(app)
    register_blueprints(app)

    # swagger api文档
    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config['title'] = app.config['SWAGGER_TITLE']  # 配置大标题
    swagger_config['description'] = app.config['SWAGGER_DESC']  # 配置公共描述内容
    swagger_config['host'] = app.config['SWAGGER_HOST']  # 请求域名

    # swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
    # swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
    # swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
    # swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
    Swagger(app, config=swagger_config)

    # 使用flask原生异常处理程序
    # app.handle_exception = handle_exception
    # app.handle_user_exception = handle_user_exception
    return app
