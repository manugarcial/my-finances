<template>
  <div class="home">
    <div class="grid-container">
      <!-- Loop through sections to create individual cards -->
      <div v-for="section in sections" :key="section.title" class="grid-item">
        <div class="card">
          <img :src="section.image" alt="Section Image" class="card-image" />
          <div class="card-content">
            <h3>{{ $t(section.title) }}</h3>
            <p>{{ $t(section.description) }}</p>
            <a :href="section.link" class="card-link">{{ $t("learn_more") }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { useI18n } from "vue-i18n";

@Options({})
export default class HomeView extends Vue {
  // Sections data with image, title, description, and link
  sections = [
    {
      image: require("@/assets/salary_calculation.jpeg"),
      title: "net_salary_title",
      description: "description_for_net_salary",
      link: "/net-salary",
    },
    {
      image: require("@/assets/mortgage_calculation.jpeg"),
      title: "mortgage",
      description: "description_for_mortgage",
      link: "/mortgage",
    },
    {
      image: require("@/assets/stock_list.jpeg"),
      title: "my_stocks",
      description: "description_for_my_stocks",
      link: "/stocks",
    },
    {
      image: require("@/assets/stock_search.jpeg"),
      title: "stock_search",
      description: "description_for_stock_search",
      link: "/stocks-search",
    },
    {
      image: require("@/assets/global_data.jpeg"),
      title: "global_economy_data",
      description: "description_for_global_economy_data",
      link: "/global-economy-data",
    },
  ];
}
</script>

<style scoped>
/* Main container styling */
.home {
  padding: 20px;
}

.grid-container {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping to create multiple rows */
  gap: 20px; /* Space between items */
  justify-content: space-between; /* Ensure items span the entire row */
}

.grid-item {
  flex: 1 1 calc(33.333% - 20px); /* Maximum 3 items per row */
  max-width: calc(33.333% - 20px); /* Prevent items from exceeding 3 per row */
  display: flex;
  justify-content: center;
}

.grid-item:last-child:nth-child(3n + 1),
.grid-item:nth-last-child(2):nth-child(3n + 1),
.grid-item:nth-last-child(3):nth-child(3n + 1) {
  flex: 1 1 100%; /* If fewer than 3 items in the last row, stretch them */
}

.grid-item:nth-last-child(2):nth-child(3n + 2) {
  flex: 1 1 calc(50% - 20px); /* If 2 items, stretch them evenly */
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
  background-color: #fff;
  width: 100%; /* Card width spans the grid item */
  max-width: 300px; /* Optional: Limit card width */
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

@media (max-width: 900px) {
  .grid-item {
    flex: 1 1 calc(50% - 20px);
    max-width: calc(50% - 20px);
  }
}

@media (max-width: 600px) {
  .grid-item {
    flex: 1 1 100%;
    max-width: 100%;
  }
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-image {
  width: 100%;
  height: auto;
  border-radius: 6px;
}

.card-content {
  text-align: center;
}

.card-content h3 {
  font-size: 1.2em;
  margin: 10px 0 5px;
}

.card-content p {
  font-size: 0.9em;
  color: #666;
}

.card-link {
  display: inline-block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.card-link:hover {
  text-decoration: underline;
}
</style>
