<template>
  <el-dropdown
    trigger="click"
    class="international"
    @command="handleSetLanguage"
  >
    <div>
      <byui-icon
        :title="$t('header.language')"
        class-name="international-icon"
        :icon="['fas', 'language']"
      ></byui-icon>
    </div>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item :disabled="language === 'zh'" command="zh"
        >中文</el-dropdown-item
      >
      <!--<el-dropdown-item :disabled="language === 'en'" command="en" @click="refreshRoute"
        >English</el-dropdown-item
      >-->
      <el-dropdown-item :disabled="language === 'thai'" command="thai"
        >Thai</el-dropdown-item
      >
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    language() {
      return this.$store.getters.language;
    },
    ...mapGetters({
      collapse: "settings/collapse",
      visitedRoutes: "tagsBar/visitedRoutes",
      device: "settings/device",
      routes: "permission/routes",
    }),
  },
  methods: {
    refreshRoute() {
      const arr = this.visitedRoutes.filter((item, index) => {
        if (item.path === this.$route.fullPath) {
          return item;
        }
      });
      const view = arr[0];
      this.pulse = true;
      this.$store.dispatch("tagsBar/delCachedRoutes", view).then(() => {
        this.$router
          .replace({
            path: "/redirect" + this.$route.fullPath,
          })
          .then(() => {
            setTimeout(() => {
              this.pulse = false;
            }, 1000);
          })
          .catch(() => {});
      });
    },
    handleSetLanguage(lang) {
      this.$i18n.locale = lang;
      // console.log(this.$i18n.locale);
      this.$store.dispatch("settings/setLanguage", lang);
      this.$message({
        message: "Switch Language Success!",
        type: "success",
      });
      this.$router.go(0);
    },
  },
};
</script>
