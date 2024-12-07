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
      <div class="app-icon">
        <router-link to="/" class="navbar-item" @click="closeMenu">
          Financapp
        </router-link>
      </div>
    </div>

    <div :class="['navbar-menu', { 'is-active': menuActive }]" ref="navbarMenu">
      <router-link to="/" class="navbar-item" @click="closeMenu">
        {{ $t("home") }}
      </router-link>
      <router-link to="/net-salary" class="navbar-item" @click="closeMenu">
        {{ $t("net_salary_title") }}
      </router-link>
      <router-link to="/mortgage" class="navbar-item" @click="closeMenu">
        {{ $t("mortgage") }}
      </router-link>
      <router-link to="/stocks" class="navbar-item" @click="closeMenu">
        {{ $t("my_stocks") }}
      </router-link>
      <router-link to="/stocks-search" class="navbar-item" @click="closeMenu">
        {{ $t("stock_search") }}
      </router-link>
      <router-link
        to="/global-economy-data"
        class="navbar-item"
        @click="closeMenu"
      >
        {{ $t("global_economy_data") }}
      </router-link>
    </div>
    <div class="left-side-menu">
      <router-link to="/login" class="navbar-item user-icon" @click="closeMenu">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="white"
        >
          <path
            d="M12 12c2.67 0 8 1.34 8 4v2H4v-2c0-2.66 5.33-4 8-4zm0-2c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"
          />
        </svg>
      </router-link>
      <div class="navbar-item language-selector" @click="toggleDropdown">
        <span>{{ currentLanguage }}</span>
        <div v-if="dropdownOpen" class="dropdown">
          <span
            v-for="(label, code) in languages"
            :key="code"
            class="dropdown-item"
            @click="selectLanguage(code)"
          >
            {{ label }}
          </span>
        </div>
      </div>
    </div>
  </nav>
  <router-view />
</template>
<script>
import { useI18n } from "vue-i18n";
import { mapActions, mapGetters } from "vuex";

export default {
  setup() {
    const { locale } = useI18n(); // Access Vue I18n's locale property

    return {
      locale,
    };
  },
  data() {
    return {
      menuActive: false,
      dropdownOpen: false,
      languages: {
        es: "Español",
        en: "English",
      },
    };
  },
  computed: {
    // Get current language from Vuex
    ...mapGetters("language", ["currentLanguage"]),
    // Get current language based on i18n locale
    currentLanguage() {
      return this.locale;
    },
  },
  created() {
    this.$store.dispatch("checkStoredUser");
  },
  methods: {
    ...mapActions("language", ["setLanguage"]),
    toggleMenu() {
      this.menuActive = !this.menuActive;
    },
    closeMenu() {
      this.menuActive = false;
      this.dropdownOpen = false;
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    selectLanguage(code) {
      this.locale = code; // Set the Vue I18n locale to the selected language code
      this.setLanguage(code);
      this.dropdownOpen = false;
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
      if (this.dropdownOpen && !event.target.closest(".language-selector")) {
        this.dropdownOpen = false;
      }
    },
  },
  mounted() {
    this.locale = this.currentLanguage;
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

.language-selector {
  position: relative;
  cursor: pointer;
  color: white;
  font-weight: bold;
  display: flex;
}

.language-selector span {
  color: white;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: -21px;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 5px 0;
  display: flex;
  flex-direction: column;
  min-width: 100px;
  z-index: 1;
}

.dropdown-item {
  padding: 8px 16px;
  color: white;
  text-align: left;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #555;
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

.left-side-menu {
  display: flex;
}

.user-icon svg {
  width: 24px;
  height: 24px;
  fill: white; /* Ensure the icon is white */
  transition: transform 0.2s ease, fill 0.2s ease;
}

.user-icon svg:hover {
  transform: scale(1.1);
  fill: #42b983; /* Optional hover color */
}
</style>
