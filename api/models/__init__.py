# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm
from contextlib import contextmanager
from common.error_code import NotFound, DBError
import logging


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            reason = str(e)
            logging.error(e)
            raise DBError()


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'is_delete' not in kwargs.keys():
            kwargs['is_delete'] = False
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)