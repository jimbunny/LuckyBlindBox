<template>
  <div class="product-container">
    <byui-query-form>
      <byui-query-form-left-panel :span="14">
        <el-button icon="el-icon-plus" type="primary" @click="handleEdit"
          >{{ $t("product.add") }}
        </el-button>
        <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
          >{{ $t("product.batchDelete") }}
        </el-button>
        <div class="filter-container" style="margin-left: 10px;">
          <el-checkbox-group v-model="checkboxVal">
            <el-checkbox label="level">
              {{ $t("product.level") }}
            </el-checkbox>
            <el-checkbox label="rank">
              {{ $t("product.rank") }}
            </el-checkbox>
            <el-checkbox label="remark">
              {{ $t("product.remark") }}
            </el-checkbox>
            <el-checkbox label="update_user">
              {{ $t("product.updateUser") }}
            </el-checkbox>
            <el-checkbox label="create_time">
              {{ $t("product.create_time") }}
            </el-checkbox>
          </el-checkbox-group>
        </div>
      </byui-query-form-left-panel>
      <byui-query-form-right-panel :span="10">
        <el-form :inline="true" :model="queryForm" @submit.native.prevent>
          <el-form-item>
            <el-input
              v-model.trim="queryForm.no"
              :placeholder="$t('product.noTip')"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-select
              v-model="queryForm.Pclass"
              :placeholder="$t('product.classTip')"
              style="width: 100%;"
            >
              <el-option :label="$t('product.coat')" value="coat"> </el-option>
              <el-option :label="$t('product.pants')" value="pants">
              </el-option>
              <el-option :label="$t('product.skirt')" value="skirt">
              </el-option>
            </el-select>
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
      :key="key"
      v-loading="listLoading"
      :data="list"
      :element-loading-text="elementLoadingText"
      border
      fit
      highlight-current-row
      @selection-change="setSelectRows"
    >
      <el-table-column type="selection"></el-table-column>
      <el-table-column prop="id" :label="$t('product.id')"></el-table-column>
      <el-table-column prop="no" :label="$t('product.no')"></el-table-column>
      <el-table-column
        prop="name"
        :label="$t('product.name')"
      ></el-table-column>
      <el-table-column prop="cover_img" :label="$t('product.cover_img')">
        <template slot-scope="scope">
          <el-popover placement="right" width="120" trigger="hover">
            <div class="demo-image__preview">
              <el-image
                v-for="item in scope.row.cover_img"
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
      <el-table-column prop="detail_img" :label="$t('product.detail_img')">
        <template slot-scope="scope">
          <el-popover placement="right" width="480" trigger="hover">
            <div class="demo-image__preview">
              <el-image
                v-for="item in scope.row.detail_img"
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
        prop="description_img"
        :label="$t('product.description_img')"
      >
        <template slot-scope="scope">
          <el-popover placement="right" width="120" trigger="hover">
            <div class="demo-image__preview">
              <el-image
                v-for="item in scope.row.description_img"
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
        prop="position"
        :label="$t('product.position')"
      ></el-table-column>
      <el-table-column
        prop="package_list"
        :label="$t('product.package_list')"
      ></el-table-column>
      <el-table-column prop="status" :label="$t('product.status')">
        <template slot-scope="scope">
          <p v-if="scope.row['status'] == 'unsold'" style="color: #67c23a;">
            {{ scope.row["status"] }}
          </p>
          <p v-else style="color: #f56c6c;">{{ scope.row["status"] }}</p>
        </template>
      </el-table-column>
      <el-table-column
        prop="in_price"
        :label="$t('product.inPrice')"
      ></el-table-column>
      <el-table-column
        prop="out_price"
        :label="$t('product.outPrice')"
      ></el-table-column>
      <el-table-column
        prop="count"
        :label="$t('product.count')"
      ></el-table-column>
      <!--<el-table-column
        prop="level"
        :label="$t('product.level')"
      ></el-table-column>
      <el-table-column
        prop="rank"
        :label="$t('product.rank')"
      ></el-table-column> 
      <el-table-column
        prop="remark"
        :label="$t('product.remark')"
      ></el-table-column>-->
      <el-table-column
        v-for="c in formThead"
        :key="c"
        :label="$t('product.' + c)"
      >
        <template slot-scope="scope">
          {{ scope.row[c] }}
        </template>
      </el-table-column>

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
import { getList, doDelete } from "@/api/product";
import Edit from "./components/ProductEdit";
import { okCode, errorCode } from "@/config/settings";
import { mapGetters } from "vuex";

export default {
  name: "Product",
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
        classification: "",
      },
      key: 1, // table key
      formTheadOptions: [
        "level",
        "rank",
        "remark",
        "update_user",
        "create_time",
      ],
      checkboxVal: [],
      formThead: [],
    };
  },
  created() {
    this.fetchData();
  },
  computed: {
    ...mapGetters({
      userName: "user/userName",
    }),
  },
  watch: {
    checkboxVal(valArr) {
      this.formThead = this.formTheadOptions.filter(
        (i) => valArr.indexOf(i) >= 0
      );
      this.key = this.key + 1; // 为了保证table 每次都会重渲 In order to ensure the table will be re-rendered each time
    },
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
