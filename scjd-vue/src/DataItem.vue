<template>
  <div class="page-container">
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
          <el-card v-loading="cardLoading" class="data-detail-header-card">
            <component
              class="data-detail-header-card-graph"
              v-if="item && `${item.type}` && cardData"
              :is="typeDict[item.type]"
              :ref="`chart-${this.$route.params.id}`"
              :id="'' + this.$route.params.id"
              width="720px"
              height="420px"
              :info="cardData"
            >
            </component>
            <div v-else>
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
import {Plus} from "@element-plus/icons";

import PatentPie from "@/components/Charts/PatentPie";
import PatentLineRace from "@/components/Charts/PatentLineRace";
import PatentLine from "@/components/Charts/PatentLine";
import PatentMap from "@/components/Charts/PatentMap";
import NewsWordMap from "@/components/Charts/NewsWordMap";
import EnterpriseBar from "@/components/EnterpriseCharts/EnterpriseBar";
import EpDistributionPie from "@/components/EnterpriseCharts/EpDistributionPie";
import EpAlterLine from "@/components/EnterpriseCharts/EpAlterLine";
import UploadDialog from "@/components/ManageComp/UploadDialog";

export default {
  name: "DataItem",
  components: {
    UploadDialog,
    Plus,
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
      loading: true,
      cardLoading: true,
      updateDialogVisible: false,
      replaceDialogVisible: false,
      activeTab: "data-history",
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
      },
      cardData: null,
    };
  },
  created() {
    this.fetchAllData(this.$route.params.id)
  },
  methods: {
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
        if (''+dataitem.type && dataitem.history.timestamp) {
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
      console.log("click");
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
    }
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

.upload-box {
  text-align: center;
}

.scroll_inner {
  height: 100%;
  padding: 0 24px;
}
</style>