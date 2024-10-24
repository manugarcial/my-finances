<template>
  <div id="stocks">
    <h1>{{ $t("Stocks") }}</h1>
    <div v-if="response">
      <div>{{ response }}</div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";
// import BoxData from "@/components/BoxData.vue";

export default {
  // components: {
  //   BoxData,
  // },
  data() {
    return {
      scripts: [],
      // output: "",
      response: null,
      stocks_list: [],
      stock_wallet: {},
      refreshInterval: null,
      boxDataItems: [
        // { number: 10, text: "IRPF Number" },
      ],
    };
  },
  created() {
    const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
    axios
      .get(`${apiBaseUrl}`)
      .then((response) => {
        this.scripts = response.data.scripts;
      })
      .catch((error) => {
        console.error("Error fetching scripts:", error);
      });
  },
  async mounted() {
    // Initial fetch when component is mounted
    await this.fetchStocks();

    // Set interval to refresh data every 5 minutes (300,000 milliseconds)
    this.refreshInterval = setInterval(() => {
      this.fetchStocks();
    }, 300000); // 5 minutes in milliseconds
  },
  beforeDestroy() {
    // Clear the interval when the component is destroyed to avoid memory leaks
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  methods: {
    async fetchStocks() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        // Sending data to backend using axios
        const res = await axios.get(`${apiBaseUrl}/stocks_investment`);
        // Save response to display
        this.response = res.data.wallet;
        console.log("response");
        console.log("--------------------------");
        console.log("wallet value");
        console.log(res.data.wallet);
        console.log("--------------------------");
        // let responseString = this.response;
        // let fixedJsonString;
        // let jsonObject;
        // try {
        //   // Replace all single quotes with double quotes
        //   fixedJsonString = responseString.replace(/'/g, '"');
        //   // Attempt to parse the fixed JSON string
        //   jsonObject = JSON.parse(fixedJsonString);
        // } catch (error) {
        //   console.error("Error parsing JSON after fixing quotes:", error);
        //   return null;
        // }
        // this.boxDataItems[0].number = jsonObject["anual irpf"];
        // this.boxDataItems[1].number = jsonObject["net salary per month"];
        // this.boxDataItems[2].number = jsonObject["irpf salary percentage"];
        // this.boxDataItems[3].number = jsonObject["mortgage loan / house rent"];
        // this.boxDataItems[4].number = jsonObject["basic spendings"];
        // this.boxDataItems[5].number = jsonObject["personal spendings"];
        // this.boxDataItems[6].number = jsonObject["savings"];
        // this.boxDataItems[7].number = jsonObject["investments"];
      } catch (error) {
        console.error("Error submitting form:", error);
        this.response = "An error occurred while submitting the form.";
      }
    },
  },
};
</script>

<style>
#stocks {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
