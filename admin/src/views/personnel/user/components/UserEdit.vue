<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="500px"
    @close="close"
  >
    <el-form
      ref="form"
      :model="form"
      :rules="status === 'add' ? addRules : editRules"
      label-width="140px"
    >
      <el-form-item :label="$t('user.username')" prop="username">
        <el-input
          v-model.trim="form.username"
          autocomplete="off"
          :disabled="status === 'edit'"
        ></el-input>
      </el-form-item>
      <el-form-item :label="$t('user.password')" prop="password">
        <el-input
          v-model.trim="form.password"
          type="password"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item :label="$t('user.email')" prop="email">
        <el-input v-model.trim="form.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item :label="$t('user.permission')" prop="permission">
        <!-- <el-checkbox-group v-model="form.permission">
          <el-checkbox label="superAdmin" v></el-checkbox>
          <el-checkbox label="admin"></el-checkbox>
          <el-checkbox label="guest"></el-checkbox>
          <el-checkbox label="user"></el-checkbox>
          <el-checkbox label="test"></el-checkbox>
        </el-checkbox-group> -->
        <el-select
          v-model="form.permission"
          filterable
          :placeholder="$t('user.permissionTip')"
          style="width: 100%;"
        >
          <el-option
            v-for="item in list"
            :key="item.permission"
            :label="item.permission"
            :value="item.permission"
          >
            <span style="float: left;">{{ item.permission }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px;">{{
              item.description
            }}</span>
          </el-option>
        </el-select>
        <!--  <el-radio v-model="form.permission" label="superAdmin"
          >超级管理员</el-radio
        >
        <el-radio v-model="form.permission" label="admin">管理员</el-radio>
        <el-radio v-model="form.permission" label="guest">游客</el-radio> 
        <el-radio v-model="form.permission" label="test">普通用户</el-radio> -->
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">{{ $t("user.close") }}</el-button>
      <el-button type="primary" @click="save">{{ $t("user.save") }}</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { isPassword } from "@/utils/validate";
import { doEdit, doAdd } from "@/api/user";
import { okCode, errorCode } from "@/config/settings";
import { getList } from "@/api/role";
export default {
  name: "UserEdit",
  data() {
    const validateUserName = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("user.usernameEmptyTip")));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (!isPassword(value)) {
        callback(new Error(this.$t("user.passowrdLengthTip")));
      } else {
        callback();
      }
    };
    const validateEditPassword = (rule, value, callback) => {
      if (value && !isPassword(value)) {
        callback(new Error(this.$t("user.passowrdLengthTip")));
      } else {
        callback();
      }
    };
    const validateEmail = (rule, value, callback) => {
      if (value === "") {
        callback(new Error(this.$t("user.emailEmpty")));
      } else {
        if (value !== "") {
          var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
          if (!reg.test(value)) {
            callback(new Error(this.$t("user.emailVerification")));
          }
        }
        callback();
      }
    };
    const validatePermission = (rule, value, callback) => {
      if (value === "") {
        callback(new Error(this.$t("user.permissionTip")));
      } else {
        callback();
      }
    };
    return {
      form: {
        username: "",
        password: "12345678",
        email: "",
        permission: "",
      },
      addRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUserName },
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword },
        ],
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
        permission: [
          {
            required: true,
            trigger: "blur",
            validator: validatePermission,
          },
        ],
      },
      editRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUserName },
        ],
        password: [{ trigger: "blur", validator: validateEditPassword }],
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
        permission: [
          {
            required: true,
            trigger: "blur",
            validator: validatePermission,
          },
        ],
      },
      title: "",
      status: "",
      dialogFormVisible: false,
      list: [],
    };
  },
  created() {
    getList({
      pageNo: 1,
      pageSize: 100000,
      description: "",
    }).then((res) => {
      const { code, msg, data } = res;
      if (code === okCode) {
        this.list = data.items;
      } else {
        this.$baseMessage(this.$t("user.getPermissionFailed"), "error");
      }
    });
  },
  methods: {
    showEdit(row) {
      if (!row) {
        this.title = this.$t("user.add");
        this.status = "add";
      } else {
        this.title = this.$t("user.edit");
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
          // if (this.title === "添加") {
          if (this.status === "add") {
            doAdd(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(this.$t("user.addUserSuccessful"), "success");
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(this.$t("user.addUserFailed"), "error");
              }
            });
          } else {
            doEdit(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("user.editUserSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(this.$t("user.editUserFailed"), "error");
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
