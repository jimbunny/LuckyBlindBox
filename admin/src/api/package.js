import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/package/getList",
    method: "get",
    params: data,
  });
}

export function getNo(data) {
  return request({
    url: "/package/getNo",
    method: "get",
    params: data,
  });
}

export function doAdd(data) {
  return request({
    url: "/package/doAdd",
    method: "post",
    type: "form",
    data,
  });
}

export function doEdit(data) {
  return request({
    url: "/package/doEdit",
    method: "put",
    type: "form",
    data,
  });
}

export function doDelete(data) {
  return request({
    url: "/package/doDelete",
    method: "delete",
    data,
  });
}

export function checkName(data) {
  return request({
    url: "/package/name/check",
    method: "get",
    params: data,
  });
}
