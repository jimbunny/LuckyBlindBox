import { asyncRoutes, constantRoutes } from "@/router";
import { getRouterList } from "@/api/router";
import { filterAsyncRoutes, filterRoutes } from "@/utils/handleRoutes";

const state = { routes: [], partialRoutes: [] };
const getters = {
    routes: (state) => state.routes,
    partialRoutes: (state) => state.partialRoutes,
};
const mutations = {
    setRoutes(state, routes) {
        state.routes = constantRoutes.concat(routes);
    },
    setAllRoutes(state, routes) {
        state.routes = constantRoutes.concat(routes);
    },
    setPartialRoutes(state, routes) {
        state.partialRoutes = constantRoutes.concat(routes);
    },
};
const actions = {
    setRoutes({ commit }, permissions) {
        let accessedRoutes;
        if (permissions.includes("SuperAdmin")) {
            accessedRoutes = asyncRoutes || [];
        } else {
            accessedRoutes = filterAsyncRoutes(asyncRoutes, permissions);
        }
        commit("setRoutes", accessedRoutes);
        return accessedRoutes;
    },
    async setAllRoutes({ commit }, permissions) {
        let { data } = await getRouterList();
        data.push({ path: "*", redirect: "/404", hidden: true });
        // let accessRoutes = filterRoutes(data);
        let accessRoutes;
        if (permissions.includes("SuperAdmin")) {
            accessRoutes = filterRoutes(data) || [];
        } else {
            accessRoutes = filterAsyncRoutes(filterRoutes(data), permissions);
        }
        commit("setAllRoutes", accessRoutes);
        return accessRoutes;
    },
    setPartialRoutes({ commit }, accessRoutes) {
        commit("setPartialRoutes", accessRoutes);
        return accessRoutes;
    },
};
export default { state, getters, mutations, actions };