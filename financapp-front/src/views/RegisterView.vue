<template>
  <div class="register-container">
    <h1>{{ $t("register") }}</h1>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <input
          type="text"
          id="name"
          :placeholder="$t('name')"
          v-model="formData.name"
          required
        />
      </div>

      <div class="form-group">
        <input
          type="text"
          id="surname"
          :placeholder="$t('surname')"
          v-model="formData.surname"
          required
        />
      </div>

      <div class="form-group">
        <input
          type="text"
          id="username"
          :placeholder="$t('username')"
          v-model="formData.username"
          required
        />
      </div>

      <div class="form-group">
        <input
          type="email"
          id="email"
          :placeholder="$t('email')"
          v-model="formData.email"
          required
        />
      </div>

      <div class="form-group">
        <input
          type="password"
          id="password"
          :placeholder="$t('password')"
          v-model="formData.password"
          required
        />
      </div>

      <button type="submit">{{ $t("register") }}</button>

      <div v-if="message" class="message">{{ message }}</div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      formData: {
        name: "",
        surname: "",
        username: "",
        password: "",
        email: "",
      },
      message: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const apiBaseUrl = process.env.VUE_APP_API_BASE_URL;
        const response = await axios.post(
          `${apiBaseUrl}/register`,
          this.formData
        );
        this.message = response.data.msg;
      } catch (error) {
        this.message = error.response.data.msg || "Registration failed";
      }
    },
  },
};
</script>

<style>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.message {
  margin-top: 1rem;
  color: #007bff;
  font-weight: bold;
}
</style>
