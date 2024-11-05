<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <h2>Add Stock</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label>Ticker:</label>
          <input v-model="stock_symbol" required />
        </div>
        <div>
          <label>Stock Index:</label>
          <input v-model="stock_index" required />
        </div>
        <div>
          <label>Currency:</label>
          <input v-model="currency" required />
        </div>
        <div>
          <label>Operation:</label>
          <select v-model="operation" required>
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>
        <div>
          <label>Cost:</label>
          <input type="number" v-model="cost" required />
        </div>
        <div>
          <label>Transaction Price:</label>
          <input type="number" v-model="transaction_price" required />
        </div>
        <div>
          <label>Stock Price:</label>
          <input type="number" v-model="stock_price" required />
        </div>
        <div>
          <label>Timestamp:</label>
          <input type="number" v-model="timestamp" required />
        </div>
        <button type="submit" class="submit-button">Add Stock</button>
        <button type="button" @click="close" class="cancel-button">
          Cancel
        </button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    close: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      stock_symbol: "",
      stock_index: "",
      currency: "",
      operation: "",
      cost: null,
      transaction_price: null,
      stock_price: null,
      timestamp: null,
      message: "", // For any error or success messages
    };
  },
  computed: {
    ...mapGetters(["getUsername"]),
    username() {
      return this.getUsername;
    },
  },
  methods: {
    async submitForm() {
      if (!this.username) {
        alert("Please log in to add stocks.");
        return;
      }

      // Prepare the data to emit
      const stockData = {
        user_id: this.username,
        stock_symbol: this.stock_symbol,
        stock_index: this.stock_index,
        currency: this.currency,
        operation: this.operation,
        cost: this.cost,
        transaction_price: this.transaction_price,
        stock_price: this.stock_price,
        timestamp: this.timestamp,
      };

      // Emit the stock data to the parent component
      this.$emit("add-stock", stockData);

      // Clear form fields after submitting
      this.resetForm();
    },
    resetForm() {
      this.stock_symbol = "";
      this.stock_index = "";
      this.currency = "";
      this.operation = "";
      this.cost = null;
      this.transaction_price = null;
      this.stock_price = null;
      this.timestamp = null;
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 15px;
  cursor: pointer;
}

.cancel-button {
  margin-left: 10px;
}
</style>
