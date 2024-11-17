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
        <span v-if="nameError" class="error">{{ nameError }}</span>
      </div>

      <div class="form-group">
        <input
          type="text"
          id="surname"
          :placeholder="$t('surname')"
          v-model="formData.surname"
          required
        />
        <span v-if="surnameError" class="error">{{ surnameError }}</span>
      </div>

      <div class="form-group">
        <input
          type="text"
          id="username"
          :placeholder="$t('username')"
          v-model="formData.username"
          required
        />
        <span v-if="usernameError" class="error">{{ usernameError }}</span>
      </div>

      <div class="form-group">
        <input
          type="email"
          id="email"
          :placeholder="$t('email')"
          v-model="formData.email"
          required
        />
        <span v-if="emailError" class="error">{{ emailError }}</span>
      </div>

      <div class="form-group">
        <input
          type="password"
          id="password"
          :placeholder="$t('password')"
          v-model="formData.password"
          required
        />
        <span v-if="passwordError" class="error">{{ passwordError }}</span>
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
  computed: {
    nameError() {
      return this.validateName();
    },
    surnameError() {
      return this.validateSurname();
    },
    usernameError() {
      return this.validateUsername();
    },
    emailError() {
      return this.validateEmail();
    },
    passwordError() {
      return this.validatePassword();
    },
    isSubmitDisabled() {
      return (
        this.nameError ||
        this.surnameError ||
        this.usernameError ||
        this.emailError ||
        this.passwordError
      );
    },
  },
  methods: {
    validateName() {
      return this.formData.name.trim() === "" ? this.$t("name_error") : null;
    },
    validateSurname() {
      return this.formData.surname.trim() === ""
        ? this.$t("surname_error")
        : null;
    },
    validateUsername() {
      const username = this.formData.username.trim();
      if (username === "") return this.$t("username_error_empty");
      if (username.length < 3) return this.$t("username_error_short");
      return null;
    },
    validateEmail() {
      const email = this.formData.email.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (email === "") return this.$t("email_error_empty");
      if (!emailRegex.test(email)) return this.$t("email_error_invalid");
      return null;
    },
    validatePassword() {
      const password = this.formData.password;
      if (password === "") return this.$t("password_error_empty");
      if (password.length < 6) return this.$t("password_error_short");
      return null;
    },
    async registerUser() {
      if (this.isSubmitDisabled) {
        console.error("Form validation failed");
        return;
      }
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

.error {
  color: #ff4d4d;
  font-size: 14px;
  margin-top: 5px;
}
</style>
