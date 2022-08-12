<template>
  <div class="container">
    <div class="flex-center">
      <div class="video-wrap">
        <video ref="video"></video>
        <balance-panel @upd="updBalance"></balance-panel>
      </div>
    </div>
    <div class="info">
      <div class="col">
        <button @click="connect">CONNECT</button>
        <button>FULL SCREEN</button>
        <table>
          <tr><td>POWER: </td><td>{{power}}%</td></tr>
          <tr><td>left cat: </td><td>{{leftCat}}</td></tr>
          <tr><td>right cat: </td><td>{{rightCat}}</td></tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import RTC from '../../RTC';
  import balancePanel from './balancePanel';

  const floor = num => Math.floor(num * 100) / 100;

  export default {
    name: "display",
    props: ['se', 'webrtc'],
    data: () => ({
      video: false,
      power: 0,
      leftCat: 0,
      rightCat: 0,
      forward: 0,
      back: 0,
      channel: null
    }),
    methods: {
      connect() {
        this.webrtc.createOffer();
      },
      powerChange(event) {
        const delta = Math.floor(event.deltaY/100);
        let power = this.power;
        if (delta > 0) {
          power -= 5;
        } else {
          power += 5;
        }
        this.power = (power <= 100 && power >= 0) ? power : this.power;
      },
      run() {

        setInterval(() => {
          const now = new Date();
          const power = this.power * 0.01;
          const direction = this.forward || this.back;
          const left = floor(this.leftCat * direction * power);
          const right = floor(this.rightCat * direction * power);
          this.channel.send(JSON.stringify({
            time: `${now.toLocaleTimeString()}: ${now.getMilliseconds()}`,
            data: [left, right]
          }));
        }, 100);
      },
      updBalance(balance) {
        this.leftCat = balance.leftCat;
        this.rightCat = balance.rightCat;
      }
    },
    watch: {
      channel: function () {
        if (this.channel) {
          this.run();
        }
      }
    },
    created() {
      this.webrtc = new RTC({isControl: true}, this.se, srcObject => {
        this.video = true;
        this.$refs.video.srcObject = srcObject;
        this.$refs.video.play();
      }, dataChannel => this.channel = dataChannel);
      document.querySelector('body').addEventListener("wheel", this.powerChange);
      document.addEventListener("keyup", event => {
        if (event.isComposing || event.keyCode === 229) {
          return;
        }

        if (event.keyCode === 87) this.forward = 0;
        if (event.keyCode === 83) this.back = 0;
      });
      document.addEventListener("keydown", event => {
        if (event.isComposing || event.keyCode === 229) {
          return;
        }
        if (event.keyCode === 87) this.forward = 1;
        if (event.keyCode === 83) this.back = -1;
        console.log(event);
      });
    },
    components: {
      balancePanel
    }
  }
</script>

<style lang="scss" scoped>
  .flex-center {
    display: flex;
    justify-content: center;
  }
  .video-wrap {
    border: 1px solid #00F601;
    margin: 0 auto;
    display: block;
    position: relative;
    margin-top: 4px;
    height: 480px;
    video {
      height: 100%;
    }
    &:before {
      content: "";
      position: absolute;
      left: -3px;
      right: -3px;
      top: -3px;
      bottom: -3px;
      border: 1px solid #00F601;
    }
  }
  .info {
    position: absolute;
    right: 0;
    top: 0;
    border: 1px solid #00F601;
    padding: 10px;
    &:before {
      content: "";
      position: absolute;
      left: -3px;
      right: -3px;
      top: -3px;
      bottom: -3px;
      border: 1px solid #00F601;
      z-index: -1;
    }
  }

</style>
