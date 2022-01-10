/* eslint-disable */
module.exports = {
    // 部署时的URL
    publicPath: process.env.NODE_ENV === "development" ? process.env.VUE_APP_PROJEVT : "/",
    // 生产环境构建文件的目录名
    outputDir: "dist",
    // 放置生成的静态资源 (js、css、img、fonts) 的 (相对于 outputDir 的) 目录。
    assetsDir: "static",
    // 开发环境每次保存时是否输出为eslint编译警告
    lintOnSave: false,
    //标题 （包括初次加载雪花屏的标题 页面的标题 浏览器的标题）
    title: "Yep Box",
    //简写
    abbreviation: "YB",
    //开发环境端口号
    devPort: "8088",
    //版本号
    version: process.env.VUE_APP_VERSION,
    //烦请保留package.json作者信息
    copyright: process.env.VUE_APP_AUTHOR,
    //不经过token校验的路由
    routesWhiteList: ["/login", "/404", "/401"],
    //加载时显示文字
    loadingText: "正在加载中...",
    //token名称
    tokenName: "access_token",
    //刷新token名称
    refreshTokenName: "refresh_token",
    //token表名
    tokenTableName: "ACCESS-TOKEN-TABLE",
    refreshTokenTableName: "REFRESH-TOKEN-TABLE",
    //token存储位置localStorage sessionStorage cookie
    storage: "localStorage",
    // storage: "cookie",
    //token类型
    tokenType: "Bearer ",
    //配后端数据的接收方式application/json;charset=UTF-8或者application/x-www-form-urlencoded;charset=UTF-8
    contentType: "application/json;charset=UTF-8",
    //消息框消失时间
    messageDuration: 3000,
    //最长请求时间
    requestTimeout: 10000,
    //操作正常code
    successCode: 200, //200
    //登录失效code
    invalidCode: 403,
    //无权限code
    noPermissionCode: 401,
    //是否显示在页面高亮错误
    errorLog: ["development", "test", "production"],
    //设置生产环境是否屏蔽f12等开发组工具快捷键
    shieldF12: false,
    //是否开启登录拦截
    loginInterception: true,
    //是否开启登录RSA加密
    loginRSA: false,
    //业务code定义
    okCode: 0,
    errorCode: -1,
    // token 刷新时间
    tokenExpiresTime: 10,
    // 默认语言
    language: "zh",
};