<template>
  <div class="order-box">
    <s-header :name="'我的订单'" :back="'/user'"></s-header>
    <van-tabs @change="onChangeTab" :color="'rgb(23, 157, 254)'" :title-active-color="'rgb(23, 157, 254)'" class="order-tab" v-model="status">
      <van-tab title="全部" name='all'></van-tab>
      <van-tab title="待发货" name="noDelivery"></van-tab>
      <van-tab title="已发货" name="delivered"></van-tab>
    </van-tabs>
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh" class="order-list-refresh">
      <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
        @offset="300"
      >
        <div v-for="(item, index) in list" :key="index" class="order-item-box">
            <div class="order-item-header">
              <span>订单时间：{{ item.createTime }}</span>
              <span>{{ item.status }}</span>
            </div>
            <van-card
              @click="goTo(item.no)"
               v-for="(one, index) in item.OrderItemVOS.slice(0,1)" :key="index"
              :num="1"
              :price="one.outPrice"
              :desc="one.description"
              :title="one.name"
              :thumb="prefix(one.picture)"
            />
            <van-collapse v-model="activeNames" >
              <van-collapse-item title="detail" :name="item.no">
                <van-card
                  v-for="(one, index) in item.OrderItemVOS.slice(1-item.OrderItemVOS.length)" :key="index" 
                  :num="1"
                  :price="one.outPrice"
                  :desc="one.description"
                  :title="one.name"
                  :thumb="prefix(one.picture)"
                />
              </van-collapse-item>
            </van-collapse>
             <div style="bottom: 0; left: 0; width: 100%; background: #fff;">
              <div style=" display: flex;justify-content: space-between;padding: 0 5%;margin: 10px 0;font-size: 14px;">
                <span>数量 {{ item.OrderItemVOS.length }}</span>
                <span style="color: red;font-size: 18px;"> 
                ¥{{ item.totalPrice }}</span>
              </div>
              </div>
        </div>
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script>
import sHeader from '@/components/SimpleHeader'
import { getOrderList } from '../service/order'
import { prefix } from '@/common/js/utils'
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      status: '',
      loading: false,
      finished: false,
      refreshing: false,
      list: [],
      page: 1,
      email: "",
      activeNames: [],
    }
  },
  components: {
    sHeader
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
    this.email = user.email
  },
  async mounted() {
    // this.loadData()
  },
  methods: {
    async loadData() {
      const { data, data: { items } } = await getOrderList({ pageNo: this.page, pageSize: 5, email: '954447255@qq.com', status: this.status })
      this.list = this.list.concat(items)
      this.totalPage = data.totalPage
      this.loading = false;
      if (this.page >= data.totalPage) this.finished = true
    },
    onChangeTab(name, title) {
      this.status = name
      this.onRefresh()
    },
    goTo(id) {
      this.$router.push({ path: `order-detail?id=${id}` })
    },
    goBack() {
      this.$router.go(-1)
    },
    onLoad() {
      if (!this.refreshing && this.page < this.totalPage) {
        this.page = this.page + 1
      }
      if (this.refreshing) {
        this.list = [];
        this.refreshing = false;
      }
      this.loadData()
    },
    onRefresh() {
      this.refreshing = true
      this.finished = false
      this.loading = true
      this.page = 1
      this.onLoad()
    },
  }
}
</script>

<style lang="less" scoped>
  @import '../common/style/mixin';
  .order-box {
    .order-header {
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
      .order-name {
        font-size: 14px;
      }
    }
    .order-tab {
      margin-top: 44px;
      position: fixed;
      left: 0;
      z-index: 1000;
      width: 100%;
    }
    .order-list-refresh {
      margin-top: 68px;
      .van-card__content {
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      .van-pull-refresh__head {
        background: #f9f9f9;
      }
      .van-list {
        min-height: calc(100vh - 88px);
        background: #f9f9f9;
        margin-top: 20px;
      }
      .order-item-box {
        margin: 20px 10px;
        background-color: #fff;
        .order-item-header {
          padding: 10px 20px 0 20px;
          display: flex;
          justify-content: space-between;
        }
        .van-card {
          background-color: #fff;
          margin-top: 0;
        }
      }
    }
  }
</style>
