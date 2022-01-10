<template>
  <vue-qr
    :logo-src="logoSrc"
    :size="size"
    :margin="0"
    :auto-color="true"
    :dot-scale="1"
    :text="appSrc"
  />
</template>
<script>
import VueQr from 'vue-qr'
export default {
  name: 'QrCode',
  props: {
    // 被生成二维码连接（必填）
    appSrc: {
      type: String,
      default: ''
    },
    // 二维码中间logo图片（选填）
    logoSrc: {
      type: String,
      default: ''
    },
    // 二维码尺寸（选填）
    size: {
      type: Number,
      default: 150
    }
  },
  components: {
    VueQr
  }
}
</script>