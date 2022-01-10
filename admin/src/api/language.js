import request from "@/utils/request";

export function getLanguage(data) {
    return request({
        url: "/language/i18n",
        method: "get",
        params: data,
    });
}

export function getTitle(data) {
    return request({
        url: "/language/getTitle",
        method: "post",
        data,
    });
}

export function updateTitle(data) {
    return request({
        url: "/language/doEdit",
        method: "put",
        data,
    });
}

export function deleteTitle(data) {
    return request({
        url: "/language/doDelete",
        method: "delete",
        data,
    });
}

export function updateLanguageFile(data) {
    return request({
        url: "/language/doEditFile",
        method: "put",
        data,
    });
}