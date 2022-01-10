<template>
  <div id="admin-system">
    <router-view />
  </div>
</template>

<script>
import { okCode, errorCode } from "@/config/settings";
import { getLanguage } from "@/api/language"; // 封装好的国际化的接口
if (process.env.NODE_ENV === "production") {
  console.log("生产环境");
} else if (process.env.NODE_ENV === "test") {
  console.log("测试环境");
} else if (process.env.NODE_ENV === "staging") {
  console.log("预发布环境");
} else if (process.env.NODE_ENV === "development") {
  console.log("开发环境");
}
export default {
  name: "App",
  mounted() {},
  created() {
    this.mergeLanguage();
  },
  methods: {
    mergeLanguage() {
      getLanguage({
        // 进行请求
        language: "zh", // 请求参数
      }).then((res) => {
        if (res.code == okCode) {
          $i18n.mergeLocaleMessage("zh", res.data);
        } else {
          console.log(res.message);
        }
      });
      getLanguage({
        // 进行请求
        language: "thai", // 请求参数
      }).then((res) => {
        if (res.code == okCode) {
          $i18n.mergeLocaleMessage("thai", res.data);
        } else {
          console.log(res.message);
        }
      });
      // $http.fetch("/addons/yun_shop/static/app/locales/test.json").then(
      //   function(response) {
      //     console.log(response.data);
      //     $i18n.mergeLocaleMessage('en', response.data.en)
      //     $i18n.mergeLocaleMessage('zh', response.data.zh)
      //   },
      //   function(response) {
      //     console.log(response);
      //   }
      // );
    },
  },
};
</script>
