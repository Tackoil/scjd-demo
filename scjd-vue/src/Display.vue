<template>
  <div
    style="width: 100%; height: 100%; display: flex; flex-flow: column"
    v-loading="loading"
    ref="outterBox"
  >
    <div style="flex: 0; margin: 10px 10px 0 10px">
      <el-button
        class="el-icon-data-board"
        size="small"
        plain
        circle
        @click="makeFullScreen"
      />
      <el-button
        :class="edit ? 'el-icon-document-checked' : 'el-icon-edit-outline'"
        size="small"
        :type="edit ? 'success' : null"
        plain
        round
        @click="handleEdit"
      >
        {{ edit ? " 保存 " : " 编辑模式 " }}
      </el-button>
    </div>
    <div
      style="
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        flex-grow: 1;
        overflow: hidden;
      "
      ref="content"
      class="bg"
    >
      <el-scrollbar>
        <grid-layout
          :layout="layout"
          :col-num="16"
          :row-height="60"
          :is-draggable="edit"
          :is-resizable="edit"
          vertical-compact
          :use-css-transforms="true"
          @layout-updated="handleLayoutReady"
        >
          <grid-item
            v-for="item in layout"
            :key="item.i"
            :x="item.x"
            :y="item.y"
            :w="item.w"
            :h="item.h"
            :i="item.i"
            :minW="item.minW"
            :minH="item.minH"
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
                <span
                  class="subtitle-text"
                  style="display: flex; align-items: center"
                >
                  <span style="flex: 1; font-size: 22px"
                  >{{ cardInfo[item.i]?.name }}
                  </span>
                  <el-popconfirm
                    title="是否移除卡片？移除卡片不会删除相关数据项目。"
                    @confirm="handleDelete(item.i)"
                  >
                    <template #reference>
                      <el-button
                        v-show="edit"
                        icon="el-icon-delete"
                        size="mini"
                        circle
                      >
                      </el-button>
                    </template>
                  </el-popconfirm>
                </span>
              </template>
              <div :ref="`chart-cont-${item.i}`" style="height: 100%">
                <component
                  :is="typeDict[cardInfo[item.i]?.type]"
                  :ref="`chart-${item.i}`"
                  :id="'' + item.i"
                  width="100%"
                  height="100%"
                  :info="cardInfo[item.i]?.info"
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
import CustomLine from "@/components/Charts/CustomLine";
import CustomHisto from "@/components/Charts/CustomHisto";
import CustomPie from "@/components/Charts/CustomPie";

import {getLayout, getCardByID, updateLayout} from "@/utils/connector.js";

var elementResizeDetectorMaker = require("element-resize-detector");
var erd = elementResizeDetectorMaker({strategy: "scroll"});

const _ = require("lodash");

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
    CustomLine,
    CustomHisto,
    CustomPie
  },
  data() {
    return {
      fullscreen: false,
      layout: [],
      cardInfo: {},
      edit: false,
      loading: false,
      timer: null,
      typeDict: {
        0: "PatentPie",
        1: "PatentLineRace",
        2: "PatentLine",
        3: "PatentMap",
        4: "EnterpriseBar",
        5: "EpDistributionPie",
        6: "EpAlterLine",
        7: "NewsWordMap",
        8: "CustomLine",
        9: "CustomHisto",
        10: "CustomPie"
      },
    };
  },
  created() {
    this.throHandleResize = _.throttle(this.handleResize, 200);
    this.fetchLayout();
  },
  mounted() {
    this.timer = setInterval(() => {
      this.fetchAllData();
    }, 60000);
  },
  beforeUnmount() {
    clearInterval(this.timer);
    this.throHandleResize.cancel();
  },
  methods: {
    handleLayoutReady(layout) {
      if (layout.length) {
        this.fetchAllData();
        setTimeout(() => {
          this.layout.forEach((item) => {
            if (this.$refs[`chart-cont-${item.i}`]) {
              erd.listenTo(this.$refs[`chart-cont-${item.i}`], () => {
                this.$nextTick(() => {
                  this.throHandleResize(item.i);
                });
              });
            }
            if (this.$refs[`chart-${item.i}`]) {
              this.$refs[`chart-${item.i}`].chart?.resize();
            }
          });
        }, 0);
      }
    },
    handleResize(i) {
      this.$refs[`chart-${i}`].chart.resize();
    },
    fetchLayout() {
      getLayout().then((res) => {
        this.layout = res;
      });
    },
    fetchAllData() {
      console.log("fetch!");
      this.layout.forEach((item) => {
        getCardByID(item.i).then((info) => {
          this.cardInfo[item.i] = info;
        });
      });
    },
    handleEdit() {
      if (this.edit) {
        updateLayout(this.layout).then(() => {
          this.$message.success("保存成功")
        }).catch(() => {
          this.$message.success("保存失败")
        })
      }
      this.edit = !this.edit;
    },
    handleDelete(i) {
      const index = this.layout.findIndex((item) => item.i === i);
      if(index !== -1){
        updateLayout(this.layout, [i]).then(() => {
          erd.uninstall(this.$refs[`chart-cont-${i}`])
          this.layout.splice(index, 1);
          this.$message.success("移除成功")
        }).catch((err) => {
          console.error(err);
          this.$message.error("移除失败")
        })
      }
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