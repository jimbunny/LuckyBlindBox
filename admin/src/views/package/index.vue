<template>
  <div class="package-container">
    <byui-query-form>
      <byui-query-form-left-panel :span="12">
        <el-button icon="el-icon-plus" type="primary" @click="handleEdit"
          >{{ $t("product.add") }}
        </el-button>
        <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
          >{{ $t("product.batchDelete") }}
        </el-button>
        <div class="filter-container" style="margin-left: 10px;">
          <el-checkbox-group v-model="checkboxVal">
            <el-checkbox label="type">
              {{ $t("product.type") }}
            </el-checkbox>
            <el-checkbox label="updateUser">
              {{ $t("product.updateUser") }}
            </el-checkbox>
            <el-checkbox label="updateTime">
              {{ $t("product.updateTime") }}
            </el-checkbox>
          </el-checkbox-group>
        </div>
      </byui-query-form-left-panel>
      <byui-query-form-right-panel :span="12">
        <el-form :inline="true" :model="queryForm" @submit.native.prevent>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.name"
              :placeholder="$t('package.nameTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.Pclass"
              :placeholder="$t('product.classTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-search" type="primary" @click="queryData"
              >{{ $t("product.search") }}
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
      <el-table-column prop="id" :label="$t('product.id')"></el-table-column>
      <el-table-column prop="no" :label="$t('product.no')"></el-table-column>
      <el-table-column
        prop="name"
        :label="$t('package.name')"
      ></el-table-column>
      <el-table-column prop="picture" :label="$t('product.picture')">
        <template slot-scope="scope">
          <el-popover placement="right" width="120" trigger="hover">
            <div class="demo-image__preview">
              <el-image
                v-for="item in scope.row.picture"
                :key="item.name"
                style="width: 100px; height: 100px; margin: 5px 5px 5px 5px;"
                :src="item.url"
                :preview-src-list="[item.url]"
              >
              </el-image>
            </div>
            <el-button slot="reference" type="text">{{
              $t("product.view")
            }}</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="description" :label="$t('package.description')">
        <template slot-scope="scope">
          <el-popover placement="right" width="480" trigger="hover">
            <div class="demo-image__preview">
              <el-image
                v-for="item in scope.row.description"
                :key="item.name"
                style="width: 100px; height: 100px; margin: 5px 5px 5px 5px;"
                :src="item.url"
                :preview-src-list="[item.url]"
              >
              </el-image>
            </div>
            <el-button slot="reference" type="text">{{
              $t("product.view")
            }}</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        prop="point"
        :label="$t('package.point')"
      ></el-table-column>
      <!-- <el-table-column prop="type" :label="$t('product.type')"></el-table-column> -->
      <el-table-column
        prop="gender"
        :label="$t('product.gender')"
      ></el-table-column>
      <el-table-column
        prop="size"
        :label="$t('product.size')"
      ></el-table-column>
      <el-table-column prop="age" :label="$t('product.age')"></el-table-column>
      <el-table-column
        prop="Pclass"
        :label="$t('product.class')"
      ></el-table-column>

      <el-table-column
        prop="count"
        :label="$t('package.count')"
      ></el-table-column>
      <!-- <el-table-column prop="price" :label="$t('package.price')"></el-table-column>
      <el-table-column prop="total" :label="$t('package.total')"></el-table-column> -->
      <el-table-column
        prop="remark"
        :label="$t('product.remark')"
      ></el-table-column>
      <el-table-column
        v-for="c in formThead"
        :key="c"
        :label="$t('product.' + c)"
      >
        <template slot-scope="scope">
          {{ scope.row[c] }}
        </template>
      </el-table-column>
      <!-- <el-table-column prop="updateUser" :label="$t('product.updateUser')"></el-table-column>
      <el-table-column prop="updateTime" :label="$t('product.updateTime')"></el-table-column> -->

      <el-table-column fixed="right" :label="$t('user.action')" width="180">
        <template v-slot="scope">
          <el-button
            type="text"
            style="color: #e6a23c;"
            @click="handleEdit(scope.row)"
            >{{ $t("product.edit") }}
          </el-button>
          <el-button
            type="text"
            style="color: #f56c6c;"
            @click="handleDelete(scope.row)"
            >{{ $t("product.delete") }}
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
import Edit from "./components/PackageEdit";
import { okCode, errorCode } from "@/config/settings";
import { getList } from "@/api/package";

export default {
  name: "Package",
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
        name: "",
        _type: "",
      },
      key: 1, // table key
      formTheadOptions: ["type", "updateUser", "updateTime"],
      checkboxVal: [],
      formThead: [],
    };
  },
  watch: {
    checkboxVal(valArr) {
      this.formThead = this.formTheadOptions.filter(
        (i) => valArr.indexOf(i) >= 0
      );
      this.key = this.key + 1; // 为了保证table 每次都会重渲 In order to ensure the table will be re-rendered each time
    },
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
          this.$t("user.deleteTip1") + row.name + this.$t("user.deleteTip2"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          () => {
            doDelete({
              ids: [row.id],
              updateUser: this.userName,
              content: row,
            }).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("package.deletePackageSuccessful"),
                  "success"
                );
                this.fetchData();
              } else {
                this.$baseMessage(
                  this.$t("package.deletePackageFailed"),
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
              doDelete({
                ids: ids,
                updateUser: this.userName,
                content: this.selectRows,
              }).then((res) => {
                const { code, msg, data } = res;
                if (code === okCode) {
                  this.$baseMessage(
                    this.$t("package.deletePackageSuccessful"),
                    "success"
                  );
                  this.fetchData();
                } else {
                  this.$baseMessage(
                    this.$t("package.deletePackageFailed"),
                    "error"
                  );
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
      if (this.queryForm.Pclass) {
        this.queryForm.Pclass = [this.queryForm.Pclass];
      }
      getList(this.queryForm).then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.list = data.items;
          this.total = data.totalCount;
          setTimeout((_) => {
            this.listLoading = false;
          }, 300);
        } else {
          this.$baseMessage(this.$t("package.getPackageFailed"), "error");
        }
      });
    },
  },
};
</script>
