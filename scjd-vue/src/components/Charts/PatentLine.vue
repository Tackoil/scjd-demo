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

      setTimeout(function () {
        option = {
          legend: {},
          tooltip: {
            trigger: "axis",
            showContent: false,
          },
          dataset: {
            source: [
              [
                "Proportion",
                "2020.10",
                "2020.11",
                "2020.12",
                "2021.01",
                "2021.02",
                "2021.03",
              ],
              ["发明专利", 326, 468, 92, 59, 84, 102],
              ["实用新型", 1390, 1670, 1077, 865, 901, 1196],
              ["外观设计", 91, 91, 79, 50, 52, 133],
            ],
          },
          xAxis: { type: "category" },
          yAxis: { gridIndex: 0 },
          grid: { top: "55%" },
          series: [
            {
              type: "line",
              smooth: true,
              seriesLayoutBy: "row",
              emphasis: { focus: "series" },
            },
            {
              type: "line",
              smooth: true,
              seriesLayoutBy: "row",
              emphasis: { focus: "series" },
            },
            {
              type: "line",
              smooth: true,
              seriesLayoutBy: "row",
              emphasis: { focus: "series" },
            },
            {
              type: "pie",
              id: "pie",
              radius: "30%",
              center: ["50%", "25%"],
              emphasis: { focus: "data" },
              label: {
                formatter: "{b}: {@2021} ({d}%)",
              },
              encode: {
                itemName: "Proportion",
                value: "2021",
                tooltip: "2021",
              },
            },
          ],
        };

        myChart.on("updateAxisPointer", function (event) {
          var xAxisInfo = event.axesInfo[0];
          if (xAxisInfo) {
            var dimension = xAxisInfo.value + 1;
            myChart.setOption({
              series: {
                id: "pie",
                label: {
                  formatter: "{b}: {@[" + dimension + "]} ({d}%)",
                },
                encode: {
                  value: dimension,
                  tooltip: dimension,
                },
              },
            });
          }
        });

        myChart.setOption(option);
      });

      option && myChart.setOption(option);
      this.chart = myChart;
    },
  },
};
</script>
