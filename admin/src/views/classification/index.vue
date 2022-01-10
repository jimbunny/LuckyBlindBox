<template>
  <div class="classification-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <byui-query-form>
          <byui-query-form-left-panel :span="12">
            <el-button icon="el-icon-plus" type="primary" @click="handleEdit"
              >{{ $t("role.add") }}
            </el-button>
            <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
              >{{ $t("role.batchDelete") }}
            </el-button>
          </byui-query-form-left-panel>
          <byui-query-form-right-panel :span="12">
            <el-form :inline="true" :model="queryForm" @submit.native.prevent>
              <el-form-item>
                <el-input
                  v-model.trim="queryForm.name"
                  :placeholder="$t('classification.nameTip')"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button
                  icon="el-icon-search"
                  type="primary"
                  @click="queryData"
                  >{{ $t("role.search") }}
                </el-button>
              </el-form-item>
            </el-form>
          </byui-query-form-right-panel>
        </byui-query-form>
        <el-table
          v-loading="listLoading"
          :data="list"
          :element-loading-text="elementLoadingText"
          highlight-current-row
          @selection-change="setSelectRows"
          @current-change="handleSignleChange"
        >
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="id" :label="$t('role.id')"></el-table-column>
          <el-table-column
            prop="name"
            :label="$t('classification.name')"
          ></el-table-column>
          <el-table-column
            prop="rank"
            :label="$t('classification.rank')"
          ></el-table-column>
          <el-table-column
            prop="create_time"
            :label="$t('classification.create_time')"
          ></el-table-column>
          <el-table-column fixed="right" :label="$t('role.action')" width="200">
            <template v-slot="scope">
              <el-button type="text" @click="handleEdit(scope.row)"
                >{{ $t("role.edit") }}
              </el-button>
              <el-button type="text" @click="handleDelete(scope.row)"
                >{{ $t("role.delete") }}
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
          node-key="name"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </el-col>
    </el-row>
    <edit ref="edit" @fetchData="fetchData"></edit>
  </div>
</template>

<script>
import { getList, doDelete } from "@/api/classification";
import Edit from "./components/ClassificationEdit";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "Classification",
  components: { Edit },
  data() {
    return {
      list: null,
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      total: 0,
      selectRows: "",
      elementLoadingText: this.$t("role.loading"),
      queryForm: {
        pageNo: 1,
        pageSize: 10,
        name: "",
      },
      data: [],
      filterText: "",
      defaultProps: {
        children: "children",
        label: "path",
      },
      currentRow: null,
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },
  async created() {
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
          this.$t("user.deleteTip1") + row.id + this.$t("user.deleteTip2"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          () => {
            doDelete({ ids: [row.id] }).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("classification.deleteClassificationSuccessful"),
                  "success"
                );
                this.fetchData();
              } else {
                this.$baseMessage(
                  this.$t("classification.deleteClassificationFailed"),
                  "error"
                );
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
                    this.$t("classification.deleteClassificationSuccessful"),
                    "success"
                  );
                  this.fetchData();
                } else {
                  this.$baseMessage(
                    this.$t("classification.deleteClassificationFailed"),
                    "error"
                  );
                }
              });
            }
          );
        } else {
          this.$baseMessage(this.$t("role.deleteTip4"), "error");
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
          this.$baseMessage(
            this.$t("classification.getClassificationFailed"),
            "error"
          );
        }
      });
    },
  },
};
</script>
