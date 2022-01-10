<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="900px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="Rules" label-width="140px">
      <el-row>
        <el-col :span="12">
          <el-form-item :label="$t('package.name')" prop="name">
            <el-input
              v-model.trim="form.name"
              autocomplete="off"
              :disabled="status === 'edit'"
              :placeholder="$t('package.nameTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('package.count')" prop="count">
            <el-input-number
              v-model.trim="form.count"
              autocomplete="off"
              :placeholder="$t('package.countTip')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('package.point')" prop="point">
            <el-input-number
              v-model.trim="form.point"
              autocomplete="off"
              :placeholder="$t('package.pointTip')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item
            :label="$t('product.picture')"
            prop="picture"
            :placeholder="$t('product.pictureTip')"
          >
            <el-upload
              ref="upload"
              action="/api/v1/package/doAdd"
              :class="{ disabled: uploadDisabled }"
              list-type="picture-card"
              :limit="limitcount"
              :on-change="handleChange"
              :on-remove="handleRemove"
              :auto-upload="false"
              :file-list="form.picture"
              multiple
              accept="image/*"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">
                {{ $t("package.pictureTip3") }}
              </div>
            </el-upload>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item :label="$t('package.no')" prop="no">
            <el-input
              v-model.trim="form.no"
              autocomplete="off"
              disabled
              :placeholder="$t('product.noTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('product.gender')" prop="gender">
            <el-select
              v-model="form.gender"
              :placeholder="$t('product.genderTip')"
              style="width: 100%;"
            >
              <el-option :label="$t('product.female')" value="female">
              </el-option>
              <el-option :label="$t('product.male')" value="male"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('product.size')" prop="size">
            <el-select
              v-model="form.size"
              :placeholder="$t('product.sizeTip')"
              style="width: 100%;"
            >
              <el-option label="S" value="S"> </el-option>
              <el-option label="M" value="M"> </el-option>
              <el-option label="L" value="L"> </el-option>
              <el-option label="XL" value="XL"> </el-option>
              <el-option label="XXL" value="XXL"> </el-option>
              <el-option label="XXXL" value="XXXL"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('product.age')" prop="age">
            <el-select
              v-model="form.age"
              :placeholder="$t('product.ageTip')"
              style="width: 100%;"
            >
              <el-option :label="$t('product.youth')" value="youth">
              </el-option>
              <el-option :label="$t('product.elderly')" value="elderly">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('product.class')" prop="Pclass">
            <el-select
              v-model="form.Pclass"
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
          <el-form-item :label="$t('product.type')" prop="type">
            <el-select
              v-model="form.type"
              :placeholder="$t('product.typeTip')"
              disabled
              style="width: 100%;"
            >
              <el-option :label="$t('product.clothes')" value="clothes">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('product.remark')" prop="remark">
            <el-input
              v-model.trim="form.remark"
              autocomplete="off"
              :placeholder="$t('product.remarkTip')"
            ></el-input>
          </el-form-item>
          <!-- <el-form-item :label="$t('package.price')" prop="price">
          <el-input-number v-model.trim="form.price" autocomplete="off" :placeholder="$t('package.priceTip')" style="width:100%" controls-position="right"></el-input-number>
        </el-form-item>
        <el-form-item :label="$t('package.total')" prop="total">
          <el-input-number v-model.trim="form.total" autocomplete="off" :placeholder="$t('package.totalTip')" style="width:100%" controls-position="right"></el-input-number>
        </el-form-item> -->
        </el-col>
        <el-col :span="24">
          <el-form-item
            :label="$t('package.description')"
            prop="description"
            :placeholder="$t('product.pictureTip')"
          >
            <el-upload
              ref="upload2"
              action="/api/v1/product/doAdd"
              :class="{ disabled: uploadDisabled2 }"
              list-type="picture-card"
              :limit="limitcount2"
              :on-change="handleChange2"
              :on-remove="handleRemove2"
              :auto-upload="false"
              :file-list="form.description"
              multiple
              accept="image/*"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">
                {{ $t("package.pictureTip3") }}
              </div>
            </el-upload>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">{{ $t("product.close") }}</el-button>
      <el-button type="primary" @click="save">{{
        $t("product.save")
      }}</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { getList, doEdit, doAdd, checkName, getNo } from "@/api/package";
import { okCode, errorCode } from "@/config/settings";
import { mapGetters } from "vuex";

