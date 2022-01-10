import Vue from "vue";
import { Toast } from 'vant'
import { getUserInfo, login, logout, validFB } from "../../service/user";
import { getCartCount } from "../../service/cart";
import {
    getAccessToken,
    removeAccessToken,
    setAccessToken,
    getRefreshToken,
    removeRefreshToken,
    setRefreshToken,
} from "../../utils/accessToken";
import { resetRouter } from "../../router";
import {
    tokenName,
    refreshTokenName,
} from "../../config/settings";

const state = {
    accessToken: getAccessToken(),
    refreshToken: getRefreshToken(),
    // expiresTime: "",
    username: "",
    avatar: "",
    email: "",
    description: "",
    confirmed: "",
    count: 0,
    cartItemIds: []
};
const getters = {
    accessToken: (state) => state.accessToken,
    username: (state) => state.username,
    avatar: (state) => state.avatar,
    description: (state) => state.description,
    refreshToken: (state) => state.refreshToken,
    expiresTime: (state) => state.expiresTime,
    email: (state) => state.email,
    confirmed: (state) => state.confirmed,
    count: (state) => state.count,
    cartItemIds: (state) => state.cartItemIds,
};
const mutations = {
    setAccessToken(state, accessToken) {
        state.accessToken = accessToken;
    },
    setUsername(state, username) {
        state.username = username;
    },
    setEmail(state, email) {
        state.email = email;
    },
    setDescription(state, description) {
        state.description = description;
    },
    setRefreshToken(state, refreshToken) {
        // 保存延续token
        state.refreshToken = refreshToken;
    },
    // SetExpiresTime(state, expiresTime) {
    //   // 保存token过期时间
    //   let NOW_DATE = parseInt(new Date().getTime() / 1000); // 保存当前登陆时间
    //   state.expiresTime = expiresTime + NOW_DATE;
    // },
    setAvatar(state, avatar) {
        state.avatar = avatar;
    },
    setConfirmed(state, confirmed) {
        state.confirmed = confirmed;
    },
    setCount(state, count) {
        state.count = count;
    },
    setCartItemIds(state, cartItemIds) {
        state.cartItemIds = cartItemIds;
    },
};
const actions = {
    async login({ commit }, userInfo) {
        if (userInfo.type == "fb") {
            const { code, data, msg } = await validFB(userInfo);
            const accessToken = data[tokenName];
            const refreshToken = data[refreshTokenName];
            if (accessToken) {
                commit("setAccessToken", accessToken);
                commit("setRefreshToken", refreshToken); // 保存延续token
                // commit("SetExpiresTime", tokenExpiresTime); // 保存token过期时间
                setAccessToken(accessToken);
                setRefreshToken(refreshToken);
                Toast.success("login successful！")
            } else {
                Toast.fail("login failed！")
            }
        } else {
            const { code, data, msg } = await login(userInfo);
            const accessToken = data[tokenName];
            const refreshToken = data[refreshTokenName];
            if (accessToken) {
                commit("setAccessToken", accessToken);
                commit("setRefreshToken", refreshToken); // 保存延续token
                // commit("SetExpiresTime", tokenExpiresTime); // 保存token过期时间
                setAccessToken(accessToken);
                setRefreshToken(refreshToken);
                Toast.success("login successful！")
                window.location.href = '/'
            } else {
                Toast.fail(msg)
            }
        }
       
    },
    async getInfo({ commit, state }) {
        // const { data } = await getInfo(state.accessToken);
        const { data } = await getUserInfo();
        if (!data) {
            this.$router.push({ path: '/login' })
            // Vue.prototype.$baseMessage(i18n.t("login.relogin"), "error");
            return false;
        }
        let { description, username, avatar, email ,confirmed} = data;
        if (username && avatar && email) {
            commit("setDescription", description);
            commit("setUsername", username);
            commit("setEmail", email);
            commit("setAvatar", avatar);
            commit("setConfirmed", confirmed);
            return data;
        } else {
            Toast.fail("get userinfo failed！")
            return false;
        }
    },

    async updateCartItemIds({ commit }, params) {
        commit("setCartItemIds", params);
    },

    async updateCart({ commit }, params) {
        const { data } = await getCartCount(params)
        commit("setCount", data.length || 0);
    },

    async logout({ commit, dispatch }) {
        await logout();
        commit("setAccessToken", "");
        commit("setRefreshToken", "");
        removeAccessToken();
        removeRefreshToken();
        // this.$router.push({ path: '/login' })
    },
    resetAccessToken({ commit }) {
        commit("setAccessToken", "");
        removeAccessToken();
    },
    resetRefreshToken({ commit }) {
        commit("setRefreshToken", "");
        removeRefreshToken();
    },
    updateAccessToken({ accessToken }) {
        setAccessToken(accessToken);
    },
};
export default { state, getters, mutations, actions };