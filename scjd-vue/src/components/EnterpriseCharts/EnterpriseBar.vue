<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
/*
  组件名：EnterpriseBar
  功能：展示十二个月内各类市场主体变化情况
  接收参数：info
      接受数据格式为
      var info = {
        time_x_label: [ 
          "2020.01","2020.02","2020.03","2020.04","2020.05","2020.06",
          "2020.07","2020.08","2020.09","2020.10","2020.11","2020.12"
        ],
        sum: [
          {
            name: "第一产业",
            data: [1036, 1748, 1915, 2519, 2865, 2962,
              3693, 3810, 4298, 4323, 4675,6209],
          },
          {
            name: "第二产业",
            data: [209, 317, 533, 844, 1019, 1155, 
            1484, 1610, 2285, 2772, 3578,4308],
          },
          {
            name: "第三产业",
            data: [204, 220, 327, 381, 482, 507,
              800, 951, 1001, 1200, 1390, 1776],
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
            name: "第一产业",
            data: [1036, 1748, 1915, 2519, 2865, 2962,
              3693, 3810, 4298, 4323, 4675,6209],
          },
          {
            name: "第二产业",
            data: [209, 317, 533, 844, 1019, 1155, 
            1484, 1610, 2285, 2772, 3578,4308],
          },
          {
            name: "第三产业",
            data: [204, 220, 327, 381, 482, 507,
              800, 951, 1001, 1200, 1390, 1776],
          },
        ],
      }
      */

      var series = [];

      for (var i = 0; i < info.sum.length; i++) {
        series.push({
          name: info.sum[i].name,
          type: "bar",
          stack: "期末总户数",
          itemStyle: {
            normal: {
              label: {
                show: true,
                position: "insideTop",
              },
            }
          },
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
          x: "2%",
          textStyle: {
            color: "#90979c",
          },
          data: ["第一产业", "第二产业", "第三产业"],
        },
        grid: {
          left: "5%",
          right: "5%",
          borderWidth: 0,
          top: "10%",
          bottom: "30%",
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
            data: info.time_x_label,
          },
        ],
        yAxis: {
          type: "value",
        },

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
    },
  },
};
</script>