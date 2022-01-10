<template>
  <div class="permission-container">
    <el-row :gutter="15">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Router</span>
            <el-button
              style="float: right; padding: 3px 0;"
              type="text"
              @click="handleChangeRouter()"
              >Update</el-button
            >
          </div>
          <div class="text item">
            <json-editor ref="router" :value="router"></json-editor>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-input
          v-model="filterText"
          placeholder="Please enter Keyword to filter"
        >
        </el-input>
        <div class="block">
          <el-tree
            ref="tree"
            class="filter-tree"
            :data="router"
            :props="defaultProps"
            node-key="path"
            default-expand-all
            :expand-on-click-node="false"
            :filter-node-method="filterNode"
          >
            // eslint-disable-next-line vue/no-template-shadow
            <span slot-scope="{ node, data }" class="custom-tree-node">
              <!-- <span>{{ generateTitle(data.label) }}</span> -->
              <span v-if="!data.meta">{{ data.path }}</span>
              <span v-else>{{ generateTitle(data.meta.title) }}</span>
            </span>
          </el-tree>
        </div>
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
import { updateRouter } from "@/api/router";
import { okCode, errorCode } from "@/config/settings";
import { generateTitle } from "@/utils/i18n";

export default {
  name: "Router",
  components: {
    JsonEditor,
  },
  data() {
    return {
      router: [],
      filterText: "",
      defaultProps: {
        children: "children",
        label: "path",
      },
    };
  },
  computed: {},
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },
  created() {
    this.fetchData();
  },
  mounted() {},
  methods: {
    generateTitle,
    handleChangeRouter() {
      updateRouter({ router: JSON.parse(this.$refs.router.getValue()) }).then(
        (res) => {
          if (res.code === okCode) {
            this.router = res.data;
            this.$baseMessage("update Router successful!", "success");
          } else {
            this.$baseMessage(`update Router failed`, "error");
          }
        }
      );
      location.reload();
    },
    fetchData() {
      getRouterList({ permission: "admin" }).then((res) => {
        this.router = res.data;
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
