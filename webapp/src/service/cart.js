import request from '../utils/axios'

export function getCartCount(data) {
  return request({
      url: "/mall/cart/getCount",
      method: "get",
      params: data,
  });
}

export function getCart(data) {
  return request({
      url: "/mall/cart/productInfo",
      method: "post",
      data,
  });
}

export function deleteCartItem(data) {
  return request({
      url: "/mall/cart/deleteProductInfo",
      method: "delete",
      data,
  });
}

export function getByCartItemIds(data) {
  return request({
      url: "/mall/cart/productList/ByIds",
      method: "put",
      data,
  });
}

// export function addCart(params) {
//   return axios.post('/shop-cart', params);
// }

// export function modifyCart(params) {
//   return axios.put('/shop-cart', params);
// }

// export function getCart(params) {
//   return axios.get('/shop-cart', { params });
// }

// export function deleteCartItem(id) {
//   return axios.delete(`/shop-cart/${id}`);
// }

// export function getByCartItemIds(params) {
//   return axios.get('/shop-cart/settle', { params });
// }

