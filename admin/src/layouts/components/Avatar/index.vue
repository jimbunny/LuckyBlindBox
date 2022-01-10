<template>
  <el-dropdown @command="handleCommand">
    <span class="el-dropdown-link">
      <el-avatar
        class="user-avatar"
        :src="require('@/assets/user.gif')"
      ></el-avatar>
      <span class="hidden-md-and-down user-name">{{ userName }}</span>
      <i class="hidden-md-and-down el-icon-arrow-down el-icon--right"></i>
    </span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item command="gotolink">
        <byui-icon :icon="['fas', 'user']"></byui-icon>
        <router-link :to="{ path: '/index' }">{{
          $t("route.personalCenter")
        }}</router-link>
      </el-dropdown-item>
      <el-dropdown-item command="logout" divided>
        <byui-icon :icon="['fas', 'sign-out-alt']"></byui-icon>
        {{ $t("header.logout") }}
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
  
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Avatar",
  data() {
    return {
      dialogVisible: false,
    };
  },
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      userName: "user/userName",
    }),
  },
  methods: {
    handleCommand(command) {
      switch (command) {
        case "logout":
          this.logout();
          break;
      }
    },
    gotolink(){
      //点击跳转至上次页面
      //this.$router.go(-1)
      //指定跳转地址
      this.$router.push("/index");
    },
    logout() {
      this.$baseConfirm(
        this.$t("header.logoutMessage") +
          this.$baseTitle +
          this.$t("header.logoutTip"),
        this.$t("header.tips"),
        this.$t("header.confirm"),
        this.$t("header.cancel"),
        () => {
          const fullPath = this.$route.fullPath;
          this.$store.dispatch("user/logout").then(() => {
            this.$router.push(`/login?redirect=${fullPath}`);
          });
        }
      );
    },
  },
};
</script>
