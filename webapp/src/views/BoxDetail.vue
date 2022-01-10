<template>
  <div class="box-detail">
    <s-header :name="'Box Detail'"></s-header>
    <div class="detail-content">
      <div class="detail-swipe-wrap">
        <van-swipe class="my-swipe" indicator-color="rgb(23, 157, 254)">
          <van-swipe-item v-for="(item, index) in detail.description" :key="index">
            <img :src="prefix(item.url)" alt="">
          </van-swipe-item>
        </van-swipe>
      </div>
      <div class="box-info">
        <div class="box-title">
          {{ detail.name }}
        </div>
        <div class="box-desc">免邮费 顺丰快递</div>
        <div class="box-price">
          <!-- <span>¥{{ detail.sellingPrice }}</span> -->
          <span>{{ detail.point }} point</span>
        </div>
      </div>
      <div style="height: 10px; background:#f9f9f9;"> </div>
        <div class="card">
          <div class="header">
            <a class="thumb"><van-image width="100%" height="100%" :src="require('../assets/point-btn.png')"/></a>
            <div class="content">
              <div class="title" style="margin:auto 5px;"> point: {{ userPoint }} </div>
              <div class="desc" style="margin:auto 5px;"> description </div>
            </div>
            <div class="right" style="height:100%; margin: auto">
              <van-button type="info" round size="mini" style="width: 90%;" @click="goToPoint"> get point </van-button>
            </div>
          </div>
        </div>
      <div class="box-intro">
        <!-- <ul>
          <li>概述</li>
          <li>参数</li>
          <li>安装服务</li>
          <li>常见问题</li>
        </ul> -->
        <div style="background:#f9f9f9;margin-bottom:44px;">
          <div class="title" style="padding:5px;"> 活动说明： </div>
          <div class="desc" style="padding:5px;"> description <br> description <br> description <br> <br> <br> </div> 
        </div>
        <div class="box-content">
          <qr-code style="display: block;" id="imageWrapper" :appSrc="appSrc" :logoSrc="logoSrc" :size="300"></qr-code> 
          <van-field :value="appSrc" style="display: none;" />
        </div>
        <!-- <div class="box-content" v-html="detail.goodsDetailContent"></div> -->
      </div>
    </div>
    <van-goods-action v-if="isLogin">
      <van-goods-action-button type="warning" text="share" @click="showShare=true"/>
      <van-goods-action-button type="danger" text="open" @click="awardProduct(detail)"/>
    </van-goods-action>
    <van-goods-action v-else>
      <van-goods-action-button type="info" text="login" @click="goToLogin()"/>
    </van-goods-action>

   <van-share-sheet
      v-model="showShare"
      :options="options"
        @select="onSelect"
      title="立即分享给好友"
    />

    <van-dialog v-model="show" title="中奖商品" confirm-button-text="查看详情" @confirm="goToCart()">
      <van-swipe :autoplay="3000" style="height: 200px;">
        <van-swipe-item v-for="product in products" :key="product.id" style="text-align: center;">
          <img style="height:200px; width:200px;" v-lazy="product.picture" />
        </van-swipe-item>
      </van-swipe>
    </van-dialog>
  </div>
</template>

<script>
import { getDetail, getAward } from '../service/package'
// import { addCart } from '../service/cart'
import sHeader from '@/components/SimpleHeader'
import { Toast } from 'vant'
import { okCode } from '../config/settings'
import QrCode from '@/components/QrCode'
import { RSAEncrypt } from '../utils/RSA'
import { mapGetters } from "vuex";
import Clipboard from 'clipboard'
import html2canvas from 'html2canvas'
import { validLogin } from '../service/user'

let Base64 = require('js-base64').Base64

