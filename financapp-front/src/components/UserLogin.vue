<template>
  <div class="login-container">
    <h1>{{ $t("login") }}</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" :placeholder="$t('username')" />

      <div class="password-container">
        <input
          :type="passwordVisible ? 'text' : 'password'"
          v-model="password"
          :placeholder="$t('password')"
          class="password-input"
        />
        <button
          type="button"
          class="toggle-password"
          @click="togglePasswordVisibility"
        >
          {{ passwordVisible ? "🙈" : "👁️" }}
        </button>
      </div>
      <button type="submit">{{ $t("login") }}</button>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </form>
    <div class="additional-options">
      <p>
        <router-link to="/register" class="link">
          {{ $t("register") }}
        </router-link>
        <!-- {{ $t("or") }}
        <router-link to="/reset-password" class="link">
          {{ $t("reset_pass") }}
        </router-link> -->
      </p>
    </div>
  </div>
</template>

<script>
import { userlogin } from "../api/api";

export default {
  data() {
    return {
      username: "",
      password: "",
      passwordVisible: false,
      errorMessage: null,
    };
  },
  computed: {
    isSubmitDisabled() {
      return !this.username.trim() || !this.password.trim();
    },
  },
  methods: {
    async handleLogin() {
      if (this.isSubmitDisabled) {
        this.errorMessage = this.$t("login_error_generic");
        return;
      }
      try {
        const response = await userlogin(this.username, this.password);

        if (response) {
          const login_user = {
            username: this.username,
            access_token: response,
          };

          // Commit user data to Vuex store
          this.$store.dispatch("login", login_user);

          // Redirect to the protected page
          this.$router.push("/protected");
        } else {
          console.error("Invalid login response:", response);
        }
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 1.5rem;
  font-size: 24px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  margin-bottom: 1rem;
  padding: 0.75rem;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

.password-container {
  position: relative;
}

.password-input {
  width: 94%;
}

.toggle-password {
  position: absolute;
  right: 0.75rem;
  top: 25%;
  font-size: 18px;
  color: #007bff;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
}

button[type="submit"] {
  padding: 0.75rem;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

.error {
  color: #ff4d4d;
  font-size: 14px;
  margin-top: 5px;
}

.form-group {
  margin-bottom: 1rem;
}

button[type="submit"]:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
