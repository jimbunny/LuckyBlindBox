/* eslint-disable */
import Vue from "vue";
import App from "./App";
import store from "./store";
import router from "./router";
import "./plugins";
import ElementUI from "element-ui"; //基于Element-UI
import i18n from "./lang";


Vue.use(ElementUI, {
    i18n: (key, value) => i18n.t(key, value),
});

if (process.env.NODE_ENV === "test") {
    const { mockXHR } = require("../mock/static");
    mockXHR();
}

Vue.config.productionTip = false;

new Vue({
    el: "#admin-system",
    router,
    store,
    i18n,
    render: (h) => h(App),
});