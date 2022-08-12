<template>
  <div>
    <switches class="transmission" v-model="drive" :text-disabled="'R'" :text-enabled="'D'"></switches>
    <div class="appliances">
      <div>POWER: {{power + '%'}}</div>
      <div>SELECTED GEAR: {{drive ? 'D' : 'R'}}</div>
      <div>{{connectionState}}</div>
      <button @click="connect">CONNECT</button>
    </div>
    <div class="power-container stick-container">
      <div id="power-slider" ref="power-slider"></div>
    </div>
    <div class="video-wrap">
      <video ref="video" :height="height"></video>
    </div>
    <div class="direction-container stick-container">
      <div id="balance-slider" ref="balance-slider"></div>
    </div>
    <div class="turn-container">
      <a v-touch:start="turnLeft" v-touch:end="endHandler" class="std-btn">LEFT</a>
      <a v-touch:start="turnRight" v-touch:end="endHandler" class="std-btn">RIGHT</a>
    </div>
  </div>
</template>

<script>
  import { mapMutations, mapState } from 'vuex';
  import store from '../../configureStore';
  import Switches from 'vue-switches';
  import VueSlider from 'vue-slider-component';
  import 'vue-slider-component/theme/antd.css';
  import '../../assets/thema.scss';
  import RTC from "../../RTC";
  import * as noUiSlider from 'nouislider/distribute/nouislider.js';
  import '../../assets/nouislider.css';

  const floor = num => Math.floor(num * 100) / 100;

  export default {
    name: "mobileDisplay",
    store: store,
    props: ['se', 'webrtc', 'videoStream', 'dataChannel'],
    data() {
      return {
        timer: null,
        power: 0,
        direction: 0,
        drive: true,
        left: 0,
        right: 0,
        channel: null
      }
    },
    computed: {
      ...mapState(['connectionState']),
      width() {
        return window.innerWidth;
      },
      height() {
        return window.innerHeight;
      }
    },
    methods: {
      ...mapMutations(['setFetching', 'setConnectionState']),
      dragEnd(index) {
        this.direction = 0;
      },
      connect() {
        this.setFetching(true);
        this.webrtc.createOffer();
      },
      run() {
        this.timer = setInterval(() => {
          const now = new Date();
          const power = this.power * 0.01;
          const direction = this.drive ? 1 : -1;
          let left = floor(this.left * direction * power);
          let right = floor(this.right * direction * power);
          const delta = left - right;
          if (delta && !this.notSimilarSign(left, right)) {
            const absDelta = Math.abs(delta);
            if (delta > 0) left = left + absDelta > 1 ? 1 : left + absDelta;
            else right = right + absDelta > 1 ? 1: right + absDelta;
          }

          //console.log('T: ', [floor(left), floor(right)]);
          this.dataChannel.send(JSON.stringify({
            //time: `${now.toLocaleTimeString()}: ${now.getMilliseconds()}`,
            data: [floor(left), floor(right)]
          }));
        }, 70);
      },
      updateSlider: function updateSlider() {
        this.$refs['power-slider'].noUiSlider.set([this.minRange, this.maxRange]);
      },
      turnLeft() {
        this.right = 1;
        this.left = -1;
      },
      turnRight() {
        this.left = 1;
        this.right = -1;
      },
      endHandler() {
        this.left = 1;
        this.right = 1;
      },
      notSimilarSign(a, b) {
        return (a > 0 && b < 0) || (a < 0 && b > 0);
      }
    },
    watch: {
      videoStream(stream) {
        if (stream) {
          this.$refs.video.srcObject = stream;
          this.$refs.video.play();
        }
      },
      dataChannel(channel) {
        if (channel) {
          this.run();
          this.setFetching(false);
        } else {
          clearInterval(this.timer);
          this.timer = null;
        }
      },
      direction(value) {
        if(value > 0) {
          this.left = 1;
          this.right = floor(1 - value);
        } else if (value < 0) {
          this.right= 1;
          this.left = floor(1 + value);
        } else {
          this.left = 1;
          this.right = 1;
        }
      }
    },
    mounted() {

      noUiSlider.create(this.$refs['power-slider'], {
        start: 0,
        step: 1,
        orientation: 'vertical',
        direction: 'rtl',
        range: {
          min: 0,
          max: 100
        }
      });

      noUiSlider.create(this.$refs['balance-slider'], {
        min: -1,
        max: 1,
        step: 0.01,
        start: 0,
        animate: false,
        range: {
          min: -1,
          max: 1
        }
      });

      this.$refs['power-slider'].noUiSlider.on('update',(values, handle) => this.power = parseInt(values[handle]));
      this.$refs['power-slider'].noUiSlider.on('end',() => this.$refs['power-slider'].noUiSlider.set(0));

      this.$refs['balance-slider'].noUiSlider.on('update',(values, handle) => this.direction = parseFloat(values[handle]));
      this.$refs['balance-slider'].noUiSlider.on('end', () => this.$refs['balance-slider'].noUiSlider.set(0));

      //this.run();
    },
    components: {
      VueSlider,
      Switches
    }
  }
</script>

<style lang="scss" scoped>
  .video-wrap {
    //border: 1px solid #00F601;
    margin: 0 auto;
    display: block;
    position: relative;
    width: 480px;
    height: calc(100vh - 2px);
    video {
      height: 100%;
      width: 100%;
      position: static;
      display: block;
    }
    &:before {
    }
  }
  .transmission {
    position: absolute;
    left: 15px;
    top: 15px;
    > div{
      height: 35px;
      width: 56px;
      &:after {
        height: 32px;
        width: 32px;
      }
    }
  }

  .power-container {
    left: 5%;
    z-index: 1;
  }
  .direction-container {
    right: 5%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .stick-container {
    position: absolute;
    top: 50%;
    border: 2px solid #00F601;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin-top: -70px;
  }
  .power-slider {
    margin: 10px auto;
  }
  .appliances {
    position: absolute;
    right: 10px;
    top: 5px;
    font-size: 21px;
    z-index: 1;
  }
  button {
    font-size: 24px;
    margin-top: 6px;
  }
  #power-slider {
    margin: 0 auto;
    height: 150px;
  }
  #balance-slider {
    width: 150px;
  }
  .turn-container {
    position: absolute;
    right: 20px;
    bottom: 20px;
    display: flex;
    .std-btn {
      width: 80px;
      height: 35px;
      border: 1px solid #00F601;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2px;
      color: #000000;
      text-decoration: none;
      background: #00F601;
      margin-right: 1px;
      &:last-child {
        margin-right: 0;
      }
      &:active {
        background: #000000;
        color: #00F601;
      }
    }
  }
</style>



