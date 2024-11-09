<template>
  <div id="stocks">
    <h1>{{ $t("Stocks") }}</h1>
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
    <!-- ApexChart for compound wallet value evolution -->
    <div v-if="!loading" class="chart-container">
      <apexchart
        width="100%"
        type="line"
        :options="chartOptions"
        :series="seriesData"
      />
    </div>
    <!-- Add Stock Button -->
    <button @click="openModal" class="submit-button">Add Stock</button>

    <!-- Add Stock Modal -->
    <AddStockModal
      v-if="isModalOpen"
      :isOpen="isModalOpen"
      :close="closeModal"
      @add-stock="handleAddStock"
    />
    <div v-if="response" class="wallet response-container">
      <div v-for="(item, index) in wallet" :key="index" class="box-data-item">
        {{ item["wallet_invested_value"] }}
        {{ item["transactions_value"] }}
        {{ item["wallet_real_value_now_without_transactions"] }}
        {{ item["wallet_real_value_now_with_transactions"] }}
        {{ item["wallet_per_change_no_transactions"] }}
        {{ item["wallet_per_change_with_transactions"] }}
      </div>
    </div>
    <br />
    <div v-if="response" class="stocks-items response-container">
      <!-- Loop through data to create multiple instances of DataDisplay component -->
      <div
        v-for="(item, index) in stockItems"
        :key="index"
        class="box-data-item"
        :class="{
          positive: item.stock_per_change >= 0,
          negative: item.stock_per_change < 0,
        }"
        @click="navigateToStock(item.stock_symbol)"
      >
        <BoxData
          :initialNumber="item.stock_per_change"
          :initialText="item.stock_symbol"
        />
      </div>
    </div>
    <div v-if="response">
      <div>{{ response }}</div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";
import BoxData from "@/components/BoxData.vue";
import VueApexCharts from "vue3-apexcharts";
import AddStockModal from "@/modals/AddStockModal.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    BoxData,
    apexchart: VueApexCharts,
    AddStockModal,
  },
  data() {
    return {
      loading: true,
      scripts: [],
      response: null,
      jsonResponse: null,
      stocks_list: [],
      stock_wallet: {},
      refreshInterval: null,
      stockItems: [],
      wallet: [],
      walletEvolution: [], // To store the wallet compound values
      seriesData: [], // Data for the chart
      newStockSymbol: "",
      isModalOpen: false,
      userData: {
        username: "",
      },
      chartOptions: {
        chart: {
          id: "wallet-evolution-chart",
          animations: {
            enabled: true,
          },
        },
        xaxis: {
          type: "datetime",
          title: {
            text: "Date",
          },
        },
        yaxis: {
          title: {
            text: "Wallet Value",
          },
          labels: {
            formatter: function (val) {
              return val.toFixed(2); // Rounds each label to an integer
            },
          },
        },
        stroke: {
          curve: "smooth",
          colors: ["9E9E9E"],
        },
        title: {
          text: "Compound Value of Stock Wallet Over Time",
          align: "center",
        },
      },
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
    }, 60000); // 5 minutes in milliseconds
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed to avoid memory leaks
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  computed: {
    ...mapGetters(["getUsername"]), // Map the getter to a computed property
    username() {
      return this.getUsername; // Access the username through the getter
    },
  },
  methods: {
    async fetchStocks() {
      console.log("fetch stocks");
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        console.log(apiBaseUrl);
        console.log(this.username);
        this.userData.username = this.username;
        console.log(this.userData);
        const res = await axios.post(
          `${apiBaseUrl}/stocks_investment`,
          this.userData
        );
        console.log("response");
        console.log(res);
        this.response = res.data.wallet;

        let fixedJsonString = this.response.replace(/'/g, '"');
        this.jsonResponse = JSON.parse(fixedJsonString);

        // Parse the response for compound_stocks_daily
        const data = this.jsonResponse["compound_stocks_daily"];
        this.walletEvolution = data.map((entry) => ({
          x: new Date(entry.date), // Ensures date is a JS Date object
          y: entry.wallet_value, // Use correct field name for y-value
        }));

        // Update seriesData for ApexCharts
        this.seriesData = [
          {
            name: "Compound Value",
            data: this.walletEvolution,
          },
        ];

        // Update other response data for display
        // eslint-disable-next-line
        const realTimeWallet = this.jsonResponse["compound_stocks_real_time"]["wallet_value"];
        this.wallet = Object.keys(realTimeWallet).map((key) => ({
          [key]: realTimeWallet[key],
        }));

        // Process stockItems
        const stocksList =
          this.jsonResponse["compound_stocks_real_time"]["stocks_list"];
        this.stockItems = Object.keys(stocksList).map((stock) => ({
          stock_symbol: stock,
          // eslint-disable-next-line
          stock_per_change: parseFloat(stocksList[stock][0].stock_change_percentage) * 100,
        }));
      } catch (error) {
        console.error("Error fetching stocks data:", error);
        this.response = "An error occurred while submitting the form.";
      } finally {
        this.loading = false;
      }
    },
    openModal() {
      this.isModalOpen = true; // Show the modal
    },
    closeModal() {
      this.isModalOpen = false; // Hide the modal
    },
    async handleAddStock(stockData) {
      console.log("hello");
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        console.log(apiBaseUrl);
        console.log(this.username);
        const response = await axios.post(`${apiBaseUrl}/add_stock`, stockData);
        console.log(response);
        // Optionally, update local state or show a success message
        alert("Stock added successfully!");

        // Refresh the stocks list to include the new stock
        await this.fetchStocks();
      } catch (error) {
        console.error("Error adding stock:", error);
        alert("An error occurred while adding the stock.");
      } finally {
        this.closeModal(); // Close the modal after submitting
      }
    },
    navigateToStock(ticker) {
      this.$router.push({ path: `/item/${ticker}` });
      window.scrollTo(0, 0);
    },
  },
  watch: {
    // Watch seriesData to set the line color based on its values
    seriesData: {
      immediate: true, // Trigger this when seriesData is initially set
      handler(newData) {
        if (newData.length > 0 && newData[0].data.length > 1) {
          const firstValue = newData[0].data[0].y;
          const lastValue = newData[0].data[newData[0].data.length - 1].y;

          // Conditionally set the line color
          this.chartOptions.stroke.colors =
            lastValue > firstValue ? ["#4CAF50"] : ["#F44336"];
        }
      },
    },
  },
};
</script>

