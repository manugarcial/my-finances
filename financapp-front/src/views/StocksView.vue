<template>
  <div id="app">
    <h1>{{ $t("Stocks") }}</h1>
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
      output: "",
      response: null,
      stocks_list: [],
      stock_wallet: {},
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
    // Call the method to fetch data when the page loads
    await this.fetchStocks();
  },
  methods: {
    async fetchStocks() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        // Sending data to backend using axios
        const res = await axios.get(`${apiBaseUrl}/stocks_investment`);
        // Save response to display
        this.response = res.data.output;
        console.log("response");
        console.log(res);
        console.log("--------------------------");
        console.log(res.data);
        console.log("--------------------------");
        console.log(res.data.output);
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
