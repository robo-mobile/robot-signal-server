<template>
  <div>
    platform
    <button @click="send">SDP</button>
  </div>
</template>

<script>
  import RTC from '../RTC';

  export default {
    name: "platform",
    methods: {
      send: function () {

      }
    },
    created() {

      const webrtc = new RTC(false);
    }
  }
</script>

<style scoped>

</style>
