import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/swipe/getList",
    method: "get",
    params: data,
  });
}

export function doEdit(data) {
  return request({
    url: "/swipe/doEdit",
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
    url: "/package/checkName",
    method: "get",
    params: data,
  });
}
