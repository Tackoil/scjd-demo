<template>
  <div style="width: 100%" v-loading="loading" ref="screen">
    <el-space>
      <el-button class="el-icon-data-line" @click="makeFullScreen"> </el-button>
      <el-switch v-model="draggable" active-text="允许拖拽"> </el-switch>
      <el-switch v-model="resizable" active-text="允许拉伸"> </el-switch>
    </el-space>
    <div v-if="false">
      <div class="layoutJSON">
        Displayed as <code>[x, y, w, h]</code>:
        <div class="columns">
          <div class="layoutItem" v-for="item in layout" :key="item.i">
            <b>{{ item.i }}</b
            >: [{{ item.x }}, {{ item.y }}, {{ item.w }}, {{ item.h }}]
          </div>
        </div>
      </div>
    </div>
    <div class="content" style="margin-left: auto; margin-right: auto">
      <grid-layout
        :layout="layout"
        :col-num="12"
        :row-height="30"
        :is-draggable="draggable"
        :is-resizable="resizable"
        vertical-compact
        :use-css-transforms="true"
      >
        <grid-item
          v-for="item in layout"
          :key="item.i"
          :x="item.x"
          :y="item.y"
          :w="item.w"
          :h="item.h"
          :i="item.i"
        >
          <el-card
            style="
              height: 100%;
              box-sizing: border-box;
              display: flex;
              flex-direction: column;
            "
            :body-style="{ flex: 1, 'box-sizing': 'border-box' }"
          >
            <template #header>
              <span class="subtitle-text"
                >{{ item.i }} : {{ picDict[item.i].name }}
              </span>
            </template>
            <div :ref="`chart-cont-${item.i}`" style="height: 100%">
              <component
                :is="picDict[item.i].comp"
                :ref="`chart-${item.i}`"
                :id="'' + item.i"
                width="100%"
                height="100%"
                :info="picDict[item.i].info"
              >
              </component>
            </div>
          </el-card>
        </grid-item>
      </grid-layout>
    </div>
  </div>
</template>

<script>
import PatentPie from "@/components/Charts/PatentPie";
import PatentLineRace from "@/components/Charts/PatentLineRace";
import PatentLine from "@/components/Charts/PatentLine";
import PatentMap from "@/components/Charts/PatentMap";
import NewsWordMap from "@/components/Charts/NewsWordMap";
import EnterpriseBar from "@/components/EnterpriseCharts/EnterpriseBar";
import EpDistributionPie from "@/components/EnterpriseCharts/EpDistributionPie";
import EpAlterLine from "@/components/EnterpriseCharts/EpAlterLine";

import {
  getPatentPie,
  getPatentLineRace,
  getPatentLine,
  getPatentMap,
  getNewsWordMap,
} from "@/utils/connector.js";

var elementResizeDetectorMaker = require("element-resize-detector");
var erd = elementResizeDetectorMaker({ strategy: "scroll" });

const _ = require("lodash");

const testLayout = [
  { x: 0, y: 0, w: 7, h: 16, i: 0 },
  { x: 0, y: 30, w: 4, h: 16, i: 1 },
  { x: 4, y: 30, w: 4, h: 16, i: 2 },
  { x: 5, y: 16, w: 4, h: 14, i: 3 },
  { x: 8, y: 30, w: 4, h: 16, i: 4 },
  { x: 9, y: 16, w: 3, h: 14, i: 5 },
  { x: 0, y: 16, w: 5, h: 14, i: 6 },
  { x: 7, y: 0, w: 5, h: 16, i: 7 },
];

