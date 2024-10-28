<template>
  <div>
    <h1>Stock Details for {{ stock_name }}</h1>
    <!-- You can add more details here, e.g., fetching data from an API -->
    <p v-if="stock_name">Company ticker: {{ ticker }}</p>
    <!-- Loading Icon (Shown only when loading is true) -->
    <div v-if="loading" class="loading-icon">
      <!-- Inline SVG for the loading spinner -->
      <svg
        width="50px"
        height="50px"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          cx="50"
          cy="50"
          r="32"
          stroke-width="8"
          stroke="#c4c4c4"
          stroke-dasharray="50.26548245743669 50.26548245743669"
          fill="none"
          stroke-linecap="round"
        >
          <animateTransform
            attributeName="transform"
            type="rotate"
            repeatCount="indefinite"
            dur="0.5s"
            keyTimes="0;1"
            values="0 50 50;360 50 50"
          />
        </circle>
        <circle
          cx="50"
          cy="50"
          r="23"
          stroke-width="8"
          stroke="#6a6a6a"
          stroke-dasharray="36.12831551628262 36.12831551628262"
          stroke-dashoffset="36.128"
          fill="none"
          stroke-linecap="round"
        >
          <animateTransform
            attributeName="transform"
            type="rotate"
            repeatCount="indefinite"
            dur="0.5s"
            keyTimes="0;1"
            values="0 50 50;-360 50 50"
          />
        </circle>
      </svg>
    </div>
    <!-- Study Period Dropdown period len ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'] -->
    <div v-if="stockValuesClose.length">
      <label for="studyPeriod">Select Study Period: </label>
      <select id="studyPeriod" v-model="study_period" @input="onPeriodChange">
        <option value="1d">1 Day</option>
        <option value="5d">1 Week</option>
        <option value="1mo" default>1 Month</option>
        <option value="3mo">3 Months</option>
        <option value="6mo">6 Months</option>
        <option value="ytd">Year to Date (YTD)</option>
        <option value="1y">1 Year</option>
        <option value="2y">2 Years</option>
        <option value="5y">5 Years</option>
        <option value="10">10 Years</option>
        <option value="max">Max period</option>
      </select>
    </div>
    <!-- Stock Chart -->
    <div v-if="stockValuesClose.length">
      <apexchart type="line" :options="chartOptions" :series="chartSeries">
      </apexchart>
    </div>
    <!-- Profile Section (Display company profile information under the chart) -->
    <div v-if="profile" class="profile-section">
      <h2>Company Profile</h2>
      <div class="profile-items">
        <div v-for="(value, key) in profile" :key="key" class="profile-item">
          <strong>{{ formatKey(key) }}:</strong>
          <span v-if="key === 'logo'">
            <img :src="value" alt="Company Logo" class="company-logo" />
          </span>
          <span v-else-if="key === 'weburl'">
            <a :href="value" target="_blank" rel="noopener noreferrer">
              {{ value }}
            </a>
          </span>
          <span v-else>{{ value }}</span>
        </div>
      </div>
    </div>
    <!-- Competitors Section (Display list of competitors excluding the current ticker) -->
    <div v-if="filteredCompetitors.length" class="competitors-section">
      <h2>Competitors</h2>
      <div class="competitors-list">
        <div
          v-for="competitor in filteredCompetitors"
          :key="competitor"
          class="competitor-item"
          @click="navigateToCompetitor(competitor.ticker)"
        >
          {{ competitor.name }}
          <img :src="competitor.logo" alt="Company Logo" class="company-logo" />
        </div>
      </div>
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
    // {'company_stock_data_values': [{'stock_ticker': 'AMZN',
    // 'stock_historical_data': {'stock_historic_close_data': [191.16000366210938, 187.97000122070312, 186.3300018310547, 185.1300048828125, 184.75999450683594, 181.9600067138672, 186.50999450683594, 180.8000030517578, 182.72000122070312, 185.1699981689453, 186.64999389648438, 188.82000732421875, 187.5399932861328, 187.69000244140625, 186.88999938964844, 187.52999877929688, 188.99000549316406, 189.07000732421875, 189.6999969482422, 184.7100067138672, 186.3800048828125, 187.8300018310547]},
    // 'stock_real_time_data': {'Current $': 187.83, 'Change': 1.45, 'Percentage change': 0.778, 'Highest today': 190.45, 'Lowest today': 187.53, 'Open $ today': 187.85, 'Prev close $': 186.38, 'Timestamp': 1729972800}}],
    // 'company_relative_strengh_index_rsi': 46, 'company_rsi_evaluation': 0.9,
    // 'company_profile': {'country': 'US', 'currency': 'USD', 'estimateCurrency': 'USD', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'finnhubIndustry': 'Retail', 'ipo': '1997-05-15', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AMZN.png', 'marketCapitalization': 1971382.473159773, 'name': 'Amazon.com Inc', 'phone': '12062661000', 'shareOutstanding': 10495.57, 'ticker': 'AMZN', 'weburl': 'https://www.amazon.com/'},
    // 'company_market_competitors': ['AMZN', 'CPNG', 'EBAY', 'DDS', 'ETSY', 'OLLI', 'M', 'JWN', 'KSS', 'SVV'],
    // 'company_recommendations': [{'buy': 49, 'hold': 4, 'period': '2024-10-01', 'sell': 0, 'strongBuy': 19, 'strongSell': 0, 'symbol': 'AMZN'}, {'buy': 48, 'hold': 3, 'period': '2024-09-01', 'sell': 0, 'strongBuy': 19, 'strongSell': 0, 'symbol': 'AMZN'}, {'buy': 46, 'hold': 2, 'period': '2024-08-01', 'sell': 0, 'strongBuy': 19, 'strongSell': 0, 'symbol': 'AMZN'}, {'buy': 45, 'hold': 2, 'period': '2024-07-01', 'sell': 0, 'strongBuy': 19, 'strongSell': 0, 'symbol': 'AMZN'}],
    // 'country_economy_rating': 1.2,
    // 'company_surprise_index': {'company_surprise_index': {'trend': [4.5898, -6.521699999999999, -35.5767], 'most_recent_is_positive': 1, 'most_recent_surprisePercent': 20.1831}},
    // 'company_sentiment': {'data': [{'symbol': 'AMZN', 'year': 2024, 'month': 1, 'change': -2000, 'mspr': -100}, {'symbol': 'AMZN', 'year': 2024, 'month': 2, 'change': -50182158, 'mspr': -99.35669}, {'symbol': 'AMZN', 'year': 2024, 'month': 3, 'change': -541788, 'mspr': -100}, {'symbol': 'AMZN', 'year': 2024, 'month': 4, 'change': 677632, 'mspr': 98.40263}, {'symbol': 'AMZN', 'year': 2024, 'month': 5, 'change': -1181238, 'mspr': -80.396576}, {'symbol': 'AMZN', 'year': 2024, 'month': 6, 'change': -8210, 'mspr': -100}, {'symbol': 'AMZN', 'year': 2024, 'month': 7, 'change': -8661380, 'mspr': -100}, {'symbol': 'AMZN', 'year': 2024, 'month': 8, 'change': -3500, 'mspr': -100}], 'symbol': 'AMZN'}}
    return {
      loading: true,
      response: null,
      stock_name: null,
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
      stockValuesClose: [],
      stockValuesOpen: [],
      stockValuesHigh: [],
      stockValuesLow: [],
      stockValuesDates: [],
      maxValue: 0,
      minValue: 0,
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
          colors: ["grey"],
        },
        xaxis: {
          categories: [], // This will be filled in `onPageLoad`
        },
        yaxis: {
          labels: {
            formatter: function (value) {
              return Math.round(value); // Round to the nearest integer
            },
          },
        },
        title: {
          text: "Stock Close Prices",
          align: "left",
        },
        annotations: {
          yaxis: [], // This will be populated in `setChartAnnotations`
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
  computed: {
    filteredCompetitors() {
      // Filter out the current ticker from the competitors list
      // eslint-disable-next-line
      return this.competitors ? this.competitors.filter(comp => comp !== this.name) : [];
    },
  },
  methods: {
    navigateToCompetitor(newTicker) {
      // Get the current URL
      const currentUrl = window.location.href;

      // Use a regex to replace the ticker in the URL
      const updatedUrl = currentUrl.replace(/item\/[^/]+/, `item/${newTicker}`);

      // Update the URL without reloading the page
      // window.history.replaceState(null, "", updatedUrl);
      // Change the window location to the new URL, which will reload the page
      window.location.href = updatedUrl;

      // Scroll to the top of the page after redirection
      // This line is actually not necessary because the page reload will reset the scroll position,
      // but you can keep it if you want to ensure it before reload.
      window.scrollTo(0, 0);
    },
    formatKey(key) {
      // Convert camelCase or snake_case to a more readable format
      return key
        .replace(/([A-Z])/g, " $1")
        .replace(/_/g, " ")
        .toUpperCase();
    },
    // Function to format dates
    formatDate(dateString) {
      const date = new Date(dateString);
      const currentYear = new Date().getFullYear();

      // Check if the year is the current year
      if (date.getFullYear() === currentYear) {
        // Format: "DD MMM"
        return `${date.getDate()} ${date.toLocaleString("default", {
          month: "short",
        })}`; // Get first 3 characters of the month
      } else {
        // Format: "YYYY-MM-DD" for other years
        return date.toISOString().split("T")[0]; // Or return any other format you prefer
      }
    },
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
          this.stockValuesClose = jsonObject["company_stock_data_values"][0]["stock_historical_data"]["stock_historic_close_data"];
          // eslint-disable-next-line
          this.stockValuesOpen = jsonObject["company_stock_data_values"][0]["stock_historical_data"]["stock_historic_open_data"];
          // eslint-disable-next-line
          this.stockValuesHigh = jsonObject["company_stock_data_values"][0]["stock_historical_data"]["stock_historic_high_data"];
          // eslint-disable-next-line
          this.stockValuesLow = jsonObject["company_stock_data_values"][0]["stock_historical_data"]["stock_historic_low_data"];
          // eslint-disable-next-line
          this.stockValuesDates = jsonObject["company_stock_data_values"][0]["stock_historical_data"]["date_historic_data"];
          // Calculate maximum and minimum values
          this.maxValue = Math.max(...this.stockValuesClose);
          this.minValue = Math.min(...this.stockValuesClose);
          // Prepare chart data
          this.chartSeries[0].data = this.stockValuesClose;
          // eslint-disable-next-line
          // this.chartOptions.xaxis.categories = this.stockValuesClose.map((_, index) => `Day ${index + 1}`);
          // this.chartOptions.xaxis.categories = this.stockValuesDates.map(date => new Date(date).toLocaleDateString());
          // eslint-disable-next-line
          this.chartOptions.xaxis.categories = this.stockValuesDates.map(date => this.formatDate(date));
          // Set annotations for max and min
          this.setChartAnnotations(this.maxValue, this.minValue);
          // Update chart line color based on first and last stock values
          this.updateLineColor();
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
          this.stock_name = jsonObject["company_profile"]["name"];
        } catch (error) {
          console.error("Error parsing JSON after fixing quotes:", error);
          return null;
        }
      } catch (error) {
        console.error("Error submitting form:", error);
        this.response = "An error occurred while submitting the form.";
      } finally {
        this.loading = false; // Hide loading icon when data is loaded
      }
    },
    onPeriodChange() {
      this.loading = true; // Optional: Show loading icon again while fetching new data
      this.resetChartColor(); // Reset chart color when period changes
      this.$nextTick(() => {
        this.onPageLoad(); // Re-fetch data after study_period changes
      });
    },
    setChartAnnotations(maxValue, minValue) {
      this.chartOptions = {
        ...this.chartOptions,
        annotations: {
          yaxis: [
            {
              y: maxValue,
              borderColor: "#00E396",
              label: {
                borderColor: "#00E396",
                style: {
                  color: "#fff",
                  background: "#00E396",
                },
                text: `Max: ${maxValue}`,
              },
            },
            {
              y: minValue,
              borderColor: "#FF4560",
              label: {
                borderColor: "#FF4560",
                style: {
                  color: "#fff",
                  background: "#FF4560",
                },
                text: `Min: ${minValue}`,
              },
            },
          ],
        },
      };
      this.$nextTick(() => {
        const chart = this.$refs.chart; // Reference to the apexchart instance
        if (chart) {
          chart.updateOptions(this.chartOptions, true, true); // Update chart with new options
        }
      });
    },
    resetChartColor() {
      // Reset stroke colors to an empty array
      this.chartOptions.stroke.colors = [];
      // Optionally set a default color or leave it empty if the chart is redrawn
      // For instance, if you want it to start gray by default:
      this.chartOptions.stroke.colors.push("#9E9E9E"); // Default gray
    },
    resetLineColor(newColor) {
      console.log(newColor);
      // Reset the colors array
      this.chartOptions.stroke.colors = []; // Clear existing colors

      // Set new color
      this.chartOptions.stroke.colors.push(newColor); // Add new color

      // Use nextTick to ensure reactivity
      this.$nextTick(() => {
        const chart = this.$refs.chart; // Access the chart instance via ref
        if (chart) {
          chart.updateOptions(this.chartOptions, true, true); // Update the chart options
        }
      });
    },
    updateLineColor() {
      if (this.stockValuesClose.length < 2) return; // Ensure there's enough data to compare

      const firstValue = this.stockValuesClose[0];
      const lastValue = this.stockValuesClose[this.stockValuesClose.length - 1];

      let color;

      if (lastValue > firstValue) {
        color = "#4CAF50"; // Green for increase
      } else if (lastValue < firstValue) {
        color = "#F44336"; // Red for decrease
      } else {
        color = "#9E9E9E"; // Grey for no change
      }

      // Call resetLineColor to update the stroke color
      this.resetLineColor(color);
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

.loading-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.loading-icon img {
  width: 50px; /* Adjust size as needed */
  height: 50px;
}

/* Profile section styles */
.company-logo {
  width: 50px;
  height: 50px;
}

.profile-section {
  margin-top: 20px;
  padding: 15px;
  border-top: 1px solid #ddd;
}

.profile-items {
  display: flex;
  flex-wrap: wrap; /* Allow items to wrap to the next line */
  gap: 20px; /* Space between items */
}

.profile-item {
  flex: 1 1 calc(33% - 20px); /* Responsive sizing for 3 items per row */
  min-width: 200px; /* Minimum width for items */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  background: #f9f9f9;
  transition: background 0.3s;
}

.profile-item:hover {
  background: #f1f1f1; /* Highlight on hover */
}

.competitors-section {
  padding: 20px;
}

.competitors-list {
  display: flex;
  flex-wrap: wrap; /* Allow items to wrap to the next line */
  gap: 20px; /* Space between items */
}

.competitor-item {
  flex: 1 1 calc(33% - 20px); /* Responsive sizing for 3 items per row */
  min-width: 200px; /* Minimum width for items */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background: #f9f9f9;
  text-align: center; /* Center the text */
  cursor: pointer; /* Indicate clickable item */
  transition: background 0.3s, transform 0.3s; /* Transition for hover effect */
}

.competitor-item:hover {
  background: #e9e9e9; /* Highlight on hover */
  transform: scale(1.05); /* Slightly scale up on hover */
}

/* Media query for smaller screens */
@media (max-width: 768px) {
  .profile-item,
  .competitor-item {
    flex: 1 1 calc(50% - 20px); /* 2 items per row on medium screens */
  }
}

@media (max-width: 480px) {
  .profile-item,
  .competitor-item {
    flex: 1 1 100%; /* 1 item per row on small screens */
  }
}
</style>
