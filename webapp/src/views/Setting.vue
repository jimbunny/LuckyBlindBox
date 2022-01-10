<template>
  <div class="seting-box">
    <s-header :name="'账号管理'"></s-header>
    <div class="input-item">
      <van-form @submit="onSubmit">
        <van-field
          v-model="login.username"
          name="username"
          label="ชื่อผู้ใช้"
          placeholder="ชื่อผู้ใช้"
          disabled
        />
        <van-field
          v-model="login.email"
          center
          clearable
          label="email"
          placeholder="email"
          disabled
        >
        </van-field>
        <van-field
          v-model="login.password"
          type="password"
          name="password"
          label="รหัสผ่าน"
          placeholder="รหัสผ่าน"
          :rules="passwordRules"
        />
        <van-field
          v-model="login.confirmPassword"
          type="password"
          name="confirmPassword"
          label="confirm Password"
          placeholder="confirm Password"
          :rules="confirmPasswordRules"
        />
        <van-field
          v-model="login.description"
          name="描述"
          label="描述"
          placeholder="描述"
        />
        <!-- <van-field
          v-model="login.phone"
          center
          clearable
          label="phone"
          placeholder="phone"
          :rules="phoneRules"
        >
        </van-field>
        <van-field name="gender" label="gender" :rules="[{ required: true, message: '请选择性别' }]">
          <template #input>
            <van-radio-group v-model="login.gender" direction="horizontal">
              <van-radio name="female">female</van-radio>
              <van-radio name="male">male</van-radio>
            </van-radio-group>
          </template>
        </van-field>
         <van-field
          v-model="login.birth"
          center
          clearable
          label="birth"
          placeholder="birth"
          @click="showPopFn()"
          :rules="[{ required: true, message: '请选择出生日期' }]"
        ></van-field> -->
        <div id="date_time_picker">
          <van-popup v-model="show" position="bottom" :style="{ height: '40%' }">
          <van-datetime-picker v-model="currentDate" type="date" :min-date="minDate" :max-date="maxDate" @change="changeFn()" @confirm="confirmFn()" @cancel="cancelFn()" />
          </van-popup>
        </div>
        <van-button class="save-btn" round color="rgb(23, 157, 254)" type="primary" native-type="submit" block>保存</van-button>
        </van-form>
        <van-button class="save-btn" round color="#0bc15f" type="primary" @click="logout" block>退出登录</van-button>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { getUserInfo, EditUserInfo, logout } from '../service/user'
import { RSAEncrypt } from '../utils/RSA'
import { setLocal } from '@/common/js/utils'
import { Toast } from 'vant'
import {okCode, errorCode,} from "../config/settings";

export default {
  components: {
    sHeader
  },
  data() {
    return {
      login: {
        email: '',
        birth: this.timeFormat(new Date()),
        // phone: '',
        // username: '',
        // password: '',
        confirmPassword: '',
        description: '',
        // gender: "female",
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
      }, {
        // 自定义校验规则
          validator: value => {
            return checkUsername({"username": value}).then((res) => {
              const { code } = res;
              if (code === okCode) {
                return true;
              } else {
                return false;
              }
            });
          },
          message: '该用户名已存在',
          trigger: 'onBlur'
      }],
      // 校验手机号码
      phoneRules: [{
          required: true,
          message: '手机号码不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
              return /^((\+66|0)(\d{1,2}\-?\d{3}\-?\d{3,4}))|((\+๖๖|๐)([๐-๙]{1,2}\-?[๐-๙]{3}\-?[๐-๙]{3,4}))$/
                  .test(value)
          },
          message: '请输入正确格式的手机号码',
          trigger: 'onBlur'
      },{
        // 自定义校验规则
          validator: value => {
            return checkPhone({"phone": value}).then((res) => {
              const { code } = res;
              if (code === okCode) {
                return true;
              } else {
                return false;
              }
            });
          },
          message: '该手机号码已经存在！',
          trigger: 'onBlur'
      }],
      // 校验邮箱
      emailRules: [{
          required: true,
          message: '邮箱不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
              return /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/
                  .test(value)
          },
          message: '请输入正确格式的邮箱',
          trigger: 'onBlur'
      },{
        // 自定义校验规则
          validator: value => {
            return checkEmail({"email": value}).then((res) => {
              const { code } = res;
              if (code === okCode) {
                return true;
              } else {
                return false;
              }
            });
          },
          message: '该邮箱已经存在！',
          trigger: 'onBlur'
      }],
      // 校验邮箱
      forgetEmailRules: [{
          required: true,
          message: '邮箱不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
              return /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/
                  .test(value)
          },
          message: '请输入正确格式的邮箱',
          trigger: 'onBlur'
      },{
        // 自定义校验规则
          validator: value => {
            return checkEmail({"email": value}).then((res) => {
              const { code } = res;
              if (code === okCode) {
                return false;
              } else {
                return true;
              }
            });
          },
          message: '该邮箱不存在！',
          trigger: 'onBlur'
      }],
    }
  },
  async mounted() {
    const { data } = await getUserInfo()
    this.login = data
  },
  methods: {
    async onSubmit(values) {
      this.login.password = RSAEncrypt(this.login.password)
      this.login.confirmPassword = RSAEncrypt(this.login.confirmPassword)
      const { code } = await EditUserInfo(this.login)
        if (code === okCode) {
          Toast.success('修改密码成功，请重新登陆！')
          this.logout()
          // const that = this
          // setTimeout( async function(){
          //   await logout()
          //     that.$store.dispatch("user/logout").then(() => {
          //     that.$router.push({ path: '/login' })
          //   });
          // },3000)
        } else {
          Toast.fail('修改密码失败！')
        }
    },
    timeFormat(time) { // 时间格式化 2019-09-08
      let year = time.getFullYear();
      let month = time.getMonth() + 1;
      let day = time.getDate();
      return year + "-" + month + "-" + day + ""
    },
    // async save() {
    //   const params = {
    //     introduceSign: this.introduceSign,
    //     nickName: this.nickName,
    //     passwordMd5: this.$md5(this.password)
    //   }
    //   const { data } = await EditUserInfo(params)
    //   Toast.success('保存成功')
    // },
    async logout() {
      await logout()
      const that = this
      this.$store.dispatch("user/logout").then(() => {
      });
      setTimeout(function(){
        that.$router.push({ path: '/login' })
      },1000)
    }
  }
}
</script>

<style lang="less" scoped>
  .seting-box {
    .input-item {
      margin-top: 44px;
    }
    .save-btn {
      width: 80%;
      margin: 20px auto ;
    }
  }
</style>
