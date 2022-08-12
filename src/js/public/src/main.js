import Vue from 'vue';
import Vuex from 'vuex';
import Vue2TouchEvents from 'vue2-touch-events';
import control from './components/control';
import platform from './components/platform';
import "babel-polyfill";

Vue.use(Vue2TouchEvents);
Vue.use(Vuex);
Vue.config.productionTip = false;

new Vue({
  el: '#app',
  data: {
  },
  components: {
    control,
    platform
  }
});
