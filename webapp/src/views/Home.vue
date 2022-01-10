<template>
  <div>
    <header class="home-header wrap" :class="{'active' : headerScroll}">
        <span class="app-name">YepBox</span>
        <router-link class="login" tag="span" to="./login" v-if="!isLogin">login</router-link>
        <router-link class="login" tag="span" to="./user" v-else>
          <van-icon name="manager-o" />
        </router-link>
    </header>
    <nav-bar></nav-bar>
    <swiper :list="swiperList"></swiper>
    <van-dropdown-menu>
      <van-dropdown-item v-model="queryForm.gender" :options="options.gender" />
      <van-dropdown-item v-model="queryForm.size" :options="options.size" />
      <van-dropdown-item v-model="queryForm.age" :options="options.age" />
      <van-dropdown-item title="class" ref="item">
        <van-cell center title="coat">
          <template #right-icon>
            <van-switch v-model="coat" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <van-cell center title="pants">
          <template #right-icon>
            <van-switch v-model="pants" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <van-cell center title="skirt">
          <template #right-icon>
            <van-switch v-model="skirt" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <div style="padding: 5px 16px;">
          <van-button type="danger" color="rgb(23, 157, 254)" block round @click="onConfirm">
            确认
          </van-button>
        </div>
      </van-dropdown-item>
    </van-dropdown-menu>

    <div class="good">
      <header class="good-header">Female Boxes</header>
      <div class="good-box">
        <div class="good-item" v-for="item in femaleBoxes" :key="item.id" @click="goToBoxesDetail(item)">
          <img :src="prefix(item.picture[0].url)" alt="">
          <div class="good-desc">
            <!-- <div class="title">{{ item.goodsName }}</div> -->
            <div class="title"  style="margin-bottom:5px;">
              <van-tag plain type="danger" size="mini">{{ item.size }}</van-tag>
              <van-tag plain type="danger" size="mini" style="margin-left:5px;">{{ item.age }}</van-tag>
              <van-tag plain type="danger" size="mini" style="margin-left:5px;">{{ item.Pclass }}</van-tag>
            </div>
            <div class="price"> {{ item.point }} point</div>
          </div>
        </div>
      </div>
    </div>
    <div class="good" :style="{ paddingBottom: '100px'}">
      <header class="good-header">Male Boxes</header>
      <div class="good-box">
        <div class="good-item" v-for="item in maleBoxes" :key="item.id" @click="goToBoxesDetail(item)">
          <img :src="prefix(item.picture[0].url)" alt="">
          <div class="good-desc">
            <div class="title"  style="margin-bottom:5px;">
              <van-tag plain type="danger" size="mini">{{ item.size }}</van-tag>
              <van-tag plain type="danger" size="mini" style="margin-left:5px;">{{ item.age }}</van-tag>
              <van-tag plain type="danger" size="mini" style="margin-left:5px;">{{ item.Pclass }}</van-tag>
              </div>
            <div class="price"> {{ item.point }} point</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navBar from '@/components/NavBar'
import swiper from '@/components/Swiper'
import { okCode, errorCode } from "../config/settings";
import { getProductList, getSwipeList } from '../service/home'
import { getUserInfo, validLogin } from '../service/user'
import { getLocal } from '@/common/js/utils'
import { Toast } from 'vant'
import {
  getAccessToken,
} from "../utils/accessToken";

