<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/title");
require("echarts/lib/component/toolbox");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/visualMap");
require("echarts/lib/chart/map");
require("echarts/lib/component/geo");
import resize from "./mixins/resize";    //自适应

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: "chart",
    },
    id: {
      type: String,
      default: "chart",
    },
    width: {
      type: String,
      default: "200px",
    },
    height: {
      type: String,
      default: "200px",
    },
  },
  data() {
    return {
      chart: null,
      // 读取本地geoJson格式文件
      xjJson: require("@/assets/geojson/XJ.json"),
    };
  },
  mounted() {
    this.initChart();
  },
  beforeUnmount() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      echarts.registerMap("XJ", this.xjJson);
      this.chart = echarts.init(document.getElementById(this.id));
      this.chart.setOption({
        title: {
          text: "2021年2月新疆各地州专利授权情况",
          subtext: "数据来自新疆维吾尔自治区市场监督管理局",
          sublink:
            "http://scjgj.xinjiang.gov.cn/xjaic/tzgg/202104/c0f7f7bdc23f4f56a4c473ed56945b9b.shtml",
          top: 10,
          left: 10,
        },
        tooltip: {
          trigger: "item",
          formatter: "{b}<br/>{c} 项(授权)",
        },
        toolbox: {
          show: true,
          orient: "vertical",
          left: "right",
          top: "center",
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {},
          },
        },
        visualMap: {
          min: 0,
          max: 500,
          text: ["High", "Low"],
          realtime: false,
          calculable: true,
          inRange: {
            color: ["lightskyblue", "yellow", "orangered"],
          },
        },
        series: [
          {
            name: "2021年2月新疆各地州专利授权情况",
            type: "map",
            roam: true, //是否开启平游或缩放
            scaleLimit: {
              //滚轮缩放的极限控制
              min: 1,
              max: 2,
            },
            mapType: "XJ", // 自定义扩展图表类型
            label: {
              show: true,
            },
            // 这里可以修改为从父组件传来的数据
            data: [
              { name: "乌鲁木齐", value: 476 },
              { name: "昌吉州", value: 61 },
              { name: "克拉玛依", value: 44 },
              { name: "石河子", value: 70 },
              { name: "伊犁州", value: 65 },
              { name: "博州", value: 16 },
              { name: "塔城", value: 30 },
              { name: "阿勒泰", value: 14 },
              { name: "吐鲁番", value: 32 },
              { name: "哈密", value: 71 },
              { name: "巴州", value: 47 },
              { name: "阿克苏", value: 62 },
              { name: "喀什", value: 36 },
              { name: "和田", value: 9 },
              { name: "克州", value: 4 },
            ],
            // 自定义名称映射
            // 左边为json文件中的数据名
            // 目前缺少建设兵团的数据
            nameMap: {
              乌鲁木齐市: "乌鲁木齐",
              昌吉回族自治州: "昌吉州",
              克拉玛依市: "克拉玛依",
              石河子市: "石河子",
              伊犁哈萨克自治州: "伊犁州",
              博尔塔拉蒙古自治州: "博州",
              塔城地区: "塔城",
              阿勒泰地区: "阿勒泰",
              吐鲁番市: "吐鲁番",
              哈密市: "哈密",
              巴音郭楞蒙古自治州: "巴州",
              阿克苏地区: "阿克苏",
              喀什地区: "喀什",
              和田地区: "和田",
              克孜勒苏柯尔克孜自治州: "克州",
            },
          },
        ],
      });
    },
  },
};
</script>
