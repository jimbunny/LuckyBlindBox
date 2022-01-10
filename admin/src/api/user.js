import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/user/getList",
    method: "get",
    params: data,
  });
}
export function doAdd(data) {
  return request({
    url: "/user/doAdd",
    method: "post",
    data,
  });
}

export function doEditUser(data) {
  return request({
    url: "/user/doEditUser",
    method: "post",
    data,
  });
}

export function doEdit(data) {
  return request({
    url: "/user/doEdit",
    method: "put",
    data,
  });
}

export function doDelete(data) {
  return request({
    url: "/user/doDelete",
    method: "delete",
    data,
  });
}

export function getInfo() {
  return request({
    url: "/user/info",
    method: "get",
  });
}
