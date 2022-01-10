import Vue from "vue";
import i18n from "@/lang";
import { getInfo } from "@/api/user";
import { login, logout } from "@/api/login";
import {
  getAccessToken,
  removeAccessToken,
  setAccessToken,
  getRefreshToken,
  removeRefreshToken,
  setRefreshToken,
} from "@/utils/accessToken";
import { resetRouter } from "@/router";
import {
  tokenName,
  refreshTokenName,
  title,
  // tokenExpiresTime,
} from "@/config/settings";

const state = {
  accessToken: getAccessToken(),
  refreshToken: getRefreshToken(),
  // expiresTime: "",
  userName: "",
  avatar: "",
  email: "",
  permissions: [],
};
const getters = {
  accessToken: (state) => state.accessToken,
  userName: (state) => state.userName,
  avatar: (state) => state.avatar,
  permissions: (state) => state.permissions,
  refreshToken: (state) => state.refreshToken,
  expiresTime: (state) => state.expiresTime,
  email: (state) => state.email,
};
const mutations = {
  setAccessToken(state, accessToken) {
    state.accessToken = accessToken;
  },
  setUserName(state, userName) {
    state.userName = userName;
  },
  setEmail(state, email) {
    state.email = email;
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
  setPermissions(state, permissions) {
    state.permissions = permissions;
  },
};
const actions = {
  async login({ commit }, userInfo) {
    const { data, msg } = await login(userInfo);
    const accessToken = data[tokenName];
    const refreshToken = data[refreshTokenName];
    if (accessToken) {
      commit("setAccessToken", accessToken);
      commit("setRefreshToken", refreshToken); // 保存延续token
      // commit("SetExpiresTime", tokenExpiresTime); // 保存token过期时间
      setAccessToken(accessToken);
      setRefreshToken(refreshToken);
      const hour = new Date().getHours();
      const thisTime =
        hour < 8
          ? i18n.t("login.morning")
          : hour <= 11
          ? i18n.t("login.shangwu")
          : hour <= 13
          ? i18n.t("login.noon")
          : hour < 18
          ? i18n.t("login.afternoon")
          : i18n.t("login.evening");
      Vue.prototype.$baseNotify(
        i18n.t("login.welcome") + `${title}`,
        `${thisTime}！`
      );
    } else {
      Vue.prototype.$baseMessage(
        // `登录接口异常，未正确返回${tokenName}...`,
        msg,
        "error"
      );
    }
  },
  async getInfo({ commit, state }) {
    // const { data } = await getInfo(state.accessToken);
    const { data } = await getInfo();
    if (!data) {
      Vue.prototype.$baseMessage(i18n.t("login.relogin"), "error");
      return false;
    }
    let { permission, username, avatar, email } = data;
    if (permission && username && avatar && email) {
      commit("setPermissions", [permission]);
      commit("setUserName", username);
      commit("setEmail", email);
      commit("setAvatar", avatar);
      return [permission];
    } else {
      Vue.prototype.$baseMessage(i18n.t("login.userFailedMsg"), "error");
      return false;
    }
  },
  async logout({ commit, dispatch }) {
    await logout();
    await dispatch("tagsBar/delAllRoutes", null, { root: true });
    commit("setAccessToken", "");
    commit("setRefreshToken", "");
    commit("setPermissions", []);
    removeAccessToken();
    removeRefreshToken();
    resetRouter();
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