export default {
  name: "PackageEdit",
  data() {
    const validateName = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("package.nameTip")));
      } else {
        if (this.status === "add") {
          checkName({ name: value }).then((res) => {
            const { code, msg, data } = res;
            if (code === okCode) {
              if (data) {
                callback();
              } else {
                callback(new Error(this.$t("package.getPackageNameTip")));
              }
            } else {
              this.$baseMessage(
                this.$t("package.getPackageNameFailed"),
                "error"
              );
            }
          });
        } else {
          callback();
        }
      }
    };
    const validateGender = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.genderTip")));
      } else {
        callback();
      }
    };
    const validateNo = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.noTip")));
      } else {
        callback();
      }
    };
    const validateSize = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.sizeTip")));
      } else {
        callback();
      }
    };
    const validateAge = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.ageTip")));
      } else {
        callback();
      }
    };
    const validateClass = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.classTip")));
      } else {
        callback();
      }
    };
    const validateType = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.typeTip")));
      } else {
        callback();
      }
    };
    const validateCount = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("package.countTip")));
      } else {
        callback();
      }
    };
    const validatePrice = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("package.priceTip")));
      } else {
        callback();
      }
    };
    const validatePicture = (rule, value, callback) => {
      if ([] == value) {
        callback(new Error(this.$t("package.pictureTip")));
      } else if (value.length < 1) {
        callback(new Error(this.$t("package.pictureTip2")));
      } else {
        callback();
      }
    };
    const validateDescription = (rule, value, callback) => {
      if ([] == value) {
        callback(new Error(this.$t("product.pictureTip")));
      } else if (value.length < 1) {
        callback(new Error(this.$t("product.pictureTip2")));
      } else {
        callback();
      }
    };
    const validateTotal = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("package.totalTip")));
      } else {
        callback();
      }
    };
    const validatePoint = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("package.pointTip")));
      } else {
        callback();
      }
    };
    return {
      form: {
        name: "",
        no: "",
        count: "",
        // price: "",
        // total: "",
        remark: "",
        picture: new Array(),
        description: new Array(),
        point: 0,
        gender: "female",
        size: "M",
        age: "youth",
        Pclass: "coat",
        type: "clothes",
        updateUser: this.userName,
        updateTime: "",
      },
      Rules: {
        name: [{ required: true, trigger: "blur", validator: validateName }],
        no: [{ required: true, trigger: "blur", validator: validateNo }],
        gender: [
          { required: true, trigger: "blur", validator: validateGender },
        ],
        size: [{ required: true, trigger: "blur", validator: validateSize }],
        age: [{ required: true, trigger: "blur", validator: validateAge }],
        Pclass: [{ required: true, trigger: "blur", validator: validateClass }],
        type: [{ required: true, trigger: "blur", validator: validateType }],
        count: [{ required: true, trigger: "blur", validator: validateCount }],
        // price: [
        //   { required: true, trigger: "blur", validator: validatePrice },
        // ],
        // total: [
        //   { required: true, trigger: "blur", validator: validateTotal },
        // ],
        point: [{ required: true, trigger: "blur", validator: validatePoint }],
        picture: [
          { required: true, trigger: "blur", validator: validatePicture },
        ],
        description: [
          { required: true, trigger: "blur", validator: validateDescription },
        ],
      },
      title: "",
      status: "",
      dialogFormVisible: false,
      list: [],
      loading: false,
      uploadDisabled: false,
      uploadDisabled2: false,
      limitcount: 1,
      limitcount2: 4,
      formData: new FormData(),
      removeList: [],
      // formData2: new FormData(),
      removeList2: [],
    };
  },
  computed: {
    ...mapGetters({
      userName: "user/userName",
    }),
  },
  created() {},
  methods: {
    handleChange(file, fileList) {
      if (file.size > 1024 * 1024) {
        this.$refs.upload.clearFiles();
        this.uploadDisabled = false;
        this.$message({
          message: this.$t("prodcut.pictureTip"),
          type: "error",
        });
      } else {
        this.uploadDisabled = fileList.length >= this.limitcount;
        this.form.picture.push(file.uid);
        this.formData.append("picture", file.raw, file.uid);
        this.form.picture = fileList;
      }
    },
    handleRemove(file, fileList) {
      this.form.picture = fileList;
      if (file.status == "success") {
        this.removeList.push(file.name);
      } else {
        this.removeList.push(file.uid);
      }
      this.uploadDisabled = fileList.length >= this.limitcount;
    },
    handleChange2(file, fileList) {
      if (file.size > 1024 * 1024) {
        this.$refs.upload2.clearFiles();
        this.uploadDisabled2 = false;
        this.$message({
          message: this.$t("prodcut.pictureTip"),
          type: "error",
        });
      } else {
        this.uploadDisabled2 = fileList.length >= this.limitcount2;
        this.form.description.push(file.uid);
        this.formData.append("description", file.raw, file.uid);
        this.form.description = fileList;
      }
    },
    handleRemove2(file, fileList) {
      this.form.description = fileList;
      if (file.status == "success") {
        this.removeList2.push(file.name);
      } else {
        this.removeList2.push(file.uid);
      }
      this.uploadDisabled2 = fileList.length >= this.limitcount2;
    },
    // reset() {
    //   this.$refs.upload.clearFiles();
    //   this.uploadDisabled = false;
    //   this.$refs.ruleForm.resetFields();
    // },
    showEdit(row) {
      if (!row) {
        this.title = this.$t("user.add");
        this.status = "add";
        getNo({ type: "PA" }).then((res) => {
          const { code, msg, data } = res;
          if (code === okCode) {
            this.form.no = data;
          } else {
            this.$baseMessage(this.$t("package.getPackageNoFailed"), "error");
          }
        });
      } else {
        this.title = this.$t("user.edit");
        this.status = "edit";
        this.uploadDisabled = true;
        this.uploadDisabled2 = true;
        this.form = Object.assign({}, row);
      }
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs.upload.clearFiles();
      this.uploadDisabled = false;
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.formData = new FormData();
      this.dialogFormVisible = false;
      this.removeList = [];
    },
    save() {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          this.form.updateUser = this.userName;
          let that = this; //修改this指向
          for (let key in this.form) {
            that.formData.append(key, this.form[key]);
          }
          that.formData.append("removeList", this.removeList);
          that.formData.append("removeList2", this.removeList2);
          if (this.status === "add") {
            doAdd(that.formData).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("package.addPackageSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(this.$t("package.addPackageFailed"), "error");
              }
            });
          } else {
            doEdit(that.formData).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("package.editPackageSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(
                  this.$t("package.editPackageFailed"),
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

<style>
.disabled .el-upload--picture-card {
  display: none;
}
</style>
