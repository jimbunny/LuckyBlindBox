<template>
    <div class="boxes-box">
    <s-header :name="'Boxes'"></s-header>
    <van-dropdown-menu style="margin-top: 44px;">
      <van-dropdown-item v-model="queryForm.gender" :options="options.gender" />
      <van-dropdown-item v-model="queryForm.size" :options="options.size" />
      <van-dropdown-item v-model="queryForm.age" :options="options.age" />
      <van-dropdown-item title="class" ref="item">
        <van-cell center title="coat">
          <template #right-icon>
            <van-switch v-model="coat" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <van-cell center title="pants">
          <template #right-icon>
            <van-switch v-model="pants" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <van-cell center title="skirt">
          <template #right-icon>
            <van-switch v-model="skirt" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <div style="padding: 5px 16px;">
          <van-button type="danger" color="rgb(23, 157, 254)" block round @click="onConfirm">
            确认
          </van-button>
        </div>
      </van-dropdown-item>
    </van-dropdown-menu>

    <div class="box">
      <img :src="require('../assets/boxBJ.png')" width="100%" />
      <LuckyWheel
        class="luck-draw"
        ref="LuckyWheel"
        width="245px"
        height="245px"
        :default-style="defaultStyle"
        :blocks="blocks"
        :prizes="prizes"
        :buttons="buttons"
        @start="startCallBack"
        @end="endCallBack"
      />

      
  </div>
    <nav-bar></nav-bar>

<!--弹出框，赋予chargeBtn事件-->
     <van-dialog
    v-model="showConfirm"
    title="温馨提示"
    show-cancel-button
    :before-close="onBeforeClose"
    @confirm="handleConfirm"
  >
<!--输入框-->
<van-form ref="point">
    <van-field
      v-model="userPoint"
      center
      clearable
      readonly
      label="当前积分"
      placeholder="当前积分"
    >
      <template #button>
        <van-button size="small" type="info" @click="goToPoint()"> get point</van-button>
      </template>
    </van-field>
    <van-field
      v-model="exchangeCount"
      rows="1"
      autosize
      label="可抽数量"
      type="textarea"
      placeholder="可抽数量"
    ><template #input>
        <div style="color: red;">{{ exchangeCount }}</div>
      </template>
    </van-field>
    <van-field
      v-model="usedPoint"
      rows="1"
      name="usedPoint"
      autosize
      label="抽奖积分"
      type="textarea"
      placeholder="请输入积分数"
      :rules="pointRules"
    />
</van-form>
</van-dialog>

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
import { LuckyWheel } from 'vue-luck-draw'
import { getAward } from '../service/package'
import navBar from '@/components/NavBar'
import sHeader from '@/components/SimpleHeader'
import { validLogin } from '../service/user'
import { okCode } from '../config/settings'
import { Toast } from 'vant'
import { mapGetters } from "vuex";

