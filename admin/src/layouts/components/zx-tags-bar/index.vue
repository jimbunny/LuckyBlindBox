<template>
  <div id="tags-bar-container" class="tags-bar-container">
    <byui-icon
      class="tags-icon"
      :icon="['fas', 'angle-double-left']"
      @click="handleScroll('left')"
    ></byui-icon>
    <scroll ref="scrollPane" class="tags-content">
      <router-link
        v-for="item in visitedRoutes"
        :key="item.path"
        ref="tag"
        :class="isActive(item) ? 'active' : ''"
        :to="{
          path: item.path,
          query: item.query,
          fullPath: item.fullPath,
        }"
        class="tags-bar-item"
        tag="span"
      >
        {{ generateTitle(item.title) }}
        <span
          v-if="!isAffix(item)"
          class="el-icon-close"
          @click.prevent.stop="closeSelectedTag(item)"
        />
      </router-link>
    </scroll>
    <byui-icon
      class="tags-icon"
      :icon="['fas', 'angle-double-right']"
      @click="handleScroll('right')"
    ></byui-icon>
    <el-dropdown @command="handleCommand">
      <span style="cursor: pointer;">
        {{ $t("tags.moreAction") }}
        <i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown" class="tags-more">
        <el-dropdown-item command="refreshRoute">
          <byui-icon :icon="['fas', 'circle-notch']" />
          {{ $t("tags.fresh") }}
        </el-dropdown-item>
        <el-dropdown-item command="closeOthersTags">
          <byui-icon :icon="['fas', 'times-circle']" />
          {{ $t("tags.closeOther") }}
        </el-dropdown-item>
        <el-dropdown-item command="closeLeftTags">
          <byui-icon :icon="['fas', 'arrow-alt-circle-left']"></byui-icon>
          {{ $t("tags.closeLeft") }}
        </el-dropdown-item>
        <el-dropdown-item command="closeRightTags">
          <byui-icon :icon="['fas', 'arrow-alt-circle-right']"></byui-icon>
          {{ $t("tags.closeRight") }}
        </el-dropdown-item>
        <el-dropdown-item command="closeAllTags">
          <byui-icon :icon="['fas', 'ban']"></byui-icon>
          {{ $t("tags.closeAll") }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import Scroll from "./components/Scroll";
import path from "path";
import { mapGetters } from "vuex";
import { generateTitle } from "@/utils/i18n";

export default {
  name: "TagsBar",
  components: { Scroll },
  data() {
    return {
      affixTags: [],
    };
  },

  computed: {
    ...mapGetters({
      layout: "settings/layout",
      visitedRoutes: "tagsBar/visitedRoutes",
      routes: "permission/routes",
    }),
  },
  watch: {
    $route() {
      this.addTags();
      this.moveToCurrentTag();
    },
  },
  mounted() {
    this.initTags();
    this.addTags();
  },
  methods: {
    generateTitle,
    isActive(route) {
      return route.path === this.$route.path;
    },
    isAffix(tag) {
      return tag.meta && tag.meta.affix;
    },
    filterAffixTags(routes, basePath = "/") {
      let tags = [];
      routes.forEach((route) => {
        if (route.meta && route.meta.affix) {
          const tagPath = path.resolve(basePath, route.path);
          tags.push({
            fullPath: tagPath,
            path: tagPath,
            name: route.name,
            meta: { ...route.meta },
          });
        }
        if (route.children) {
          const tempTags = this.filterAffixTags(route.children, route.path);
          if (tempTags.length >= 1) {
            tags = [...tags, ...tempTags];
          }
        }
      });
      return tags;
    },
    initTags() {
      const affixTags = (this.affixTags = this.filterAffixTags(this.routes));
      for (const tag of affixTags) {
        if (tag.name) {
          this.$store.dispatch("tagsBar/addVisitedRoute", tag);
        }
      }
    },
    addTags() {
      const { name } = this.$route;
      if (name) {
        this.$store.dispatch("tagsBar/addRoute", this.$route);
      }
      return false;
    },
    moveToCurrentTag() {
      const tags = this.$refs.tag;
      this.$nextTick(() => {
        for (const tag of tags) {
          if (tag.to.path === this.$route.path) {
            this.$refs.scrollPane.moveToTarget(tag);
            if (tag.to.fullPath !== this.$route.fullPath) {
              this.$store.dispatch("tagsBar/updateVisitedRoute", this.$route);
            }
            break;
          }
        }
      });
    },
    handleCommand(command) {
      switch (command) {
        case "refreshRoute":
          this.refreshRoute();
          break;
        case "closeOthersTags":
          this.closeOthersTags();
          break;
        case "closeLeftTags":
          this.closeLeftTags();
          break;
        case "closeRightTags":
          this.closeRightTags();
          break;
        case "closeAllTags":
          this.closeAllTags();
          break;
      }
    },
    refreshRoute() {
      const arr = this.visitedRoutes.filter((item, index) => {
        if (item.path === this.$route.fullPath) {
          return item;
        }
      });
      const view = arr[0];
      this.$store.dispatch("tagsBar/delCachedRoutes", view).then(() => {
        const { fullPath } = view;
        this.$nextTick(() => {
          this.$router
            .replace({
              path: "/redirect" + this.$route.fullPath,
            })
            .catch(() => {});
        });
      });
    },
    closeSelectedTag(view) {
      this.$store
        .dispatch("tagsBar/delRoute", view)
        .then(({ visitedRoutes }) => {
          if (this.isActive(view)) {
            this.toLastView(visitedRoutes, view);
          }
        });
    },
    closeOthersTags() {
      const arr = this.visitedRoutes.filter((item, index) => {
        if (item.path === this.$route.fullPath) {
          return item;
        }
      });
      const view = arr[0];
      this.$router.push(view);
      this.$store.dispatch("tagsBar/delOthersRoutes", view).then(() => {
        this.moveToCurrentTag();
      });
    },
    closeLeftTags() {
      const arr = this.visitedRoutes.filter((item, index) => {
        if (item.path === this.$route.fullPath) {
          return item;
        }
      });
      const view = arr[0];
      this.$router.push(view);
      this.$store.dispatch("tagsBar/delLeftRoutes", view).then(() => {
        this.moveToCurrentTag();
      });
    },
    closeRightTags() {
      const arr = this.visitedRoutes.filter((item, index) => {
        if (item.path === this.$route.fullPath) {
          return item;
        }
      });
      const view = arr[0];
      this.$router.push(view);
      this.$store.dispatch("tagsBar/delRightRoutes", view).then(() => {
        this.moveToCurrentTag();
      });
    },
    closeAllTags() {
      const arr = this.visitedRoutes.filter((item, index) => {
        if (item.path === this.$route.fullPath) {
          return item;
        }
      });
      const view = arr[0];
      this.$store.dispatch("tagsBar/delAllRoutes").then(({ visitedRoutes }) => {
        if (this.affixTags.some((tag) => tag.path === view.path)) {
          return;
        }
        this.toLastView(visitedRoutes, view);
      });
    },
    toLastView(visitedRoutes, view) {
      const latestView = visitedRoutes.slice(-1)[0];
      if (latestView) {
        this.$router.push(latestView);
      } else {
        if (view.name === "Index") {
          this.$router.replace({ path: "/redirect" + view.fullPath });
        } else {
          this.$router.push("/");
        }
      }
    },
    handleScroll(e) {
      let $wrap = $(".tags-bar-container .el-scrollbar__wrap");
      if ("left" === e) {
        $wrap.animate({ scrollLeft: 0 }, 400);
      } else {
        $wrap.animate({ scrollLeft: $wrap[0].scrollWidth }, 400);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.tags-bar-container {
  position: relative;
  box-sizing: border-box;
  height: 44px;
  user-select: none;
  background: $base-color-white;

  .tags-icon {
    float: left;
    width: 30px;
    margin-top: 16px;
    font-size: $base-font-size-default;
    color: $base-color-gray;
    text-align: center;
    vertical-align: auto;
    cursor: pointer;

    &:hover {
      opacity: 0.9;
    }
  }

  .tags-content {
    float: left;
    width: calc(100% - 145px);

    .tags-bar-item {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-items: center;
      height: $base-input-height;
      padding: 0 15px 0 15px;
      margin-top: 6px;
      margin-right: 5px;
      font-size: $base-font-size-small;
      line-height: $base-input-height;
      cursor: pointer;
      background: $base-color-white;
      border: 1px solid $base-border-color;
      border-radius: $base-border-radius;

      &.active {
        color: $base-color-white;
        background-color: $base-color-blue;
        border: 1px solid $base-color-blue;
      }

      .el-icon-close {
        position: relative;
        box-sizing: border-box;
        display: inline-flex;
        align-items: center;
        justify-items: center;
        width: 15px;
        height: 15px;
        margin: 0 0 0 3px;

        &::before {
          position: absolute;
          top: 2px;
          left: 1.5px;
        }

        &:hover {
          color: $base-color-white;
          background-color: $base-color-red;
          border-radius: 50%;
        }
      }
    }
  }

  ::v-deep {
    .el-dropdown {
      margin-top: 15px;
    }
  }
}
</style>
