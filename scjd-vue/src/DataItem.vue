<template>
  <el-page-header
    class="manage-header"
    @back="this.$router.back()"
    content="数据项目详情"
  />
  <div class="data-detail">
    <div class="data-detail-header">
      <div class="data-detail-header-left">
        <div class="data-detail-header-left-title">
          {{ (item && item.name) || "数据项目名称" }}
        </div>
        <div>我觉得这里还可以加点更新日期什么的</div>
        <el-space
          class="data-detail-header-left-buttons"
          :size="16"
          alignment="start"
          wrap="true"
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
          >
            {{ item && item.display ? "在数据大屏中移除" : "在数据大屏显示" }}
          </el-button>
          <el-button
            type="success"
            round
            plain
            icon="el-icon-upload2"
            size="small"
          >
            更新数据内容
          </el-button>
          <el-button
            type="danger"
            round
            plain
            icon="el-icon-delete"
            size="small"
          >
            删除数据项目
          </el-button>
        </el-space>
      </div>
      <el-card v-loading="loading" class="data-detail-header-card">
        <component
          class="data-detail-header-card-graph"
          v-if="item && `${item.type}`"
          :is="typeDict[item.type]"
          :ref="`chart-${this.$route.params.id}`"
          :id="'' + this.$route.params.id"
          width="720px"
          height="420px"
          :info="cardData"
        >
        </component>
        <div v-else>
          <plus class="data-detail-header-card-empty-icon" />
          <div class="data-detail-header-card-empty-text">
            单击添加新数据卡片
          </div>
        </div>
      </el-card>
    </div>
    <el-tabs class="data-detail-tab" v-model="activeTab">
      <el-tab-pane label="数据历史" name="data-history">
        <el-table :data="history"> 
            <el-table-column prop="time" label="更新时间"/>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="数据内容" name="data-detail">数据内容</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getDataItem, getCardByID } from "@/utils/connector";
import { parseTime } from "@/utils/index"
import { Plus } from "@element-plus/icons";

import PatentPie from "@/components/Charts/PatentPie";
import PatentLineRace from "@/components/Charts/PatentLineRace";
import PatentLine from "@/components/Charts/PatentLine";
import PatentMap from "@/components/Charts/PatentMap";
import NewsWordMap from "@/components/Charts/NewsWordMap";
import EnterpriseBar from "@/components/EnterpriseCharts/EnterpriseBar";
import EpDistributionPie from "@/components/EnterpriseCharts/EpDistributionPie";
import EpAlterLine from "@/components/EnterpriseCharts/EpAlterLine";

export default {
  name: "DataItem",
  components: {
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
      activeTab: "data-history",
      item: {},
      history: [],
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
    this.loading = true;
    Promise.all([
      getDataItem(this.$route.params.id),
      getCardByID(this.$route.params.id),
    ]).then(([dataitem, carddata]) => {
      this.item = dataitem;
      this.cardData = carddata.info;
      if(dataitem && dataitem.history){
          this.history = dataitem.history.map(item => {
              item.time = parseTime(new Date(item.timestamp));
              return item
          })
      }
      console.log(dataitem)
      this.loading = false;
    });
  },
  methods: {
    onCardClick() {
      console.log("click");
    },
  },
};
</script>

<style>
.manage-header {
  padding: 24px;
}

.data-detail {
  padding: 0 24px;
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
  transform: translate(-25%, -25%) scale(50%);
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
</style>