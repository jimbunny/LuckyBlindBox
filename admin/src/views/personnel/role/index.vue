<template>
  <div class="role-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
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
                  v-model.trim="queryForm.description"
                  :placeholder="$t('role.descriptionTip')"
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
          <!-- @current-change="handleSignleChange" -->
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="id" :label="$t('role.id')"></el-table-column>
          <!--<el-table-column prop="department" label="部门"></el-table-column>
          <el-table-column prop="departmentID" label="部门ID"></el-table-column>
          <el-table-column prop="postion" label="职位"></el-table-column>
          <el-table-column prop="postionID" label="职位ID"></el-table-column> -->
          <el-table-column
            prop="permission"
            :label="$t('role.permission')"
          ></el-table-column>
          <el-table-column
            prop="description"
            :label="$t('role.description')"
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
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <byui-query-form style="margin-top: 5px;">
          <byui-query-form-left-panel :span="16">
            <el-input v-model="filterText" :placeholder="$t('role.filterText')">
            </el-input>
          </byui-query-form-left-panel>
          <byui-query-form-right-panel :span="8">
            <el-button
              icon="el-icon-edit"
              type="primary"
              @click="updatePermissionMenu"
              >{{ $t("role.update") }}
            </el-button>
          </byui-query-form-right-panel>
        </byui-query-form>
        <div class="block">
          <el-tree
            ref="tree"
            :data="data"
            show-checkbox
            node-key="name"
            default-expand-all
            :props="defaultProps"
            :filter-node-method="filterNode"
          >
            <span slot-scope="{ node, data }" class="custom-tree-node">
              <template>
                <!--<byui-icon :icon="['fas', data.meta.icon]" /> -->
                <span v-if="!data.meta">{{ data.path }}</span>
                <span v-else>{{ generateTitle(data.meta.title) }}</span>
              </template>
            </span>
          </el-tree>
        </div>
      </el-col>
    </el-row>
    <edit ref="edit" @fetchData="fetchData"></edit>
  </div>
</template>

<script>
import { getList, doDelete } from "@/api/role";
import Edit from "./components/RoleEdit";
import { okCode, errorCode } from "@/config/settings";
import { getRouterList } from "@/api/router";
import { generateTitle } from "@/utils/i18n";
import { getCheckedMenu, doPermissionEdit } from "@/api/menu";

export default {
  name: "Role",
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
        description: "",
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
    const res = await getRouterList({ permission: "admin" });
    const { code, msg, data } = res;
    if (code === okCode) {
      this.data = data;
    } else {
      this.$baseMessage(this.$t("role.getMenuFailed"), "error");
    }
    this.fetchData();
  },
  methods: {
    generateTitle,
    updatePermissionMenu() {
      if (this.currentRow == null) {
        this.$baseMessage(this.$t("role.getMenuFailed"), "error");
        return;
      }
      doPermissionEdit({
        permission: this.currentRow.permission,
        names: this.$refs.tree.getCheckedKeys(),
      }).then((res) => {
        if (res.code === okCode) {
          this.$baseMessage(
            this.$t("role.editPermissionMenuSuccessful"),
            "success"
          );
        } else {
          this.$baseMessage(this.$t("role.editPermissionMenuFailed"), "error");
        }
      });
    },
    handleSignleChange(val) {
      if (val) {
        this.currentRow = val;
        getCheckedMenu({ permission: val.permission }).then((res) => {
          if (res.code === okCode) {
            this.$refs.tree.setCheckedKeys(res.data);
          } else {
            this.$baseMessage(this.$t("role.getPermissionMenuFailed"), "error");
          }
        });
      }
    },
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
          this.$t("role.deleteTip1") +
            row.permission +
            this.$t("role.deleteTip2"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          () => {
            doDelete({ ids: [row.id] }).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("role.deleteRoleSuccessful"),
                  "success"
                );
                this.fetchData();
              } else {
                this.$baseMessage(this.$t("role.deleteRoleFailed"), "error");
              }
            });
          }
        );
      } else {
        if (this.selectRows.length > 0) {
          const ids = [];
          this.selectRows.map((item) => ids.push(item.id));
          // const ids = this.selectRows.map((item) => item.id).join();
          this.$baseConfirm(
            this.$t("role.deleteTip3"),
            this.$t("header.tips"),
            this.$t("header.confirm"),
            this.$t("header.cancel"),
            () => {
              doDelete({ ids: ids }).then((res) => {
                const { code, msg, data } = res;
                if (code === okCode) {
                  this.$baseMessage(
                    this.$t("role.deleteRoleSuccessful"),
                    "success"
                  );
                  this.fetchData();
                } else {
                  this.$baseMessage(this.$t("role.deleteRoleFailed"), "error");
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
          this.$baseMessage(this.$t("role.getPermissionFailed"), "error");
        }
      });
    },
    filterNode(value, data) {
      if (!value) return true;
      if (data.meta) {
        return this.generateTitle(data.meta.title).indexOf(value) !== -1;
      } else {
        return true;
      }
      // generateTitle(data.meta.title)
      // return generateTitle(data.meta).indexOf(value) !== -1;
    },
  },
};
</script>
