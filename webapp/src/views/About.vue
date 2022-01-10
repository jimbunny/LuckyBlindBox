<template>
  <div class="about">
    <s-header :name="'关于我们'"></s-header>
    <div class="about-body">
      <van-divider :style="{ color: 'rgb(23, 157, 254)', borderColor: 'rgb(23, 157, 254)', fontSize: '20px', fontWeight: 500 }">简介</van-divider>
      <div>YepBox
      </div>
      <van-divider :style="{ color: 'rgb(23, 157, 254)', borderColor: 'rgb(23, 157, 254)', fontSize: '20px', fontWeight: 500 }">test</van-divider>
      <div>
        <div>掘金小册配套学习文档：<a target="_blank" href="https://juejin.im/book/6844733826191589390">《Vue 商城项目开发实战》</a></div>
        <br/>
        <div>后端 API 地址：<a target="_blank" href="https://github.com/newbee-ltd/newbee-mall-api">https://github.com/newbee-ltd/newbee-mall-api</a></div>
        <br/>
        <div>前端 Vue 开源地址：<a target="_blank" href="https://github.com/newbee-ltd/newbee-mall-vue-app">https://github.com/newbee-ltd/newbee-mall-vue-app</a></div>
        <br/>
        <div>线上预览地址：<a target="_blank" href="http://47.99.134.126:5000/">http://vue-app.newbee.ltd</a></div>
      </div>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
export default {
  components: {
    sHeader
  },
}
</script>

<style lang="less" scoped>
  .about {
    box-sizing: border-box;
    padding: 20px;
    .about-body {
      margin-top: 44px;
      font-size: 16px;
      a {
        color: #007fff;
      }
    }
  }
</style>
