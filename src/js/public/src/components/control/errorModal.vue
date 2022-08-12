<template>
  <div class="modal-body">
    <div class="modal-header">
      Error
    </div>
    <div class="modal-msg">
      The connection to the platform has been lost. Sorry :)
    </div>
    <a href="#" class="std-btn">
      RECONNECT
    </a>
  </div>
</template>

<script>
  export default {
    name: "errorModal"
  }
</script>

<style lang="scss" scoped>
  .modal-body {
    width: 80vw;
    background: #000000;
    border: 1px solid ;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 18px;
    z-index: 1;
  }
  .modal-header {
    padding: 2px 5px;
    background: #00F601;
    font-size: 20px;
    color: #000000;
  }
  .modal-msg {
    padding: 10px;
    margin-bottom: 5px;
  }
  .std-btn {
    margin: 0 auto;
    border: 1px solid #00F601;
    width: 100px;
    text-align: center;
    display: block;
    padding: 2px;
    color: #000000;
    margin-bottom: 20px;
    text-decoration: none;
    background: #00F601;
    &:active {
      background: #000000;
      color: #00F601;
    }
  }
</style>
