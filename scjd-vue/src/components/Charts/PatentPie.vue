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
      this.chart = echarts.init(document.getElementById(this.id));
      this.chart.setOption({
        title: {
          text: "2021年2月新疆专利授权状况统计",
          top: 10,
          left: 10,
        },
        tooltip: {
          trigger: "item",
          // a: 专利类型
          // b: 具体类型
          // c: 数量
          // d: 百分比
          formatter: "{a} <br/>{b}: {c} ({d}%)",
        },
        legend: {
          data: [
            "发明专利",
            "实用新型",
            "外观设计",
            "个人",
            "工矿企业",
            "大专院校",
            "科研机构",
            "机关团体",
          ],
        },
        series: [
          {
            name: "专利类型",
            type: "pie",
            selectedMode: "single",
            radius: [0, "40%"],
            label: {
              position: "inside",
              fontSize: 14,
            },
            labelLine: {
              show: false,
            },
            data: [
              { value: 84, name: "发明专利", selected: true }, // 这个数据被关注程度较高
              { value: 901, name: "实用新型" },
              { value: 52, name: "外观设计" },
            ],
          },
          {
            name: "申请人类型",
            type: "pie",
            radius: ["55%", "70%"],
            labelLine: {
              length: 30,
            },
            label: {
              formatter: "{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ",
              backgroundColor: "#F6F8FC",
              borderColor: "#8C8D8E",
              borderWidth: 1,
              borderRadius: 4,

              rich: {
                a: {
                  color: "#6E7079",
                  lineHeight: 22,
                  align: "center",
                },
                hr: {
                  borderColor: "#8C8D8E",
                  width: "100%",
                  borderWidth: 1,
                  height: 0,
                },
                b: {
                  color: "#4C5058",
                  fontSize: 14,
                  fontWeight: "bold",
                  lineHeight: 33,
                },
                per: {
                  color: "#fff",
                  backgroundColor: "#4C5058",
                  padding: [3, 4],
                  borderRadius: 4,
                },
              },
            },
            data: [
              { value: 262, name: "个人" },
              { value: 546, name: "工况企业" },
              { value: 134, name: "大专院校" },
              { value: 55, name: "科研机构" },
              { value: 40, name: "机关团体" },
            ],
          },
        ],
      });
      
    },
  },
};
</script>
