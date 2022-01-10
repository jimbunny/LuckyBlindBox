<template>
  <el-scrollbar
    :class="{ 'side-bar-container': true, 'is-collapse': collapse }"
  >
    <logo />
    <el-menu
      :background-color="variables['menu-background']"
      :text-color="variables['menu-color']"
      :active-text-color="variables['menu-color-active']"
      :default-active="activeMenu"
      :collapse="collapse"
      :collapse-transition="false"
      :default-openeds="defaultOpens"
      :unique-opened="uniqueOpened"
      mode="vertical"
    >
      <side-bar-item
        v-for="route in routes"
        :key="route.path"
        :base-path="route.path"
        :item="route"
      />
    </el-menu>
  </el-scrollbar>
</template>
<script>
import Logo from "@/layouts/components/Logo";
import SideBarItem from "./components/SideBarItem";
import variables from "@/styles/variables.scss";
import { mapGetters } from "vuex";
import { defaultOopeneds, uniqueOpened } from "@/config/settings";

export default {
  name: "SideBar",
  components: { SideBarItem, Logo },
  data() {
    return {
      uniqueOpened,
    };
  },
  computed: {
    ...mapGetters({
      collapse: "settings/collapse",
      routes: "permission/routes",
    }),
    defaultOpens() {
      if (this.collapse) {
      }
      return defaultOopeneds;
    },
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
};
</script>
<style lang="scss" scoped>
.side-bar-container {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: $base-z-index;
  width: $base-left-menu-width;
  height: 100vh;
  overflow: hidden;
  background: $base-menu-background;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  transition: all 0.2s ease-in-out;

  ::v-deep {
    .el-scrollbar__wrap {
      overflow-x: hidden;
    }

    .el-menu {
      border: 0;
    }

    .svg-inline {
      &--fa {
        width: 1rem;
      }
    }

    .el-menu-item {
      height: 46px !important;
      overflow: hidden;
      line-height: 46px !important;
      text-overflow: ellipsis;
      white-space: nowrap;

      &:hover {
        color: $base-color-white !important;
        background-color: $base-menu-background-active !important;
      }

      &.is-active {
        color: $base-color-white !important;
        background-color: $base-menu-background-active !important;
      }
    }

    .nest-menu {
      [class*="menu"] {
        background-color: $base-menu-children-background !important;

        &.is-active {
          color: $base-color-white !important;
          background-color: $base-menu-background-active !important;
        }
      }
    }
  }

  &.is-collapse {
    width: $base-left-menu-width-min;
    border-right: 0 !important;

    ::v-deep {
      .title {
        display: none;
      }

      .el-menu--collapse {
        border-right: 0 !important;

        .el-submenu__icon-arrow {
          right: 10px;
          margin-top: -3px;
        }

        .el-submenu__title {
          span {
            display: none;
          }
        }
      }
    }
  }
}
</style>
