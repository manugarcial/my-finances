<template>
  <div id="app">
    <h1>{{ $t("Global Economy Data") }}</h1>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      scripts: [],
      output: "",
    };
  },
  created() {
    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        this.scripts = response.data.scripts;
      })
      .catch((error) => {
        console.error("Error fetching scripts:", error);
      });
  },
  methods: {
    executeScript(scriptUrl) {
      axios
        .get(`http://127.0.0.1:5000${scriptUrl}`)
        .then((response) => {
          this.output = response.data.output;
        })
        .catch((error) => {
          console.error("Error executing script:", error);
        });
    },
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
