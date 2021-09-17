<template>
  <div class="page-container" ref="pageContainer">
    <el-page-header
      class="manage-header"
      @back="this.$router.back()"
      content="数据项目详情"
    />
    <div class="data-detail" v-loading="loading">
      <el-scrollbar view-class="scroll_inner">
        <div class="data-detail-header">
          <div class="data-detail-header-left">
            <div class="data-detail-header-left-title">
              {{ (item && item.name) || "数据项目名称" }}
            </div>
            <div>最近更新时间：{{ latestHistoryTime }}</div>
            <el-space
              class="data-detail-header-left-buttons"
              :size="16"
              alignment="start"
              :wrap="true"
            >
              <el-button
                :type="item && item.display ? 'warning' : 'primary'"
                round
                :icon="
              item && item.display
                ? 'el-icon-remove-outline'
                : 'el-icon-data-line'
            "
                size="small"
                @click="handleToggleDisplay"
              >
                {{ item && item.display ? "在数据大屏中移除" : "在数据大屏显示" }}
              </el-button>
              <el-button
                type="success"
                round
                plain
                icon="el-icon-upload2"
                size="small"
                @click="() => {updateDialogVisible = true}"
              >
                更新数据内容
              </el-button>
              <el-button
                v-if="item.removable"
                type="danger"
                round
                plain
                icon="el-icon-delete"
                size="small"
                @click="handleDelete"
              >
                删除数据项目
              </el-button>
            </el-space>
          </div>
          <el-card v-loading="cardLoading" class="data-detail-header-card" :body-style="{'position': 'relative'}">
            <div
              class="data-detail-header-card-mask"
              v-if="item.removable && item && item.type !== null && cardData"
              @click="handleCardRemove">
              <el-icon :size="48" color="#FFFFFF" >
                <delete />
              </el-icon>
            </div>
            <component
              class="data-detail-header-card-graph"
              v-if="item && item.type !== null && cardData"
              :is="typeDict[item.type]"
              :ref="`chart-${this.$route.params.id}`"
              :id="'' + this.$route.params.id"
              width="720px"
              height="420px"
              :info="cardData"
            >
            </component>
            <div v-else @click="onCardClick">
              <plus class="data-detail-header-card-empty-icon"/>
              <div class="data-detail-header-card-empty-text">
                单击添加新数据卡片
              </div>
            </div>
          </el-card>
        </div>
        <el-tabs class="data-detail-tab" v-model="activeTab">
          <el-tab-pane label="数据历史" name="data-history">
            <el-table :data="history" class="data-detail-pane-table">
              <el-table-column prop="time" label="更新时间"/>
              <el-table-column label="操作" fixed="right">
                <template #default="scope">
                  <el-space>
                    <el-button
                      size="mini"
                      type="text"
                      :disabled="!scope.row || !scope.row.file_url"
                      @click="handleDownload(this.$route.params.id, scope.row.timestamp)">下载
                    </el-button>
                    <el-button
                      size="mini"
                      type="text"
                      @click="() => {
                    this.uploadId = scope.row.id;
                    this.replaceDialogVisible = true;
                  }"
                    >
                      替换
                    </el-button>
                  </el-space>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-scrollbar >
    </div>
    <upload-dialog
      name="更新数据项目"
      v-model="updateDialogVisible"
      :itemID="$route.params.id"
      :timestamp="new Date().valueOf()"
      type="new"
      @success="handleUploadSuccess"
    >
    </upload-dialog>
    <upload-dialog
      name="替换数据项目"
      v-model="replaceDialogVisible"
      :uploadId="uploadId"
      type="update"
      @success="handleUploadSuccess"
    >
    </upload-dialog>
    <el-dialog
      title="新建数据卡片"
      v-model="addCardDialogVisible"
      destroy-on-close
      :close-on-click-modal="false"
      :before-close="handleAddCardCancel"
    >
      <el-steps :active="addStep" simple>
        <el-step
          title="选择数据卡片类型"
        ></el-step>
        <el-step
          title="预览数据卡片"
        ></el-step>
        <el-step
          title="设置数据卡片大小"
        ></el-step>
      </el-steps>
      <div class="addCard-container" v-if="addStep === 1">
        <div class="addCard-button-group">
          <div class="addCard-button" @click="() => {selectCardType('line')}">
            <svg class="addCard-button-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="80" height="80"><path d="M970.105263 970.105263H53.894737V53.894737h53.894737v862.315789h862.315789z" fill="#444A5C" p-id="1590"></path><path d="M668.294737 840.757895l-167.073684-161.684211H107.789474v-53.894737h414.989473l145.51579 140.126316 140.126316-140.126316h161.68421v53.894737h-140.126316zM107.789474 549.726316l-37.726316-37.726316L377.263158 204.8l215.578947 215.578947 323.368421-323.368421 37.726316 37.726316L592.842105 495.831579l-215.578947-215.578947z" fill="#333" p-id="1591"></path></svg>
            折线图
          </div>
          <div class="addCard-button" @click="() => {selectCardType('histo')}">
            <svg class="addCard-button-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="80" height="80"><path d="M700.631579 323.368421H53.894737V53.894737h646.736842v269.473684zM107.789474 269.473684h538.947368V107.789474H107.789474v161.68421zM970.105263 646.736842H53.894737V377.263158h916.210526v269.473684zM107.789474 592.842105h808.421052V431.157895H107.789474v161.68421zM592.842105 970.105263H53.894737v-269.473684h538.947368v269.473684z m-485.052631-53.894737h431.157894v-161.68421H107.789474v161.68421z" fill="#333" p-id="1451"></path></svg>
            柱状图
          </div>
          <div class="addCard-button" @click="() => {selectCardType('pie')}">
            <svg class="addCard-button-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="80" height="80"><path d="M512 53.894737C258.694737 53.894737 53.894737 258.694737 53.894737 512S258.694737 970.105263 512 970.105263 970.105263 765.305263 970.105263 512 765.305263 53.894737 512 53.894737zM916.210526 485.052632H528.168421L291.031579 172.463158C355.705263 134.736842 431.157895 107.789474 512 107.789474c215.578947 0 388.042105 167.073684 404.210526 377.263158z m-404.210526 431.157894C291.031579 916.210526 107.789474 732.968421 107.789474 512c0-123.957895 53.894737-231.747368 140.126315-307.2L501.221053 538.947368H916.210526c-16.168421 210.189474-188.631579 377.263158-404.210526 377.263158z" fill="#333" p-id="1312"></path></svg>
            饼图
          </div>
        </div>
      </div>
      <div class="addCard-container" v-else-if="addStep === 2">
        <component :is="typeDict[item.type]" :info="cardData" :style="{width: '100%', height: '400px'}"></component>
      </div>
      <div class="addCard-container" v-else>
        <div class="addCard-chart-setting-container">
          <grid-layout
            class="addCard-chart-preview"
            ref="miniContainer"
            style="flex: 1"
            :layout="layout"
            :col-num="16"
            :row-height="layoutRowHeight"
            :is-draggable="true"
            :is-resizable="true"
            vertical-compact
            :use-css-transforms="true"
            @layout-updated="handleLayoutReady"
          >
            <grid-item
              v-for="layoutItem in layout"
              :key="layoutItem.i"
              :x="layoutItem.x"
              :y="layoutItem.y"
              :w="layoutItem.w"
              :h="layoutItem.h"
              :i="layoutItem.i"
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
                  >{{ item.name }}
                  </span>
                </span>
                </template>
                <div :ref="`chart-cont-${layoutItem.i}`" style="height: 100%">
                  <component
                    :is="typeDict[item.type]"
                    :ref="`chart-${layoutItem.i}`"
                    :id="'' + layoutItem.i"
                    width="100%"
                    height="100%"
                    :info="cardData"
                  >
                  </component>
                </div>
              </el-card>
            </grid-item>
          </grid-layout>
          <div class="addCard-form">
            <el-form label-width="80px" size="small">
              <el-form-item label="宽度">
                <el-input-number
                  v-model="layout[0].w"
                  :min="1"
                  :max="16"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="高度">
                <el-input-number
                  v-model="layout[0].h"
                  :min="1"
                ></el-input-number>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
      <template #footer v-if="addStep === 2">
        <el-button @click="() => {this.addStep -= 1}"> 上一步 </el-button>
        <el-button @click="() => {this.addStep += 1}" type="primary"> 下一步 </el-button>
      </template>
      <template #footer v-else-if="addStep === 3">
        <el-button type="primary" @click="handleCardSave"> 完成 </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import {
  getDataItem,
  getDataItemHistory,
  downloadDatafileUrl,
  deleteDataItem, getDataParse, updateDataItem,
} from "@/utils/connector";
import {parseTime} from "@/utils"
import {Plus, Delete} from "@element-plus/icons";

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
import UploadDialog from "@/components/ManageComp/UploadDialog";


