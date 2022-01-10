/* eslint-disable */
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import Cookies from 'js-cookie'
import elementEnLocale from 'element-ui/lib/locale/lang/en' // element-ui lang
import elementZhLocale from 'element-ui/lib/locale/lang/zh-CN' // element-ui lang
import enLocale from './en'
import zhLocale from './zh'
import thaiLocale from './thai'
Vue.use(VueI18n)

const messages = {
    en: {
        ...enLocale,
        ...elementEnLocale
    },
    zh: {
        ...zhLocale,
        ...elementZhLocale
    },
    thai: {
        ...thaiLocale,
        ...elementZhLocale
    }
}

const i18n = new VueI18n({
    // set locale
    // options: en | zh | es
    locale: Cookies.get('language') || 'zh',
    // set locale messages
    messages
})

window.$i18n = i18n;
export default i18n