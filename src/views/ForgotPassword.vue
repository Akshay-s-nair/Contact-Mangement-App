<template>
  <div class="loginnav">
    <router-link class="home-link" to="/"><img src="ContactEase2.png" alt="ContactEase Logo" class="logoLogin"></router-link>
    <router-link class="home-link" to="/">Home</router-link>
  </div>
  <div class="forgot-password">
    <div v-if="!showResetForm">
      <h2>Forgot Password</h2>
      <form @submit.prevent="handleRequestPasswordReset">
        <div>
          <label for="email">Email:</label>
          <input v-model="email" type="email" id="email" required />
          <span v-if="errors.email">{{ errors.email }}</span>
        </div>
        <div>
          <label for="phone">Phone:</label>
          <input v-model="phone" type="text" id="phone" required />
          <span v-if="errors.phone">{{ errors.phone }}</span>
        </div>
        <button type="submit">Request Password Reset</button>
        
      </form>
    </div>

    <div v-if="showResetForm">
      <h2>Reset Password</h2>
      <form @submit.prevent="handleResetPassword">
        <div>
          <label for="newPassword">New Password:</label>
          <input v-model="newPassword" type="password" id="newPassword" required />
        </div>
        <div>
          <label for="confirmPassword">Confirm Password:</label>
          <input v-model="confirmPassword" type="password" id="confirmPassword" required />
        </div>
        <button type="submit">Reset Password</button>
      </form>
    </div>
    <div v-if="success" class="success">{{ success }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      email: '',
      phone: '',
      newPassword: '',
      confirmPassword: '',
      showResetForm: false,
      errors: {},
    };
  },
  computed: {
    ...mapState(['error', 'success'])
  },
  methods: {
    ...mapActions(['requestPasswordReset', 'resetPassword']),
    async handleRequestPasswordReset() {
      this.errors = {};
      await this.requestPasswordReset({ email: this.email, phone: this.phone });
      if (!this.error) {
        this.showResetForm = true;
      }
    },
    async handleResetPassword() {
      await this.resetPassword({ email: this.email, phone: this.phone, newPassword: this.newPassword ,confirmPassword:this.confirmPassword});
      if (!this.error) {
        this.$router.push('/login');
        }


    }
  }
};
</script>

<style scoped>
.forgot-password {
  max-width: 400px;
  margin: 0 auto;
}
.success {
  color: green;
}
.error {
  color: red;
}
button{
  background-color: #da5b01;
  width: 420px;
  margin-top: 10px;
  transition: all .2s ease-in-out;
}
button:hover{
  background-color: #c45200;
  width: 420px;
  margin-top: 10px;
}
@media (max-width: 768px) {
  .forgot-password {
    max-width: 250px;
    margin: 0 auto;
}

}
</style>
