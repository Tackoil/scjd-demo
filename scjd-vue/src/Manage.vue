<template>
  <el-page-header
    class="manage-header"
    @back="this.$router.back()"
    content="数据管理"
  />
  <div class="manage-table">
    <el-button class="el-icon-plus" plain round> 添加新的数据项目 </el-button>
    <el-table :data="tableData" class="manage-table-box">
      <el-table-column prop="name" label="数据项目"> </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template #default="scope">
          <el-button @click="handleItemClick(scope.row)" type="text" size="small">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getDataList } from "@/utils/connector.js";

export default {
  name: "manage",
  data() {
    return {
      tableData: [],
    };
  },
  created() {
    getDataList().then((res) => (this.tableData = res));
  },
  methods: {
    handleItemClick(item){
      if(item && item.id){
        this.$router.push(`/dataitem/${item.id}`)
      }
    }
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

