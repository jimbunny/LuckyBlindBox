<template>
  <div class="actionLog-container">
    <byui-query-form>
      <byui-query-form-left-panel :span="18">
        <el-form :inline="true" :model="queryForm" @submit.native.prevent>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.username"
              :placeholder="$t('log.usernameTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.model"
              :placeholder="$t('log.modelTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.action"
              :placeholder="$t('log.actionTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-search" type="primary" @click="fetchData"
              >{{ $t("product.search") }}
            </el-button>
          </el-form-item>
        </el-form>
      </byui-query-form-left-panel>
      <byui-query-form-right-panel :span="6">
        <el-form :inline="true">
          <el-form-item>
            <el-button icon="el-icon-refresh" type="primary" @click="queryData"
              >{{ $t("log.refresh") }}
            </el-button>
          </el-form-item>
        </el-form>
      </byui-query-form-right-panel>
    </byui-query-form>

    <el-table
      v-loading="listLoading"
      :data="list"
      :element-loading-text="elementLoadingText"
      @selection-change="setSelectRows"
    >
      <el-table-column prop="id" :label="$t('product.id')"></el-table-column>
      <el-table-column
        prop="username"
        :label="$t('log.username')"
      ></el-table-column>
      <el-table-column prop="model" :label="$t('log.model')"></el-table-column>
      <el-table-column
        prop="action"
        :label="$t('log.action')"
      ></el-table-column>
      <el-table-column
        prop="content"
        :label="$t('log.content')"
      ></el-table-column>
      <el-table-column
        prop="updateTime"
        :label="$t('log.updateTime')"
      ></el-table-column>
    </el-table>
    <el-pagination
      background
      :current-page="queryForm.pageNo"
      :page-size="queryForm.pageSize"
      :layout="layout"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    >
    </el-pagination>
  </div>
</template>

<script>
import { getList, doDelete } from "@/api/actionLog";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "ActionLog",
  data() {
    return {
      list: null,
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      total: 0,
      selectRows: "",
      elementLoadingText: this.$t("user.loading"),
      queryForm: {
        pageNo: 1,
        pageSize: 50,
        username: "",
        model: "",
        action: "",
      },
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    setSelectRows(val) {
      this.selectRows = val;
    },
    handleSizeChange(val) {
      this.queryForm.pageSize = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.queryForm.pageNo = val;
      this.fetchData();
    },
    queryData() {
      this.queryForm.pageNo = 1;
      this.fetchData();
    },
    fetchData() {
      this.listLoading = true;
      getList(this.queryForm).then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.list = data.items;
          this.total = data.totalCount;
          setTimeout((_) => {
            this.listLoading = false;
          }, 300);
        } else {
          this.$baseMessage(this.$t("log.getLogFailed"), "error");
        }
      });
    },
  },
};
</script>
