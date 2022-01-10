<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="500px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="140px">
      <el-form-item :label="$t('role.description')" prop="description">
        <el-input v-model="form.description" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item :label="$t('role.permission')" prop="permission">
        <el-input
          v-model="form.permission"
          autocomplete="off"
          :disabled="status != 'add'"
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
import { doAdd, doEdit, checkPermission } from "@/api/role";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "RoleEdit",
  data() {
    var validatePermission = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("role.permissionTip1")));
      }
      if (this.status == "add") {
        checkPermission({ permission: value }).then((res) => {
          const { code, msg, data } = res;
          if (code === okCode) {
            if (data.status) {
              return callback(new Error(this.$t("role.permissionTip2")));
            } else {
              callback();
            }
          } else {
            return callback(new Error(this.$t("role.permissionTip3")));
          }
        });
      } else {
        callback();
      }
    };
    return {
      form: {
        id: "",
        description: "",
        permission: "",
      },
      rules: {
        permission: [
          {
            validator: validatePermission,
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
                  this.$t("role.addPermissionSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(this.$t("role.addPermissionFailed"), "error");
              }
            });
          } else {
            doEdit(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("role.editPermissionSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(
                  this.$t("role.editPermissionFailed"),
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
