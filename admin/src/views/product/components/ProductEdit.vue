<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="900px"
    @close="close"
  >
    <el-form
      ref="form"
      :model="form"
      :rules="Rules"
      label-width="140px"
      enctype="multipart/form-data"
    >
      <el-row>
        <el-col :span="12">
          <el-form-item :label="$t('product.no')" prop="no">
            <el-input
              v-model.trim="form.no"
              autocomplete="off"
              disabled
              :placeholder="$t('product.noTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('product.name')" prop="name">
            <el-input
              v-model.trim="form.name"
              autocomplete="off"
              :placeholder="$t('product.nameTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('product.position')" prop="position">
            <el-input
              v-model.trim="form.position"
              autocomplete="off"
              :placeholder="$t('product.positionTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('product.inPrice')" prop="in_price">
            <el-input-number
              v-model.trim="form.in_price"
              autocomplete="off"
              :placeholder="$t('product.inPriceTip')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('product.outPrice')" prop="out_price">
            <el-input-number
              v-model.trim="form.out_price"
              autocomplete="off"
              :placeholder="$t('product.outPriceTip')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('product.rank')" prop="rank">
            <el-input-number
              v-model.trim="form.rank"
              autocomplete="off"
              :placeholder="$t('product.rankTip')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item
            :label="$t('product.cover_img')"
            prop="cover_img"
            :placeholder="$t('product.cover_img')"
          >
            <el-upload
              ref="upload"
              action="/api/v1/admin/product/doAdd"
              :class="{ disabled: uploadDisabled }"
              list-type="picture-card"
              :limit="limitcount1"
              :on-change="handleChange"
              :on-remove="handleRemove"
              :auto-upload="false"
              :file-list="form.cover_img"
              multiple
              accept="image/*"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">
                {{ $t("product.pictureTip3") }}
              </div>
            </el-upload>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            :label="$t('product.classification')"
            prop="classification"
          >
            <el-select
              v-model="form.classification"
              :placeholder="$t('product.classTip')"
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
          <el-form-item :label="$t('product.status')" prop="status">
            <el-select
              v-model="form.status"
              :placeholder="$t('product.statusTip')"
              style="width: 100%;"
            >
              <el-option :label="$t('product.startSelling')" value="1">
              </el-option>
              <el-option :label="$t('product.stopSelling')" value="0">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('product.package_list')" prop="package_list">
            <el-input
              v-model.trim="form.package_list"
              autocomplete="off"
              :placeholder="$t('package.packageListTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('product.level')" prop="level">
            <el-input-number
              v-model.trim="form.level"
              autocomplete="off"
              :placeholder="$t('product.levelTip')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('product.count')" prop="count">
            <el-input-number
              v-model.trim="form.count"
              autocomplete="off"
              :placeholder="$t('product.count')"
              style="width: 100%;"
              controls-position="right"
            ></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('product.remark')" prop="remark">
            <el-input
              v-model.trim="form.remark"
              autocomplete="off"
              :placeholder="$t('product.remarkTip')"
            ></el-input>
          </el-form-item>
          <el-form-item
            :label="$t('product.description_img')"
            prop="description_img"
            :placeholder="$t('product.description_img')"
          >
            <el-upload
              ref="upload"
              action="/api/v1/admin/product/doAdd"
              :class="{ disabled: uploadDisabled }"
              list-type="picture-card"
              :limit="limitcount1"
              :on-change="handleChange"
              :on-remove="handleRemove"
              :auto-upload="false"
              :file-list="form.description_img"
              multiple
              accept="image/*"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">
                {{ $t("product.pictureTip3") }}
              </div>
            </el-upload>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item
            :label="$t('product.detail_img')"
            prop="detail_img"
            :placeholder="$t('product.detail_img')"
          >
            <el-upload
              ref="upload"
              action="/api/v1/admin/product/doAdd"
              :class="{ disabled: uploadDisabled }"
              list-type="picture-card"
              :limit="limitcount4"
              :on-change="handleChange"
              :on-remove="handleRemove"
              :auto-upload="false"
              :file-list="form.detail_img"
              multiple
              accept="image/*"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">
                {{ $t("product.pictureTip3") }}
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
import { isPassword } from "@/utils/validate";
import { doEdit, doAdd, getNo, checkName } from "@/api/product";
import { okCode, errorCode } from "@/config/settings";
import { mapGetters } from "vuex";
import qs from "qs";
import axios from "axios";
import { tokenType } from "@/config/settings";
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
} from "@/utils/accessToken";

