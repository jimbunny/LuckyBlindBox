<template>
  <span
    :title="
      isFullscreen ? $t('header.exitFullScreen') : $t('header.enterFullScreen')
    "
  >
    <byui-icon
      :icon="[
        'fas',
        isFullscreen ? 'compress-arrows-alt' : 'expand-arrows-alt',
      ]"
      @click="click"
    ></byui-icon>
  </span>
</template>

<script>
import screenfull from "screenfull";

export default {
  name: "FullScreenBar",
  data() {
    return {
      isFullscreen: false,
    };
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {
    this.destroy();
  },
  methods: {
    click() {
      if (!screenfull.isEnabled) {
        this.$baseMessage($t("header.errorFullScreen"), "error");
        return false;
      }
      screenfull.toggle();
      this.$emit("refresh");
    },
    change() {
      this.isFullscreen = screenfull.isFullscreen;
    },
    init() {
      if (screenfull.isEnabled) {
        screenfull.on("change", this.change);
      }
    },
    destroy() {
      if (screenfull.isEnabled) {
        screenfull.off("change", this.change);
      }
    },
  },
};
</script>
