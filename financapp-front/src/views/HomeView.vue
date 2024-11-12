<template>
  <div class="home">
    <div class="grid-container">
      <!-- Loop through sections to create individual cards -->
      <div v-for="section in sections" :key="section.title" class="grid-item">
        <div class="card">
          <img :src="section.image" alt="Section Image" class="card-image" />
          <div class="card-content">
            <h3>{{ section.title }}</h3>
            <p>{{ section.description }}</p>
            <a :href="section.link" class="card-link">Learn More</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";

@Options({})
export default class HomeView extends Vue {
  // Sections data with image, title, description, and link
  sections = [
    {
      // image: require("@/assets/section1.jpg")
      image: "https://picsum.photos/id/237/200/300",
      title: "Section 1",
      description: "Description for Section 1.",
      link: "/section1",
    },
    {
      // image: require("@/assets/section2.jpg"),
      image: "https://picsum.photos/id/237/200/300",
      title: "Section 2",
      description: "Description for Section 2.",
      link: "/section2",
    },
    {
      // image: require("@/assets/section3.jpg"),
      image: "https://picsum.photos/id/237/200/300",
      title: "Section 3",
      description: "Description for Section 3.",
      link: "/section3",
    },
    // Add more sections as needed
  ];
}
</script>

<style scoped>
/* Main container styling */
.home {
  padding: 20px;
}

/* Grid container */
.grid-container {
  display: grid;
  gap: 20px;
}

/* Card item styling */
.grid-item {
  display: flex;
  justify-content: center;
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
  width: 300px;
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

/* Responsive Grid Layout */
@media (min-width: 600px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 900px) {
  .grid-container {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
