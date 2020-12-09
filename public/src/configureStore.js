import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    isConnect: false,
    config: {},
    error: null,
    fetching: false,
    connectionState: null
  },
  mutations: {
    setConfig(state, config) {
      state.config = config;
    },
    setAuth(state, value) {
      state.isConnect = value;
    },
    setFetching(state, value) {
      state.fetching = value;
    },
    setConnectionState(state, value) {
      state.connectionState = value;
    }
  }
});

export default store
