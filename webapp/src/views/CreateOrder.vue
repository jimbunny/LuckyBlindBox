<template>
  <div class="create-order">
    <s-header :name="'生成订单'" @callback="deleteLocal"></s-header>
    <div class="address-wrap">
      <div class="name" @click="goTo">
        <span>{{ address.username }} </span>
        <span>{{ address.phone }}</span>
      </div>
      <div class="address">
        {{ address.detailAddress }} {{ address.townName }} {{ address.cityName }} {{ address.provinceName }} {{ address.postCode }}
      </div>
      <van-icon class="arrow" name="arrow" />
    </div>
    <div class="good">
      <div class="good-item" v-for="(item, index) in cartList" :key="index">
        <div class="good-img"><img :src="prefix(item.picture)" alt=""></div>
        <div class="good-desc">
          <div class="good-title">
            <span>{{ item.name }}</span>
            <van-count-down :time="item.time" ref="countDown" @finish="finish">
              <template #default="timeData">
                <span class="block">{{ timeData.hours }}</span>
                <span class="colon">:</span>
                <span class="block">{{ timeData.minutes }}</span>
                <span class="colon">:</span>
                <span class="block">{{ timeData.seconds }}</span>
              </template>
            </van-count-down>
            <!-- <span>x1</span> -->
          </div>
          <div class="good-btn">
            <div class="price">¥{{ item.outPrice }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="pay-wrap">
      <!-- 优惠券单元格 -->
      <van-coupon-cell
        :coupons="coupons"
        :chosen-coupon="chosenCoupon"
        @click="showList = true"
        style="padding-bottom:10px;"
      />
      <div class="price">
          <span style="color: #2c3e50;">商品金额</span>
          <span> 
          ¥{{ priceTip }}</span>
      </div>
      <van-button v-if="showTime" @click="createOrder" class="pay-btn" color="rgb(23, 157, 254)" type="primary" block>生成订单</van-button>
      <van-button v-else @click="goToHome" class="pay-btn" color="rgb(23, 157, 254)" type="primary" block>返回首页</van-button>
    </div>
    <van-popup
      closeable
      :close-on-click-overlay="false"
      v-model="showPay"
      position="bottom"
      :style="{ height: '30%' }"
      @close="close"
    >
      <div :style="{ width: '90%', margin: '0 auto', padding: '50px 0' }">
        <div style="bottom: 0; left: 0; width: 100%; background: #fff;">
        <div style=" display: flex;justify-content: space-between;padding: 0 5%;margin: 10px 0;font-size: 14px;">
          <span>账户金额</span>
          <span style="color: red;font-size: 18px;"> 
          ¥{{ balance }}</span>
        </div>
        <div style=" display: flex;justify-content: space-between;padding: 0 5%;margin: 10px 0;font-size: 14px;">
          <span>订单金额</span>
          <span style="color: red;font-size: 18px;"> 
          ¥{{ priceTip }}</span>
        </div>
      </div>
        <van-button v-if="balance>=total" :style="{ marginBottom: '10px' }" color="#1989fa" block @click="payOrder()">确认下单</van-button>
        <van-button v-else color="#4fc08d" block @click="goToBalance()">余额不足，去充值</van-button>
      </div>
    </van-popup>
    <!-- 优惠券列表 -->
      <van-popup
        v-model="showList"
        round
        position="bottom"
        style="height: 90%; padding-top: 4px;"
      >
        <van-coupon-list
          :coupons="coupons"
          :chosen-coupon="chosenCoupon"
          :disabled-coupons="disabledCoupons"
          @change="onChange"
          @exchange="onExchange"
        />
      </van-popup>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { getCart, getByCartItemIds } from '../service/cart'
import { getDefaultAddress, getAddressDetail } from '../service/address'
import { ExchangeCoupon, UseCoupon } from '../service/coupon'
import { createOrder, payOrder } from '../service/order'
import { setLocal, getLocal } from '@/common/js/utils'
import { Toast } from 'vant'
import { okCode } from '../config/settings'
import { mapGetters } from "vuex";

// const coupon = {
//   available: 0,
//   condition: '无使用门槛\n最多优惠12元',
//   reason: '',
//   value: 150,
//   name: '优惠券名称',
//   startAt: 1489104000,
//   endAt: 1514592000,
//   valueDesc: '1.5',
//   unitDesc: '元',
// };

export default {
  components: {
    sHeader
  },
  data() {
    return {
      cartList: [],
      address: {},
      showPay: false,
      orderNo: '',
      cartItemIds: [],
      email: "",
      time: 0,
      showTime: true,
      balance: 0,
      chosenCoupon: -1,
      coupons: [],
      disabledCoupons: [],
      showList: false,
      couponPrice: 0,
      discountType: 0,
      finalPrice: 0,
      priceTip: ""
    }
  },
  async mounted() {
    const user = await this.$store.dispatch("user/getInfo");
    this.email = user.email
    this.balance = user.balance
    this.init()
    const {code, data} = await UseCoupon({email: this.email, totalPrice: this.total})
    this.coupons = data.coupons
    this.disabledCoupons = data.disabledCoupons
  },
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      email: "user/email",
      username: "user/username",
    }),
  },
  created() {
  },
  watch: {
    "chosenCoupon": function (val) {
      if (val >= 0) {
        if (this.discountType == 1) {
          this.finalPrice = this.total-this.couponPrice
          this.priceTip = this.total.toString() + "-" + this.couponPrice.toString() + "=" + this.finalPrice.toString()
        } else {
          this.finalPrice = this.total*this.couponPrice/10
          this.priceTip = this.total.toString() + "*" + (this.couponPrice/10).toString() + "=" + this.finalPrice.toString()
        }
      }else {
        this.priceTip = this.total;
      }
    },
  },
  methods: {
    async init() {
      Toast.loading({ message: '加载中...', forbidClick: true });
      const { addressId, cartItemIds } = this.$route.query
      const _cartItemIds = cartItemIds ? JSON.parse(cartItemIds) : this.$store.state.user.cartItemIds
      this.$store.dispatch("user/updateCartItemIds", _cartItemIds);
      const { data: list } = await getByCartItemIds({ cartItemIds: _cartItemIds.join(',') })
      const { data: address } = addressId ? await getAddressDetail({"addressId": addressId}) : await getDefaultAddress({"email": this.email})
      if (!address) {
        this.$router.push({ path: 'address' })
        return
      }
      this.cartList = list
      this.address = address
      this.showTime = true
      this.priceTip = this.total
      Toast.clear()
    },
    goTo() {
      this.$router.push({ path: `address?cartItemIds=${JSON.stringify(this.cartItemIds)}` })
    },
    deleteLocal() {
      this.$store.dispatch("user/updateCartItemIds", []);
    },
    async createOrder() {
      this.showPay = true
    },
    onChange(index) {
      this.showList = false;
      this.chosenCoupon = index;
      this.couponPrice = this.coupons[index].valueDesc 
      this.discountType = this.coupons[index].discountType
    },
    async onExchange(key) {
      // this.coupons.push(coupon);
       const {code, data}  = await ExchangeCoupon({email:"954447255@qq.com", key: this.key})
      if (code === okCode) {
        Toast.success("兑换成功！")
        setTimeout(function(){
          this.init()
        },1000)
      } else {
        Toast.fail("兑换码不正确，或者已经兑换过！")
      }
    },
    close() {
      // this.$router.push({ path: 'order' })
    },
    async payOrder(type) {
      Toast.loading
      // await payOrder({ orderNo: this.orderNo, payType: type })
      const params = {
        email: this.email,
        addressId: this.address.addressId,
        totalPrice: this.finalPrice,
        phone: this.address.phone,
        username: this.address.username,
        payType: 'account',
        productList: this.cartList.map(item => item.id)
      }
      const { code, data } = await createOrder(params)
      if (code === okCode) {
        this.$store.dispatch("user/updateCartItemIds", []);
        this.orderNo = data
        this.$router.push({ path: 'order' })
      } else {
        Toast.fail("订单创建失败！请联系客服！")
      }
    },
    goToHome() {
      this.$router.push({ path: `/home` })
    },
    goToBalance() {
      this.$router.push({ path: `/balance` })
    },
    async finish() {
      const { code, data } = await getCart({ email: this.email })
      if (code === okCode) {
        this.cartList = data
        if (this.cartList.length===0) {
          this.showTime = false
        }
      } else {
        Toast.fail('获取购物车信息失败！')
      }
    },
  },
  computed: {
    total: function() {
      let sum = 0
      this.cartList.forEach(item => {
        sum += item.outPrice
      })
      return sum
    }
  }
}
</script>

