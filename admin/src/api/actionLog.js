import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/log/getList",
    method: "get",
    params: data,
  });
}