export default {
  name: "ProductEdit",
  data() {
    const validateDetailImg = (rule, value, callback) => {
      if ([] == value) {
        callback(new Error(this.$t("product.pictureTip")));
      } else if (value.length < limitcount4) {
        callback(new Error(this.$t("product.pictureTip2")));
      } else {
        callback();
      }
    };
    const validateImg = (rule, value, callback) => {
      if ([] == value) {
        callback(new Error(this.$t("product.pictureTip")));
      } else if (value.length < limitcount1) {
        callback(new Error(this.$t("product.pictureTip2")));
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
    const validateName = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.nameTip")));
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
    const validateRank = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("product.rankTip")));
      } else {
        callback();
      }
    };
    const validateClassification = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.classTip")));
      } else {
        callback();
      }
    };
    const validatePackageList = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.packageListTip")));
      } else {
        callback();
      }
    };
    const validateStatus = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.statusTip")));
      } else {
        callback();
      }
    };
    const validatePosition = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("product.positionTip")));
      } else {
        callback();
      }
    };
    const validateInPrice = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("product.inPriceTip")));
      } else {
        callback();
      }
    };
    const validateOutPrice = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("product.outPriceTip")));
      } else {
        callback();
      }
    };
    const validateLevel = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("product.levelTip")));
      } else {
        callback();
      }
    };
    const validateCount = (rule, value, callback) => {
      if (0 == value) {
        callback(new Error(this.$t("product.countTip")));
      } else {
        callback();
      }
    };
    return {
      form: {
        no: "",
        name: "",
        description_img: [],
        cover_img: [],
        detail_img: [],
        position: "",
        in_price: "",
        out_price: "",
        rank: 0,
        remark: "",
        status: "1",
        classification: "clothes",
        count: 0,
        package_list: "",
        level: 1,
      },
      Rules: {
        no: [{ required: true, trigger: "blur", validator: validateNo }],
        name: [{ required: true, trigger: "blur", validator: validateName }],
        package_list: [
          { required: true, trigger: "blur", validator: validatePackageList },
        ],
        count: [{ required: true, trigger: "blur", validator: validateCount }],
        classification: [
          {
            required: true,
            trigger: "blur",
            validator: validateClassification,
          },
        ],
        status: [
          { required: true, trigger: "blur", validator: validateStatus },
        ],
        position: [
          { required: true, trigger: "blur", validator: validatePosition },
        ],
        in_price: [
          { required: true, trigger: "blur", validator: validateInPrice },
        ],
        out_price: [
          { required: true, trigger: "blur", validator: validateOutPrice },
        ],
        rank: [{ required: true, trigger: "blur", validator: validateRank }],
        level: [{ required: true, trigger: "blur", validator: validateLevel }],
        detail_img: [
          { required: true, trigger: "blur", validator: validateDetailImg },
        ],
        cover_img: [
          { required: true, trigger: "blur", validator: validateImg },
        ],
        description_img: [
          {
            required: true,
            trigger: "blur",
            validator: validateImg,
          },
        ],
      },
      title: "",
      status: "",
      dialogFormVisible: false,
      list: [],
      loading: false,
      uploadDisabled: false,
      limitcount1: 1,
      limitcount4: 4,
      formData: new FormData(),
      removeList: [],
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
    showEdit(row) {
      this.removeList = [];
      if (!row) {
        this.title = this.$t("user.add");
        this.status = "add";
        getNo().then((res) => {
          const { code, msg, data } = res;
          if (code === okCode) {
            this.form.no = data;
          } else {
            this.$baseMessage(this.$t("product.getProductNoFailed"), "error");
          }
        });
      } else {
        this.title = this.$t("user.edit");
        this.status = "edit";
        this.uploadDisabled = true;
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
          if (this.status === "add") {
            doAdd(that.formData)
              .then((res) => {
                const { code, msg, data } = res;
                if (code === okCode) {
                  this.$baseMessage(
                    this.$t("product.addProductSuccessful"),
                    "success"
                  );
                  this.$emit("fetchData");
                  this.close();
                } else {
                  this.$baseMessage(
                    this.$t("product.addProductFailed"),
                    "error"
                  );
                }
              })
              .catch(function (error) {
                console.log(error);
              });
          } else {
            doEdit(that.formData)
              .then((res) => {
                const { code, msg, data } = res;
                if (code === okCode) {
                  this.$baseMessage(
                    this.$t("product.editProductSuccessful"),
                    "success"
                  );
                  this.$emit("fetchData");
                  this.close();
                } else {
                  this.$baseMessage(
                    this.$t("product.editProductFailed"),
                    "error"
                  );
                }
              })
              .catch(function (error) {
                console.log(error);
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