export default {
  components: {
    LuckyWheel,
    navBar,
    sHeader
  },
  data() {
    return {
      images: [
        'https://100px.net/assets/img/0.efbe4dff.png',
        'https://100px.net/assets/img/0.efbe4dff.png',
      ],
      products: [],
      show: false,
      userPoint: 0,
      userEmail: "",
      showConfirm: false,
      confirmStatus: false,
      usedPoint: "",
      exchangeCount: 0,
      isLogin: false,
      prizes: [],
      buttons: [{
        radius: '45px',
        imgs: [{ src: require('../assets/lo-btn.png'), width: '102%', top: '-127%' }]
      }],
      blocks: [
        { padding: '3px', background: '#a70c1b' },
        { padding: '6px', background: '#ffb633' },
      ],
      defaultStyle: {
        fontColor: '#a70c1b',
        fontSize: '10px',
      },
      coat: false,
      pants: false,
      skirt: false,
      queryForm: {
        pageNo: 1,
        pageSize: 1000,
        name: "",
        gender: "",
        size: "",
        age: "",
        Pclass: new Array(),
        count: 0,
        email:"",
        point: ""
      },
      options: {
        "gender": [ 
          { text: 'gender', value: '' },
          { text: 'female', value: 'female' },
          { text: 'male', value: 'male' },
        ],
        "age": [ 
          { text: 'age', value: '' },
          { text: 'youth', value: 'youth' },
          { text: 'elderly', value: 'elderly' },
        ],
        "size": [ 
          { text: 'size', value: '' },
          { text: 'S', value: 'S' },
          { text: 'M', value: 'M' },
          { text: 'L', value: 'L' },
          { text: 'XL', value: 'XL' },
          { text: 'XXL', value: 'XXL' },
        ],
      },
      // 校验密码
      pointRules: [{
          required: true,
          message: '抽奖积分不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return value != 0;
          },
          message: '抽奖积分不能为空',
          trigger: 'onBlur'
      }, {
        // 自定义校验规则
          validator: value => {
            return value <= this.userPoint;
          },
          message: '抽奖积分超出账户积分',
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
    count () {
      return this.$store.state.user.count
    },
  },
  watch: {
    "usedPoint": function (val) {
      this.exchangeCount =  val
    },
  },
  async mounted () {
    this.getPrizesList()
    const login  = await validLogin()
    if (login.code == okCode) {
      this.isLogin = true
      const user = await this.$store.dispatch("user/getInfo"); 
      this.userPoint = user.point
      this.queryForm.email = user.email
    }
  },
  methods: {
    goToDetail() {
      this.$router.push({ path: `/cart` })
    },
    onConfirm() {
      if (this.coat) {
        if(this.queryForm.Pclass.indexOf('coat') <= -1){
          this.queryForm.Pclass.push('coat')
        }
      } else {
        if(this.queryForm.Pclass.indexOf('coat') > -1){
          this.queryForm.Pclass.remove('coat')
        }
      }
      if (this.pants) {
        if(this.queryForm.Pclass.indexOf('pants') <= -1){
          this.queryForm.Pclass.push('pants')
        }
      } else {
        if(this.queryForm.Pclass.indexOf('pants') > -1){
          this.queryForm.Pclass.remove('pants')
        }
      }
      if (this.skirt) {
        if(this.queryForm.Pclass.indexOf('skirt') <= -1){
          this.queryForm.Pclass.push('skirt')
        }
      } else {
        if(this.queryForm.Pclass.indexOf('skirt') > -1){
          this.queryForm.Pclass.remove('skirt')
        }
      }
      this.$refs.item.toggle();
    },
    goBack() {
      this.$router.go(-1)
    },
    goToCart() {
      this.$router.push({ path: '/cart' })
    },
    goTo(r) {
      this.$router.push({ path: r })
    },
    getPrizesList () {
      const prizes = []
      let data = [
        { name: '谢谢参与', img: 'https://100px.net/assets/img/0.efbe4dff.png'},
        { name: '红包', img: 'https://100px.net/assets/img/0.efbe4dff.png'},
        { name: '抽奖次数+3', img: 'https://100px.net/assets/img/0.efbe4dff.png' },
        { name: '礼物', img: 'https://100px.net/assets/img/0.efbe4dff.png'},
        { name: '谢谢参与', img: 'https://100px.net/assets/img/0.efbe4dff.png' },
        { name: '红包', img: 'https://100px.net/assets/img/0.efbe4dff.png' },
        { name: '抽奖次数+3', img: 'https://100px.net/assets/img/0.efbe4dff.png' },
        { name: '礼物', img: 'https://100px.net/assets/img/0.efbe4dff.png' }
      ]
      data.forEach((item, index) => {
        prizes.push({
          name: item.name,
          background: index % 2 === 0 ? '#ffd099' : '#fff',
          fonts: [{ text: item.name, top: '8%' }],
          imgs:[{ src: item.img, width: '30%', top: '30%' }],
        })
      })
      this.prizes = prizes
    },
    onBeforeClose(action, done) {//确认or取消
      if (action === 'cancel') {//取消按钮
        this.$refs["point"].resetValidation("usedPoint");
        this.usedPoint= 0;
        return done();
      } else if (action === 'confirm') {//确定按钮
          //向后端传值并关闭dialog弹出框
          return done(false);
          };
    },
    // 实例弹窗确认
    handleConfirm() {
    this.$refs["point"]
      .validate()
      .then(() => {
        this.showConfirm = false;
        this.confirmStatus = true;
        this.startCallBack()
        this.confirmStatus = false;
      })
      .catch(() => {});
    },
    startCallBack () {
     if (!this.isLogin) {
        this.$dialog.alert({
          title: '温馨提示',
          message: '请登陆',
          theme: 'round-button',
        }).then(() => {
          // on close
          this.goToLogin()
        });
      } 
      else if (this.queryForm.age=="" || this.queryForm.gender=="" || this.queryForm.size=="" || this.queryForm.Pclass.length==0) {
        Toast.fail("请选择抽奖条件！")
      } 
      else {
        if (this.confirmStatus) {
          this.queryForm.count= this.exchangeCount
          this.queryForm.point = this.usedPoint
          this.queryForm.Pclass = this.queryForm.Pclass[0]
          const that = this
          getAward(this.queryForm).then((res) => {
            const { code , data } = res;
            if (code === okCode) {
              that.$refs.LuckyWheel.play()
              this.products = data
              that.$store.dispatch("user/updateCart", {
                "email": that.queryForm.email
              });
              setTimeout(() => {
                that.$refs.LuckyWheel.stop(Math.random() * 8 >> 0)
              }, 2000)
            } else {
              setTimeout(function(){
                Toast.fail('商品库存不足，请耐心等待！')
              },1000)
            }
          });
        } else {
          this.showConfirm = true;
        }
      }
    },
    endCallBack (prize) {
      // alert(`恭喜你获得${prize.name}`)
      if (this.products==[]) {
        this.show=false
      } else {
        this.show=true
      }
    },
    goToLogin(item) {
      this.$router.push({ path: `/login` })
    },
    goToPoint(item) {
      this.$router.push({ path: `/point` })
    },
  }
}
</script>
<style lang="less" scoped>
  @import '../common/style/mixin';
  .boxes-box {
    background: url(~@/assets/blue.jpeg) no-repeat;
    width:100%;
    height:100%;
    background-size:100% 100%;
    .boxes-header {
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
      .user-name {
        font-size: 14px;
      }
    }
  }
  .box {
    position: relative;
    margin: 20px auto;
    width: 310px;
    height: 310px;
  }
  .luck-draw {
    width: 245px;
    height: 245px;
    position: absolute;
    left: 49%;
    top: 48%;
    transform: translate(-50%, -50%)
  }

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