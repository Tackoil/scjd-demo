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
require("echarts/lib/chart/bar");
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
        backgroundColor: "#344b58",

        title: {
          text: "市场主体产业变化情况",
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
          data: ["第一产业", "第二产业", "第三产业"],
        },

        calculable: true,

        grid: {
          left: "5%",
          right: "5%",
          borderWidth: 0,
          top: 150,
          bottom: 95,
          textStyle: {
            color: "#fff",
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
                color: "#90979c",
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
                color: "#90979c",
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
            name: "第一产业",
            type: "bar",
            stack: "期末总户数",
            barMaxWidth: 35,
            barGap: "10%",
            itemStyle: {
              normal: {
                color: "rgba(255,144,128,1)",
                label: {
                  show: true,
                  textStyle: {
                    color: "#fff",
                  },
                  position: "insideTop",
                  formatter(p) {
                    return p.value > 0 ? p.value : "";
                  },
                },
              },
            },
            data: [
              1036, 1748, 1915, 2519, 2865, 2962, 3693, 3810, 4298, 4323, 4675,
              6209,
            ],
          },
          {
            name: "第二产业",
            type: "bar",
            stack: "期末总户数",
            itemStyle: {
              normal: {
                color: "rgba(0,191,183,1)",
                barBorderRadius: 0,
                label: {
                  show: true,
                  position: "insidetop",
                  formatter(p) {
                    return p.value > 0 ? p.value : "";
                  },
                },
              },
            },
            data: [
              209, 317, 533, 844, 1019, 1155, 1484, 1610, 2285, 2772, 3578,
              4308,
            ],
          },
          {
            name: "第三产业",
            type: "bar",
            stack: "期末总户数",
            symbolSize: 10,
            symbol: "circle",
            itemStyle: {
              normal: {
                color: "rgba(252,230,48,1)",
                barBorderRadius: 0,
                label: {
                  show: true,
                  position: "top",
                  formatter(p) {
                    return p.value > 0 ? p.value : "";
                  },
                },
              },
            },
            data: [
              204, 220, 327, 381, 482, 507, 800, 951, 1001, 1200, 1390, 1776,
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
