<template>
  <div id="app">
    <button @click="subscribe">SUBSCRIBE</button>
  </div>
</template>

<script>
const {subscribe} = require('./Observer');

export default {
  name: 'app',
  methods: {
    subscribe() {
      subscribe('offer', 'sdp');
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
