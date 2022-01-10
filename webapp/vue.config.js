// vue.config.js
// 这些配置 大家复制就行 基本都是写死的
// 配置之后重启 
 
// 这个配置就是 vue脚手架帮你 开启了一个隐藏的服务器
// 帮你转发了
module.exports = {
    // 修改的配置 配置 proxy 服务器代理
    // "/api/getok.php"
    // http://122.51.238.153/getok.php
    devServer: {
        proxy: {
            // change xxx-api/login => mock/login
            // detail: https://cli.vuejs.org/config/#devserver-proxy
            [process.env.VUE_APP_BASE_API]: {
                target: `http://127.0.0.1:5555/`,
                changeOrigin: true,
                pathRewrite: {
                    ["^" + process.env.VUE_APP_BASE_API]: process.env.VUE_APP_BASE_API,
                },
            },
        },
    }
  }