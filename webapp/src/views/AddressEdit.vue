<template>
  <div class="address-box">
    <s-header :name="`${type == 'add' ? '新增地址' : '编辑地址'}`"></s-header>
    <div class="input-item">
      <van-form @submit="onSubmit">
        <van-field
          v-model="address.username"
          name="username"
          label="姓名"
          placeholder="收件人姓名"
          :rules="[{ required: true, message: '请填写收件人姓名' }]"
        />
        <van-field
          v-model="address.phone"
          center
          clearable
          label="电话"
          placeholder="收件人电话号码"
          :rules="phoneRules"
        >
        </van-field>
        <van-field
          v-model="address.region"
          is-link
          readonly
          label="地区"
          placeholder="请选择所在地区"
          @click="show = true"
          :rules="[{ required: true, message: '请选择所在地区' }]"
        />
        <van-popup v-model="show" round position="bottom" :style="{ height: '80%' }">

          <van-search style="z-index:999999999; width:100%; position: fixed;" v-model="addressSearch" placeholder="请输入搜索关键词" />
          <van-list
            v-model="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="onLoad"
            style="margin-top: 40px;"
          >
            <van-cell v-for="item in list" :key="item.id" @click="selectAddress(item)" :title="item.townName+' '+item.cityName+' '+item.provinceName" size="large" :label="item.postCode" :label-class="'address'"/>
        </van-list>
        </van-popup>
        <van-field
          v-model="address.detailAddress"
          rows="2"
          autosize
          label="详细地址"
          placeholder="街道门牌、楼层房间号等信息"
          :rules="[{ required: true, message: '请填写详细地址' }]"
        >
        </van-field>
        <van-cell title="设置默认收货地址">
          <template #right-icon>
            <van-switch v-model="address.defaultFlag" size="20" />
          </template>
        </van-cell>
        <van-button class="save-btn" round color="rgb(23, 157, 254)" type="primary" native-type="submit" block>保存</van-button>
        </van-form>
        <van-button  v-if="type === 'edit'" class="save-btn" round type="primary" @click="deleteAddress()" block>删除</van-button>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { getAddressConfigList, AddAddress, EditAddress, DeleteAddress, getAddressList } from '../service/address'
import { RSAEncrypt } from '../utils/RSA'
import { setLocal } from '@/common/js/utils'
import { Toast } from 'vant'
import {okCode, errorCode,} from "../config/settings";
import { mapGetters } from "vuex";

export default {
  components: {
    sHeader
  },
  data() {
    return {
      type: "add",
      addressSearch: "",
      list: [],
      addressId: "",
      loading: false,
      finished: false,
      address: {
        email: '',
        username: '',
        phone: '',
        cityName: '',
        provinceName: '',
        townName: '',
        detailAddress: '',
        defaultFlag: 0,
        postCode: '',
      },
      currentDate: new Date(),
      changeDate: new Date(),
      show: false, // 用来显示弹出层
      minDate: new Date(1949, 10, 1),//出生日期起始范围
      maxDate: new Date(),//出生日期起始范围
      // 校验密码
      passwordRules: [{
          required: true,
          message: '密码不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return 8 <= value.length && value.length<=18;
          },
          message: '密码长度在8-18位之间',
          trigger: 'onBlur'
      }],
      // 校验密码
      confirmPasswordRules: [{
          required: true,
          message: '确认密码不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return value === this.login.password
          },
          message: '两次密码不一致！',
          trigger: 'onBlur'
      }],
      // 校验用户名号码
      usernameRules: [{
          required: true,
          message: '用户名不能为空',
          trigger: 'onBlur'
      }],
      // 校验手机号码
      phoneRules: [{
          required: true,
          message: '收件人手机号码不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
              return /^((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))$/
                  .test(value)
          },
          message: '请输入正确格式的手机号码',
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
  async mounted() {
    const { addressId, type, from } = this.$route.query
    this.type = type; this.addressId = addressId
   if (this.type == 'edit') {
     const { code, data } = await getAddressList({"pageNo":1,"pageSize": 50, "addressId": this.addressId})
      if (code != okCode) {
        Toast.fail("获取地址列表失败！")
      } else{
        this.address = data
        this.address.region = this.address.townName + " " + this.address.cityName + " " + this.address.provinceName + " " + this.address.postCode
        if (this.address.defaultFlag == 1) {
          this.address.defaultFlag = true
        } else {
          this.address.defaultFlag = false
        }
      }
   }
  },
  watch: {
    addressSearch: async function (val) {
      const { code, data } = await getAddressConfigList({"pageNo":1,"pageSize": 50, "address": val})
      if (code != okCode) {
        Toast.fail("获取地址列表失败！")
      } else{
        this.list = data.items
      }
    }
  },
  methods: {
    async deleteAddress() {
      const { code } = await DeleteAddress({addressId: this.address.addressId})
      if (code === okCode) {
        Toast.success('地址删除成功！')
        const that = this
        setTimeout(function(){
          that.$router.push({ path: `address?from=mine` })
        }, 2000)
      } else {
        Toast.fail('地址删除失败！')
      }
    },
    selectAddress(item) {
      this.address.provinceName = item.provinceName
      this.address.cityName = item.cityName
      this.address.townName = item.townName
      this.address.postCode = item.postCode
      this.show=false
      this.address.region = item.townName + " " + item.cityName + " " + item.provinceName + " " + item.postCode
    },
    async onLoad() {
      // 异步更新数据
      // setTimeout 仅做示例，真实场景中一般为 ajax 请求
      const { code, data } = await getAddressConfigList({"pageNo":1,"pageSize": 50})
      if (code != okCode) {
        Toast.fail("获取地址列表失败！")
      } else{
        this.list = data.items
      }
      // 加载状态结束
      this.loading = false;
      this.finished = true;
    },
    async onSubmit(values) {
      this.address.email = this.email
      if (this.type=="add") {
        const { code } = await AddAddress(this.address)
        if (code === okCode) {
          Toast.success('地址添加成功！')
          const that = this
          setTimeout(function(){
            that.$router.push({ path: `address?from=mine` })
          }, 2000)
        } else {
          Toast.fail('地址添加失败！')
        }
      } else {
        const { code } = await EditAddress(this.address)
        if (code === okCode) {
          Toast.success('地址编辑成功！')
          const that = this
          setTimeout(function(){
            that.$router.push({ path: `address?from=mine` })
          }, 2000)
        } else {
          Toast.fail('地址编辑失败！')
        }
      }
    }
  }
}
</script>

<style lang="less" scoped>
.address {
    color: red;
}
  .address-box {
    .input-item {
      margin-top: 44px;
    }
    .save-btn {
      width: 80%;
      margin: 20px auto ;
    }
  }
</style>
