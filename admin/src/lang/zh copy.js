/* eslint-disable */
import { okCode, errorCode } from "@/config/settings";
import { getLanguage } from "@/api/language"; // 封装好的国际化的接口

let zhLocale = {};
getLanguage({ // 进行请求
    language: "zh" // 请求参数
}).then(res => {
    if (res.code == okCode) {
        zhLocale = res.data;
        console.log(zhLocale)
        alert("aaaa")
        return zhLocale;
    } else {
        console.log(res.message);
    }
})
module.exports = zhLocale; // 输出