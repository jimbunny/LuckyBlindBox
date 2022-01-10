#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/29 下午4:59
# software: PyCharm


class RedPrint:
    def __init__(self, name):
        # self.name 就是视图中的文件级别的路由
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        print(self.mound)
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
