import {createApp} from 'vue';
import App from './App.vue';

import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';

import VueGridLayout from 'vue-grid-layout'

const app = createApp(App);

app.use(ElementPlus);

app.use(VueGridLayout)

app.mount('#app');