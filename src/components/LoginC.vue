<template>
  <div class="loginnav">
    <router-link class="home-link" to="/"><img src="ContactEase2.png" alt="ContactEase Logo" class="logoLogin"></router-link>
    <router-link class="home-link" to="/">Home</router-link>
  </div>
  <div class="login">
    <h1 class="welcomeText">Hello there, welcome back</h1>
    <div class="formHead">
      <div class="formBody">
        <h2 class="name-LoginRegister">Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="text" v-model="form.email" id="email" />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" v-model="form.password" id="password" />
            <router-link class="" to="/forgot">Forgot Password?</router-link>
          </div>
          <div class="error-div">
            <p v-if="success" class="success">{{ success }}</p>
            <p v-if="error" class="error">{{ error }}</p>
          </div>
          <button class="button-LoginRegister" type="submit">Login</button>
        </form>
        <hr>
        <div class="registerFromLogin">
          <p>Don't have an account? <router-link class="" to="/register">Signup</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      }
    };
  },
  computed: {
    ...mapState(['error', 'success'])
  },
  methods: {
    ...mapActions(['login']),
    handleLogin() {
      this.login(this.form);
    }
  }
};
</script>


<style scoped>
  @import "./LoginRegister.css";



  label {
    display: block;
    margin-bottom: 5px;
  }

  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
  }

  .error-div {
    margin-top: 10px;
  }

  .success {
    color: green;
  }

  .error {
    color: red;
  }

  button {
    background-color:#ec7c2c;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #e86100;
  }
  
</style>
