<template>
  <el-dialog
    :title="name"
    v-model="inner_visible"
    :before-close="handleUpdateDialogClose"
  >
    <el-upload
      :disabled="uploading"
      class="upload-box"
      :show-file-list="false"
      action="fakeAction"
      :http-request="handleUpload"
      drag
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
  </el-dialog>
</template>

<script>

import {newUploadData, replaceUploadData} from "@/utils/connector";

export default {
  name: "UploadDialog",
  props: ["name", "itemID", "timestamp", "modelValue", "uploadId", "type"],
  emits: ["success", "update:modelValue"],
  data() {
    return {
      uploading: false,
    }
  },
  computed: {
    inner_visible: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  methods: {
    handleUpdateDialogClose(done) {
      if (!this.uploading) {
        done()
      }
    },
    handleUpload(paras){
      this.uploading = true;
      const file = paras.file;
      if(this.type === "update"){
        replaceUploadData(this.uploadId, file).then(res => {
          if (res.status === 200) {
            this.$message.success("上传成功");
            this.uploading = false;
            this.inner_visible = false;
            this.$emit("success")
          }
        }).catch( err => {
          console.log(err)
          this.$message.error("上传失败")
          this.uploading = false;
        })
      }else{
        newUploadData(this.itemID, this.timestamp, file).then(res => {
          if (res.status === 201) {
            this.$message.success("上传成功");
            this.uploading = false;
            this.inner_visible = false;
            this.$emit("success")
          }
        }).catch( err => {
          console.log(err)
          this.$message.error("上传失败")
          this.uploading = false;
        })
      }
    }
  }
}
</script>

<style>

</style>