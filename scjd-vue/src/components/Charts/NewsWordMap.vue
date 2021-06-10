<template>
  <div :style="{ height: height, width: width }" ref="news-word-map-cont"></div>
</template>

<script>
/*
  组件名：NewsWordMAp
  功能：展示网站上部分数据的词频，得到其云图
  接收参数：
    width,height为div的尺寸
    info：绘图所必须的数据，用对象的方式存储
      接受数据格式为
      [
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
      ]
  */
import WordCloud from "wordcloud";
import resize from "./mixins/resize";


export default {
  name: "NewsWordMap",
  mixins: [resize],
  props: {
    height: String,
    width: String,
    info: {
      type: Array,
    },
  },
  data() {
    return {
      chart: { resize: () => this.resize() },
    };
  },
  watch: {
    info(){
      this.resize()
    }
  },
  methods: {
    resize() {
      WordCloud(this.$refs["news-word-map-cont"], {
        list: this.info,
        maxRotation: 0,
        minRotation: 0,
        fontWeight: 300,
        classes: "web-font"
      });
    },
  },
};
</script>

<style>
@font-face {
  font-family: 'webfont';
  font-display: swap;
  src: url('//at.alicdn.com/t/webfont_bvdfgr3u05u.eot'); /* IE9*/
  src: url('//at.alicdn.com/t/webfont_bvdfgr3u05u.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
  url('//at.alicdn.com/t/webfont_bvdfgr3u05u.woff2') format('woff2'),
  url('//at.alicdn.com/t/webfont_bvdfgr3u05u.woff') format('woff'), /* chrome、firefox */
  url('//at.alicdn.com/t/webfont_bvdfgr3u05u.ttf') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+*/
  url('//at.alicdn.com/t/webfont_bvdfgr3u05u.svg#NotoSansHans-DemiLight') format('svg'); /* iOS 4.1- */
}

.web-font{
    font-family:"webfont" !important;
    -webkit-font-smoothing: antialiased;
    -webkit-text-stroke-width: 0.2px;
    -moz-osx-font-smoothing: grayscale;
}
</style>