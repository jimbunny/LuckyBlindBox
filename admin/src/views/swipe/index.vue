<template>
  <div class="swipe-container">
    <el-form ref="form" :model="form" label-width="140px">
      <el-upload
        ref="upload"
        action="/api/v1/product/doAdd"
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
          {{ $t("product.pictureTip3") }}
        </div>
      </el-upload>
      <el-button type="primary" @click="save">{{
        $t("product.save")
      }}</el-button>
    </el-form>
  </div>
</template>

<script>
import { okCode, errorCode } from "@/config/settings";
import { getList, doEdit } from "@/api/swipe";

export default {
  name: "Swipe",
  data() {
    return {
      form: {
        picture: new Array(),
      },
      uploadDisabled: false,
      limitcount: 6,
      formData: new FormData(),
      removeList: [],
    };
  },
  watch: {
    "form.picture"(newVal, oldVal) {
      this.uploadDisabled = newVal.length >= this.limitcount;
    },
  },
  created() {
    this.fetchData();
  },
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
    fetchData() {
      this.listLoading = true;
      getList().then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.form.picture = data;
          setTimeout((_) => {
            this.listLoading = false;
          }, 300);
        } else {
          this.$baseMessage(this.$t("swipe.getSwipeFailed"), "error");
        }
      });
    },
    save() {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          let that = this; //修改this指向
          for (let key in this.form) {
            that.formData.append(key, this.form[key]);
          }
          that.formData.append("removeList", this.removeList);
          doEdit(that.formData).then((res) => {
            const { code, msg, data } = res;
            if (code === okCode) {
              this.$baseMessage(
                this.$t("swipe.editSwipeSuccessful"),
                "success"
              );
              this.fetchData();
            } else {
              this.$baseMessage(this.$t("swipe.editSwipeFailed"), "error");
            }
          });
        }
      });
    },
  },
};
</script>
