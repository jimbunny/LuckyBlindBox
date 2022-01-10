<template>
  <div class="share">
    <s-header :name="'扫码分享'"></s-header>
    <div class="share-body">
       <qr-code id="imageWrapper" :appSrc="appSrc" :logoSrc="logoSrc" :size="300"></qr-code>
       <van-field :value="appSrc" disabled />
       <van-share-sheet
        v-model="showShare"
        :options="options"
         @select="onSelect"
        title="立即分享给好友"
      />
      <div style="margin: 16px;">
        <van-button round block type="info"  @click="showShare=true">分享</van-button>
      </div>

      <van-pull-refresh v-model="isLoading" @refresh="onRefresh">
        <!-- <van-cell v-for="item in list" :key="item" :title="item" /> -->
        <van-cell-group>
          <van-cell v-for="item in list" :key="item.id" :value="item.register_on">
            <!-- 使用 title 插槽来自定义标题 -->
            <template #title>
              <span class="custom-title">{{ item.invited }}</span>
              <van-tag plain type="danger" style="margin-top: 5px; float: right;"> + {{ item.point }} point</van-tag>
            </template>
          </van-cell> 
        </van-cell-group>
      </van-pull-refresh>
    </div>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import QrCode from '@/components/QrCode'
import { RSAEncrypt } from '../utils/RSA'
import { mapGetters } from "vuex";
import Clipboard from 'clipboard'
import { Toast } from 'vant'
import html2canvas from 'html2canvas';
import { inviteList } from '../service/user'

let Base64 = require('js-base64').Base64

export default {
  components: {
    sHeader,
    QrCode,
  },
  // mixins: [Clipboard],
  data() {
    return {
      logoSrc: require('../assets/logo.png'),
      showShare: false,
      options: [
        { name: 'Facebook', icon: 'https://upload.wikimedia.org/wikipedia/commons/4/44/Facebook_Logo.png' },
        { name: '复制链接', icon: 'link', className: "copy"},
        { name: '二维码', icon: 'qrcode' },
      ],
      list: [],
      isLoading: false,
    }
  },
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      email: "user/email",
      username: "user/username",
    }),
    appSrc:{
      //getter
      get:function(){
        return 'http://localhost:8083/#/home?inviterId=' + Base64.encode(this.email)
      },
      //setter
      set:function(newValue){
        // 这里由于该计算属性被赋值，将被调用
      }
    },
    paramsEmail:{
      //getter
      get:function(){
        return this.email
      },
      //setter
      set:function(newValue){
        // 这里由于该计算属性被赋值，将被调用
      }
    },
  },
  async created() {
    await this.$store.dispatch("user/getInfo"); 
    const { code, data, msg } = await inviteList({"email": this.email});
    this.list = data
  },
  methods: {
    async onRefresh() {
      const { code, data, msg } = await inviteList({"email": this.email});
      this.list = data
      Toast('刷新成功');
      this.isLoading = false;
    },
    onSelect(option) {
      if(option.name === '复制链接') {
        this.$copyText(this.appSrc).then( e => {
          Toast("已复制到剪切板，请分享");
        }, function (e) {
          Toast("该浏览器不支持自动复制");
          console.log(e)
        })
      } else if(option.name === '二维码') {
          html2canvas(document.getElementById("imageWrapper")).then(canvas => {
          let saveUrl = canvas.toDataURL('image/png')
          let aLink = document.createElement('a')
          let blob = this.base64ToBlob(saveUrl)
          let evt = document.createEvent('HTMLEvents')
          evt.initEvent('click', true, true)
          aLink.download = '二维码.jpg'
          aLink.href = URL.createObjectURL(blob)
          aLink.click()
        });
      } else {
        window.location.href = 'https://www.facebook.com/sharer.php?u=' + this.appSrc;
      }
      // Toast(option.name);
    },
    //这里把图片转base64
	    base64ToBlob (code) {
	       let parts = code.split(';base64,')
	       let contentType = parts[0].split(':')[1]
	       let raw = window.atob(parts[1])
	       let rawLength = raw.length
	       let uInt8Array = new Uint8Array(rawLength)
	       for (let i = 0; i < rawLength; ++i) {
	           uInt8Array[i] = raw.charCodeAt(i)
	       }
	       return new Blob([uInt8Array], {type: contentType})
	   },
  }
}
</script>

<style lang="less" scoped>
  .share {
    box-sizing: border-box;
    padding: 20px;
    background: rgb(249, 249, 249);
    .share-body {
      margin-top: 44px;
      font-size: 16px;
      text-align:center;
      a {
        color: #007fff;
      }
      .custom-title {
        margin-right: 4px;
        float: left;
        vertical-align: middle;
      }
    }
  }
</style>
