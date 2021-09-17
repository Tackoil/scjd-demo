<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/dataset");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/grid");
require("echarts/lib/component/legend");
require("echarts/lib/component/title");
require("echarts/lib/chart/line");
require("echarts/lib/chart/pie");
import resize from "./mixins/resize";

export default {
  name: "CustomPie",
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
  // vue3.x版本要修改beforeDestroy()为 beforeUnmount()
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

      setTimeout(function () {
        option = {
          tooltip: {
            trigger: "item",
          },
          legend: {
            orient: 'vertical',
            left: 'left',
          },
          series: [
            {
              name: info && info.name,
              type: 'pie',
              data: info && info.series,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };
        myChart.setOption(option);
      });

      option && myChart.setOption(option);
      this.chart = myChart;
    },
  }
}
</script>
