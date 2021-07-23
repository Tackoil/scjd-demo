<template>
  <div style="width: 100%; height: 100%; display: flex; flex-flow: column;" v-loading="loading" ref="outterBox">
    <div style="flex: 0; margin: 10px 10px 0 10px;">
      <el-button 
        :class=" edit ? 'el-icon-document-checked' : 'el-icon-edit-outline'" 
        size="small"  
        :type="edit ? 'success' : null" plain round @click="handleEdit"> {{edit ? " 保存 " : " 编辑模式 "}} </el-button>
    </div>
    <div v-if="false" style="flex: 0">
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
    <div style="margin-left: auto; margin-right: auto; width: 100%; flex-grow: 1; overflow: hidden" ref="content" class="bg">
      <el-scrollbar >
      <grid-layout
        :layout="layout"
        :col-num="16"
        :row-height="60"
        :is-draggable="edit"
        :is-resizable="edit"
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
              display: flex;
              box-sizing: border-box;
              flex-direction: column;
            "
            :body-style="{ flex: 1 }"
          >
            <template #header>
              <span class="subtitle-text" style="display: flex; align-items: center"
                > 
                  <span style="flex: 1; font-size: 22px">{{ picDict[item.i].name }} </span>
                <el-button v-show="edit" icon="el-icon-delete" size="mini" circle> </el-button>
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
      </el-scrollbar>
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
  getEnterpriseBar,
  getEpAlterLine,
  getEpDistributionPie,
} from "@/utils/connector.js";

var elementResizeDetectorMaker = require("element-resize-detector");
var erd = elementResizeDetectorMaker({ strategy: "scroll" });

const _ = require("lodash");

const testLayout = [
  { x: 0, y: 0, w: 7, h: 9, i: 0 },
  { x: 0, y: 9, w: 7, h: 9, i: 1 },
  { x: 12, y: 0, w: 4, h: 7, i: 2 },
  { x: 11, y: 14, w: 5, h: 8, i: 3 },
  { x: 0, y: 18, w: 7, h: 4, i: 4 },
  { x: 7, y: 14, w: 4, h: 8, i: 5 },
  { x: 7, y: 7, w: 9, h: 6, i: 6 },
  { x: 7, y: 0, w: 5, h: 7, i: 7 },
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
      fullscreen: false,
      layout: JSON.parse(JSON.stringify(testLayout)),
      edit: false,
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
        5: {
          comp: "ep-distribution-pie",
          name: "各行业企业分布情况",
          info: [],
          fetch: getEpDistributionPie,
        },
        6: {
          comp: "ep-alter-line",
          name: "企业注册、变更、注销统计",
          info: {
            time_x_label: [],
            sum: [],
          },
          fetch: getEpAlterLine,
        },
        7: {
          comp: "enterprise-bar",
          name: "市场主体产业数目变化",
          info: {
            time_x_label: [],
            sum: [],
          },
          fetch: getEnterpriseBar,
        },
      },
    };
  },
  mounted() {
    this.fetchAllData();
    this.layout.forEach((item) => {
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
    handleEdit(){
      if(this.edit) {
        // save new setting
      }
      this.edit = ! this.edit;
    },
    makeFullScreen() {
      this.fullscreen = true;
      const fullarea = this.$refs["content"];
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
.bg {
  background-color: rgb(245, 248, 251);
}

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

.el-scrollbar__view {
  height: 100%;
}
</style>