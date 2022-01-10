import request from '../utils/axios'

export function GetCouponInfo(data) {
  return request({
      url: "/mall/coupon/getList",
      method: "get",
      params:data,
  });
}

export function ExchangeCoupon(data) {
  return request({
      url: "/mall/coupon/exchange",
      method: "post",
      data,
  });
}

export function UseCoupon(data) {
  return request({
      url: "/mall/coupon/use",
      method: "get",
      params: data,
  });
}
