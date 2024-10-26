<template>
  <div>
    <h1>Stock Details for {{ ticker }}</h1>
    <!-- You can add more details here, e.g., fetching data from an API -->
    <p v-if="stock">Company: {{ stock.name }}</p>
    <p v-else>Loading...</p>
    <!-- Stock Chart -->
    <div v-if="stockValues.length">
      <apexchart type="line" :options="chartOptions" :series="chartSeries">
      </apexchart>
    </div>
    <div v-if="response">
      <div>{{ response }}</div>
    </div>
    <router-link to="/stocks-search">Back to Search</router-link>
  </div>
</template>

<script>
import axios from "axios";
import VueApexCharts from "vue3-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts,
  },
  props: ["ticker"],
  data() {
    return {
      response: null,
      study_period: "1mo",
      stock_historical_values: null,
      stock_current_values: null,
      rsi_index: null,
      rsi_evaluation: null,
      profile: null,
      competitors: null,
      recomendation: null,
      economy_rating: null,
      surprise_index: null,
      sentiment: null,
      stockValues: [],
      chartOptions: {
        chart: {
          height: 350,
          type: "line",
          zoom: {
            enabled: false,
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: "smooth",
        },
        xaxis: {
          categories: [], // This will be filled in `onPageLoad`
        },
        title: {
          text: "Stock Close Prices",
          align: "left",
        },
      },
      chartSeries: [
        {
          name: "Close Price",
          data: [],
        },
      ],
    };
  },
  methods: {
    async onPageLoad() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        // Sending data to backend using axios
        const res = await axios.post(`${apiBaseUrl}/single_stock`, {
          ticker: this.ticker,
          period: this.study_period,
        });
        this.response = res.data.stock;
        console.log(this.response);

        let responseString = this.response;
        let fixedJsonString;
        let jsonObject;
        try {
          // Replace all single quotes with double quotes
          fixedJsonString = responseString.replace(/'/g, '"');
          // Attempt to parse the fixed JSON string
          jsonObject = JSON.parse(fixedJsonString);
          // eslint-disable-next-line
          this.stockValues = jsonObject["company_stock_data_values"][0]["stock_historical_data"]["stock_historic_close_data"];
          // Prepare chart data
          this.chartSeries[0].data = this.stockValues;
          // eslint-disable-next-line
          this.chartOptions.xaxis.categories = this.stockValues.map((_, index) => `Day ${index + 1}`);
          // TO DO: the historical values that we get here are just 1 per day,
          // not valid to show graphs from a short period of time 1d, 1w.
          // PROP: create another function that retrieves those values properly
          this.stock_values = jsonObject["company_stock_data_values"];
          this.rsi_index = jsonObject["company_relative_strengh_index_rsi"];
          this.rsi_evaluation = jsonObject["company_rsi_evaluation"];
          this.profile = jsonObject["company_profile"];
          this.competitors = jsonObject["company_market_competitors"];
          this.recomendation = jsonObject["company_recommendations"];
          this.economy_rating = jsonObject["country_economy_rating"];
          this.surprise_index = jsonObject["company_surprise_index"];
          this.sentiment = jsonObject["company_sentiment"];
        } catch (error) {
          console.error("Error parsing JSON after fixing quotes:", error);
          return null;
        }
      } catch (error) {
        console.error("Error submitting form:", error);
        this.response = "An error occurred while submitting the form.";
      }
    },
  },
  mounted() {
    this.onPageLoad(); // Call the method on component mount
  },
};
</script>
<style scoped>
/* Add any necessary styling for your chart */
#stockChart {
  max-width: 600px;
  max-height: 400px;
}
</style>