<style lang="less" scoped>
  @import '../common/style/mixin';
  .create-order {
    background: #f9f9f9;
    .address-wrap {
      margin-bottom: 20px;
      background: #fff;
      position: relative;
      margin-top: 44px;
      font-size: 14px;
      padding: 15px;
      color: #222333;
      .name, .address {
        margin: 10px 0;
      }
      .arrow {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 20px;
      }
      &::before {
        position: absolute;
        right: 0;
        bottom: 0;
        left: 0;
        height: 2px;
        background: -webkit-repeating-linear-gradient(135deg, #ff6c6c 0, #ff6c6c 20%, transparent 0, transparent 25%, #1989fa 0, #1989fa 45%, transparent 0, transparent 50%);
        background: repeating-linear-gradient(-45deg, #ff6c6c 0, #ff6c6c 20%, transparent 0, transparent 25%, #1989fa 0, #1989fa 45%, transparent 0, transparent 50%);
        background-size: 80px;
        content: '';
      }
    }
    .good {
      margin-bottom: 180px;
    }
    .good-item {
      padding: 10px;
      background: #fff;
      display: flex;
      .good-img {
        img {
          .wh(100px, 100px)
        }
      }
      .good-desc {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex: 1;
        padding: 20px;
        .good-title {
          display: flex;
          justify-content: space-between;
        }
        .good-btn {
          display: flex;
          justify-content: space-between;
          .price {
            font-size: 16px;
            color: red;
            line-height: 28px;
          }
          .van-icon-delete {
            font-size: 20px;
            margin-top: 4px;
          }
        }
      }
    }
    .pay-wrap {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      background: #fff;
      padding: 10px 0;
      padding-bottom: 50px;
      border-top: 1px solid #e9e9e9;
      >div {
        display: flex;
        justify-content: space-between;
        padding: 0 5%;
        margin: 10px 0;
        font-size: 14px;
        span:nth-child(2) {
          color: red;
          font-size: 18px;
        }
      }
      .pay-btn {
        position: fixed;
        bottom: 7px;
        right: 0;
        left: 0;
        width: 90%;
        margin: 0 auto;
      }
    }
  }
</style>
