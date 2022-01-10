<template>
  <div class="permission-container">
    <el-row :gutter="15">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Chinese</span>
            <el-button
              style="float: right; padding: 3px 0;"
              type="text"
              @click="handleChangeLanguage('zh')"
              >Update</el-button
            >
          </div>
          <div class="text item">
            <json-editor ref="zh" :value="zh"></json-editor>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Thai</span>
            <el-button
              style="float: right; padding: 3px 0;"
              type="text"
              @click="handleChangeLanguage('thai')"
              >Update</el-button
            >
          </div>
          <div class="text item">
            <json-editor ref="thai" :value="thai"></json-editor>
          </div>
        </el-card>
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
import { getLanguage, updateLanguageFile } from "@/api/language"; // 封装好的国际化的接口
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "Language",
  components: {
    JsonEditor,
  },
  data() {
    return {
      zh: {},
      thai: {},
    };
  },
  computed: {},
  created() {
    getLanguage({
      // 进行请求
      language: "zh", // 请求参数
    }).then((res) => {
      if (res.code == okCode) {
        this.zh = res.data;
      } else {
        console.log(res.message);
      }
    });
    getLanguage({
      // 进行请求
      language: "thai", // 请求参数
    }).then((res) => {
      if (res.code == okCode) {
        this.thai = res.data;
      } else {
        console.log(res.message);
      }
    });
  },
  mounted() {},
  methods: {
    handleChangeLanguage(language) {
      if (language == "thai") {
        updateLanguageFile({
          // 进行请求
          type: "thai", // 请求参数
          language: JSON.parse(this.$refs.thai.getValue()),
        }).then((res) => {
          if (res.code == okCode) {
            this.thai = res.data;
            this.$baseMessage("update Thai successful!", "success");
          } else {
            this.$baseMessage("update Thai failed!", "error");
            console.log(res.message);
          }
        });
      } else {
        updateLanguageFile({
          // 进行请求
          type: "zh", // 请求参数
          language: JSON.parse(this.$refs.zh.getValue()),
        }).then((res) => {
          if (res.code == okCode) {
            this.zh = res.data;
            this.$baseMessage("update Chinese successful!", "success");
          } else {
            this.$baseMessage("update Chinese successful!", "error");
            console.log(res.message);
          }
        });
      }
    },
  },
};
</script>
