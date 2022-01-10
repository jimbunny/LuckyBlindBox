import request from '../utils/axios'

export function getDetail(data) {
  return request({
      url: "/product/detail",
      method: "get",
      params: data,
  });
}

export function getAward(data) {
  return request({
      url: "/package/award",
      method: "post",
      data,
  });
}

// export function getDetail(id) {
//   return axios.get(`/goods/detail/${id}`);
// }

// export function getCategory() {
//   return axios.get('/categories');
// }

// export function search(params) {
//   return axios.get('/search', { params });
// }

