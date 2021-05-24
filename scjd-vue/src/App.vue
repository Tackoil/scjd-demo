<template>
  <el-container style="height: 100vh">
    <el-header height="70px">新疆市场监督管理局大数据平台</el-header>
    <el-main>
      <transition name="el-fade-in-linear"> </transition>
      <div class="chart-container">
        <ChartMap height="100%" width="100%" />
      </div>
    </el-main>
    <el-footer height="70px">
      北京邮电大学电子工程学院通信与网络研究中心（2021）
    </el-footer>
  </el-container>
</template>

<script>
// import Splitter from 'primevue/splitter';
// import SplitterPanel from 'primevue/splitterpanel';
import ChartMap from "@/components/Charts/Map";

export default {
  name: "App",
  // components: {Splitter, SplitterPanel},
  components: { ChartMap },
  methods: {},
};
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
  padding-bottom: 0;
  overflow: hidden;
}
.chart-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
</style>
