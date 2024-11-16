<template>
  <div class="reset-password-container">
    <h1>Reset Password</h1>
    <form @submit.prevent="handleReset">
      <input v-model="email" placeholder="Enter your email" />
      <button type="submit">Send Reset Link</button>
    </form>
  </div>
</template>

<script>
import { sendPasswordReset } from "../api/api";

export default {
  data() {
    return {
      email: "",
    };
  },
  methods: {
    async handleReset() {
      try {
        // const response = await sendPasswordReset(this.email);
        // TODO: implement the call that will handle change psswd
        console.log("Reset link sent:", response);
        alert("A reset link has been sent to your email.");
        this.$router.push("/login");
      } catch (error) {
        console.error("Failed to send reset link:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Similar to login styles */
.reset-password-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
