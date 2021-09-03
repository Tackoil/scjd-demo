<template>
  <el-page-header
    class="manage-header"
    @back="this.$router.back()"
    content="数据管理"
  />
  <div class="manage-table">
    <el-button class="el-icon-plus" plain round @click="dialogVisible = true">
      添加新的数据项目
    </el-button>
    <el-table :data="tableData" class="manage-table-box">
      <el-table-column prop="name" label="数据项目"> </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template #default="scope">
          <el-button
            @click="handleItemClick(scope.row)"
            type="text"
            size="small"
            >查看</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog
    title="新建数据项目"
    v-model="dialogVisible"
    width="30%"
  >
    <span>请输入数据项目名称</span>
    <el-input v-model="newDataItemTitle" placeholder="请输入内容"> </el-input>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleNewDataItem"
          >新建
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { getDataList, newDataItem } from "@/utils/connector.js";

export default {
  name: "manage",
  data() {
    return {
      tableData: [],
      dialogVisible: false,
      newDataItemTitle: "",
    };
  },
  created() {
    getDataList().then((res) => (this.tableData = res));
  },
  methods: {
    handleItemClick(item) {
      if (item && item.id) {
        this.$router.push(`/dataitem/${item.id}`);
      }
    },
    handleNewDataItem() {
      this.$nextTick().then(
        newDataItem(this.newDataItemTitle).then((res) => {
        this.$router.push(`/dataitem/${res}`)
      })
      )
    },
  },
};
</script>

<style>
.manage-header {
  padding: 24px;
}

.manage-table {
  margin: 0 24px;
}

.manage-table-box {
  margin-top: 16px;
}
</style>
