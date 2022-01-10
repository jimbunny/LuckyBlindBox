#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/29 上午10:40
# software: PyCharm

# #简单查询
# print(session.query(User).all())
# print(session.query(User.name, User.fullname).all())
# print(session.query(User, User.name).all())
#
# #带条件查询
# print(session.query(User).filter_by(name='user1').all())
# print(session.query(User).filter(User.name == "user").all())
# print(session.query(User).filter(User.name.like("user%")).all())
#
# #多条件查询
# print(session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all())
# print(session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all())
#
# #sql过滤
# print(session.query(User).filter("id>:id").params(id=1).all())
#
# #关联查询
# print(session.query(User, Address).filter(User.id == Address.user_id).all())
# print(session.query(User).join(User.addresses).all())
# print(session.query(User).outerjoin(User.addresses).all())
#
# #聚合查询
# print(session.query(User.name, func.count('*').label("user_count")).group_by(User.name).all())
# print(session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all())
#
# #子查询
# stmt = session.query(Address.user_id, func.count('*').label("address_count")).group_by(Address.user_id).subquery()
# print(session.query(User, stmt.c.address_count).outerjoin((stmt, User.id == stmt.c.user_id)).order_by(User.id).all())
#
# #exists
# print(session.query(User).filter(exists().where(Address.user_id == User.id)))
# print(session.query(User).filter(User.addresses.any()))

# #限制返回字段查询
# person = session.query(Person.name, Person.created_at,
# Person.updated_at).filter_by(name="zhongwei").order_by(
# Person.created_at).first()
#
# #查询总记录数
#  from sqlalchemy import func
#
# # count User records, without
# # using a subquery.
# session.query(func.count(User.id))
#
# # return count of user "id" grouped
# # by "name"
# session.query(func.count(User.id)).\
#     group_by(User.name)
#
# from sqlalchemy import distinct
#
# # count distinct "name" values
# session.query(func.count(distinct(User.name)))


# def to_dict(self):
#     model_dict = dict(self.__dict__)
#     del model_dict['_sa_instance_state']
#     for key, value in model_dict.items():
#         if isinstance(value, date):
#             model_dict[key] = value.strftime('%Y-%m-%d')
#         if key == 'picture':
#             urls = model_dict[key].split(",")
#             model_dict[key] = setting.domain + "/api/v1/pictureManagement/get?type=product&id=" + urls[0]
#
#     return model_dict
#
#
# def dobule_to_dict(self):
#     result = {}
#     for key in self.__mapper__.c.keys():
#         if getattr(self, key) is not None:
#             result[key] = str(getattr(self, key))
#         else:
#             result[key] = getattr(self, key)
#     return result
#
#
# # 配合todict一起使用
# def to_json(all_vendors):
#     v = [ven.dobule_to_dict() for ven in all_vendors]
#     return v