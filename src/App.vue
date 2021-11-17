<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    <Perf title="iOS 性能数据"/>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Perf from './components/Perf.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld,
    Perf
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
