<template>
  <div class="top-bar-container">
    <div class="byui-main">
      <el-row>
        <el-col :xl="6" :lg="6" :md="6" :sm="6" :xs="2">
          <logo/>
        </el-col>
        <el-col :xl="14" :lg="12" :md="16" :sm="16" :xs="18">
          <el-menu
            :active-text-color="variables['menu-color-active']"
            :background-color="variables['menu-background']"
            :default-active="activeMenu"
            :menu-trigger="menuTrigger"
            :text-color="variables['menu-color']"
            mode="horizontal"
          >
            <tab-item
              v-for="route in routes"
              :key="route.path"
              :base-path="route.path"
              :item="route"
            />
          </el-menu>
        </el-col>
        <el-col :xl="4" :lg="6" :md="2" :sm="2" :xs="4">
          <div class="right-panel">
            <error-log class="hidden-md-and-down"/>
            <full-screen-bar class="hidden-md-and-down" @refresh="refreshRoute"></full-screen-bar>
            <theme-bar class="hidden-md-and-down"></theme-bar>
            <byui-icon class="hidden-md-and-down"
                       title="重载路由"
                       :pulse="pulse"
                       :icon="['fas', 'redo']"
                       @click="refreshRoute"
            />
            <lang-select class="right-menu-item hover-effect" />
            <avatar></avatar>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Logo from "@/layouts/components/Logo";
import tabItem from "./components/TopBarItem";
import variables from "@/styles/variables.scss";
import { mapGetters } from "vuex";
import { Avatar, Breadcrumb, ErrorLog, FullScreenBar, ThemeBar } from "@/layouts/components";
import LangSelect from "@/components/LangSelect";

export default {
  components: {
    Avatar,
    Breadcrumb,
    ErrorLog,
    FullScreenBar,
    ThemeBar,
    tabItem,
    Logo,
    LangSelect,
  },
  data() {
    return {
      pulse: false,
      menuTrigger: "hover",
    };
  },
  computed: {
    ...mapGetters({
      routes: "permission/routes",
      visitedRoutes: "tagsBar/visitedRoutes",
    }),
    activeMenu() {
      const route = this.$route;
      const { meta, path } = route;
      if (meta.activeMenu) {
        return meta.activeMenu;
      }
      return path;
    },
    variables() {
      return variables;
    },
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
          .catch(() => {
          });
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.top-bar-container {
  background: $base-color-header;

  .el-menu.el-menu--horizontal {
    border-bottom: solid 0 transparent;
  }

  ::v-deep {
    .byui-main {
      background: $base-color-header;

      .el-menu {
        &--horizontal {
          float: right;
          border-bottom: solid 0 transparent !important;
        }

        > .top-bar-item-container {
          display: inline-block;
        }
      }
    }
  }

  .right-panel {
    display: flex;
    align-content: center;
    align-items: center;
    justify-content: flex-end;
    height: 55px;

    ::v-deep {
      .user-avatar {
        margin-top: 5px;
        margin-right: 5px;
        font-weight: 600;
        cursor: pointer;
      }

      .user-name {
        position: relative;
        top: -16px;
        margin-right: 35px;
        margin-left: 5px;
        font-weight: 600;
        cursor: pointer;
        color: rgba($base-color-white, 0.9);
      }

      .user-name + i {
        position: absolute;
        top: 17px;
        right: 15px;
        color: rgba($base-color-white, 0.9);
      }

      svg {
        width: 1em;
        height: 1em;
        margin-right: 15px;
        font-size: $base-font-size-big;
        color: rgba($base-color-white, 0.9);
        cursor: pointer;
        fill: rgba($base-color-white, 0.9);
      }

      button {
        svg {
          margin-right: 0;
          color: rgba($base-color-white, 0.9);
          cursor: pointer;
          fill: rgba($base-color-white, 0.9);
        }
      }

      .el-badge {
        margin-right: 15px;
      }
    }
  }
}
</style>
