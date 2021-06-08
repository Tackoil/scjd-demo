<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
// 按需引入
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/legend");
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
      this.chart = echarts.init(this.$el, "macarons");

      this.chart.setOption({
        title: {
          text: "各行业企业分布情况",
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
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },

        legend: {
          left: "center",
          bottom: "10%",
          data: [
            "农、林、牧、渔业",
            "采矿业",
            "制造业",
            "电力、热力、燃气",
            "建筑业",
            "批发和零售业",
            "交通运输、仓储和邮政业",
            "住宿和餐饮业",
            "信息运输、电子软件业",
            "金融业",
            "房地产业",
            "租赁和商务服务业",
            "科学研究和技术服务业",
            "水利、环境和公共设施管理业",
            "居民服务业",
            "教育",
            "文化、体育和娱乐业",
            "其他",
          ],
        },

        series: [
          {
            name: "WEEKLY WRITE ARTICLES",
            type: "pie",
            roseType: "radius",
            radius: [15, 95],
            center: ["50%", "38%"],
            data: [
              { value: 42176, name: "批发和零售业" },
              { value: 31663, name: "租赁和商务服务业" },
              { value: 28685, name: "建筑业" },
              { value: 23703, name: "制造业" },
              { value: 22393, name: "科学研究和技术服务业" },
              { value: 18358, name: "农、林、牧、渔业" },
              { value: 16920, name: "信息运输、电子软件业" },
              { value: 10095, name: "房地产业" },
              { value: 9910, name: "交通运输、仓储和邮政业" },
              { value: 7221, name: "文化、体育和娱乐业" },
              { value: 7154, name: "金融业" },
              { value: 5930, name: "住宿和餐饮业" },
              { value: 4279, name: "教育" },
              { value: 3908, name: "电力、热力、燃气" },
              { value: 3250, name: "水利、环境和公共设施管理业" },
              { value: 2348, name: "采矿业" },
              { value: 131, name: "其他" },
            ],
            animationEasing: "cubicInOut",
            animationDuration: 2600,
          },
        ],
      });
    },
  },
};
</script>
