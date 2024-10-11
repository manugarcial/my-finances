<template>
  <div id="app">
    <h1>{{ $t("Net Salary title") }} Hola</h1>
    <div id="app">
      <h1>Form Test</h1>
      <form @submit.prevent="submitForm">
        <!-- Select dropdown -->
        <div>
          <label for="category">Category:</label>
          <select v-model="formData.category" id="category" required>
            <option value="technology">Technology</option>
            <option value="finance">Finance</option>
            <option value="health">Health</option>
          </select>
        </div>

        <!-- Submit button -->
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>

      <!-- Display server response -->
      <div v-if="response">
        <h2>Server Response:</h2>
        <pre>{{ response }}</pre>
      </div>
    </div>
    <div v-if="output">
      <h2>Script Output:</h2>
      <pre>{{ output }}</pre>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      scripts: [],
      output: "",
      formData: {
        category: "technology",
        quantity: 1,
      },
      response: null,
    };
  },
  created() {
    axios
      .get("http://127.0.0.1:5000/")
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
        // Sending data to backend using axios
        const res = await axios.post(
          "http://127.0.0.1:5000/calculate_irpf",
          this.formData
        );
        // Save response to display
        this.response = res.data;
        console.log("Response data:", this.response);
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
