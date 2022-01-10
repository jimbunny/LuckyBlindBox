<template>
    
    <div class="boxes-box">
    <s-header :name="'Boxes'"></s-header>
    <van-dropdown-menu style="margin-top: 44px;">
      <van-dropdown-item v-model="value1" :options="options.gender" />
      <van-dropdown-item v-model="value2" :options="options.size" />
      <van-dropdown-item v-model="value3" :options="options.age" />
      <!-- <van-dropdown-item title="class" ref="item">
        <van-cell center title="coat">
          <template #right-icon>
            <van-switch v-model="switch1" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <van-cell center title="pants">
          <template #right-icon>
            <van-switch v-model="switch2" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <van-cell center title="skirt">
          <template #right-icon>
            <van-switch v-model="switch3" size="24" active-color="#1890ff" />
          </template>
        </van-cell>
        <div style="padding: 5px 16px;">
          <van-button type="danger" block round @click="onConfirm">
            确认
          </van-button>
        </div>
      </van-dropdown-item> -->
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
    <van-dialog v-model="show" title="中奖商品" confirm-button-text="查看详情" @confirm="goToDetail">
      <van-swipe :autoplay="3000" style="height: 200px;">
        <van-swipe-item v-for="(image, index) in images" :key="index">
          <img v-lazy="image" />
        </van-swipe-item>
      </van-swipe>
    </van-dialog>
  </div>
</template>

<script>
import { LuckyWheel,} from 'vue-luck-draw'
import navBar from '@/components/NavBar'
import sHeader from '@/components/SimpleHeader'
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
      show: false,
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
      value1: 0,
      value2: 0,
      value3: 0,
      switch1: false,
      switch2: false,
      switch3: false,
      options: {
        "gender": [ 
          { text: 'gender', value: 0 },
          { text: 'female', value: 1 },
          { text: 'male', value: 2 },
        ],
        "age": [ 
          { text: 'age', value: 0 },
          { text: 'youth', value: 1 },
          { text: 'elderly', value: 2 },
        ],
        "size": [ 
          { text: 'size', value: 0 },
          { text: 'S', value: 1 },
          { text: 'M', value: 2 },
          { text: 'L', value: 3 },
          { text: 'XL', value: 4 },
          { text: 'XXL', value: 5 },
        ],
      }
    }
  },
  mounted () {
    this.getPrizesList()
  },
  methods: {
    goToDetail() {
      this.$router.push({ path: `/cart` })
    },
    onConfirm() {
      this.$refs.item.toggle();
    },
    goBack() {
      this.$router.go(-1)
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
    startCallBack () {
      this.$refs.LuckyWheel.play()
      setTimeout(() => {
        this.$refs.LuckyWheel.stop(Math.random() * 8 >> 0)
      }, 2000)
    },
    endCallBack (prize) {
      // alert(`恭喜你获得${prize.name}`)
      this.show=true
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
</style>