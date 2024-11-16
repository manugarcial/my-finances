<template>
  <div id="net_salary">
    <h1 class="page-title">{{ $t("net_salary_title") }}</h1>
    <div class="form-results">
      <form class="form-container" @submit.prevent="submitForm">
        <div class="form-group">
          <label for="numberInput"> {{ $t("anual_salary") }} </label>
          <input
            type="number"
            v-model.number="formData.salary"
            id="numberInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="country">{{ $t("tax_country") }}</label>
          <select
            v-model="formData.country"
            id="country"
            class="input-field"
            required
          >
            <option value="es" default>{{ $t("spain") }}</option>
            <option value="us" disabled>{{ $t("united_states") }}</option>
            <option value="uk" disabled>{{ $t("united_kingdom") }}</option>
          </select>
          <span v-if="countryError" class="error">{{ countryError }}</span>
        </div>
        <div v-if="regionsForSelectedCountry.length > 0" class="form-group">
          <label for="region">{{ $t("autonomous_region") }}</label>
          <select
            v-model="formData.region"
            id="region"
            class="input-field"
            required
          >
            <option
              v-for="region in regionsForSelectedCountry"
              :key="region.value"
              :value="region.value"
            >
              {{ region.name }}
            </option>
          </select>
          <span v-if="regionError" class="error">{{ regionError }}</span>
        </div>
        <div class="form-group">
          <label for="rentInput">{{ $t("anual_rent") }}</label>
          <input
            type="number"
            v-model.number="formData.anual_rent"
            id="rentInput"
            class="input-field"
            required
          />
          <span v-if="numberError" class="error">{{ numberError }}</span>
        </div>
        <div class="form-group">
          <label for="healthInput">
            {{ $t("health_expenses") }}
          </label>
          <input
            type="number"
            v-model.number="formData.health"
            id="healthInput"
            class="input-field"
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
            {{ $t("calculate") }}
          </button>
        </div>
      </form>
      <div v-if="response" class="response-container">
        <div class="salary-items">
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
        { number: 10, text: this.$t("annual_irpf_cost") },
        { number: 20, text: this.$t("net_salary_per_month") },
        { number: 30, text: this.$t("irpf_percentage") },
        { number: 10, text: this.$t("loan_rent") },
        { number: 10, text: this.$t("basic_spendings") },
        { number: 10, text: this.$t("personal_spendings") },
        { number: 10, text: this.$t("savings") },
        { number: 10, text: this.$t("investments") },
      ],
      scripts: [],
      formData: {
        salary: 30000,
        currency: "eur",
        country: "es",
        region: null,
        age: 1,
        anual_rent: 0,
        health: 0,
      },
      regions: {
        es: [
          { value: "an", name: "Andalucía" },
          { value: "ar", name: "Aragón" },
          { value: "as", name: "Asturias" },
          { value: "ib", name: "Baleares" },
          { value: "cn", name: "Canarias" },
          { value: "cb", name: "Cantabria" },
          { value: "cl", name: "Castilla y León" },
          { value: "cm", name: "Castilla-La Mancha" },
          { value: "ct", name: "Cataluña" },
          { value: "vc", name: "C. Valenciana" },
          { value: "ex", name: "Extremadura" },
          { value: "ga", name: "Galicia" },
          { value: "md", name: "Madrid" },
          { value: "mu", name: "Murcia" },
          { value: "na", name: "Navarra" },
          { value: "pv", name: "País Vasco" },
          { value: "ri", name: "La Rioja" },
        ],
        us: [
          { value: "al", name: "Alabama" },
          { value: "ak", name: "Alaska" },
          { value: "az", name: "Arizona" },
          { value: "ar", name: "Arkansas" },
          { value: "ca", name: "California" },
          { value: "co", name: "Colorado" },
          { value: "ct", name: "Connecticut" },
          { value: "de", name: "Delaware" },
          { value: "fl", name: "Florida" },
          { value: "ga", name: "Georgia" },
          { value: "hi", name: "Hawaii" },
          { value: "id", name: "Idaho" },
          { value: "il", name: "Illinois" },
          { value: "in", name: "Indiana" },
          { value: "ia", name: "Iowa" },
          { value: "ks", name: "Kansas" },
          { value: "ky", name: "Kentucky" },
          { value: "la", name: "Louisiana" },
          { value: "me", name: "Maine" },
          { value: "md", name: "Maryland" },
          { value: "ma", name: "Massachusetts" },
          { value: "mi", name: "Michigan" },
          { value: "mn", name: "Minnesota" },
          { value: "ms", name: "Mississippi" },
          { value: "mo", name: "Missouri" },
          { value: "mt", name: "Montana" },
          { value: "ne", name: "Nebraska" },
          { value: "nv", name: "Nevada" },
          { value: "nh", name: "New Hampshire" },
          { value: "nj", name: "New Jersey" },
          { value: "nm", name: "New Mexico" },
          { value: "ny", name: "New York" },
          { value: "nc", name: "North Carolina" },
          { value: "nd", name: "North Dakota" },
          { value: "oh", name: "Ohio" },
          { value: "ok", name: "Oklahoma" },
          { value: "or", name: "Oregon" },
          { value: "pa", name: "Pennsylvania" },
          { value: "ri", name: "Rhode Island" },
          { value: "sc", name: "South Carolina" },
          { value: "sd", name: "South Dakota" },
          { value: "tn", name: "Tennessee" },
          { value: "tx", name: "Texas" },
          { value: "ut", name: "Utah" },
          { value: "vt", name: "Vermont" },
          { value: "va", name: "Virginia" },
          { value: "wa", name: "Washington" },
          { value: "wv", name: "West Virginia" },
          { value: "wi", name: "Wisconsin" },
          { value: "wy", name: "Wyoming" },
        ],
        uk: [
          { value: "eng", name: "England" },
          { value: "nir", name: "Northern Ireland" },
          { value: "sct", name: "Scotland" },
          { value: "wls", name: "Wales" },
        ],
      },
      response: null,
    };
  },
  computed: {
    // Returns the regions based on the selected country
    regionsForSelectedCountry() {
      return this.regions[this.formData.country] || [];
    },
    // Validation for number input
    numberError() {
      if (this.formData.number === null || this.formData.number === "") {
        return "Number is required.";
      }
      if (this.formData.number <= 0) {
        return "Number must be greater than zero.";
      }
      return null;
    },
    // Validation for currency selector
    currencyError() {
      if (this.formData.currency === "") {
        return "Currency selection is required.";
      }
      return null;
    },
    // Validation for country selector
    countryError() {
      if (this.formData.country === "") {
        return "Country selection is required.";
      }
      return null;
    },
    // Validation for region selector
    regionError() {
      if (this.formData.region === "") {
        return "Region selection is required.";
      }
      return null;
    },
    // Check overall form validity
    isFormValid() {
      return !this.numberError && !this.currencyError;
    },
    // Disable submit button if numberError exists or currency is not selected
    isSubmitDisabled() {
      return this.numberError !== null || this.formData.currency === "";
    },
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
  methods: {
    async submitForm() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        // Sending data to backend using axios
        const res = await axios.post(
          `${apiBaseUrl}/calculate_irpf`,
          this.formData
        );
        // Save response to display
        this.response = res.data.output;
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
        this.boxDataItems[0].number = jsonObject["annual_irpf"];
        this.boxDataItems[1].number = jsonObject["monthly_net_salary"];
        this.boxDataItems[2].number = jsonObject["irpf_salary_percentage"];
        this.boxDataItems[3].number = jsonObject["mortgage_or_rent_budget"];
        this.boxDataItems[4].number = jsonObject["basic_expenses_budget"];
        this.boxDataItems[5].number = jsonObject["personal_expenses_budget"];
        this.boxDataItems[6].number = jsonObject["savings_budget"];
        this.boxDataItems[7].number = jsonObject["investment_budget"];
      } catch (error) {
        console.error("Error submitting form:", error);
        this.response = "An error occurred while submitting the form.";
      }
    },
  },
};
</script>

<style scoped>
#net_salary {
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

.response-container .salary-items {
  display: flex;
  flex-wrap: wrap;
}

.salary-items .box-data-item {
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
