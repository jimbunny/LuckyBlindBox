import request from '../utils/axios'

// export function addAddress(params) {
//   return axios.post('/address', params);
// }

export function AddAddress(data) {
  return request({
      url: "/mall/addressInfo",
      method: "post",
      data,
  });
}

export function EditAddress(data) {
  return request({
      url: "/mall/addressInfo",
      method: "put",
      data,
  });
}

export function DeleteAddress(data) {
  return request({
      url: "/mall/addressInfo",
      method: "delete",
      data,
  });
}

export function getDefaultAddress(data) {
  return request({
      url: "/mall/address/default",
      method: "get",
      params: data,
  });
}
// export function getDefaultAddress() {
//   return axios.get('/address/default');
// }

// export function getAddressList() {
//   return axios.get('/address', { pageNumber: 1, pageSize: 1000 })
// }
export function getAddressConfigList(data) {
  return request({
      url: "/mall/addressConfigInfo",
      method: "get",
      params: data,
  });
}

export function getAddressList(data) {
  return request({
      url: "/mall/addressInfo",
      method: "get",
      params: data,
  });
}

export function getAddressDetail(data) {
  return request({
      url: "/mall/address/detail",
      method: "post",
      data,
  });
}
// export function getAddressDetail(id) {
//   return axios.get(`/address/${id}`)
// }


