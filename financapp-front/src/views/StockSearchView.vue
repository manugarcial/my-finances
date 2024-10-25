<template>
  <div id="app">
    <h1>Stock Search</h1>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search for stocks..."
      @input="filterStocks"
    />
    <ul v-if="filteredStocks.length > 0 && searchQuery" class="dropdown">
      <li
        v-for="stock in filteredStocks"
        :key="stock.ticker"
        @click="navigateToItem(stock.ticker)"
        class="dropdown-item"
      >
        {{ stock.ticker }} - {{ stock.name }}
      </li>
    </ul>

    <!-- Carousel Section -->
    <div class="carousel">
      <div
        class="carousel-inner"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div
          class="carousel-item"
          v-for="stock in stocks.slice(0, 10)"
          :key="stock.ticker"
          @click="navigateToItem(stock.ticker)"
        >
          <p>{{ stock.ticker }} - {{ stock.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import stockData from "../data/stockData";
export default {
  data() {
    return {
      searchQuery: "",
      currentIndex: 0,
      visibleItems: 3,
      carousel_stocks: [
        { ticker: "AAPL", name: "Apple Inc." },
        { ticker: "MSFT", name: "Microsoft Corporation" },
        { ticker: "GOOGL", name: "Alphabet Inc." },
        { ticker: "AMZN", name: "Amazon.com, Inc." },
        { ticker: "FB", name: "Meta Platforms, Inc." },
        { ticker: "TSLA", name: "Tesla, Inc." },
        { ticker: "NFLX", name: "Netflix, Inc." },
        { ticker: "BRK.B", name: "Berkshire Hathaway Inc." },
        { ticker: "JNJ", name: "Johnson & Johnson" },
        { ticker: "V", name: "Visa Inc." },
      ],
      stocks: stockData,
      filteredStocks: [],
    };
  },
  computed: {
    carouselStocks() {
      return [
        ...this.carousel_stocks,
        ...this.carousel_stocks,
        ...this.carousel_stocks,
        ...this.carousel_stocks,
        ...this.carousel_stocks,
      ];
    },
  },
  methods: {
    filterStocks() {
      const query = this.searchQuery.toLowerCase();
      this.filteredStocks = this.stocks.filter(
        (stock) =>
          stock.name.toLowerCase().includes(query) ||
          stock.ticker.toLowerCase().includes(query)
      );
    },
    navigateToItem(ticker) {
      this.$router.push({ path: `/item/${ticker}` });
    },
    startCarousel() {
      setInterval(() => {
        this.currentIndex =
          (this.currentIndex + 1) % this.carousel_stocks.length; // Loop through the first 10 items
      }, 1);
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.startCarousel(); // Start the carousel animation
    });
  },
};
</script>

<style scoped>
#app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  position: relative; /* Position relative for absolute children */
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.dropdown {
  list-style-type: none;
  padding: 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 200px; /* Limit height */
  overflow-y: auto; /* Scroll if too many results */
  position: absolute; /* Position it under the input */
  background-color: white;
  width: 100%; /* Match input width */
  z-index: 1; /* Ensure it's on top of other elements */
}

.dropdown-item {
  padding: 8px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f0f0f0; /* Highlight on hover */
}

.carousel {
  margin-top: 20px;
  position: relative; /* Positioning for inner carousel */
  overflow: hidden; /* Hide overflow */
  width: 100%;
  max-width: 600px;
  border-radius: 8px;
}

.carousel-inner {
  display: flex;
  transition: transform 30s ease;
}

.carousel-item {
  min-width: 33.33%; /* Full width for each item */
  box-sizing: border-box;
  padding: 10px; /* Add padding for content */
  text-align: center; /* Center the text */
  background: #f9f9f9; /* Light background for items */
  /* border-radius: 4px; Rounded corners */
}
</style>
