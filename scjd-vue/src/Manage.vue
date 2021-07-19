<template>
  <div>
    <el-form
      :model="ruleForm"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="图表id" prop="id">
        <el-input v-model="ruleForm.id"></el-input>
      </el-form-item>
      <el-form-item label="图表描述" prop="name">
        <el-input v-model="ruleForm.name"></el-input>
      </el-form-item>
      <el-form-item label="上传数据">
        <!-- action不应该写死，后面修改 -->
        <el-upload
          class="upload-demo"
          ref="upload"
          action="http://localhost:8000/file/json_upload/"
          :on-preview="handlePreview"
          :before-remove="beforeRemove"
          :on-exceed="handleExceed"
          :file-list="fileList"
          :before-upload="beforeUpload"
          :auto-upload="true"
          :multiple="false"
          :limit="1"
          accept=".json"
          drag
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <template #tip>
            <div class="el-upload__tip">只能上传 json文件，且不超过5MB</div>
          </template>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="save()">立即创建</el-button>
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
        id: "",          // 图表的id
        name: "",        // 图表的描述
        type: "",        // 图表的种类（从预设的几种类型中选择）
        info: "",        // 图表数据在服务器端的路径
      },
      fileList: [],
    };
  },
  methods: {
    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    handlePreview(file) {
      console.log(file);
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

    // 上传表单
    async save() {
      const res = await axios.post(`${baseurl} `, this.ruleForm);
      if (res) {
        this.$message({
          type: "success",
          message: "保存成功",
        });
      }
    },
  },
};
</script>

<style>
</style>

