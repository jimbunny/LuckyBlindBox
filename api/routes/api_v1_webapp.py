#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import Blueprint
from flask_restful import Api
from common.code import errors
from resources.webapp import testAPI

api_v1_webapp = Blueprint('api_v1_webapp', __name__)

api = Api(api_v1_webapp, catch_all_404s=True, serve_challenge_on_401=True, errors=errors)

# api.add_resource(testAPI.TestResource, '/test', endpoint='getTest')
# #-------------------Mall-----------------------
# # swipe management
# api.add_resource(swipeManagement.SwipeManagementResource, '/swipeManagement/getList', endpoint='getSwipeManagement')
# api.add_resource(swipeManagement.SwipeManagementResource, '/swipeManagement/doEdit', endpoint='editSwipeManagement')
# # login
# api.add_resource(MallLogin.MallRegisterResource, '/mall/register')
# api.add_resource(MallLogin.MallLoginResource, '/mall/login')
# api.add_resource(MallLogin.MallLogoutResource, '/mall/logout')
# api.add_resource(MallLogin.CheckUsernameResource, '/mall/checkUsername')
# api.add_resource(MallLogin.CheckPhoneResource, '/mall/checkPhone')
# api.add_resource(MallLogin.CheckEmailResource, '/mall/checkEmail')
# api.add_resource(MallLogin.ConfirmEmailResource, '/mall/confirm')
# api.add_resource(MallLogin.ResendResource, '/mall/resend')
# api.add_resource(MallLogin.ForgetPasswordResource, '/mall/forgetPassword')
# api.add_resource(MallLogin.ValidFBResource, '/mall/validFB')
# api.add_resource(MallLogin.IsLoginResource, '/mall/validLogin')
#
# # balance
# api.add_resource(mallUsers.BalanceResource, '/mall/balanceInfo', endpoint='addBalance')
# api.add_resource(mallUsers.BalanceResource, '/mall/balanceInfo', endpoint='getBalance')
#
# # point
# api.add_resource(mallUsers.PointResource, '/mall/pointInfo', endpoint='addPoint')
# api.add_resource(mallUsers.PointResource, '/mall/pointInfo', endpoint='getPoint')
#
# # address
# api.add_resource(address.AddressResource, '/mall/addressInfo', endpoint='addAddress')
# api.add_resource(address.AddressResource, '/mall/addressInfo', endpoint='getAddress')
# api.add_resource(address.AddressResource, '/mall/addressInfo', endpoint='putAddress')
# api.add_resource(address.AddressResource, '/mall/addressInfo', endpoint='deleteAddress')
# api.add_resource(address.AddressConfigResource, '/mall/addressConfigInfo', endpoint='getAddressConfig')
# api.add_resource(address.AddressOrderResource, '/mall/address/default', endpoint='getDefaultAddress')
# api.add_resource(address.AddressOrderResource, '/mall/address/detail', endpoint='getAddressDetail')
# # user
# api.add_resource(mallUsers.MallUserResource, '/mall/userInfo')
# api.add_resource(mallUsers.InvitersResource, '/mall/inviteList')
#
# # advice
# api.add_resource(advices.AdvicesResource, '/mall/advice/getList', endpoint='getAdvice')
# api.add_resource(advices.AdvicesResource, '/mall/advice/doAdd', endpoint='addAdvice')
#
# # cart
# api.add_resource(carts.CartsResource, '/mall/cart/getCount', endpoint='getCartCount')
# api.add_resource(carts.CartsResource, '/mall/cart/productInfo', endpoint='postProductInfo')
# api.add_resource(carts.CartsResource, '/mall/cart/productList/ByIds', endpoint='putCreateOrderInfo')
# api.add_resource(carts.CartsResource, '/mall/cart/deleteProductInfo', endpoint='deleteProductInfo')
#
# # order
# api.add_resource(orders.OrdersResource, '/mall/order/getList', endpoint='getOrderList')
# api.add_resource(orders.OrdersByNoResource, '/mall/order/byNo', endpoint='getOrderByNo')
# api.add_resource(orders.OrdersResource, '/mall/order/doAdd', endpoint='doAddOrders')
# api.add_resource(orders.OrdersResource, '/mall/order/doEdit', endpoint='doEditOrders')
#
# # coupon
# api.add_resource(coupons.CouponsResource, '/mall/coupon/getList', endpoint='getCouponList')
# api.add_resource(coupons.CouponsResource, '/mall/coupon/doAdd', endpoint='postCouponList')
# api.add_resource(coupons.CouponsResource, '/mall/coupon/doEdit', endpoint='putCouponList')
# api.add_resource(coupons.CouponsResource, '/mall/coupon/doDelete', endpoint='deleteCouponList')
# api.add_resource(coupons.ExchangeResource, '/mall/coupon/exchange', endpoint='postCouponKey')
# api.add_resource(coupons.ExchangeResource, '/mall/coupon/use', endpoint='getCoupon')