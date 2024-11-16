<template>
  <div>
    <button v-if="isLoggedIn" @click="logout">{{ $t("logout") }}</button>
    <router-view />
  </div>
</template>

<script>
import { loginUser, logoutUser } from "../api/auth"; // Define API interactions

export default {
  data() {
    return {
      tokenExpirationTimer: null,
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("accessToken");
    },
  },
  methods: {
    async login(username, password) {
      const response = await loginUser(username, password);
      if (response.access_token) {
        localStorage.setItem("accessToken", response.access_token);

        // Set up auto-logout on token expiration (15 min here; adjust based on backend)
        this.setAutoLogout(15 * 60 * 1000); // 15 minutes in ms
      }
    },
    logout() {
      // Clear the token and stop the timer
      localStorage.removeItem("accessToken");
      clearTimeout(this.tokenExpirationTimer);
      this.$router.push("/login");
    },
    setAutoLogout(expirationTime) {
      clearTimeout(this.tokenExpirationTimer);
      this.tokenExpirationTimer = setTimeout(() => {
        alert("Session expired. Logging out...");
        this.logout();
      }, expirationTime);
    },
  },
  mounted() {
    // If user is already logged in on app load, set auto-logout
    if (this.isLoggedIn) {
      // Here you might want to check the remaining time and set it accordingly.
      this.setAutoLogout(15 * 60 * 1000); // Adjust based on the remaining time
    }
  },
};
</script>
