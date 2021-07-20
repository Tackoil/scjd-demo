<template>
  <div>
    <el-form
      :model="ruleForm"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="图表描述" prop="name">
        <el-input v-model="ruleForm.name"></el-input>
      </el-form-item>
      <el-form-item label="图表type" prop="type">
        <el-input v-model="ruleForm.type"></el-input>
      </el-form-item>
      <el-form-item label="上传数据">
        <!-- action不应该写死，后面修改 -->
        <el-upload
          class="upload-demo"
          ref="upload"
          action="http://localhost:8000/storage/files/"
          :on-exceed="handleExceed"
          :on-success="handleUpload"
          :before-remove="beforeRemove"
          :before-upload="beforeUpload"
          :file-list="fileList"
          :auto-upload="false"
          :multiple="false"
          :limit="1"
          accept=".json"
          :data="ruleForm"
          drag
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <template #tip>
            <div class="el-upload__tip">只能上传 json文件，且不超过5MB</div>
          </template>
        </el-upload>
      </el-form-item>
      <el-form-item label="是否可删除">
        <el-switch v-model="ruleForm.can_del"></el-switch>
      </el-form-item>
      <el-form-item>
        <el-button
          style="margin-left: 10px"
          type="success"
          @click="submitUpload"
          >创建图表数据</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
const baseurl = "http://localhost:8000";

export default {
  data() {
    return {
      ruleForm: {
        name: "", // 图表的描述
        type: "", // 图表的种类（从预设的几种类型中选择）
        can_del: true, // 图表是否可删除，默认新增图表可删除
      },
      fileList: [],
    };
  },
  methods: {
    // 移除上传文件时要确认
    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    // 上传文件之前的钩子
    beforeUpload(file) {
      //判断文件格式
      let hz = file.name.split(".").pop();
      // console.log("hz",hz)
      if (hz != "json") {
        this.$message.error(`只能选择json文件`);
        return false;
      }

      // 判断文件大小
      let fileSize = file.size / 1024 / 1024 < 5;
      if (!fileSize) {
        this.$message.error("上传文件大小不能超过 5MB");
        return false;
      }
    },

    // 上传文件个数超过定义的数量
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${
          files.length + fileList.length
        } 个文件`
      );
    },

    // 手动上传文件
    submitUpload() {
      this.$refs.upload.submit();
    },

    // 成功上传以后,
    async handleUpload(res) {
      this.$message.success("上传成功");
      console.log("info", res.id); // 为啥返回的res是一个对象？
      // 尝试下载
      await axios
        .get(`${baseurl}/storage/files/${res.id}/download/`)
        .then(function (response) {
          let file = response.data;
          console.log(file);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
};
</script>

<style>
.demo-ruleForm {
  margin: 25px;
}
</style>

