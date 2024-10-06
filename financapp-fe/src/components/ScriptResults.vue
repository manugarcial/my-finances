<template>
  <div>
    <h2>Script Result</h2>
    <p>{{ result.output }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      result: {}
    };
  },
  created() {
    const scriptName = this.$route.path.replace('/', '');
    axios.get(`http://127.0.0.1:5000/${scriptName}`)
      .then(response => {
        this.result = response.data;
      });
  }
};
</script>

<style>
/* Add your styles here */
</style>
