<template>
  <div class="user-box">
    <s-header :name="'Me'"></s-header>
    <div class="user-info">
      <div class="info">
        <img :src="user.avatar"/>
        <div class="user-desc">
          <span>userName：{{ user.username }}</span>
          <span>email：{{ user.email }}</span>
          <span class="name">introduceSign：{{ user.description ? user.description: '这个人太懒什么都没留下！' }}</span>
        </div>
      </div>
    </div>

    <van-row style="background:#fff;">
      <van-col span="8" class="money" @click="goTo('balance')">
        <div class="count"> {{ user.balance }} </div>
        <div class="text"> Balance </div>
      </van-col>
      <van-col span="8" class="money" @click="goTo('coupon')">
        <div style="border-left: solid 1px rgb(178 189 199);border-right: solid 1px rgb(178 189 199);">
        <div class="count"> {{ user.coupon }} </div>
        <div class="text"> Coupon </div>
        </div>
      </van-col>
      <van-col span="8" class="money" @click="goTo('point')">
        <div class="count"> {{ user.point }} </div>
        <div class="text"> Point </div>
      </van-col>
      <van-col span="24" style="height: 10px; background:#f9f9f9;"></van-col>
    </van-row>

    <ul class="user-list">
      <li @click="goTo('order')">
        <van-icon name="cart-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
        我的订单
        </span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('balance')">
        <van-icon name="cashier-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          充值管理</span>
        <van-icon name="arrow" />
      </li>
       <li @click="goTo('coupon')">
        <van-icon name="gold-coin-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          优惠券兑换</span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('point')">
        <van-icon name="gold-coin-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          积分兑换</span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('setting')">
        <van-icon name="friends-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          账号管理</span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('address?from=mine')">
         <van-icon name="location-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          地址管理</span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('share')">
         <van-icon name="share-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          扫码分享</span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('contact')">
         <van-icon name="chat-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          意见反馈</span>
        <van-icon name="arrow" />
      </li>
      <li @click="goTo('about')">
        <van-icon name="star-o" size="25" style="margin: auto 5px;"/>
        <span style="width:100%;">
          关于我们</span>
        <van-icon name="arrow" />
      </li>
    </ul>
    <nav-bar></nav-bar>
  </div>
</template>

<script>
import navBar from '@/components/NavBar'
import sHeader from '@/components/SimpleHeader'
import {okCode, errorCode,} from "../config/settings";
import { Toast } from 'vant'

export default {
  components: {
    navBar,
    sHeader
  },
  data() {
    return {
      user: {},
      value: '',
    }
  },
  async mounted() {
    this.user = await this.$store.dispatch("user/getInfo");
  },
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    goTo(r) {
      this.$router.push({ path: r })
    },
  }
}
</script>

<style lang="less" scoped>
  @import '../common/style/mixin';
  .money {
    padding: 20px 0px 15px 0px;
    .count {
      width:100%; text-align: center; font-size: 14px;
    }
    .text {
      width:100%; text-align: center; font-size: 14px; font-weight: bold;
    }
  }
  .user-box {
    background:#f9f9f9;
    .user-header {
      position: fixed;
      top: 0;
      left: 0;
      z-index: 10000;
      .fj();
      .wh(100%, 44px);
      line-height: 44px;
      padding: 0 10px;
      .boxSizing();
      color: #252525;
      background: #fff;
      border-bottom: 1px solid #dcdcdc;
      .user-name {
        font-size: 14px;
      }
    }
    .user-info {
      width: 100%;
      height: 115px;
      background: url(~@/assets/bj.png) no-repeat;
      background-size: 100% 100%;
      margin-top: 44px;
      .info {
        position: relative;
        display: flex;
        width: 100%;
        height: 100%;
        padding: 25px 20px;
        .boxSizing();
        img {
          .wh(60px, 60px);
          border-radius: 50%;
          margin-top: 4px;
        }
        .user-desc {
          display: flex;
          flex-direction: column;
          margin-left: 10px;
          line-height: 20px;
          font-size: 14px;
          color: #fff;
          span {
            color: #fff;
            font-size: 14px;
            padding: 2px 0;
          }
        }
        .account-setting {
          position: absolute;
          top: 10px;
          right: 20px;
          font-size: 13px;
          color: #fff;
          .van-icon-setting-o {
            font-size: 16px;
            vertical-align: -3px;
            margin-right: 4px;
          }
        }
      }
    }
    .user-list {
      background:#fff;
      padding: 0 20px;
      li {
        height: 40px;
        line-height: 40px;
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        .van-icon-arrow {
          margin-top: 13px;
        }
      }
    }
  }
</style>
