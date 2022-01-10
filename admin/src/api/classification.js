import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/classification/getList",
    method: "get",
    params: data,
  });
}

export function doAdd(data) {
  return request({
    url: "/classification/doAdd",
    method: "post",
    data,
  });
}

export function doEdit(data) {
  return request({
    url: "/classification/doEdit",
    method: "put",
    data,
  });
}

export function doDelete(data) {
  return request({
    url: "/classification/doDelete",
    method: "delete",
    data,
  });
}

export function checkName(data) {
  return request({
    url: "/classification/name/check",
    method: "post",
    data,
  });
}
