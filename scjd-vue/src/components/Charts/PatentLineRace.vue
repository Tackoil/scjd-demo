<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/title");
require("echarts/lib/component/toolbox");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/grid");
require("echarts/lib/component/legend");
require("echarts/lib/chart/line");
import resize from "./mixins/resize";

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
    };
  },
  mounted() {
    this.initChart();
  },
  // vue3.x版本要修改beforeDestroy()为 beforeUnmount()
  beforeUnmount() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      var chartDom = document.getElementById(this.id);
      var myChart = echarts.init(chartDom);
      var option;

      option = {
        title: {
          text: "2020年各地州专利授权状况年累计变化",
          left: 10,
          top: 10,
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },
        legend: {
          top: 35,
          data: [
            "乌鲁木齐",
            "昌吉州",
            "克拉玛依",
            "石河子",
            "伊犁州",
            "博州",
            "塔城",
            "阿勒泰",
            "吐鲁番",
            "哈密",
            "巴州",
            "阿克苏",
            "喀什",
            "和田",
            "克州",
          ],
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        toolbox: {
          right: 10,
          show: true,
          feature: {
            saveAsImage: { show: true },
          },
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: [
            "2020.01",
            "2020.02",
            "2020.03",
            "2020.04",
            "2020.05",
            "2020.06",
            "2020.07",
            "2020.08",
            "2020.09",
            "2020.10",
            "2020.11",
            "2020.12",
          ],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "乌鲁木齐",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [
              1000,
              1100,
              1400,
              1400,
              2000,
              2400,
              3000,
              3000,
              4000,
              4766,
              5315,
              5332,
            ],
          },
          {
            name: "昌吉州",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [100, 110, 140, 170, 200, 240, 300, 350, 400, 476, 531, 533],
          },
          {
            name: "克拉玛依",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [55, 102, 138, 188, 246, 313, 386, 413, 457, 473, 556, 646],
          },
          {
            name: "石河子",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [20, 109, 114, 192, 208, 271, 307, 339, 350, 399, 498, 523],
          },
          {
            name: "伊犁州",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [35, 95, 141, 229, 261, 354, 396, 396, 403, 481, 518, 558],
          },
          {
            name: "博州",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639],
          },
          {
            name: "塔城",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639],
          },
          {
            name: "阿勒泰",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [25, 65, 82, 121, 129, 155, 159, 168, 195, 209, 209, 226],
          },
          {
            name: "吐鲁番",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639],
          },
          {
            name: "哈密",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [1, 19, 21, 35, 52, 59, 67, 84, 86, 100, 117, 136],
          },
          {
            name: "巴州",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [1, 19, 21, 35, 52, 59, 67, 84, 86, 100, 117, 136],
          },
          {
            name: "阿克苏",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639],
          },
          {
            name: "喀什",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [[6, 15, 18, 28, 32, 33, 36, 41, 41, 47, 56, 57]],
          },
          {
            name: "和田",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [69, 96, 116, 210, 280, 301, 360, 397, 413, 489, 570, 639],
          },
          {
            name: "克州",
            type: "line",
            stack: "总量",
            smooth: true,
            areaStyle: {},
            data: [3, 4, 13, 21, 28, 37, 38, 45, 48, 58, 58, 58],
          },
        ],
      };

      option && myChart.setOption(option);
      this.chart = myChart;
      window.onresize = function () {
        this.chart.resize();
      };
    },
  },
};
</script>
