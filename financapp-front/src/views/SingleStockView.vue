<template>
  <div>
    <h1>Stock Details for {{ ticker }}</h1>
    <!-- You can add more details here, e.g., fetching data from an API -->
    <p v-if="stock">Company: {{ stock.name }}</p>
    <p v-else>Loading...</p>
    <router-link to="/stocks-search">Back to Search</router-link>
  </div>
</template>

<script>
import stockData from "../data/stockData";
export default {
  props: ["ticker"],
  data() {
    return {
      stocks: stockData,
    };
  },
};
</script>