var elementResizeDetectorMaker = require("element-resize-detector");
var erd = elementResizeDetectorMaker({strategy: "scroll"});

const _ = require("lodash");

export default {
  name: "DataItem",
  components: {
    UploadDialog,
    Plus,
    Delete,
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
      loading: true,
      cardLoading: true,
      updateDialogVisible: false,
      replaceDialogVisible: false,
      addCardDialogVisible: false,
      activeTab: "data-history",
      addStep: 1,
      item: {},
      history: [],
      uploadId: "",
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
      cardData: null,
      layout: [{
        x: 0,
        y: 0,
        w: 16,
        h: 10,
        i: 0
      }],
      layoutRowHeight: 60,
    };
  },
  created() {
    this.throHandleResize = _.throttle(this.handleResize, 200);
    this.fetchAllData(this.$route.params.id)
  },
  mounted() {
    window.onresize = this.updateLayoutRowHeight;
  },
  updated() {
    this.updateLayoutRowHeight();
  },
  methods: {
    updateLayoutRowHeight() {
      console.log("!@#!@#", "update", this.$refs.pageContainer, this.$refs.miniContainer);
      if(this.$refs.miniContainer && this.$refs.miniContainer.$el.clientWidth) {
        const rate = this.$refs.pageContainer.clientWidth / this.$refs.miniContainer.$el.clientWidth;
        this.layoutRowHeight = 60 / rate;
        console.log("!@#!@#", "update", 60 / rate);
      }
    },
    fetchAllData(id) {
      this.loading = true;
      this.cardLoading = true;
      Promise.all([
        getDataItem(id),
        getDataItemHistory(id),
      ]).then(([dataitem, historydata]) => {
        this.item = dataitem;
        if (historydata) {
          this.history = historydata.map(item => {
            item.time = parseTime(new Date(item.timestamp));
            return item
          })
        }
        if (dataitem.type !== null && dataitem.history.timestamp) {
          this.loading = false;
          this.cardLoading = true;
          return getDataParse(id, dataitem.history.timestamp)
        }
      }).then(data => {
        this.cardData = data;
      }).finally(() => {
        this.loading = false;
        this.cardLoading = false;
      })
    },
    onCardClick() {
      if(this.history.length === 0){
        this.$message({
          type: 'error',
          message: '暂无数据，请先添加数据后创建数据卡片'
        })
      } else {
        this.addCardDialogVisible = true;
      }
    },
    selectCardType(type) {
      this.item = Object.assign({}, this.item, {
        type: {
          'line': 8,
          'histo': 9,
          'pie': 10
        }[type]
      })
      this.addStep += 1;
    },
    handleDownload(id, time) {
      const url = downloadDatafileUrl(id, time)
      const alink = document.createElement('a')
      alink.setAttribute("href", url)
      alink.click()
    },
    handleDelete() {
      if (this.$route.params.id) {
        this.$confirm('将永久删除该数据项目, 相关历史记录将一并删除，是否继续?', '删除数据项目', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(() => {
              deleteDataItem(this.$route.params.id).then(res => {
                if (res.code === 0) {
                  this.$message({
                    type: 'success',
                    message: '已删除'
                  })
                  this.$router.back()
                } else {
                  this.$message({
                    type: 'error',
                    message: res.msg || '删除失败'
                  })
                }
              })
            }
          )
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除',
            })
          })
      }
    },
    handleCardRemove() {
      if (this.$route.params.id) {
        this.$confirm('将永久删除该数据卡片, 相关历史记录不会被删除', '删除数据卡片', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(() => {
            updateDataItem(this.$route.params.id, {type: null, display: false}).then(() => {
                  this.$message.success("已删除");
                  this.fetchAllData(this.$route.params.id)
              }).catch(() => {
                this.$message.error("删除失败");
            })
            }
          )
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除',
            })
          })
      }
    },
    handleToggleDisplay() {
      this.item.display = !this.item.display;
      updateDataItem(this.$route.params.id, this.item).then(res => {
        if (res) {
          this.$message.success(`已在数据大屏上${this.item.display ? "显示" : "移除"}`)
        }
      }).catch(() => {
        this.item.display = !this.item.display;
      })
    },
    handleUploadSuccess(){
      if (this.$route.params.id) {
        this.fetchAllData(this.$route.params.id)
      }
    },
    handleCardSave() {
      updateDataItem(this.$route.params.id, {
        type: this.item.type,
        w: this.layout[0].w,
        h: this.layout[0].h,
        minw: this.layout[0].w,
        minh: this.layout[0].h,
      }).then(() => {
        this.$message.success("成功添加数据卡片");
        this.addCardDialogVisible = false;
        this.addStep = 1;
      }).catch(() => {
        this.$message.error("添加失败");
      })
    },
    handleAddCardCancel(done) {
      updateDataItem(this.$route.params.id, {type: null, display: false}).then(() => {
        this.item.type = null;
        this.item.display = false;
        this.addStep = 1;
        done();
      })
    },
    handleLayoutReady(layout) {
      if (layout.length) {
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
  },
  computed: {
    latestHistoryTime() {
      if (Array.isArray(this.history) && this.history.length !== 0) {
        const historyCopy = [...this.history];
        const res = historyCopy.sort((a, b) => b.timestamp - a.timestamp)[0].timestamp;
        return parseTime(new Date(res));
      } else {
        return "暂未更新";
      }
    }
  },
  watch: {
    item: function(newValue, oldValue){
      if(newValue.type !== oldValue.type && newValue.type !== null && newValue.history){
        updateDataItem(this.$route.params.id, newValue).then(() =>
          getDataParse(this.$route.params.id, newValue.history.timestamp)
        ).then(res => {
          this.cardData = res;
        }).catch(() => {
          updateDataItem(this.$route.params.id, Object.assign(newValue, {type: null}))
        })
      }
    },
  }
};
</script>

