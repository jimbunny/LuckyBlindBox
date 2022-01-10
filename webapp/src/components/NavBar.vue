<template>
  <div class="nav-bar">
    <ul class="nav-list">
      <router-link tag="li" class="nav-list-item active" to="home">
        <i class="nbicon nblvsefenkaicankaoxianban-1"></i>
        <span>Home</span>
      </router-link>
      <router-link tag="li" class="nav-list-item" to="boxes">
        <i class="nbicon nbfenlei"></i>
        <span>Boxes</span>
      </router-link>
      <router-link tag="li" class="nav-list-item" to="cart">
        <van-icon  name="shopping-cart-o" :badge="!count ? '' : count" />
        <span>Award</span>
      </router-link>
      <router-link tag="li" class="nav-list-item" to="user">
        <i class="nbicon nblvsefenkaicankaoxianban-"></i>
        <span>Me</span>
      </router-link>
    </ul>
  </div>
</template>

<script>
import { okCode, errorCode } from "../config/settings";
import { validLogin } from '../service/user'
  export default {
    async mounted() {
      const { code, data } = await validLogin()
      const path = this.$route.path
      if (code == okCode && path != '/home') {
        this.$store.dispatch('user/updateCart', {
                  "email": data.email
                })
      }
    },
    data() {
      return {}
    },
    computed: {
      count () { 
        return this.$store.state.user.count
      }
    }
  }
</script>

<style lang="less" scoped >
    @import '../common/style/mixin';
    .nav-bar{
      position: fixed;
      left: 0;
      bottom: 0;
      width: 100%;
      padding: 5px 0;
      z-index: 1000;
      background: #fff;
      transform: translateZ(0);
      -webkit-transform: translateZ(0);
      .nav-list {
        width: 100%;
        .fj();
        flex-direction: row;
        padding: 0;
        .nav-list-item {
          display: flex;
          flex: 1;
          flex-direction: column;
          text-align: center;
          color: #666;
          &.router-link-active {
            color: @primary;
          }
          i {
            text-align: center;
            font-size: 22px;
          }
          span{
            font-size: 12px;
          }
          .van-icon-shopping-cart-o {
            margin: 0 auto;
            margin-bottom: 2px;
          }
        }
      }
    }
</style>
