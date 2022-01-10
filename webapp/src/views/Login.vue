<template>
  <div class="login">
    <s-header :name="type == 'login' ? 'เข้าสู่ระบบ' : type == 'register' ? 'ลงทะเบียน': 'forget password'" :back="'/home'"></s-header>
    <img class="logo" :src="require('../assets/logo.png')" alt="">
    <div v-if="type == 'login'" class="login-body login">
      <van-form @submit="onSubmit">
        <van-field
          v-model="username"
          name="username"
          label="ชื่อผู้ใช้"
          placeholder="ชื่อผู้ใช้"
          :rules="[{ required: true, message: 'โปรดกรอกชื่อผู้ใช้' }]"
        />
        <van-field
          v-model="password"
          type="password"
          name="password"
          label="รหัสผ่าน"
          placeholder="รหัสผ่าน"
          :rules="[{ required: true, message: 'โปรดกรอกรหัสผ่าน' }]"
        />
        <div class="verify">
          <Verify ref="loginVerifyRef" @error="error" :showButton="false" @success="success" :width="'100%'" :height="'40px'" :fontSize="'16px'" :codeLength="4" :type="1"></Verify>
        <!-- <slide-verify  
          ref="slideblock"  
          @again="onAgain"  
          @fulfilled="onFulfilled"  
          @success="onSuccess"  
          @fail="onFail"  
          @refresh="onRefresh"  
          :accuracy="accuracy"  
          :slider-text="text"  
          ></slide-verify>  
          <div>{{msg}}</div>   -->
        </div>
        <div style="margin: 16px;">
          <div class="link-register" @click="toggle('register')">ลงทะเบียน </div>
          <div class="link-forget" @click="toggle('forget')">ลืมรหัสผ่าน</div>
          <van-button round block type="primary"  native-type="submit">เข้าสู่ระบบ</van-button>
          <van-divider>or</van-divider>
          <fb-signin-button
          class="van-button van-button--info van-button--normal van-button--block van-button--round"
          style="margin-top:20px;"
          :params="fbSignInParams"
          @success="onSignInSuccess"
          @error="onSignInError">
          <div class="van-button__content">
          เข้าสู่ระบบด้วย Facebook 
          </div>
        </fb-signin-button>
        </div>
      </van-form>
    </div>
    <div v-if="type == 'register'" class="login-body register">
      <van-form @submit="onSubmit">
        <van-field
          v-model="login.username"
          name="username"
          label="ชื่อผู้ใช้"
          placeholder="ชื่อผู้ใช้"
          :rules="usernameRules"
        />
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
          v-model="login.email"
          center
          clearable
          label="email"
          placeholder="email"
          :rules="emailRules"
        >
        </van-field>
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
        ></van-field> 
        <div id="date_time_picker">
          <van-popup v-model="show" position="bottom" :style="{ height: '40%' }">
          <van-datetime-picker v-model="currentDate" type="date" :min-date="minDate" :max-date="maxDate" @change="changeFn()" @confirm="confirmFn()" @cancel="cancelFn()" />
          </van-popup>
        </div>-->
        <div class="verify">
          <Verify ref="loginVerifyRef" @error="error" :showButton="false" @success="success" :width="'100%'" :height="'40px'" :codeLength="4" :fontSize="'16px'" :type="1"></Verify>
        </div>
        <div style="margin: 16px;">
          <div class="link-login" @click="toggle('login')">เข้าสู่ระบบ</div>
          <van-button round block type="info" color="rgb(23, 157, 254)" native-type="submit">ลงทะเบียน</van-button>
        </div>
      </van-form>
    </div>
    <div v-if="type == 'forget'" class="login-body forget">
      <van-form @submit="onSubmit">
        <van-field
          v-model="email"
          center
          clearable
          label="email"
          placeholder="email"
          :rules="forgetEmailRules"
        >
        </van-field>
        <div class="verify">
          <Verify ref="loginVerifyRef" @error="error" :showButton="false" @success="success" :width="'100%'" :height="'40px'" :codeLength="4" :fontSize="'16px'" :type="1"></Verify>
        </div>
        <div style="margin: 16px;">
          <van-button round block type="info" color="rgb(23, 157, 254)" native-type="submit">找回密码</van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { checkUsername, login, register, getUserInfo, checkPhone, checkEmail, validFB, forgetPassword } from '../service/user'