export default {
  name: 'home',
  data() {
    return {
      swiperList: [],
      isLogin: false,
      headerScroll: false,
      hots: [],
      femaleBoxes: [],
      maleBoxes: [],
      coat: false,
      pants: false,
      skirt: false,
      queryForm: {
        pageNo: 1,
        pageSize: 1000,
        name: "",
        gender: "",
        size: "",
        age: "",
        Pclass: new Array()
      },
      options: {
        "gender": [ 
          { text: 'gender', value: '' },
          { text: 'female', value: 'female' },
          { text: 'male', value: 'male' },
        ],
        "age": [ 
          { text: 'age', value: '' },
          { text: 'youth', value: 'youth' },
          { text: 'elderly', value: 'elderly' },
        ],
        "size": [ 
          { text: 'size', value: '' },
          { text: 'S', value: 'S' },
          { text: 'M', value: 'M' },
          { text: 'L', value: 'L' },
          { text: 'XL', value: 'XL' },
          { text: 'XXL', value: 'XXL' },
        ],}
    }
  },
  components: {
    navBar,
    swiper
  },
  watch: {
    queryForm:{
      handler(newVal,oldVal){
          this.ProductList();
        },
        deep:true
    }
  },
  async mounted() {
    const inviterId = localStorage.getItem('inviterId');
    if (!inviterId) {
      inviterId = this.$route.query.inviterId
      localStorage.setItem('inviterId', inviterId);
    }
    const { code } = await validLogin()
    if (code == okCode) {
      this.isLogin = true
    }
    window.addEventListener('scroll', this.pageScroll)
    Toast.loading({
      message: 'กำลังเข้าสู่ระบบ...',
      forbidClick: true
    });
    getSwipeList().then((res) => {
      const { code, msg, data } = res;
      if (code === okCode) {
        this.swiperList = data;
        setTimeout((_) => {
          Toast.clear()
        }, 300);
      } else {
        Toast.fail('ขณะนี้ระบบขัดข้องอยู่ระหว่างการแก้ไข, กรุณาทำรายการใหม่ภายหลัง!');
      }
    });
    this.ProductList();
  },
  methods: {
    ProductList() {
      getProductList(this.queryForm).then((res) => {
      const { code, msg, data } = res;
      if (code === okCode) {
        this.femaleBoxes = data.items.filter(i => i.gender=='female');;
        this.maleBoxes = data.items.filter(i => i.gender=='male');;
        setTimeout((_) => {
          Toast.clear()
        }, 300);
      } else {
        Toast.fail('ขณะนี้ระบบขัดข้องอยู่ระหว่างการแก้ไข, กรุณาทำรายการใหม่ภายหลัง!');
      }
    });
    },
    onConfirm() {
      if (this.coat) {
        if(this.queryForm.Pclass.indexOf('coat') <= -1){
          this.queryForm.Pclass.push('coat')
        }
      } else {
        if(this.queryForm.Pclass.indexOf('coat') > -1){
          this.queryForm.Pclass.remove('coat')
        }
      }
      if (this.pants) {
        if(this.queryForm.Pclass.indexOf('pants') <= -1){
          this.queryForm.Pclass.push('pants')
        }
      } else {
        if(this.queryForm.Pclass.indexOf('pants') > -1){
          this.queryForm.Pclass.remove('pants')
        }
      }
      if (this.skirt) {
        if(this.queryForm.Pclass.indexOf('skirt') <= -1){
          this.queryForm.Pclass.push('skirt')
        }
      } else {
        if(this.queryForm.Pclass.indexOf('skirt') > -1){
          this.queryForm.Pclass.remove('skirt')
        }
      }
      this.$refs.item.toggle();
    },
    pageScroll() {
      let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
      scrollTop > 100 ? this.headerScroll = true : this.headerScroll = false
    },
    goToDetail(item) {
      this.$router.push({ path: `product/${item.goodsId}` })
    },
    goToBoxesDetail(item) {
      this.$router.push({ path: `box/${item.no}` })
    }
  }
}
</script>

<style lang="less" scoped >
  @import '../common/style/mixin';
  .home-header {
      position: fixed;
      left: 0;
      top: 0;
      .wh(100%, 50px);
      .fj();
      line-height: 50px;
      padding: 0 15px;
      .boxSizing();
      font-size: 15px;
      color: #fff;
      z-index: 10000;
      .app-name {
        padding: 0 10px;
        color: @primary;
        font-size: 20px;
        font-weight: bold;
      }
      &.active {
        background: @primary;
        .app-name {
          padding: 0 10px;
          color: #fff;
          font-size: 20px;
          font-weight: bold;
        }
        .login {
          color: #fff;
        }
      }
      .icon-iconyonghu{
        color: #fff;
        font-size: 22px;
      }
      .login {
        color: @primary;
        line-height: 52px;
        .van-icon-manager-o {
          font-size: 20px;
          vertical-align: -3px;
        }
      }
  }
  .good {
    .good-header {
      background: #f9f9f9;
      height: 50px;
      line-height: 50px;
      text-align: center;
      color: @primary;
      font-size: 16px;
      font-weight: 500;
    }
    .good-box {
      display: flex;
      justify-content: flex-start;
      flex-wrap: wrap;
      .good-item {
        box-sizing: border-box;
        width: 50%;
        border-bottom: 1PX solid #e9e9e9;
        padding: 10px 10px;
        img {
          display: block;
          width: 120px;
          margin: 0 auto;
        }
        .good-desc {
          text-align: center;
          font-size: 14px;
          padding: 10px 0;
          .title {
            color: #222333;
          }
          .price {
            color: @primary;
          }
        }
        &:nth-child(2n + 1) {
          border-right: 1PX solid #e9e9e9;
        }
      }
    }
  }
  .floor-list {
      width: 100%;
      padding-bottom: 50px;
      .floor-head {
        width: 100%;
        height: 40px;
        background: #F6F6F6;
      }
      .floor-content {
        display: flex;
        flex-shrink: 0;
        flex-wrap: wrap;
        width: 100%;
        .boxSizing();
        .floor-category {
          width: 50%;
          padding: 10px;
          border-right: 1px solid #dcdcdc;
          border-bottom: 1px solid #dcdcdc;
          .boxSizing();
          &:nth-child(2n) {
            border-right: none;
          }
          p {
            font-size: 17px;
            color: #333;
            &:nth-child(2) {
              padding: 5px 0;
              font-size: 13px;
              color: @primary;
            }
          }
          .floor-products {
            .fj();
            width: 100%;
            img {
              .wh(65px, 65px);
            }
          }
      }
    }
  }
</style>
