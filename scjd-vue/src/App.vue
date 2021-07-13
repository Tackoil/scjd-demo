<template>
  <el-container style="height: 100vh">
    <el-header height="70px">
      <i style="margin-right: 12px" :class="this.coll ? 'el-icon-arrow-right' : 'el-icon-arrow-left'" @click="() => {this.coll = !this.coll}"></i>
      新疆市场监督管理局大数据平台
      </el-header>
    <el-container style="overflow: hidden"> 
      <el-aside width="auto"> 
        <el-menu router :collapse="coll">
          <el-menu-item index="/"> 
          <i class="el-icon-data-line"></i>
          <span>数据大屏</span> 
          </el-menu-item>
          <el-menu-item index="./manage"> 
          <i class="el-icon-takeaway-box"></i>
          <span>数据管理 </span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main v-loading="loading" style="padding: 0; overflow: hidden">
      <el-scrollbar>
        <router-view> </router-view>
      </el-scrollbar>
    </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default{
  name: "App",
  data(){
    return {
      coll: true,
    }
  }
}
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
}

#app {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.el-header,
.el-footer {
  background-color: #003399;
  color: rgb(255, 253, 253);
  line-height: 70px;
}

.el-footer {
  text-align: center;
}

.el-header {
  font-size: 20px;
}

.el-aside {
  color: #333;
  background-color: rgb(238, 241, 246);
}

.el-main {
  background-color: rgb(245, 248, 251);
  overflow: hidden;
}
</style>
