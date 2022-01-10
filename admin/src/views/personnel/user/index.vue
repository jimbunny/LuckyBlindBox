<template>
  <div class="user-container">
    <byui-query-form>
      <byui-query-form-left-panel :span="12">
        <el-button icon="el-icon-plus" type="primary" @click="handleEdit"
          >{{ $t("user.add") }}
        </el-button>
        <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
          >{{ $t("user.batchDelete") }}
        </el-button>
      </byui-query-form-left-panel>
      <byui-query-form-right-panel :span="12">
        <el-form :inline="true" :model="queryForm" @submit.native.prevent>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.username"
              :placeholder="$t('user.usernameTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-search" type="primary" @click="queryData"
              >{{ $t("user.search") }}
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
      <el-table-column type="selection"></el-table-column>
      <el-table-column prop="id" :label="$t('user.id')"></el-table-column>
      <el-table-column
        prop="username"
        :label="$t('user.username')"
      ></el-table-column>
      <el-table-column prop="email" :label="$t('user.email')"></el-table-column>

      <el-table-column :label="$t('user.permission')">
        <template v-slot="{ row }">
          <!-- <el-tag v-for="(item, index) in row.permissions" :key="index">{{
            item
          }}</el-tag> -->
          <el-tag>{{ row.permission }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column
        prop="login_time"
        :label="$t('user.loginTime')"
      ></el-table-column>
      <el-table-column fixed="right" :label="$t('user.action')" width="200">
        <template v-slot="scope">
          <el-button type="text" @click="handleEdit(scope.row)"
            >{{ $t("user.edit") }}
          </el-button>
          <el-button type="text" @click="handleDelete(scope.row)"
            >{{ $t("user.delete") }}
          </el-button>
        </template>
      </el-table-column>
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
    <edit ref="edit" @fetchData="fetchData"></edit>
  </div>
</template>

<script>
import { getList, doDelete } from "@/api/user";
import Edit from "./components/UserEdit";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "User",
  components: { Edit },
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
        pageSize: 10,
        username: "",
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
    handleEdit(row) {
      if (row.id) {
        this.$refs["edit"].showEdit(row);
      } else {
        this.$refs["edit"].showEdit();
      }
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm(
          this.$t("user.deleteTip1") +
            row.username +
            this.$t("user.deleteTip2"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          () => {
            doDelete({ ids: [row.id] }).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("user.deleteUserSuccessful"),
                  "success"
                );
                // this.$baseMessage(res.msg, "success");
                this.fetchData();
              } else {
                this.$baseMessage(this.$t("user.deleteUserFailed"), "error");
              }
            });
          }
        );
      } else {
        if (this.selectRows.length > 0) {
          const ids = [];
          this.selectRows.map((item) => ids.push(item.id));
          this.$baseConfirm(
            this.$t("user.deleteTip3"),
            this.$t("header.tips"),
            this.$t("header.confirm"),
            this.$t("header.cancel"),
            () => {
              doDelete({ ids: ids }).then((res) => {
                const { code, msg, data } = res;
                if (code === okCode) {
                  this.$baseMessage(
                    this.$t("user.deleteUserSuccessful"),
                    "success"
                  );
                  this.fetchData();
                } else {
                  this.$baseMessage(this.$t("user.deleteUserFailed"), "error");
                }
              });
            }
          );
        } else {
          this.$baseMessage(this.$t("user.deleteTip4"), "error");
          return false;
        }
      }
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
          this.$baseMessage(this.$t("user.getUserFailed"), "error");
        }
      });
    },
  },
};
</script>
