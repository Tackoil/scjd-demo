import {createApp} from 'vue';
import App from './App.vue';

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/saga-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';

const app = createApp(App);

app.use(PrimeVue);
app.config.globalProperties.$primevue = {ripple: true};

app.use(ElementPlus);

app.mount('#app');