<style>
.page-container {
  display: flex;
  flex-flow: column;
  height: 100%;
}

.manage-header {
  padding: 24px;
}

.data-detail {
  flex: 1;
  overflow: hidden;
}

.data-detail-header {
  display: flex;
}

.data-detail-header-left {
  flex: 1;
}

.data-detail-header-left-title {
  font-size: 24px;
  line-height: 1.7;
}

.data-detail-header-left-buttons {
  margin-top: 16px;
}

.data-detail-header-card {
  width: 400px;
  height: 250px;
}

.data-detail-header-card .data-detail-header-card-mask {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  z-index: 999;
  top: -20px;
  left: -20px;
  width: 420px;
  height: 280px;
  transition: opacity ease-in-out .3s;
  opacity: 0;
  background-color: #333333;
}

.data-detail-header-card:hover .data-detail-header-card-mask {
  opacity: .8;
}

.data-detail-header-card-graph {
  transform: translate(-25%, -25%) scale(0.5);
}

.data-detail-header-card-empty-icon {
  margin-top: 75px;
  margin-left: 160px;
  width: 40px;
  height: 40px;
  align-self: center;
}

.data-detail-header-card-empty-text {
  text-align: center;
}

.data-detail-tab {
  margin: 16px 0;
}

.data-detail-pane-table {
  margin: 16px 0;
}

.addCard-container {
  padding: 30px 0 0 0;
}

.addCard-button-group {
  display: flex;
  align-self: center;
  justify-content: space-around;
}

.addCard-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 8px;
  width: 150px;
  height: 150px;
  border: 2px dashed #999;
  border-radius: 8px;
  transition: border ease-in 0.3s;
}

.addCard-button:hover {
  border: 2px dashed #039;
}

.addCard-button-icon {
  margin: 8px;
}

.addCard-chart {
  width: 100%;
  height: 100%;
}

.addCard-chart-setting-container {
   display: flex;
}

.addCard-form {
  display: flex;
  flex-direction: column;
  margin: 8px;
}

.upload-box {
  text-align: center;
}

.scroll_inner {
  height: 100%;
  padding: 0 24px;
}
</style>