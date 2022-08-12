<template>
  <div class="wrap">
    <div class="content">
      <div class="border">
        Enter HASH of your platform, please :
        <div class="field">
          <pre>░░░░░░░</pre>
          <div class="stars">{{stars}}<span class="cursor">▐</span></div>
        </div>
        <input
            v-model="pass"
            :maxlength="4"
            v-on:keyup.enter="submit"
            @blur="setFocus"
            ref="hash"
            type="text"
            class="hide">
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex';
  import store from '../../configureStore';

  export default {
    name: "auth",
    store: store,
    data: () => ({
      pass: '',
      stars: ''
    }),
    watch: {
      pass() {
        this.stars = this.pass.split('').reduce(acc => acc += '*', '');
      },
    },
    mounted() {
      this.setFocus();
    },
    computed: mapState(['config', 'isConnect']),
    methods: {
      setFocus() {
        if (this.$refs['hash']) {
          this.$refs['hash'].focus();
          this.$refs['hash'].click();
        }
      },
      submit() {
        this.$emit('submit', this.pass);
      }
    }
  }
</script>

<style lang="scss" scoped>
  .wrap {
    position: relative;
    width: 500px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 40px;
    .content {
      position: absolute;
      left: 60px;
      top: 30px;
      height: 40px;
      font-size: 22px;
    }
  }
  .field {
    position: relative;
    .stars {
      position: absolute;
      left: 4px;
      top: -2px;
    }
    .cursor {
      position: relative;
      left: -11px;
      animation-name: cursor;
      animation-duration: 1s;
      animation-iteration-count: infinite;
    }
  }
  .hide {
    //display: none;
    opacity: 0;
    height: 0;
    width: 0;
  }
  @keyframes cursor {
    0%   {opacity: 1;}
    100%  {opacity: 0;}
  }
  .border {
    border: 1px solid #00F601;
    padding: 20px;
    position: relative;
    &:before {
      content: "";
      position: absolute;
      top: -4px;
      bottom: -4px;
      left: -4px;
      right: -4px;
      border: 1px solid #00F601;
    }
  }
</style>
