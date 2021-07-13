<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
/*
  组件名：EpAlterLine
  功能：展示十二个月内企业注册、变更、注销数目变化情况
  接收参数：info
      接受数据格式为
      var info = {
          time_x_label: [ 
            "2020.01","2020.02","2020.03","2020.04","2020.05","2020.06",
            "2020.07","2020.08","2020.09","2020.10","2020.11","2020.12"
          ],
          sum: [
            {
              name: "注册",
              data: [1036, 1748, 1915, 2519, 2865, 2962, 
                3693, 3810, 4298, 4323, 4675,6209,],
            },
            {
              name: "变更",
              data: [1155, 844, 2285, 2772, 317, 533, 
                1610, 209, 3578, 1484, 4308,1019],
            },
            {
              name: "注销",
              data: [482, 220, 1200, 381, 951, 1001, 
                204, 1390, 507, 800, 1776, 327,
              ],
            },
          ],
        }
*/
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
  watch: {
    info: {
      handler(value) {
        this.initChart(value);
      },
      deep: true, //深度监听
    },
  },
  mounted() {
    this.initChart(this.info);
  },
  beforeUnmount() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart(info) {
      var chartDom = document.getElementById(this.id);
      var myChart = echarts.init(chartDom);
      var option;

      
      /*
      var info = {
        time_x_label: [ 
          "2020.01","2020.02","2020.03","2020.04","2020.05","2020.06",
          "2020.07","2020.08","2020.09","2020.10","2020.11","2020.12"
        ],
        sum: [
          {
            name: "注册",
            data: [1036, 1748, 1915, 2519, 2865, 2962, 
              3693, 3810, 4298, 4323, 4675,6209,],
          },
          {
            name: "变更",
            data: [1155, 844, 2285, 2772, 317, 533, 
              1610, 209, 3578, 1484, 4308,1019],
          },
          {
            name: "注销",
            data: [482, 220, 1200, 381, 951, 1001, 
              204, 1390, 507, 800, 1776, 327,
            ],
          },
        ],
      }
      */

      var series = [];
      for (var i = 0; i < info.sum.length; i++) {
        series.push({
          name: info.sum[i].name,
          type: "line",
          stack: "期末总户数",
          itemStyle: {
            smooth: true,
          },
          animationDuration: 2800,
          animationEasing: "cubicInOut",
          data: info.sum[i].data,
        });
      }
      option = {
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
          textStyle: {
            color: "#90979c",
          },
          data: ["注册", "变更", "注销"],
        },

        grid: {
          left: "5%",
          right: "5%",
          borderWidth: 0,
          top: "10%",
          containLabel: true,
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
            data:info.time_x_label,
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

        series: series,
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