<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="500px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="140px">
      <el-form-item :label="$t('classification.name')" prop="name">
        <el-input v-model="form.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item :label="$t('classification.rank')" prop="rank">
        <el-input
          v-model="form.rank"
          type="number"
          autocomplete="off"
        ></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">{{ $t("role.close") }}</el-button>
      <el-button type="primary" @click="save">{{ $t("role.save") }}</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { doAdd, doEdit, checkName } from "@/api/classification";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "ClassificationEdit",
  data() {
    var validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("classification.nameTip1")));
      }
      checkName({ name: value, status: this.status, id: this.form.id }).then(
        (res) => {
          const { code, msg, data } = res;
          if (code === okCode) {
            if (data.status) {
              return callback(new Error(this.$t("classification.nameTip2")));
            } else {
              callback();
            }
          } else {
            return callback(new Error(this.$t("classification.nameTip3")));
          }
        }
      );
    };

    var validateRank = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("classification.rankTip1")));
      } else {
        callback();
      }
    };
    return {
      form: {
        id: "",
        name: "",
        rank: "",
      },
      rules: {
        name: [
          {
            validator: validateName,
            required: true,
            trigger: "blur",
          },
        ],
        rank: [
          {
            validator: validateRank,
            required: true,
            trigger: "blur",
          },
        ],
      },
      title: "",
      status: "",
      dialogFormVisible: false,
    };
  },
  created() {},
  methods: {
    showEdit(row) {
      if (!row) {
        this.title = this.$t("role.add");
        this.status = "add";
      } else {
        this.title = this.$t("role.edit");
        this.status = "edit";
        this.form = Object.assign({}, row);
      }
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.dialogFormVisible = false;
    },
    save() {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          if (this.status === "add") {
            doAdd(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("classification.addClassificationSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(
                  this.$t("classification.addClassificationFailed"),
                  "error"
                );
              }
            });
          } else {
            doEdit(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("classification.editClassificationSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(
                  this.$t("classification.editClassificationFailed"),
                  "error"
                );
              }
            });
          }
        } else {
          return false;
        }
      });
    },
  },
};
</script>
