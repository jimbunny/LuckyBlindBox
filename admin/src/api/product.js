import request from "@/utils/request";
import axios from "axios";
import { tokenType } from "@/config/settings";
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
} from "@/utils/accessToken";

export function getList(data) {
  return request({
    url: "/product/getList",
    method: "get",
    params: data,
  });
}

export function getNo(data) {
  return request({
    url: "/product/no",
    method: "get",
    params: data,
  });
}

export function doAdd(data) {
  // return  axios.post('api/v1/productManagement/doAdd', data, {"headers" :{"Authorization":tokenType + getAccessToken()}})
  return request({
    url: "/product/doAdd",
    method: "post",
    // headers: {
    //     'Content-Type': 'multipart/form-data'
    // },
    type: "form",
    data,
  });
}

export function doEdit(data) {
  // return  axios.put('api/v1/productManagement/doEdit', data, {"headers" :{"Authorization":tokenType + getAccessToken()}})
  return request({
    url: "/product/doEdit",
    method: "put",
    type: "form",
    data,
  });
}

export function doDelete(data) {
  return request({
    url: "/product/doDelete",
    method: "delete",
    data,
  });
}

export function checkName(data) {
  return request({
    url: "/product/name/check",
    method: "post",
    params: data,
  });
}
