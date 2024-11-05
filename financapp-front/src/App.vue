<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <button
        @click="toggleMenu"
        class="hamburger"
        aria-label="Toggle menu"
        ref="hamburger"
      >
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </button>
      <!-- <img src="path/to/your/icon.png" alt="App Icon" class="app-icon" /> -->
      <div class="app-icon">Financapp</div>
    </div>

    <div :class="['navbar-menu', { 'is-active': menuActive }]" ref="navbarMenu">
      <router-link to="/" class="navbar-item" @click="closeMenu">
        Home
      </router-link>
      <router-link to="/net-salary" class="navbar-item" @click="closeMenu">
        Net Salary
      </router-link>
      <router-link to="/mortgage" class="navbar-item" @click="closeMenu">
        Mortgage
      </router-link>
      <router-link to="/stocks" class="navbar-item" @click="closeMenu">
        Stocks
      </router-link>
      <router-link to="/stocks-search" class="navbar-item" @click="closeMenu">
        Stocks Search
      </router-link>
      <router-link
        to="/global-economy-data"
        class="navbar-item"
        @click="closeMenu"
      >
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
  created() {
    this.$store.dispatch("checkStoredUser").then(() => {
      console.log("Checked stored user in App.vue");
    });
  },
  methods: {
    toggleMenu() {
      this.menuActive = !this.menuActive;
    },
    closeMenu() {
      this.menuActive = false;
    },
    handleClickOutside(event) {
      const menu = this.$refs.navbarMenu;
      const hamburger = this.$refs.hamburger;
      // Check if the click was outside the menu and the hamburger button
      if (menu && hamburger) {
        if (
          this.menuActive &&
          !menu.contains(event.target) &&
          !hamburger.contains(event.target)
        ) {
          this.closeMenu();
        }
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
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
    color: white;

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

.navbar-brand {
  display: flex;
  .app-icon {
    color: white;
    margin-left: 10px;
  }
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
