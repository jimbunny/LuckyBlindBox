import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/role/getList",
    method: "get",
    params: data,
  });
}

export function doAdd(data) {
  return request({
    url: "/role/doAdd",
    method: "post",
    data,
  });
}

export function doEdit(data) {
  return request({
    url: "/role/doEdit",
    method: "put",
    data,
  });
}

export function doDelete(data) {
  return request({
    url: "/role/doDelete",
    method: "delete",
    data,
  });
}

export function checkPermission(data) {
  return request({
    url: "/role/permission/check",
    method: "post",
    data,
  });
}