import { RSAEncrypt } from '../utils/RSA'
import { setLocal, getLocal } from '@/common/js/utils'
import { Toast } from 'vant'
import { DatetimePicker } from "vant";
import Verify from '@/components/Verify'
import {okCode, errorCode,} from "../config/settings";

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      login: {
        email: '',
        // birth: this.timeFormat(new Date()),
        // phone: '',
        username: '',
        password: '',
        confirmPassword: '',
        // gender: "female",
      },
      currentDate: new Date(),
      changeDate: new Date(),
      show: false, // 用来显示弹出层
      type: 'login',
      verify: false,
      minDate: new Date(1949, 10, 1),//出生日期起始范围
      maxDate: new Date(),//出生日期起始范围
      fbSignInParams: {
        scope: 'email,user_likes',
        return_scopes: true
      },
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
  components: {
    sHeader,
    Verify
  },
  mounted() {
    // this.timeFormat(new Date());
  },
  methods: {
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
      this.login.birth = this.timeFormat(this.currentDate);
      this.show = false;
    },
    cancelFn(){
      this.show = true;
    },
    timeFormat(time) { // 时间格式化 2019-09-08
      let year = time.getFullYear();
      let month = time.getMonth() + 1;
      let day = time.getDate();
      return year + "-" + month + "-" + day + ""
    },
    async onSignInSuccess (response) {
        if(response.status === 'connected') {
          const FBParams = {accessToken: response.authResponse.accessToken,userID:response.authResponse.userID, type: "fb"}
          const inviterId = localStorage.getItem('inviterId');
          if(inviterId) {
            await this.$store.dispatch("user/login", {accessToken: response.authResponse.accessToken,userID:response.authResponse.userID, type: "fb", inviterId: inviterId}, "fb");
          } else {
            await this.$store.dispatch("user/login", {accessToken: response.authResponse.accessToken,userID:response.authResponse.userID, type: "fb"}, "fb");
          }        
          window.location.href = '/'
        } else {
          Toast.fail("facebook验证失败！")
        }
        console.log(response) //返回第三方的登录信息 token等
      },
      onSignInError (error) {
        Toast.fail("facebook验证失败！")
      },
    dealTriVer() {
      // 执行验证码的验证，通过 this.verify 知道验证码是否填写正确
      this.$refs.loginVerifyRef.$refs.instance.checkCode()
    },
    toggle(v) {
      this.verify = false
      this.type = v
    },
    async onSubmit(values) {
      // this.dealTriVer()
      // if (!this.verify) {
      //   Toast.fail('验证码未填或填写错误!')
      //   return
      // } 
      if (this.type == 'login') {
        await this.$store.dispatch("user/login", {
          "username": values.username,
          "password": RSAEncrypt(values.password),
          "type": "user"
        });
      } else if (this.type == 'forget') {
        const { code } = await forgetPassword({ email: this.email})
        if (code === okCode) {
          Toast.success('重置密码已经发送到您的邮箱，请查收！')
          this.type = 'login'
        } else {
          Toast.fail('重置密码发送失败！')
        }
      } else if (this.type == 'register') {
        const inviterId = localStorage.getItem('inviterId');
        if(inviterId) {
          this.login.inviterId = inviterId
        }
        this.login.password = RSAEncrypt(this.login.password)
        this.login.confirmPassword = RSAEncrypt(this.login.confirmPassword)
        const { code } = await register(this.login)
        if (code === okCode) {
          Toast.success('注册成功')
          this.type = 'login'
        } else {
          Toast.fail('注册失败')
        }
      }
    },
    success(obj) {
      this.verify = true
      // 回调之后，刷新验证码
      obj.refresh()
    },
    error(obj) {
      this.verify = false
      // 回调之后，刷新验证码
      obj.refresh()
    }
  },
}
</script>

<style lang="less">
  .fb-signin-button {
    /* This is where you control how the button looks. Be creative! */
    color: white;
    background: rgb(23, 157, 254);
    border-color: rgb(23, 157, 254);
  }
  .login {
    .logo {
      width: 120px;
      height: 120px;
      display: block;
      margin: 80px auto 0px;
    }
    .login-body {
      padding: 0 20px;
    }
    .login {
      .link-register {
        font-size: 14px;
        margin-bottom: 20px;
        color: #1989fa;
        display: inline-block;
      }
      .link-forget {
        float: right;
        font-size: 14px;
        margin-bottom: 20px;
        color: #1989fa;
        display: inline-block;
      }
    }
    .register {
      .link-login {
        font-size: 14px;
        margin-bottom: 20px;
        color: #1989fa;
        display: inline-block;
      }
    }
    .verify-bar-area {
      margin-top: 24px;
      .verify-left-bar {
        border-color: rgb(23, 157, 254);
      }
      .verify-move-block {
        background-color: rgb(23, 157, 254);
        color: #fff;
      }
    }
    .verify {
      >div {
        width: 100%;
      }
      padding: 0 0.46667rem;
      display: flex;
      justify-content: center;
      .cerify-code-panel {
        margin-top: 16px;
      }
      .verify-code {
        width: 40%!important;
        float: left!important;
      }
      .verify-code-area {
        float: left!important;
        width: 54%!important;
        margin-left: 14px!important;
        .varify-input-code {
          width: 90px;
          height: 38px!important;
          border: 1px solid #e9e9e9;
          padding-left: 10px;
          font-size: 16px;
        }
        .verify-change-area {
          line-height: 44px;
          float: right;
        }
      }
    }
  }
</style>
