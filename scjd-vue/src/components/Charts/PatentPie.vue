<template>
  <div :id="id" :class="className" :style="{ height: height, width: width }" />
</template>

<script>
/*
  组件名：PatentMap
  功能：复合展示某一个月新疆全省专利授权的专利类型和申请人类型
  接收参数：
    className: echarts挂载的div的class
    id：echarts挂载的div的id
    width,height为div的尺寸
    info：绘图所必须的数据，用对象的方式存储
      接受数据格式为
      num_patent_types:[] 数组长度为3，分别为专利类型为"发明专利","实用新型","外观设计"的专利数量
      num_applicants_types:[] 数组长度为5，分别为申请人为"个人","工矿企业","大专院校","科研机构","机关团体"的专利数量
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
        deep: true//深度监听
      }
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
      this.chart = echarts.init(document.getElementById(this.id));
      this.chart.setOption({
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
              { value: info.num_patent_types[0], name: "发明专利", selected: true }, // 这个数据被关注程度较高
              { value: info.num_patent_types[1], name: "实用新型" },
              { value: info.num_patent_types[2], name: "外观设计" },
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
              { value: info.num_applicants_types[0], name: "个人" },
              { value: info.num_applicants_types[1], name: "工况企业" },
              { value: info.num_applicants_types[2], name: "大专院校" },
              { value: info.num_applicants_types[3], name: "科研机构" },
              { value: info.num_applicants_types[4], name: "机关团体" },
            ],
          },
        ],
      });
    },
  },
};
</script>
