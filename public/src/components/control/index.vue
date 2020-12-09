<template>
  <div>
    <div v-if="isConnect">
      <mobile-display :se="se"
                      :webrtc="webrtc"
                      :videoStream="videoStream"
                      :dataChannel="dataChannel" v-if="detectMob"></mobile-display>
      <display
          :se="se"
          :webrtc="webrtc"
          :videoStream="videoStream"
          :dataChannel="dataChannel" v-else></display>
    </div>
    <auth v-else @submit="connect"></auth>

    <div v-if="fetching" class="fetching">LOADING...</div>

    <error-modal v-if="isConnError" />
  </div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex';
  import SignalEmitter from '../../SignalEmitter';
  import RTC from '../../RTC';
  import auth from './auth';
  import display from './display';
  import mobileDisplay from "./mobileDisplay";
  import errorModal from "./errorModal";
  import store from '../../configureStore';
  import config from "../../../config";

  export default {
    name: "control",
    store: store,
    components: {
      auth,
      display,
      mobileDisplay,
      errorModal
    },
    data() {
      return {
        videoStream: null,
        dataChannel: null,
        isConnError: false
      }
    },
    computed: {
      ...mapState(['config', 'isConnect', 'fetching', 'connectionState']),
      detectMob() {
        const toMatch = [
          /Android/i,
          /webOS/i,
          /iPhone/i,
          /iPad/i,
          /iPod/i,
          /BlackBerry/i,
          /Windows Phone/i
        ];

        return toMatch.some((toMatchItem) => {
          return navigator.userAgent.match(toMatchItem);
        });
      }
    },
    methods: {
      ...mapMutations(['setAuth', 'setFetching', 'setConnectionState']),
      connect(id) {
        this.setFetching(true);
        this.se = new SignalEmitter({
          id: id,
          isControl: true,
          signalServer: this.config.signalServer,
        });

        this.se.connection.onopen = () => {
          store.commit('setAuth', true);
          this.createRTC();
          this.setFetching(false);
        };
      },
      createRTC() {
        console.log('SE: ', this.se);
        this.webrtc = new RTC({isControl: true}, this.se);

        this.webrtc.on('videoStream', srcObject => {
          this.videoStream = srcObject;
          this.setFetching(false);
        });

        this.webrtc.on('dataChannel', dataChannel => this.dataChannel = dataChannel);
        this.webrtc.on('connectionStateChange', this.setConnectionState);

      }
    },
    created() {
      store.commit('setConfig', config);
    },
    watch: {
      connectionState(conState) {
        console.log('CON_STATE: ', conState);
        this.isConnError = ['failed', 'closed', 'disconnected'].some(state => state === conState);
        if (this.isConnError) {
          this.dataChannel = null;
          this.videoStream = null;
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  .fetching {
    position: fixed;
    z-index: 1;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #000000;
  }
</style>
