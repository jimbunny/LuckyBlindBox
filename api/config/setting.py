#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

import os
import multiprocessing
basedir = os.path.abspath(os.path.dirname(__file__))

MODE = 'develop'  # develop: 开发模式; production: 生产模式


class ProductionConfig(object):
    """
    生产配置
    """
    APP_ID = "1129997654166624"
    APP_Secret = "df8e756e14a54c2645a418cc294baa8f"
    avatar = "https://i.gtimg.cn/club/item/face/img/2/15922_100.gif"
    domain = "http://127.0.0.1:5555"
    BIND = '0.0.0.0:5555'
    DEBUG = False
    WORKERS = multiprocessing.cpu_count() * 2 + 1
    WORKER_CONNECTIONS = 10000
    BACKLOG = 64
    TIMEOUT = 60
    LOG_LEVEL = 'INFO'
    LOG_DIR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 100
    LOG_FILE_BACKUP_COUNT = 10
    PID_FILE = 'run.pid'
    # sqlite 数据库配置
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'example.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOSTNAME = '127.0.0.1'
    PORT = '3307'
    DATABASE = 'LuckyBox'
    USERNAME = 'root'
    PASSWORD = '123456'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                                   DATABASE)
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BASEDIR = basedir
    # 安全配置
    CSRF_ENABLED = True
    SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'
    JWT_EXPIRY_HOURS = 1
    JWT_REFRESH_DAYS = 1
    JWT_SECRET = 'jklklsadhfjkhwbii9/sdf\sdf'
    SECURITY_PASSWORD_SALT = 'jklklsadhfjkhwbii9/sdf\sdf'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'yepbox.shop@gmail.com'
    MAIL_PASSWORD = 'Yepbox1122'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'yepbox.shop@gmail.com'

    Inviter_Point = 15
    countDown = 1800

    # whitelist
    whiteList = ["127.0.0.1"]
    blackList = []

    # redis
    RATELIMIT_STORAGE_URL = "redis://127.0.0.1:6379"  # 将被限制不可以再正常访问的请求放入缓存

    # swagger
    SWAGGER_TITLE = "Lucky Blind Box API Doc"  # 配置大标题
    SWAGGER_DESC = "Flask Restful API Doc about shopping!"  # 配置公共描述内容
    SWAGGER_HOST = "http://127.0.0.1:5555"  # 请求域名 http://localhost:5555/apidocs/


class DevelopConfig(object):
    """
    开发配置
    """
    APP_ID = "1129997654166624"
    APP_Secret = "df8e756e14a54c2645a418cc294baa8f"
    avatar = "https://i.gtimg.cn/club/item/face/img/2/15922_100.gif"
    domain = "http://127.0.0.1:5555"
    BIND = '0.0.0.0:5555'
    DEBUG = True
    WORKERS = 2
    WORKER_CONNECTIONS = 1000
    BACKLOG = 64
    TIMEOUT = 30
    LOG_LEVEL = 'DEBUG'
    LOG_DIR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    LOG_FILE_MAX_BYTES = 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 1
    PID_FILE = 'run.pid'
    # sqlite 数据库配置
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'example.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@127.0.0.1/demo"
    HOSTNAME = '127.0.0.1'
    PORT = '3307'
    DATABASE = 'LuckyBox'
    USERNAME = 'root'
    PASSWORD = '123456'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                                   DATABASE)

    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BASEDIR = basedir
    # 安全配置
    CSRF_ENABLED = True
    SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'
    JWT_EXPIRY_HOURS = 1
    JWT_REFRESH_DAYS = 1
    JWT_SECRET = 'jklklsadhfjkhwbii9/sdf\sdf'
    SECURITY_PASSWORD_SALT = 'jklklsadhfjkhwbii9/sdf\sdf'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'yepbox.shop@gmail.com'
    MAIL_PASSWORD = 'wozhdpvhetjtbpjr'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'yepbox.shop@gmail.com'

    Inviter_Point = 15
    countDown = 1800

    # whitelist
    whiteList = ["127.0.0.1"]
    blackList = []

    # redis
    RATELIMIT_STORAGE_URL = "redis://127.0.0.1:6379"  # 将被限制不可以再正常访问的请求放入缓存

    # swagger
    SWAGGER_TITLE = "Lucky Blind Box API Doc"  # 配置大标题
    SWAGGER_DESC = "Flask Restful API Doc about shopping!"  # 配置公共描述内容
    SWAGGER_HOST = "http://127.0.0.1:5555"  # 请求域名 http://localhost:5555/apidocs/


if MODE == 'production':
    config = ProductionConfig
else:
    config = DevelopConfig

