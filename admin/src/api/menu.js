/* eslint-disable */
import request from "@/utils/request";

export function getTree(data) {
    return request({
        url: "/menu/getTree",
        method: "get",
        params: data,
    });
}
export function doAdd(data) {
    return request({
        url: "/menu/doAdd",
        method: "post",
        data,
    });
}

export function doPermissionEdit(data) {
    return request({
        url: "/menu/permission/doEdit",
        method: "put",
        data,
    });
}

export function doDelete(data) {
    return request({
        url: "/menu/doDelete",
        method: "delete",
        data,
    });
}

export function getCheckedMenu(data) {
    return request({
        url: "/menu/checked",
        method: "get",
        params: data,
    });
}