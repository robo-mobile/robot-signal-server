<template>
  <div @mousemove="mouseMove" ref="balance" class="balance">
    <div class="left part">LEFT TURN</div>
    <div class="right part">RIGHT TURN</div>
  </div>
</template>

<script>
  const floor = num => Math.floor(num * 100) / 100;

  export default {
    name: "balancePanel",
    data: () => ({
      balanceWidth: 480
    }),
    methods: {
      mouseMove(e) {
        const x = e.layerX || e.offsetX;
        const half = this.balanceWidth / 2;
        let leftCat;
        let rightCat;
        if (x >= half) {
          leftCat = 1;
          rightCat = floor((this.balanceWidth - x) / (half / 100) / 100);
        } else {
          rightCat = 1;
          leftCat = floor(x / (half / 100) / 100);
        }
        this.$emit('upd', {leftCat, rightCat});
      },
    }
  }
</script>

<style lang="scss" scoped>
  .balance {
    position: absolute;
    bottom: 0;
    height: 100px;
    width: 480px;
    border: 1px solid #00F601;
    left: 50%;
    margin-left: -240px;
    font-size: 20px;
    display: flex;
    .part {
      width: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .left {
      border-right: 1px solid #00F601;
    }
    &:before {
      content: "";

    }
  }
</style>
