<template>
  <div id="app">
    <h1>Python Scripts</h1>
    <ul>
      <li v-for="script in scripts" :key="script.url">
        <button @click="executeScript(script.url)">
          {{ script.name }}
        </button>
      </li>
    </ul>
    <div v-if="output">
      <h2>Script Output:</h2>
      <pre>{{ output }}</pre>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      scripts: []
    };
  },
  created() {
    axios.get('http://127.0.0.1:5000/')
      .then(response => {
        this.scripts = response.data.scripts;
      });
  },
  methods: {
    executeScript(scriptUrl) {
      axios.get(`http://127.0.0.1:5000${scriptUrl}`)
        .then(response => {
          console.log('Script executed:', response.data);
        })
        .catch(error => {
          console.error('Error executing script:', error);
        });
    }
  }
};
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