export default {
  data() {
    return {
      detail: {},
      isLogin: false,
      logoSrc: require('../assets/logo.png'),
      products: ['https://upload.wikimedia.org/wikipedia/commons/4/44/Facebook_Logo.png','https://upload.wikimedia.org/wikipedia/commons/4/44/Facebook_Logo.png'],
      userPoint: 0,
      userEmail: "",
      show: false,
      showShare: false,
      options: [
        { name: 'Facebook', icon: 'https://upload.wikimedia.org/wikipedia/commons/4/44/Facebook_Logo.png' },
        { name: '复制链接', icon: 'link', className: "copy"},
        { name: '二维码', icon: 'qrcode' },
      ],
    }
  },
  components: {
    sHeader,
    QrCode
  },
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      email: "user/email",
      username: "user/username",
    }),
    count () {
      return this.$store.state.user.count
    },
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
  },
  async created() {
    const { id } = this.$route.params
    const { code, data } = await getDetail({'no':id})
    if (code === okCode) {
      this.detail = data[0]
    } else {
      Toast.fail('该套餐不存在！')
      this.detail = []
    }
    const login  = await validLogin()
    if (login.code == okCode) {
      this.isLogin = true
      const user = await this.$store.dispatch("user/getInfo"); 
      this.userPoint = user.point
      this.userEmail = user.email
    }  
  },
  methods: {
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
    goBack() {
      this.$router.go(-1)
    },
    async awardProduct(detail) {
      if (this.userPoint < detail.point) {
        this.$dialog.alert({
          title: '温馨提示',
          message: '积分不足，请充值！',
        }).then(() => {
          // on close
        });
      } else {
        const that = this
        this.$dialog.confirm({
          title: '温馨提示',
          message: '请确认是否要消耗' + this.detail.point + '积分抽奖吗？',
        })
          .then(() => {
            // on confirm
            this.detail.email = this.userEmail
            getAward(this.detail).then((res) => {
              const { code , data } = res;
              if (code === okCode) {
                this.products = data
                this.show = true 
                that.$store.dispatch("user/updateCart", {
                  "email": that.email
                });
              } else {
                setTimeout(function(){
                  Toast.fail('商品库存不足，请耐心等待！')
                },1000)
              }
            });
          })
          .catch(() => {
            // on cancel
          });
      }
    },
    goTo() {
      this.$router.push({ path: '/cart' })
    },
    // async addCart() {
    //   const { data, resultCode } = await addCart({ goodsCount: 1, goodsId: this.detail.goodsId })
    //   if (resultCode == 200 ) Toast.success('添加成功')
    //   this.$store.dispatch('updateCart')
    // },
    // async goToCart() {
    //   const { data, resultCode } = await addCart({ goodsCount: 1, goodsId: this.detail.goodsId })
    //   this.$store.dispatch('updateCart')
    //   this.$router.push({ path: '/cart' })
    // },
    goToDetail(item) {
      this.$router.push({ path: `product/${item.goodsId}` })
    },
    goToCart(item) {
      this.$router.push({ path: `/cart` })
    },
    goToPoint(item) {
      this.$router.push({ path: `/point` })
    },
    goToLogin() {
      this.$router.push({ path: `/login` })
    },
  },
}
</script>

<style lang="less">
  @import '../common/style/mixin';
  .card {
    position: relative;
    box-sizing: border-box;
    padding: 4px 8px;
    color: #323233;
    font-size: 12px;
    background-color: #ffffff;
    .header {
      display: -webkit-box;
      display: -webkit-flex;
      display: flex;
      width: 100%;
      .thumb {
        position: relative;
        -webkit-box-flex: 0;
        -webkit-flex: none;
        flex: none;
        width: 60px;
        height: 60px;
        margin-right: 16px;
      }
      .content {
        position: relative;
        display: -webkit-box;
        display: -webkit-flex;
        display: flex;
        -webkit-box-flex: 1;
        -webkit-flex: 1;
        flex: 1;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -webkit-flex-direction: column;
        flex-direction: column;
        -webkit-box-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
        min-width: 0;
        min-height: 1.62rem;
        .title {
          max-height: 0.85333rem;
          font-weight: 500;
          line-height: 0.42667rem;
          word-wrap: break-word;
          display: -webkit-box;
          overflow: hidden;
          text-overflow: ellipsis;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
        }
        .desc {
          max-height: 0.53333rem;
          color: #646566;
          line-height: 0.53333rem;
          overflow: hidden;
          word-wrap: break-word;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
      }
      .right {
        flex: 1
      }
    }
  }
  .box-detail {
    .detail-header {
      position: fixed;
      top: 0;
      left: 0;
      z-index: 10000;
      .fj();
      .wh(100%, 44px);
      line-height: 44px;
      padding: 0 10px;
      .boxSizing();
      color: #252525;
      background: #fff;
      border-bottom: 1px solid #dcdcdc;
      .box-name {
        font-size: 14px;
      }
    }
    .detail-content {
      margin-top: 44px;
      .detail-swipe-wrap {
        .my-swipe .van-swipe-item {
          img {
            width: 100%;
            // height: 300px;
          }
        }
      }
      .box-info {
        padding: 0 10px;
        .box-title {
          font-size: 18px;
          text-align: left;
          color: #333;
        }
        .box-desc {
          font-size: 14px;
          text-align: left;
          color: #999;
          padding: 5px 0;
        }
        .box-price {
          .fj();
          span:nth-child(1) {
            color: #F63515;
            font-size: 22px;
          }
          span:nth-child(2) {
            color: #999;
            font-size: 16px;
          }
        }
      }
      .box-intro {
        width: 100%;
        ul {
          .fj();
          width: 100%;
          margin: 10px 0;
          li {
            flex: 1;
            padding: 5px 0;
            text-align: center;
            font-size: 15px;
            border-right: 1px solid #999;
            box-sizing: border-box;
            &:last-child {
              border-right: none;
            }
          }
        }
        .box-content {
          padding: 0 20px;
          img {
            width: 100%;
          }
        }
      }
    }
  }
</style>
