import request from '../utils/axios'

export function contact(data) {
  return request({
      url: "/mall/advice/doAdd",
      method: "post",
      data,
  });
}

