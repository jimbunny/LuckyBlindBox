<template>
  <div class="point">
    <s-header :name="'积分兑换'"></s-header>
    <div class="point-body">
      <van-tabs v-model="activeName" type="card" color="rgb(23, 157, 254)">
        <van-tab title="积分兑换" name="point">
          <van-field name="balance" label="账户余额" style="width:50%; float:left;">
            <template #input>
              <div style="color: red;">{{ userBalance }}</div>
            </template>
          </van-field>
          <van-field name="point" label="账户积分" style="width:50%;">
            <template #input>
              <div style="color: red;">{{ userPoint }}</div>
            </template>
          </van-field>
          <van-form @submit="onSubmit">
            <van-field
              v-model="point.balance"
              name="balance"
              label="兑换金额"
              type="number"
              placeholder="兑换金额"
              :rules="balanceRules"
            />
            <van-field
              v-model="point.point"
              name="point"
              label="兑换积分"
              type="number"
              placeholder="兑换积分"
              readonly
            >
            <template #input>
              <div style="color: red;">{{ point.point }}</div>
            </template>
            </van-field>
            <!-- <van-field
              v-model="point.date"
              center
              clearable
              name="date"
              label="兑换日期"
              placeholder="date"
              @click="showPopFn()"
              :rules="[{ required: true, message: '兑换日期' }]"
            ></van-field>
            <div id="date_time_picker">
              <van-popup v-model="show" position="bottom" :style="{ height: '40%' }">
              <van-datetime-picker v-model="currentDate" type="date" :min-date="minDate" :max-date="maxDate" @change="changeFn()" @confirm="confirmFn()" @cancel="cancelFn()" />
              </van-popup>
            </div> -->
            <van-field
              v-model="point.remark"
              name="remark"
              label="备注"
              placeholder="备注"
            />
            <div style="margin: 16px;">
              <van-button round block type="info" native-type="submit">提交</van-button>
            </div>
          </van-form>
        </van-tab>
        <van-tab title="历史查询" name="history">
          <van-pull-refresh v-model="isLoading" @refresh="onRefresh">
          <!-- <van-cell v-for="item in list" :key="item" :title="item" /> -->
            <van-row class="van-cell">
              <van-col span="4">序号</van-col>
              <van-col span="6">金额</van-col>
              <van-col span="6">积分</van-col>
              <van-col span="8">时间</van-col>
            </van-row>
            <van-divider :style="{ margin: '0 0' }"/>
            <div v-for="item in list" :key="item.id"  :name="item.id">
            <van-row class="van-cell"> 
              <van-col span="4">{{ item.id }}</van-col>
              <van-col span="6">{{ item.balance }}</van-col>
              <van-col span="6">{{ item.point }}</van-col>
              <van-col span="8">{{ item.date }}</van-col>
            </van-row>
            <van-divider :style="{ margin: '0 0' }"/>
            </div>
            
        </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { mapGetters } from "vuex";
import { AddPointInfo, GetPointInfo } from '../service/user'
import {okCode, errorCode,} from "../config/settings"
import { Toast } from 'vant'

export default {
  components: {
    sHeader
  },
  data() {
    return {
      activeName: 'point',
      show: false,
      currentDate: new Date(),
      minDate: new Date(1949, 10, 1),//出生日期起始范围
      maxDate: new Date(),//出生日期起始范围
      point: {
        balance: 0,
        point: 0,
        type: "balance",
        remark: "",
        email: "",
        date: this.timeFormat(new Date()),
      },
      userBalance: "",
      userPoint: "",
      list: [],
      activeNames: [],
      isLoading: false,
      // 校验密码
      balanceRules: [{
          required: true,
          message: '兑换金额不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return value != 0;
          },
          message: '兑换金额不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return value <= this.userBalance;
          },
          message: '兑换金额超出账户余额',
          trigger: 'onBlur'
      }],
    }
  },
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      email: "user/email",
      username: "user/username",
    }),
  },
  watch: {
    "point.balance": function (val) {
      this.point.point = 2 * val
    },
  },
  async created() {
    this.init()
  },
  methods: {
    async init() {
      const user = await this.$store.dispatch("user/getInfo"); 
      this.userBalance = user.balance
      this.userPoint = user.point
      const { code, data, msg } = await GetPointInfo({"email": this.email, "pageNo": 1, "pageSize": 100});
      this.list = data.items
    },
    showPopFn() {
      this.show = true;
    },
    showPopup() {
      this.show = true;
    },
    changeFn() { // 值变化是触发
      this.changeDate = this.currentDate // Tue Sep 08 2020 00:00:00 GMT+0800 (中国标准时间)
    },
    confirmFn() { // 确定按钮
      this.point.date = this.timeFormat(this.currentDate);
      this.show = false;
    },
    cancelFn(){
      this.show = true;
    },
    async onRefresh() {
      const { code, data, msg } = await GetPointInfo({"email": this.email, "pageNo": 1, "pageSize": 100});
      this.list = data.items
      Toast('刷新成功');
      this.isLoading = false;
    },
    async onSubmit(values) {
      this.point.email = this.email;
      const { code } = await AddPointInfo(this.point)
        if (code === okCode) {
          const { code, data, msg } = await GetPointInfo({"email": this.email, "pageNo": 1, "pageSize": 100});
          this.list = data.items
          Toast.success('积分兑换成功！')
          const that = this
          setTimeout(function(){
            that.init()
          }, 1000)
        } else {
          Toast.fail('积分兑换失败！')
        }
    },
    timeFormat(time) { // 时间格式化 2019-09-08
      let year = time.getFullYear();
      let month = time.getMonth() + 1;
      let day = time.getDate();
      return year + "-" + month + "-" + day + ""
    },
  },
}
</script>

<style lang="less">
  .point {
    box-sizing: border-box;
    background: rgb(249, 249, 249);
    // padding: 20px;
    .point-body {
      text-align:center;
      margin-top: 44px;
      font-size: 16px;
      a {
        color: #007fff;
      }
    }
  }
  .van-tabs__nav--card {
    box-sizing: border-box;
    height: 0.8rem;
    margin: 0 0 !important;
    border: 0.02667rem solid #ee0a24;
    border-radius: 0.05333rem;
  }
</style>
