<template>
  <div :style="{ height: height, width: width }" ref="news-word-map-cont"></div>
</template>

<script>
import WordCloud from "wordcloud";

export default {
  name: "NewsWordMap",
  props: {
    height: String,
    width: String,
    info: {
      type: Object,
    },
  },
  data() {
    return {
      mapList: [
        ["工作", 76],
        ["发展", 68],
        ["质量", 61],
        ["文化", 56],
        ["党史", 48],
        ["企业", 47],
        ["学习", 46],
        ["会议", 44],
        ["润疆", 43],
        ["质量奖", 39],
        ["教育", 37],
        ["气象", 34],
        ["开展", 32],
        ["坚持", 28],
        ["深入", 26],
        ["能源", 25],
        ["服务", 25],
        ["组织", 25],
      ],
      chart: { resize: () => this.resize() },
    };
  },
  methods: {
    resize() {
      WordCloud(this.$refs["news-word-map-cont"], {
        list: this.mapList,
        maxRotation: 0,
        minRotation: 0,
      });
    },
  },
};
</script>

<style>
</style>