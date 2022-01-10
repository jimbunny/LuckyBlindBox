<template>
  <div class="contact">
    <s-header :name="'意见反馈'"></s-header>
    <div class="contact-body">
      <van-form @submit="onSubmit">
        <van-field
          v-model="message"
          rows="5"
          autosize
          type="textarea"
          maxlength="200"
          placeholder="请输入反馈意见"
          show-word-limit
          :rules="[{ required: true }]"
        />
        <div style="margin: 16px;">
          <van-button round block type="info"  native-type="submit">提交</van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { contact } from '../service/me'
import {okCode, errorCode,} from "../config/settings";
import { Toast } from 'vant'
import { mapGetters } from "vuex";

export default {
  components: {
    sHeader
  },
   data() {
    return {
      message: "",
    }
  },
  computed: {
    ...mapGetters({
      email: "user/email",
      username: "user/username",
    }),
  },
  async mounted() {
    this.user = await this.$store.dispatch("user/getInfo");
  },
  // created() {
  //   console.log(this.$store.state.user.email);
  // },
  methods: {
    async onSubmit(values) {
      const { code, data, msg } = await contact({"email": this.user.email, "username": this.user.username, "advice": this.message})
      if (code === okCode) {
        this.user = data
        Toast.success('意见反馈成功！')
        const that = this
        setTimeout(function () {
          that.$router.push({ path: '/user' })
        }, 3000);
      } else {
        Toast.fail('意见反馈失败！')
      }
    },
  }
}
</script>

<style lang="less" scoped>
  .contact {
    box-sizing: border-box;
    padding: 20px;
    background: rgb(249, 249, 249);
    .contact-body {
      margin-top: 44px;
      font-size: 16px;
      a {
        color: #007fff;
      }
    }
  }
</style>
