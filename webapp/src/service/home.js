import request from '../utils/axios'

// export function getHome(params) {
//   return axios.get('/index-infos');
// }

export function getProductList(data) {
  return request({
      url: "/packageManagement/getList",
      method: "get",
      params: data,
  });
}

export function getSwipeList(data) {
  return request({
      url: "/swipeManagement/getList",
      method: "get",
      params: data,
  });
}