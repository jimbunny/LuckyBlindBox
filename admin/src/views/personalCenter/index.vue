<template>
  <div class="personalCenter-container">
    <el-row :gutter="12">
      <el-col :xs="24" :sm="24" :md="8" :lg="6" :xl="6">
        <el-card shadow="always">
          <div class="personal-center-user-info">
            <el-avatar
              class="user-avatar"
              style="height: 100px; width: 100px; line-height: 100px;"
              :src="require('@/assets/user.gif')"
            ></el-avatar>
            <div class="personal-center-user-info-full-name">
              {{ form.username }}
            </div>
            <div class="personal-center-user-info-description">
              {{ form.email }}
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="18" :xl="18">
        <el-tabs :tab-position="tabPosition">
          <el-tab-pane :label="$t('personalCenter.profile')">
            <el-row :gutter="12">
              <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-form
                  ref="ruleForm"
                  :model="form"
                  :rules="editRules"
                  label-width="150px"
                >
                  <el-form-item
                    :label="$t('personalCenter.username')"
                    prop="username"
                  >
                    <el-input
                      v-model.trim="form.username"
                      autocomplete="off"
                      disabled
                    ></el-input>
                  </el-form-item>
                  <el-form-item
                    :label="$t('personalCenter.newPassword')"
                    prop="password"
                  >
                    <el-input
                      v-model.trim="form.password"
                      type="password"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item
                    :label="$t('personalCenter.confirmPassword')"
                    prop="confirmPassword"
                  >
                    <el-input
                      v-model.trim="form.confirmPassword"
                      type="password"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item
                    :label="$t('personalCenter.email')"
                    prop="email"
                  >
                    <el-input
                      v-model.trim="form.email"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">{{
                      $t("personalCenter.update")
                    }}</el-button>
                    <el-button @click="resetForm('ruleForm')">{{
                      $t("personalCenter.reset")
                    }}</el-button>
                  </el-form-item>
                </el-form>
              </el-col>
            </el-row>
          </el-tab-pane>
          <!-- <el-tab-pane label="基本设置">基本设置</el-tab-pane>
          <el-tab-pane label="安全设置">安全设置</el-tab-pane>
          <el-tab-pane label="账户绑定">安全设置</el-tab-pane> -->
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { getInfo, doEditUser } from "@/api/user";
import { okCode, errorCode } from "@/config/settings";
import { isPassword } from "@/utils/validate";

export default {
  name: "PersonalCenter",
  data() {
    const validateUserName = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("personalCenter.usernameEmptyTip")));
      } else {
        callback();
      }
    };
    const validateEditPassword = (rule, value, callback) => {
      if (value && !isPassword(value)) {
        callback(new Error(this.$t("personalCenter.passowrdLengthTip")));
      } else {
        if (this.form.confirmPassword !== "") {
          this.$refs.ruleForm.validateField("confirmPassword");
        }
        callback();
      }
    };
    const validateEditConfirmPassword = (rule, value, callback) => {
      if (value && !isPassword(value)) {
        callback(new Error(this.$t("personalCenter.confirmPasswordLengthTip")));
      } else {
        if (value !== this.form.password) {
          callback(
            new Error(this.$t("personalCenter.confirmPassworddifferentTip"))
          );
        }
        callback();
      }
    };
    const validateEmail = (rule, value, callback) => {
      if (value === "") {
        callback(new Error(this.$t("personalCenter.emailEmpty")));
      } else {
        if (value !== "") {
          var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
          if (!reg.test(value)) {
            callback(new Error(this.$t("personalCenter.emailVerification")));
          }
        }
        callback();
      }
    };
    return {
      form: {
        id: "",
        username: "",
        password: "",
        confirmPassword: "",
        email: "",
      },
      tabPosition: "top",
      editRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUserName },
        ],
        password: [{ trigger: "blur", validator: validateEditPassword }],
        confirmPassword: [
          { trigger: "blur", validator: validateEditConfirmPassword },
        ],
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
      },
    };
  },
  computed: {
    ...mapGetters({
      userName: "user/userName",
      email: "user/email",
    }),
  },
  created() {
    getInfo().then((res) => {
      const { code, msg, data } = res;
      if (code === okCode) {
        this.form = data;
      } else {
        // this.$baseMessage(msg || `获取用户信息失败！`, "error");
        this.$baseMessage(this.$t("personalCenter.getUserInfoFailed"), "error");
      }
    });
  },
  methods: {
    resetForm(formName) {
      // this.$refs[formName].resetFields();
      this.form.username = this.userName;
      this.form.email = this.email;
      this.form.password = "";
      this.form.confirmPassword = "";
    },
    async submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          doEditUser(this.form).then((res) => {
            const { code, msg, data } = res;
            if (code === okCode) {
              if (this.form.password) {
                this.$baseMessage(
                  this.$t("personalCenter.editUserInfoSuccessful"),
                  "success"
                );
                setTimeout((_) => {
                  const fullPath = this.$route.fullPath;
                  this.$store.dispatch("user/logout").then(() => {
                    this.$router.push(`/login?redirect=${fullPath}`);
                  });
                }, 1000);
              } else {
                this.$baseMessage(
                  this.$t("personalCenter.editEmailSuccessful"),
                  "success"
                );
              }
            } else {
              this.$baseMessage(
                this.$t("personalCenter.editUserInfoFailed"),
                "error"
              );
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.personal-center-user-info {
  padding: 20px;
  text-align: center;
}
.personal-center-user-info-full-name {
  margin-top: 15px;
  font-size: 24px;
  font-weight: 500;
  color: #262626;
}
.personal-center-user-info-description {
  margin-top: 8px;
}
.personal-center-user-info-follow {
  margin-top: 15px;
}
</style>
