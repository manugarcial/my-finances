<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import { userlogin } from "../api/api";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await userlogin(this.username, this.password);
        if (response.access_token) {
          this.$router.push("/protected");
        }
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
  },
};
</script>
