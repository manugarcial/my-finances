<template>
  <div id="stocks">
    <h1>{{ $t("Stocks") }}</h1>
    <div class="wallet response-container">
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
    <div class="stocks-items response-container">
      <!-- Loop through data to create multiple instances of DataDisplay component -->
      <div
        v-for="(item, index) in stockItems"
        :key="index"
        class="box-data-item"
        :class="{
          positive: item.stock_per_change >= 0,
          negative: item.stock_per_change < 0,
        }"
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

export default {
  components: {
    BoxData,
  },
  data() {
    return {
      scripts: [],
      response: null,
      stocks_list: [],
      stock_wallet: {},
      refreshInterval: null,
      stockItems: [],
      wallet: [],
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
  methods: {
    async fetchStocks() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        // Sending data to backend using axios
        const res = await axios.get(`${apiBaseUrl}/stocks_investment`);
        // Save response to display
        this.response = res.data.wallet;
        this.stockItems = [];
        let responseString = this.response;
        let fixedJsonString;
        let jsonObject;
        try {
          // Replace all single quotes with double quotes
          fixedJsonString = responseString.replace(/'/g, '"');
          // Attempt to parse the fixed JSON string
          jsonObject = JSON.parse(fixedJsonString);
        } catch (error) {
          console.error("Error parsing JSON after fixing quotes:", error);
          return null;
        }
        this.wallet = [];
        // let wallet_info = [];
        for (const [key, value] of Object.entries(jsonObject["wallet_value"])) {
          let wallet_data = {
            [key]: value,
          };
          // wallet_info.push(wallet_data);
          this.wallet.push(wallet_data);
        }

        // this.wallet.push(wallet_info);

        for (const [key, value] of Object.entries(jsonObject["stocks_list"])) {
          let stock_change_info = {
            stock_symbol: key,
            stock_per_change:
              parseFloat(value[0]["stock_change_percentage"]).toFixed(4) * 100,
          };
          this.stockItems.push(stock_change_info);
        }
      } catch (error) {
        console.error("Error submitting form:", error);
        this.response = "An error occurred while submitting the form.";
      }
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