export default {
  name: "Display",
  components: {
    PatentPie,
    PatentLineRace,
    PatentLine,
    PatentMap,
    EnterpriseBar,
    EpDistributionPie,
    EpAlterLine,
    NewsWordMap,
  },
  data() {
    return {
      layout: JSON.parse(JSON.stringify(testLayout)),
      draggable: false,
      resizable: false,
      loading: true,
      picDict: {
        0: {
          comp: "patent-pie",
          name: "2021年2月新疆专利授权状况统计",
          info: {
            num_patent_types: [],
            num_applicants_types: [],
          },
          fetch: getPatentPie,
        },
        1: {
          comp: "patent-line-race",
          name: "2020年各地州专利授权状况年累计变化",
          info: {
            time_x_label: [],
            sum: [],
          },
          fetch: getPatentLineRace,
        },
        2: {
          comp: "patent-line",
          name: "新疆三种专利每月申请受理趋势变化",
          info: {
            dataset: {
              source: [],
            },
          },
          fetch: getPatentLine,
        },
        3: {
          comp: "patent-map",
          name: "2021年2月新疆各地州专利授权情况",
          info: {
            num: [],
          },
          fetch: getPatentMap,
        },
        4: {
          comp: "news-word-map",
          name: "市场监督新闻动态",
          info: [],
          fetch: getNewsWordMap,
        },
        5: { comp: "ep-distribution-pie" },
        6: { comp: "ep-alter-line" },
        7: { comp: "enterprise-bar" },
      },
    };
  },
  mounted() {
    this.fetchAllData();
    this.layout.map((item) => {
      erd.listenTo(this.$refs[`chart-cont-${item.i}`], () => {
        this.$nextTick(() => {
          this.deHandleResize(item.i);
        });
      });
    });
    setTimeout(() => {
      for (const i in this.picDict) {
        this.$refs[`chart-${i}`].chart?.resize();
        this.loading = false;
      }
    }, 1200);
    setInterval(this.fetchAllData, 60000);
  },
  methods: {
    handleResize(i) {
      this.$refs[`chart-${i}`].chart.resize();
    },
    fetchAllData() {
      for (const index in this.picDict) {
        if (this.picDict[index].fetch) {
          this.picDict[index]
            .fetch()
            .then((info) => (this.picDict[index].info = info));
        }
      }
    },
    makeFullScreen() {
      console.log("did");
      const fullarea = this.$refs["screen"];
      if (fullarea.requestFullscreen) {
        fullarea.requestFullscreen();
      } else if (fullarea.webkitRequestFullScreen) {
        fullarea.webkitRequestFullScreen();
      } else if (fullarea.mozRequestFullScreen) {
        fullarea.mozRequestFullScreen();
      } else if (fullarea.msRequestFullscreen) {
        // IE11
        fullarea.msRequestFullscreen();
      }
    },
  },
  created() {
    this.deHandleResize = _.debounce(this.handleResize, 200);
  },
  unmounted() {
    this.deHandleResize.cancel();
  },
};
</script>


<style>
.chart-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}

.columns {
  -moz-columns: 120px;
  -webkit-columns: 120px;
  columns: 120px;
}
.vue-resizable-handle {
  z-index: 5000;
  position: absolute;
  width: 20px;
  height: 20px;
  bottom: 0;
  right: 0;
  background: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/Pg08IS0tIEdlbmVyYXRvcjogQWRvYmUgRmlyZXdvcmtzIENTNiwgRXhwb3J0IFNWRyBFeHRlbnNpb24gYnkgQWFyb24gQmVhbGwgKGh0dHA6Ly9maXJld29ya3MuYWJlYWxsLmNvbSkgLiBWZXJzaW9uOiAwLjYuMSAgLS0+DTwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+DTxzdmcgaWQ9IlVudGl0bGVkLVBhZ2UlMjAxIiB2aWV3Qm94PSIwIDAgNiA2IiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjojZmZmZmZmMDAiIHZlcnNpb249IjEuMSINCXhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiDQl4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjZweCIgaGVpZ2h0PSI2cHgiDT4NCTxnIG9wYWNpdHk9IjAuMzAyIj4NCQk8cGF0aCBkPSJNIDYgNiBMIDAgNiBMIDAgNC4yIEwgNCA0LjIgTCA0LjIgNC4yIEwgNC4yIDAgTCA2IDAgTCA2IDYgTCA2IDYgWiIgZmlsbD0iIzAwMDAwMCIvPg0JPC9nPg08L3N2Zz4=");
  background-position: bottom right;
  padding: 0 3px 3px 0;
  background-repeat: no-repeat;
  background-origin: content-box;
  box-sizing: border-box;
  cursor: se-resize;
}

.vue-grid-item.resizing {
  opacity: 0.9;
}
.vue-grid-item .text {
  font-size: 24px;
  text-align: center;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  height: 24px;
}
.vue-grid-item .minMax {
  font-size: 12px;
}
.vue-grid-item .add {
  cursor: pointer;
}
.remove {
  position: absolute;
  right: 2px;
  top: 0;
  cursor: pointer;
}

.subtitle-text {
  font-size: 16px;
  font-weight: 700;
}
</style>