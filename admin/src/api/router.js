import request from "@/utils/request";

export function getRouterList(data) {
  return request({
    url: "/router/getList",
    method: "get",
    params: data,
  });
}

export function updateRouter(data) {
  return request({
    url: "/router/doEdit",
    method: "put",
    data,
  });
}
