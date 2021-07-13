<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
/*
  组件名：EpDistributionPie
  功能：展示各领域内企业的数量分布
  接收参数：info
      接受数据格式为数组，格式：
      var info = [
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
              { value: 5930, name: "其他" },
            ];
*/
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
      type: Array,
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
    /*
      var info = [
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
              { value: 5930, name: "其他" },
            ];
      */
      var field = [];
      for(var i=0;i<info.length;i++){
        field.push(info[i].name);
      }
      this.chart = echarts.init(this.$el, "macarons");

      this.chart.setOption({
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          left: "center",
          bottom: "5%",
          data: field,
        },

        series: [
          {
            name: "WEEKLY WRITE ARTICLES",
            type: "pie",
            roseType: "radius",
            radius: [15, 95],
            center: ["50%", "38%"],
            data: info,
            animationEasing: "cubicInOut",
            animationDuration: 2600,
          },
        ],
      });
    },
  },
};
</script>
