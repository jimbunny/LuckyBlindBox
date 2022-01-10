import axios from 'axios'
import { Toast } from 'vant'
import router from '../router'
import store from "@/store";
import _ from "lodash"
import {
    contentType,
    invalidCode,
    noPermissionCode,
    requestTimeout,
    okCode,
    errorCode,
    tokenType,
    debounce,
} from "../config/settings";
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
} from "./accessToken";

axios.defaults.baseURL = process.env.NODE_ENV == 'development' ? 'http://backend-api-01.newbee.ltd/api/v1' : 'http://127.0.0.1:5555/api/v1'
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: requestTimeout,
  headers: {
      "Content-Type": contentType,
  },
});

function startLoading() {
  // 开始加载
  Toast.loading({
      message: '加载中...',
      forbidClick: true,
  });
}
function endLoading() {
  // 结束加载
  Toast.clear()
}

service.interceptors.request.use(
    (config) => {
        if (getAccessToken()) {
            config.headers["Authorization"] =
                tokenType + getAccessToken();
        }
        if (config.data) {
            if (config.type !== "form") {
                config.data = _.pickBy(config.data, _.identity);
            }
        }
        const url = config.url;
        if (url.replace(/[\/]/g, "") === "refreshtoken") {
            config.headers["Authorization"] =
                tokenType + getRefreshToken();
        }
        startLoading()

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

const errorMsg = (message) => {
  return Toast.fail(message)
};

function refreshToken() {
  // instance是当前request.js中已创建的axios实例
  return service.put("/refresh/token").then((res) => res);
}

// 给实例添加一个setToken方法，用于登录后将最新token动态添加到header，同时将token保存在localStorage中
service.setToken = (token) => {
  service.defaults.headers["Authorization"] = tokenType + token;
  setAccessToken(token);
};

// 是否正在刷新的标记
let isRefreshing = false;
// 重试队列，每一项将是一个待执行的函数形式
let requests = [];

service.interceptors.response.use(
  (response) => {
      endLoading()
      const { status, data, config } = response;
      const { code, msg } = data;
      if (code !== okCode && code !== errorCode) {
          switch (code) {
              case invalidCode:
                  errorMsg(msg || `backend API${code}error`);
                  store.dispatch("user/resetAccessToken");
                  store.dispatch("user/resetRefreshToken");
                  break;
              case noPermissionCode:
                router.push({ path: '/login' })
                //   const config = response.config;
                //   if (!isRefreshing) {
                //       isRefreshing = true;
                //       return refreshToken()
                //           .then((res) => {
                //               const { code } = res;
                //               if (code === okCode) {
                //                   const { access_token } = res.data;
                //                   service.setToken(access_token);
                //                   config.headers["Authorization"] = tokenType + access_token;
                //                   config.baseURL = process.env.VUE_APP_BASE_API;
                //                   // 已经刷新了token，将所有队列中的请求进行重试
                //                   requests.forEach((cb) => cb(access_token));
                //                   requests = [];
                //                   return service(config);
                //               } else {
                //                 Toast.fail(`Please login！`)
                //                   router.push({
                //                       path: "/login",
                //                   });
                //               }
                //           })
                //           .catch((res) => {
                //               Toast.fail(`Token Expired，Please login again！`)
                //             //   Message({
                //             //       message: `Token Expired，Please login again！`,
                //             //       type: "error",
                //             //       duration: 10000,
                //             //   });
                //               store.dispatch("user/resetAccessToken");
                //               store.dispatch("user/resetRefreshToken");
                //               console.error("refreshtoken error =>", res);
                //               router.push({
                //                 path: "/login",
                //                 });
                //               // setTimeout(function () {
                //               //   window.location.href = "/";
                //               // }, 3000);
                //           })
                //           .finally(() => {
                //               isRefreshing = false;
                //           });
                //   } else {
                //       // 正在刷新token，将返回一个未执行resolve的promise
                //       return new Promise((resolve) => {
                //           // 将resolve放进队列，用一个函数形式来保存，等token刷新后直接执行
                //           requests.push((token) => {
                //               config.baseURL = process.env.VUE_APP_BASE_API;
                //               config.headers["Authorization"] = tokenType + token;
                //               resolve(service(config));
                //           });
                //       });
                //   }
                  break;
              default:
                  errorMsg(msg || `backend API${code}error`);
                  break;
          }
          if (code == noPermissionCode) {
              Toast.fail("Please login!")
            return ""
          } else {
            return Promise.reject(
                "Request exception interception:" +
                JSON.stringify({ url: config.url, code, msg }) || "Error"
            );
          }     
      } else {
          return data;
      }
  },
  (error) => {
      endLoading()
      /*网络连接过程异常处理*/
      let { message } = error;
      switch (message) {
          case "Network Error":
              message = "backend API connection error";
              break;
          case "timeout":
              message = "backend API timeout";
              break;
          case "Request failed with status code":
              message = "backend API" + message.substr(message.length - 3) + "error";
              break;
      }
      errorMsg(message || "backend API unknown Error");
      return Promise.reject(error);
  }
);

export default service;