#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import Blueprint
from routes.API import Api
from resources.admin import testAPI, login, auths, languages, users, routers, icons, roles, menus, products, logs, \
    images, classifications, packages
from common.code import errors

api_v1_admin = Blueprint('api_v1_admin', __name__)

api = Api(api_v1_admin, catch_all_404s=True, serve_challenge_on_401=True, errors=errors)

api.add_resource(testAPI.TestResource, '/test', endpoint='get_test')
#  login
api.add_resource(login.RegisterResource, '/register')
api.add_resource(login.LoginResource, '/login')
api.add_resource(login.LogoutResource, '/logout')
api.add_resource(login.UserResource, '/user/info')
api.add_resource(auths.AuthorizationResource, '/refresh/token')
# language
api.add_resource(languages.LanguageResource, '/language/i18n', endpoint='getLanguage')
api.add_resource(languages.LanguageResource, '/language/getTitle', endpoint='postTitle')
api.add_resource(languages.LanguageResource, '/language/doEdit', endpoint='putTitle')
api.add_resource(languages.LanguageResource, '/language/doDelete', endpoint='deleteTitle')
api.add_resource(languages.LanguageFileResource, '/language/doEditFile', endpoint='putLanguageFile')
# route
api.add_resource(routers.RouterResource, '/router/getList', endpoint='getRouter')
api.add_resource(routers.RouterResource, '/router/doEdit', endpoint='putRouter')
# menu
api.add_resource(menus.MenuResource, '/menu/checked', endpoint='getCheckedMenu')
api.add_resource(menus.MenuResource, '/menu/permission/doEdit', endpoint='putPermissionEdit')
# # user
api.add_resource(users.UserResource, '/user/getList', endpoint='getUserList')
api.add_resource(users.UserResource, '/user/doEdit', endpoint='putUser')
api.add_resource(users.UserResource, '/user/doDelete', endpoint='deleteUser')
api.add_resource(users.UserResource, '/user/doEditUser', endpoint='postUser')
api.add_resource(login.RegisterResource, '/user/doAdd', endpoint='addUser')
# role
api.add_resource(roles.RoleResource, '/role/getList', endpoint='getRole')
api.add_resource(roles.RoleResource, '/role/doAdd', endpoint='postRole')
api.add_resource(roles.RoleResource, '/role/doEdit', endpoint='putRole')
api.add_resource(roles.RoleResource, '/role/doDelete', endpoint='deleteRole')
api.add_resource(roles.PermissionResource, '/role/permission/check', endpoint='postCheckPermission')
# icon
api.add_resource(icons.ColorfulIconResource, '/icon/getList', endpoint='getIconList')
# # package
api.add_resource(packages.PackageResource, '/package/getList', endpoint='getPackage')
api.add_resource(packages.PackageResource, '/package/doAdd', endpoint='addPackage')
api.add_resource(packages.PackageResource, '/package/doEdit', endpoint='editPackage')
api.add_resource(packages.PackageResource, '/package/doDelete', endpoint='deletePackage')
api.add_resource(packages.PackageNameResource, '/package/name/check', endpoint='checkPackageName')
api.add_resource(packages.PackageIDResource, '/package/no', endpoint='getPackageNo')
api.add_resource(packages.PackageDetailResource, '/package/detail', endpoint='getPackageDetail')
api.add_resource(packages.PackageAwardResource, '/package/award', endpoint='getPackageAward')
# product
api.add_resource(products.ProductResource, '/product/getList', endpoint='getProductList')
api.add_resource(products.ProductResource, '/product/doAdd', endpoint='postProduct')
api.add_resource(products.ProductResource, '/product/doEdit', endpoint='putProduct')
api.add_resource(products.ProductResource, '/product/doDelete', endpoint='deleteProduct')
api.add_resource(products.ProductNoResource, '/product/no', endpoint='getProductNo')
api.add_resource(products.ProductDetailResource, '/product/detail', endpoint='getProductDetail')
# classification
api.add_resource(classifications.ClassificationResource, '/classification/getList', endpoint='getClassificationList')
api.add_resource(classifications.ClassificationResource, '/classification/doAdd', endpoint='postClassifications')
api.add_resource(classifications.ClassificationResource, '/classification/doEdit', endpoint='putClassification')
api.add_resource(classifications.ClassificationResource, '/classification/doDelete', endpoint='deleteClassification')
api.add_resource(classifications.ClassificationNameResource, '/classification/name/check', endpoint='postCheckName')
# log
# api.add_resource(logs.LogResource, '/log/getList', endpoint='getLog')
# image
api.add_resource(images.ImageResource, '/image', endpoint='getImage')
