<template>
  <div id="mortgage">
    <h1 class="page-title">{{ $t("Mortgage") }}</h1>
    <div class="form-results">
      <form class="form-container" @submit.prevent="submitForm">
        <div class="form-group">
          <label for="numberInput">Capital lend by the bank:</label>
          <input
            type="number"
            v-model.number="formData.capital"
            id="numberInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Anual interes rate:</label>
          <input
            type="number"
            v-model.number="formData.interest"
            id="interestInput"
            class="input-field"
            step="0.01"
            min="0"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Mortgage years:</label>
          <input
            type="number"
            v-model.number="formData.mortgage_years"
            id="interestInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Additional yearly payment:</label>
          <input
            type="number"
            v-model.number="formData.additional_yearly_payment"
            id="interestInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Start payment year:</label>
          <input
            type="number"
            v-model.number="formData.start_payment_year"
            id="interestInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Buy / Selling Tax:</label>
          <input
            type="number"
            v-model.number="formData.purchase_tax"
            id="interestInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Sell price:</label>
          <input
            type="number"
            v-model.number="formData.sell_price"
            id="interestInput"
            class="input-field"
            step="0.01"
            min="0"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Bank financiation:</label>
          <input
            type="number"
            v-model.number="formData.bank_finance_percentage"
            id="interestInput"
            class="input-field"
            step="0.01"
            min="0"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="interestInput">Agency commission:</label>
          <input
            type="number"
            v-model.number="formData.agency_commission"
            id="interestInput"
            class="input-field"
            step="0.01"
            min="0"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <button
            type="submit"
            :disabled="isSubmitDisabled"
            class="submit-button"
          >
            Calcular
          </button>
        </div>
      </form>
      <div v-if="response" class="response-container">
        <h2>Mortgage</h2>
        <div class="mortgage-items">
          <div
            v-for="(item, index) in boxDataItems"
            :key="index"
            class="box-data-item"
          >
            <BoxData :initialNumber="item.number" :initialText="item.text" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <router-view></router-view>
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
      boxDataItems: [
        { number: 10, text: "Mortgage years" },
        { number: 20, text: "Mortgage months" },
        { number: 30, text: "Total loan value" },
        { number: 10, text: "Sell / Buy Tax" },
        { number: 10, text: "Minimal money needed" },
        { number: 10, text: "Annual taxes" },
        { number: 10, text: "Total expense no mortgage cancelations" },
        { number: 10, text: "Total expense with mortgage cancelations" },
        { number: 10, text: "Minimun resell price" },
        { number: 10, text: "Resell percentage rise" },
      ],
      scripts: [],
      formData: {
        capital: 100000,
        interest: 3.5,
        mortgage_years: 25,
        additional_yearly_payment: 6000,
        start_payment_year: 3,
        purchase_tax: 8,
        sell_price: 190000,
        bank_finance_percentage: 65,
        agency_commission: 2,
      },
      response: null,
    };
  },
  computed: {
    // Validation for number input
    // numberError() {
    //   if (this.formData.number === null || this.formData.number === "") {
    //     return "Number is required.";
    //   }
    //   if (this.formData.number <= 0) {
    //     return "Number must be greater than zero.";
    //   }
    //   return null;
    // },
    // Disable submit button if numberError exists or currency is not selected
    // isSubmitDisabled() {
    //   return this.numberError !== null || this.formData.capital === "";
    // },
  },
  created() {
    // Use VUE_APP_API_BASE_URL from environment variables
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
  methods: {
    async submitForm() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        console.log(apiBaseUrl);
        // Sending data to backend using axios
        const res = await axios.post(
          `${apiBaseUrl}/calculate_mortgage`,
          this.formData
        );
        // Save response to display
        this.response = res.data.output;
        console.log(this.response);
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

        // {'mortgage_years': 11, 'mortgage_months': 1, 'total_loan_value': 150187.08, 'sell_buy_tax': 15200.0, 'minimal_money_needed': 71250.0,
        // 'annual_taxes': 525.0, 'total_mortgage_value_no_cancelations': 236637.08, 'total_mortgage_value_with_cancelations': 219032.94,
        // 'minimun_resell_price': 245754.96, 'resell_percentage_rise': 29.35}

        this.boxDataItems[0].number = jsonObject["mortgage_years"];
        this.boxDataItems[1].number = jsonObject["mortgage_months"];
        this.boxDataItems[2].number = jsonObject["total_loan_value"];
        this.boxDataItems[3].number = jsonObject["sell_buy_tax"];
        this.boxDataItems[4].number = jsonObject["minimal_money_needed"];
        this.boxDataItems[5].number = jsonObject["annual_taxes"];
        this.boxDataItems[6].number =
          jsonObject["total_mortgage_value_no_cancelations"];
        this.boxDataItems[7].number =
          jsonObject["total_mortgage_value_with_cancelations"];
        this.boxDataItems[8].number = jsonObject["minimun_resell_price"];
        this.boxDataItems[9].number = jsonObject["resell_percentage_rise"];
      } catch (error) {
        console.error("Error submitting form:", error);
        this.response = "An error occurred while submitting the form.";
      }
    },
  },
};
</script>

<style>
#mortgage {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  max-width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
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

/* Form and results container */
.form-results {
  display: flex;
  flex-direction: row;
  width: 100%;
}

/* Form container */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #f9f9f9;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 50%;
}

/* Form groups */
.form-group {
  display: flex;
  flex-direction: column;
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
  flex-direction: column;
  width: 50%;
}

.response-container.response {
  display: flex;
  max-width: 100%;
}

.response-container .mortgage-items {
  display: flex;
  flex-wrap: wrap;
}

.mortgage-items .box-data-item {
  flex-basis: 25%; /* Each child takes up 25% of the container's width */
  box-sizing: border-box; /* Ensures padding and border are included in the width */
  padding: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-container {
    grid-template-columns: 1fr; /* Stack form and response on top of each other */
  }

  .form-results {
    flex-direction: column;
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
  }
}
</style>
