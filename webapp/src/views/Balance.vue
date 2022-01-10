<template>
  <div class="balance">
    <s-header :name="'充值中心'"></s-header>
    <div class="balance-body">
      <van-tabs v-model="activeName" type="card" color="rgb(23, 157, 254)">
        <van-tab title="余额充值" name="balance">
          <van-field name="balance" label="账户余额">
              <template #input>
                <div style="color: red;">{{ userBalance }}</div>
              </template>
            </van-field>
          <van-form @submit="onSubmit">
            <van-field
              v-model="balance.balance"
              name="balance"
              label="充值金额"
              type="number"
              placeholder="充值金额"
              :rules="balanceRules"
            />
            <van-field name="type" label="充值方式" :rules="[{ required: true, message: '请选择充值方式' }]">
              <template #input>
                <van-radio-group v-model="balance.type" direction="horizontal">
                  <van-radio name="bank">银行卡</van-radio>
                  <van-radio name="ture">True 钱包</van-radio>
                </van-radio-group>
              </template>
            </van-field>
            <van-field name="picture" label="汇款凭证" :rules="[{ required: true, message: '请选上传图片' }]">
              <template #input>
                <van-uploader v-model="balance.picture" :after-read="uploadFile"
                :max-count="1" :max-size="500 * 1024" @oversize="onOversize"/>
              </template>
            </van-field>
            <van-field
              v-model="balance.date"
              center
              clearable
              name="date"
              label="汇款日期"
              placeholder="date"
              @click="showPopFn()"
              :rules="[{ required: true, message: '请选择汇款日期' }]"
            ></van-field>
            <div id="date_time_picker">
              <van-popup v-model="show" position="bottom" :style="{ height: '40%' }">
              <van-datetime-picker v-model="currentDate" type="date" :min-date="minDate" :max-date="maxDate" @change="changeFn()" @confirm="confirmFn()" @cancel="cancelFn()" />
              </van-popup>
            </div>
            <van-field
              v-model="balance.remark"
              name="remark"
              label="备注"
              placeholder="备注"
            />
            <div style="margin: 16px;">
              <van-button round block type="info" native-type="submit">提交</van-button>
            </div>
          </van-form>
          <img style="width: 300px;" :src="require('../assets/money.jpg')" alt="">
        </van-tab>
        <van-tab title="历史查询" name="history">
          <van-pull-refresh v-model="isLoading" @refresh="onRefresh">
          <!-- <van-cell v-for="item in list" :key="item" :title="item" /> -->
          <van-collapse v-model="activeNames">
            <van-row class="van-cell">
              <van-col span="4">序号</van-col>
              <van-col span="6">金额</van-col>
              <van-col span="6">状态</van-col>
              <van-col span="8">时间</van-col>
            </van-row>
            <van-divider :style="{ margin: '0 0' }"/>
            <van-collapse-item v-for="item in list" :key="item.id"  :name="item.id">
              <template #title>
                <!-- <div>{{ item.balance }} <van-icon name="question-o" /></div> -->
                <van-row>
                  <van-col span="4">{{ item.id }}</van-col>
                  <van-col span="6">{{ item.balance }}</van-col>
                  <van-col span="6"><van-tag plain type="primary">{{ item.status }}</van-tag></van-col>
                  <van-col span="8">{{ item.date }}</van-col>
                </van-row>
              </template>
              {{ item.reason }}
            </van-collapse-item>
          </van-collapse>
          <!-- <van-cell-group>
            <van-cell v-for="item in list" :key="item.id" :value="item.date">
              <template #title>
                <span class="custom-title">{{ item.balance }}</span>
                <span >{{ item.id }}</span>
                <van-tag plain type="danger" style="margin-top: 5px; float: right;"> {{ item.status }}</van-tag>
              </template>
            </van-cell> 
          </van-cell-group> -->
        </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { mapGetters } from "vuex";
import { AddBalanceInfo, GetBalanceInfo } from '../service/user'
import {okCode, errorCode,} from "../config/settings";
import { Toast } from 'vant'

export default {
  components: {
    sHeader
  },
  data() {
    return {
      activeName: 'balance',
      show: false,
      currentDate: new Date(),
      minDate: new Date(1949, 10, 1),//出生日期起始范围
      maxDate: new Date(),//出生日期起始范围
      formData: new FormData(),
      balance: {
        balance: 0,
        type: "bank",
        picture: [],
        remark: "",
        email: "",
        date: this.timeFormat(new Date()),
      },
      userBalance: "",
      list: [],
      activeNames: [],
      isLoading: false,
      // 校验密码
      balanceRules: [{
          required: true,
          message: '充值金额不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return value != 0;
          },
          message: '充值金额不能为空',
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
  async created() {
    const user = await this.$store.dispatch("user/getInfo"); 
    this.userBalance = user.balance
    const { code, data, msg } = await GetBalanceInfo({"email": this.email, "pageNo": 1, "pageSize": 100});
    this.list = data.items
  },
  methods: {
    onOversize(file) {
      Toast('文件大小不能超过 500kb');
    },
    async onRefresh() {
      const { code, data, msg } = await GetBalanceInfo({"email": this.email, "pageNo": 1, "pageSize": 100});
      this.list = data.items
      Toast('刷新成功');
      this.isLoading = false;
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
      this.balance.date = this.timeFormat(this.currentDate);
      this.show = false;
    },
    cancelFn(){
      this.show = true;
    },
    uploadFile(file) {
      this.formData.append("picture", file.file);
      //使用axios上传文件到服务器,注意设置axios的headers为{ "Content-Type": "multipart/form-data" }
    },
    async onSubmit(values) {
      this.balance.email = this.email;
      let that = this;                              //修改this指向
      for (let key in this.balance) {
        if (key == 'picture') {
          continue
        }
      　that.formData.append(key, this.balance[key])
      }
      const { code } = await AddBalanceInfo(that.formData)
        if (code === okCode) {
          const { code, data, msg } = await GetBalanceInfo({"email": this.email, "pageNo": 1, "pageSize": 100});
          this.list = data.items
          Toast.success('等待审核。。。！')
        } else {
          Toast.fail('提交失败')
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
  .balance {
    box-sizing: border-box;
    background: rgb(249, 249, 249);
    // padding: 20px;
    .balance-body {
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