<style scoped>
#stocks {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.positive {
  color: green; /* or any other style for positive */
}

.negative {
  color: red; /* or any other style for negative */
}
h1.title {
  color: #333;
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  width: 100%;
  grid-column: 1 / -1; /* Ensure the title spans the entire grid width */
}

/* Main container for the form and response side by side */
.main-container {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 50% 50% split */
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin-top: 20px;
}

.label {
  margin-bottom: 8px;
  font-weight: bold;
}

.input-field {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: all 0.3s;
}

.input-field:focus {
  border-color: #007bff;
  outline: none;
}

/* Error messages */
.error {
  color: #ff4d4d;
  font-size: 14px;
  margin-top: 5px;
}

/* Submit button */
.submit-button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:disabled {
  background-color: #b0b0b0;
}

.submit-button:not(:disabled):hover {
  background-color: #0056b3;
}

/* Response container */
.response-container {
  background-color: #f9f9f9;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  white-space: pre-wrap;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;
}

.stock-items.response-container {
  display: flex;
  flex-wrap: wrap;
}

.stocks-items .box-data-item {
  flex-basis: 33%; /* Each child takes up 25% of the container's width */
  box-sizing: border-box; /* Ensures padding and border are included in the width */
  padding: 10px;
}

.box-data-item {
  cursor: pointer; /* Add this line to show a pointer on hover */
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-container {
    grid-template-columns: 1fr; /* Stack form and response on top of each other */
  }
  .title {
    font-size: 20px;
  }

  .input-field {
    font-size: 14px;
    padding: 8px;
  }

  .submit-button {
    font-size: 14px;
    padding: 10px;
  }

  .form-container {
    width: calc(100% - 40px);
    margin-bottom: 20px;
  }

  .response-container {
    width: calc(100% - 40px);
    flex-direction: column;
  }
}
</style>
