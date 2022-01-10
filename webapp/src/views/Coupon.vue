<template>
  <div class="coupon">
    <s-header :name="'优惠券兑换'"></s-header>
    <div class="coupon-body">
      <!-- 优惠券列表 -->
      <van-sticky :offset-top="44">
      <van-search
        v-model="key"
        shape="round"
        left-icon=""
        show-action
        placeholder="请输入兑换码"
      >
        <template #action>
          <van-button type="danger" plain class="van-coupon-list__exchange" @click="exchangeCouponFn" :disabled="exchangeStatus">兑换</van-button>
        </template>
      </van-search>
      </van-sticky>
        <div class="van-coupon-list__list van-coupon-list__list--with-bottom">
          <div v-for="(item, index) in coupons" :key="index" class="van-coupon">
            <div class="van-coupon__content" style="padding: 0px !important;">
              <div class="van-coupon__head">
                <h2 class="van-coupon__amount">{{ item.discountCondition }}<span> {{item.discountCondition>1? "元":"折" }} </span></h2>
                <p class="van-coupon__condition">{{ item.couponType==0 ? "无门槛": "有门槛" }}  <br> 高于{{item.couponCondition}}元优惠</p></div>
              <div class="van-coupon__body">
                <p class="van-coupon__name">{{ item.couponName }}</p>
                <p class="van-coupon__valid">{{ item.startTime }} - {{ item.endTime }}</p>
              </div>
            </div>
            <p class="van-coupon__description">{{ item.description }}</p>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { GetCouponInfo, ExchangeCoupon } from '../service/coupon'
import { okCode } from '../config/settings'
import { Toast } from 'vant'
import { mapGetters } from "vuex";

export default {
  components: {
    sHeader
  },
  data() {
    return {
      key: '',
      exchangeStatus: true,
      coupons: []
    }
  },
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      email: "user/email",
      username: "user/username",
    }),
  },
  async mounted() {
    this.user = await this.$store.dispatch("user/getInfo");
    this.init()
  },
  watch: {
    "key": function (val) {
      if (val) {
        this.exchangeStatus = false;
      }
    },
  },
  methods: {
    async init() {
      const {code, data} = await GetCouponInfo({email:this.email, pageNo:1, pageSize:10})
      if (code === okCode) {
        this.coupons = data.items
      } else {
        Toast.fail("获取优惠券列表失败！")
      }
    },
    goBack() {
      this.$router.go(-1)
    },
    async exchangeCouponFn(val) {
      const {code, data}  = await ExchangeCoupon({email:this.email, key: this.key})
      if (code === okCode) {
        Toast.success("兑换成功！")
        setTimeout(function(){
          this.init()
        },1000)
      } else {
        Toast.fail("兑换码不正确，或者已经兑换过！")
      }
    },
  }
}
</script>

<style lang="less" scoped>
  .coupon {
    box-sizing: border-box;
    // padding: 20px;
    background: #f7f8fa;
    .coupon-body {
      background: #f7f8fa; 
      margin-top: 44px;
      font-size: 16px;
      a {
        color: #007fff;
      }
    }
  }
</style>
