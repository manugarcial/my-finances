<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <!-- <img src="path/to/your/icon.png" alt="App Icon" class="app-icon" /> -->
      <button
        @click="toggleMenu"
        class="hamburger"
        aria-label="Toggle menu"
        ref="hamburguer"
      >
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </button>
    </div>

    <div :class="['navbar-menu', { 'is-active': menuActive }]" ref="navbarMenu">
      <router-link to="/" class="navbar-item">Home</router-link>
      <router-link to="/net-salary" class="navbar-item">Net Salary</router-link>
      <router-link to="/mortgage" class="navbar-item">Mortgage</router-link>
      <router-link to="/stocks" class="navbar-item">Stocks</router-link>
      <router-link to="/stocks-search" class="navbar-item">
        Stocks Search
      </router-link>
      <router-link to="/global-economy-data" class="navbar-item">
        Global Economy Data
      </router-link>
    </div>
  </nav>
  <router-view />
</template>
<script>
export default {
  data() {
    return {
      menuActive: false,
    };
  },
  methods: {
    toggleMenu() {
      this.menuActive = !this.menuActive;
    },
    // handleClickOutside(event) {
    //   const menu = this.$refs.navbarMenu;
    //   const hamburger = this.$refs.hamburger;

    //   // Check if the menu is active and the clicked target is outside the menu and the hamburger button
    //   // eslint-disable-next-line
    //   if (this.menuActive && menu && !menu.contains(event.target) && !hamburger.contains(event.target)) {
    //     this.menuActive = false; // Close the menu
    //   }
    // },
  },
  // mounted() {
  //   // Add event listener to the document for detecting clicks
  //   document.addEventListener("click", this.handleClickOutside);
  // },
  // beforeUnmount() {
  //   // Clean up the event listener when the component is destroyed
  //   document.removeEventListener("click", this.handleClickOutside);
  // },
};
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333; /* Navbar background color */
  padding: 10px 20px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.app-icon {
  height: 40px; /* Adjust as needed */
}

.hamburger {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 24px; /* Adjust as needed */
}

.bar {
  width: 30px; /* Width of the hamburger bars */
  height: 3px; /* Height of the hamburger bars */
  background-color: white; /* Color of the bars */
  transition: all 0.3s;
}

.navbar-menu {
  display: none; /* Hide menu by default */
  flex-direction: column;
  position: absolute;
  top: 44px; /* Adjust based on your navbar height */
  left: 0;
  background-color: #333; /* Match with navbar background */
  width: 100%;
}

.navbar-menu.is-active {
  display: flex; /* Show menu when active */
}

.navbar-item {
  color: white; /* Link color */
  padding: 10px 20px; /* Adjust spacing */
  text-decoration: none; /* Remove underline */
}

.navbar-item:hover {
  background-color: #555; /* Hover effect */
}
</style>
