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
require("echarts/lib/component/dataZoom");
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
    info: {
      type: Object,
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
          text: "企业注册、变更、注销统计",
          x: "20",
          top: "20",
          textStyle: {
            color: "#000",
            fontSize: "22",
          },
          subtextStyle: {
            color: "#90979c",
            fontSize: "16",
          },
        },

        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            textStyle: {
              color: "#fff",
            },
          },
        },

        legend: {
          x: "5%",
          top: "10%",
          textStyle: {
            color: "#90979c",
          },
          data: ["注册", "变更", "注销"],
        },

        calculable: false,

        grid: {
          left: "5%",
          right: "5%",
          borderWidth: 0,
          top: 150,
          bottom: 95,
          containLabel: true,
          textStyle: {
            color: "#000",
          },
        },

        toolbox: {
          right: 10,
          show: true,
          feature: {
            saveAsImage: { show: true },
          },
        },
        xAxis: [
          {
            type: "category",
            axisLine: {
              lineStyle: {
                color: "#696969",
              },
            },
            splitLine: {
              show: false,
            },
            axisTick: {
              show: false,
            },
            splitArea: {
              show: false,
            },
            axisLabel: {
              interval: 0,
            },
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
        ],

        yAxis: [
          {
            type: "value",
            splitLine: {
              show: false,
            },
            axisLine: {
              lineStyle: {
                color: "#696969",
              },
            },
            axisTick: {
              show: false,
            },
            axisLabel: {
              interval: 0,
            },
            splitArea: {
              show: false,
            },
          },
        ],

        dataZoom: [
          {
            show: true,
            height: 30,
            xAxisIndex: [0],
            bottom: 30,
            start: 10,
            end: 80,
            handleIcon:
              "path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z",
            handleSize: "110%",
            handleStyle: {
              color: "#d3dee5",
            },
            textStyle: {
              color: "#fff",
            },
            borderColor: "#90979c",
          },
          {
            type: "inside",
            show: true,
            height: 15,
            start: 1,
            end: 35,
          },
        ],

        series: [
          {
            name: "注册",
            type: "line",
            stack: "期末总户数",
            barMaxWidth: 35,
            itemStyle: {
              normal: {
                color: "#FF005A",
                lineStyle: {
                  color: "#FF005A",
                  width: 2,
                },
              },
              smooth: true,
              type: "line",
              animationDuration: 2800,
              animationEasing: "cubicInOut",
            },
            data: [
              1036, 1748, 1915, 2519, 2865, 2962, 3693, 3810, 4298, 4323, 4675,
              6209,
            ],
          },
          {
            name: "变更",
            type: "line",
            stack: "期末总户数",
            barMaxWidth: 35,
            itemStyle: {
              normal: {
                color: "#3888fa",
                lineStyle: {
                  color: "#3888fa",
                  width: 2,
                },
              },
              smooth: true,
              type: "line",
              animationDuration: 2800,
              animationEasing: "cubicInOut",
            },
            data: [
              1155, 844, 2285, 2772, 317, 533, 1610, 209, 3578, 1484, 4308,
              1019,
            ],
          },
          {
            name: "注销",
            type: "line",
            stack: "期末总户数",
            barMaxWidth: 35,
            itemStyle: {
              normal: {
                color: "#DAA520",
                lineStyle: {
                  color: "#DAA520",
                  width: 2,
                },
              },
              smooth: true,
              type: "line",
              animationDuration: 2800,
              animationEasing: "cubicInOut",
            },
            data: [
              482, 220, 1200, 381, 951, 1001, 204, 1390, 507, 800, 1776, 327,
            ],
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