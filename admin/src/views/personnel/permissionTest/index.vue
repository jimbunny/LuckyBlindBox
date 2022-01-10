<template>
  <div class="permission-container">
    <el-form ref="form" :model="form" :inline="true">
      <el-form-item label="当前账号拥有的权限">
        {{ JSON.stringify(permissions) }}
      </el-form-item>
    </el-form>
    <br />
    <el-row :gutter="15">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-table
          :data="tableData"
          row-key="path"
          border
          default-expand-all
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        >
          <el-table-column prop="name" label="name"></el-table-column>
          <el-table-column prop="path" label="path"></el-table-column>
          <el-table-column prop="component" label="component"></el-table-column>
          <el-table-column prop="redirect" label="redirect"></el-table-column>
          <el-table-column prop="meta.title" label="标题"></el-table-column>
          <el-table-column label="图标">
            <template slot-scope="scope">
              <span v-if="scope.row.meta">
                <byui-icon
                  v-if="scope.row.meta.icon"
                  :icon="['fas', scope.row.meta.icon]"
                ></byui-icon>
              </span>
            </template>
          </el-table-column>
          <el-table-column label="是否固定">
            <template slot-scope="scope">
              <span v-if="scope.row.meta">
                {{ scope.row.meta.affix }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="是否无缓存">
            <template slot-scope="scope">
              <span v-if="scope.row.meta">
                {{ scope.row.meta.noKeepAlive }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <json-editor :value="res"></json-editor>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import checkPermission from "@/utils/permission";
import { mapGetters } from "vuex";
import { tokenTableName } from "@/config/settings";
import { getRouterList } from "@/api/router";
import JsonEditor from "@/components/JsonEditor";

export default {
  name: "Permission",
  components: {
    JsonEditor,
  },
  data() {
    return {
      form: {
        permission: "",
      },
      tableData: [],
      res: [],
    };
  },
  computed: {
    ...mapGetters({
      userName: "user/userName",
      permissions: "user/permissions",
    }),
  },
  created() {
    this.fetchData();
  },
  mounted() {
    this.form.permission = this.userName;
  },
  methods: {
    handleChangePermission() {
      localStorage.setItem(
        tokenTableName,
        `${this.form.permission}-accessToken`
      );
      location.reload();
    },
    fetchData() {
      getRouterList().then((res) => {
        this.tableData = res.data;
        this.res = res;
      });
    },
    checkPermission,
  },
};
</script>
